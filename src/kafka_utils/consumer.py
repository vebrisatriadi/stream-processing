import json
import logging
from typing import Callable, Optional
from kafka import KafkaConsumer
from json import loads

class KafkaStreamConsumer:
    def __init__(
        self, 
        bootstrap_servers: list = ['localhost:9092'],
        topic: str = 'default_topic',
        group_id: Optional[str] = None,
        auto_offset_reset: str = 'earliest'
    ):
        """
        Initialize Kafka Consumer
        
        :param bootstrap_servers: List of Kafka broker addresses
        :param topic: Kafka topic to consume from
        :param group_id: Consumer group ID
        :param auto_offset_reset: Offset reset strategy
        """
        try:
            self.consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id or f'{topic}_consumer_group',
                auto_offset_reset=auto_offset_reset,
                enable_auto_commit=True,
                value_deserializer=lambda x: loads(x.decode('utf-8')),
                key_deserializer=lambda x: loads(x.decode('utf-8')) if x else None
            )
            
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            
            self.topic = topic
        except Exception as e:
            self.logger.error(f"Kafka Consumer Initialization Error: {e}")
            raise

    def consume(
        self, 
        process_func: Optional[Callable] = None, 
        batch_size: int = 1
    ):
        """
        Consume messages from Kafka topic
        
        :param process_func: Optional function to process each message
        :param batch_size: Number of messages to process in a batch
        """
        try:
            self.logger.info(f"Starting consumer for topic: {self.topic}")
            
            for message_batch in iter(lambda: list(next(self.consumer) for _ in range(batch_size)), []):
                batch_results = []
                
                for message in message_batch:
                    try:
                        # Log message details
                        self.logger.info(
                            f"Received message from {message.topic} "
                            f"partition {message.partition}"
                        )
                        
                        # Process message if function provided
                        if process_func:
                            result = process_func(message.value)
                            batch_results.append(result)
                        else:
                            batch_results.append(message.value)
                    
                    except Exception as msg_error:
                        self.logger.error(
                            f"Error processing individual message: {msg_error}"
                        )
                
                yield batch_results

        except Exception as e:
            self.logger.error(f"Kafka Consumer Error: {e}")
            raise

    def consume_continuous(
        self, 
        process_func: Callable, 
        error_handler: Optional[Callable] = None
    ):
        """
        Continuously consume messages
        
        :param process_func: Function to process each message
        :param error_handler: Optional function to handle errors
        """
        try:
            for messages in self.consume():
                for message in messages:
                    try:
                        process_func(message)
                    except Exception as msg_error:
                        if error_handler:
                            error_handler(message, msg_error)
                        else:
                            self.logger.error(
                                f"Error processing message: {msg_error}"
                            )
        except KeyboardInterrupt:
            self.logger.info("Consumer stopped by user")
        finally:
            self.close()

    def close(self):
        """
        Close Kafka consumer connection
        """
        try:
            self.consumer.close()
            self.logger.info("Kafka Consumer closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing Kafka Consumer: {e}")

# Example usage
def process_message(message):
    print(f"Processing message: {message}")

def main():
    consumer = KafkaStreamConsumer(
        bootstrap_servers=['localhost:9092'],
        topic='user_events'
    )
    
    # Consume messages with a processing function
    consumer.consume_continuous(process_message)

if __name__ == '__main__':
    main()
    #