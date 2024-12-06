from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.descriptors import Kafka, Json, Postgres
import json

class UserEventProcessor:
    def __init__(self):
        # Create execution environment
        self.env = StreamExecutionEnvironment.get_execution_environment()
        
        # Table environment settings
        settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
        self.table_env = StreamTableEnvironment.create(stream_execution_environment=self.env, environment_settings=settings)
        
        # Add necessary dependencies
        self.env.add_jars(
            'file:///opt/flink/lib/kafka-connector.jar',
            'file:///opt/flink/lib/postgres-connector.jar'
        )

    def setup_kafka_source(self, topic='user_events', bootstrap_servers='kafka:9092'):
        """Configure Kafka source"""
        self.table_env.connect(
            Kafka()
            .version('universal')
            .topic(topic)
            .property('bootstrap.servers', bootstrap_servers)
            .start_from_latest()
        ).with_format(
            Json()
        ).with_schema({
            'user_id': 'STRING',
            'name': 'STRING',
            'email': 'STRING',
            'age': 'INT',
            'income': 'DOUBLE',
            'timestamp': 'TIMESTAMP'
        }).in_append_mode().create_temporary_table('kafka_source')

    def setup_postgres_sink(self, table_name='processed_users'):
        """Configure PostgreSQL sink"""
        self.table_env.connect(
            Postgres()
            .url('jdbc:postgresql://postgres:5432/streamdb')
            .table(table_name)
            .username('streamuser')
            .password('streampassword')
        ).with_schema({
            'user_id': 'STRING',
            'name': 'STRING',
            'income_category': 'STRING'
        }).in_upsert_mode().create_temporary_table('postgres_sink')

    def process_stream(self):
        """Stream processing logic"""
        # Read from Kafka source
        source_table = self.table_env.from_path('kafka_source')
        
        # Process and categorize income
        processed_table = source_table.select(
            'user_id', 
            'name', 
            self.table_env.sql_query('''
                CASE 
                    WHEN income < 50000 THEN 'LOW_INCOME'
                    WHEN income BETWEEN 50000 AND 100000 THEN 'MIDDLE_INCOME'
                    ELSE 'HIGH_INCOME'
                END AS income_category
            ''')
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