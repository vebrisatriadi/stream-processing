import json
import logging
from typing import Dict, Any
from kafka import KafkaProducer
from json import dumps

class KafkaStreamProducer:
    def __init__(self, 
                 bootstrap_servers: list = ['localhost:9092'], 
                 topic: str = 'default_topic'):
        """
        Initialize Kafka Producer
        
        :param bootstrap_servers: List of Kafka broker addresses
        :param topic: Default Kafka topic to produce messages
        """
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda x: dumps(x).encode('utf-8'),
                key_serializer=lambda x: dumps(x).encode('utf-8') if x else None
            )
            self.topic = topic
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
        except Exception as e:
            logging.error(f"Kafka Producer Initialization Error: {e}")
            raise

    def send_message(self, 
                     message: Dict[str, Any], 
                     topic: str = None, 
                     key: str = None):
        """
        Send a message to Kafka topic
        
        :param message: Message to send
        :param topic: Optional topic override
        :param key: Optional message key
        """
        try:
            # Use provided topic or default topic
            send_topic = topic or self.topic
            
            # Send message
            future = self.producer.send(
                topic=send_topic, 
                key=key, 
                value=message
            )
            
            # Block until message is sent
            record_metadata = future.get(timeout=10)
            
            self.logger.info(
                f"Message sent to {record_metadata.topic} "
                f"partition {record_metadata.partition}"
            )
            
            return record_metadata
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            raise

    def send_batch(self, 
                   messages: list, 
                   topic: str = None):
        """
        Send multiple messages in a batch
        
        :param messages: List of messages to send
        :param topic: Optional topic override
        """
        try:
            send_topic = topic or self.topic
            
            for message in messages:
                self.send_message(message, send_topic)
            
            self.producer.flush()
        except Exception as e:
            self.logger.error(f"Batch send error: {e}")
            raise

    def close(self):
        """
        Close Kafka producer connection
        """
        try:
            self.producer.close()
            self.logger.info("Kafka Producer closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing Kafka Producer: {e}")

# Example usage
def main():
    producer = KafkaStreamProducer(
        bootstrap_servers=['localhost:9092'],
        topic='user_events'
    )
    
    sample_message = {
        'user_id': '123',
        'name': 'John Doe',
        'event_type': 'login'
    }
    
    producer.send_message(sample_message)
    producer.close()

if __name__ == '__main__':
    main()