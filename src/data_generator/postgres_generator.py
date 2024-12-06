import os
import time
import random
import psycopg2
from faker import Faker
from kafka import KafkaProducer
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgresDataGenerator:
    def __init__(self, 
                 pg_host='postgres', 
                 pg_port=5432, 
                 pg_db='streamdb', 
                 pg_user='streamuser', 
                 pg_password='streampassword',
                 kafka_bootstrap_servers=['kafka:9092']):
        # PostgreSQL Connection
        self.pg_conn_params = {
            'host': pg_host,
            'port': pg_port,
            'database': pg_db,
            'user': pg_user,
            'password': pg_password
        }
        
        # Kafka Producer
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Faker for generating realistic data
        self.fake = Faker()

    def generate_user_data(self):
        """Generate synthetic user data"""
        return {
            'user_id': self.fake.uuid4(),
            'name': self.fake.name(),
            'email': self.fake.email(),
            'age': random.randint(18, 80),
            'income': random.uniform(20000, 200000),
            'timestamp': self.fake.date_time_this_year().isoformat()
        }

    def insert_to_postgres(self, data):
        """Insert data into PostgreSQL"""
        try:
            with psycopg2.connect(**self.pg_conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO users 
                        (user_id, name, email, age, income, created_at) 
                        VALUES (%(user_id)s, %(name)s, %(email)s, %(age)s, %(income)s, %(timestamp)s)
                    """, data)
                conn.commit()
        except Exception as e:
            logger.error(f"PostgreSQL insertion error: {e}")

    def produce_to_kafka(self, topic, data):
        """Produce data to Kafka topic"""
        try:
            self.producer.send(topic, data)
            self.producer.flush()
        except Exception as e:
            logger.error(f"Kafka production error: {e}")

    def run(self, interval=5, topic='user_events'):
        """Continuous data generation and streaming"""
        logger.info("Starting data generation...")
        while True:
            try:
                # Generate data
                user_data = self.generate_user_data()
                
                # Insert to PostgreSQL
                self.insert_to_postgres(user_data)
                
                # Produce to Kafka
                self.produce_to_kafka(topic, user_data)
                
                logger.info(f"Generated and streamed user data: {user_data['user_id']}")
                
                # Wait before next generation
                time.sleep(interval)
            
            except Exception as e:
                logger.error(f"Generation error: {e}")
                time.sleep(10)

if __name__ == '__main__':
    generator = PostgresDataGenerator()
    generator.run()