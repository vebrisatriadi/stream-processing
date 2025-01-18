# Update imports at the top
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
# Remove the old import and add these instead
from pyflink.table.descriptors import Schema
from pyflink.table.table_descriptor import TableDescriptor
from pyflink.table import Schema
import json

class UserEventProcessor:
    def __init__(self):
        self.env = StreamExecutionEnvironment.get_execution_environment()
        settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
        self.table_env = StreamTableEnvironment.create(stream_execution_environment=self.env, environment_settings=settings)
        
        # Update the jar paths to include the full Flink Kafka connector
        self.env.add_jars(
            # "file:///Users/vebrisatriadi/Flink/flink-1.20.0/lib/flink-connector-files-1.20.0.jar",
            # "file:///Users/vebrisatriadi/Flink/flink-1.20.0/lib/flink-connector-kafka-1.20.0.jar",  # Updated version
            # "file:///Users/vebrisatriadi/Flink/flink-1.20.0/lib/kafka-clients-3.2.3.jar"
            "file:///opt/flink/lib/flink-connector-kafka-1.17.1.jar",  # Update version as needed
            "file:///opt/flink/lib/kafka-clients-3.2.3.jar",           # Add Kafka clients
            "file:///opt/flink/lib/postgres-connector.jar"
        )
        
    def setup_kafka_source(self, topic='user_events', bootstrap_servers='kafka:9092'):
        """Configure Kafka source"""
        self.table_env.create_temporary_table(
            'kafka_source',
            TableDescriptor.for_connector('kafka')
            .schema(Schema.new_builder()  # Changed from Schema() to Schema.new_builder()
                .column('user_id', 'STRING')
                .column('name', 'STRING')
                .column('email', 'STRING')
                .column('age', 'INT')
                .column('income', 'DOUBLE')
                .column('timestamp', 'TIMESTAMP')
                .build())
            .option('topic', topic)
            .option('properties.bootstrap.servers', bootstrap_servers)
            .option('format', 'json')
            .option('scan.startup.mode', 'latest-offset')
            .build()
        )

    def setup_postgres_sink(self, table_name='processed_users'):
        """Configure PostgreSQL sink"""
        self.table_env.create_temporary_table(
            'postgres_sink',
            TableDescriptor.for_connector('jdbc')
                .schema(Schema.new_builder()
                    .column('user_id', 'STRING')
                    .column('name', 'STRING')
                    .column('income_category', 'STRING')
                    .build())
                .option('url', 'jdbc:postgresql://postgres:5432/streamdb')
                .option('table-name', table_name)
                .option('username', 'X')
                .option('password', 'X')
                .build()
        )

    def process_stream(self):
        """Stream processing logic"""
        # Read from Kafka source
        source_table = self.table_env.from_path('kafka_source')
        
        # Process and categorize income
        processed_table = source_table.select(
            'user_id', 
            'name',
            # Use a complete SQL query instead of just the CASE statement
            self.table_env.sql_query('''
                SELECT 
                    CASE 
                        WHEN income < 50000 THEN 'LOW_INCOME'
                        WHEN income BETWEEN 50000 AND 100000 THEN 'MIDDLE_INCOME'
                        ELSE 'HIGH_INCOME'
                    END
                FROM kafka_source
            ''').select("f0").as_('income_category')
        )
        
        # Write to PostgreSQL sink
        processed_table.execute_insert('postgres_sink')

    def run(self):
        """Execute the stream processing job"""
        self.setup_kafka_source()
        self.setup_postgres_sink()
        self.process_stream()
        self.env.execute('User Event Stream Processor')

if __name__ == '__main__':
    processor = UserEventProcessor()
    processor.run()