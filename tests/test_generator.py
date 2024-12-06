import pytest
from unittest.mock import Mock, patch
from src.data_generator.postgres_generator import PostgresDataGenerator

def test_generate_user_data():
    generator = PostgresDataGenerator()
    user_data = generator.generate_user_data()
    
    assert 'user_id' in user_data
    assert 'name' in user_data
    assert 'email' in user_data
    assert 18 <= user_data['age'] <= 80
    assert 20000 <= user_data['income'] <= 200000

@patch('psycopg2.connect')
def test_insert_to_postgres(mock_connect):
    generator = PostgresDataGenerator()
    mock_cursor = Mock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    test_data = generator.generate_user_data()
    generator.insert_to_postgres(test_data)
    
    mock_cursor.execute.assert_called_once()

@patch('kafka.KafkaProducer')
def test_produce_to_kafka(mock_kafka_producer):
    generator = PostgresDataGenerator()
    mock_producer = Mock()
    generator.producer = mock_producer
    
    test_data = generator.generate_user_data()
    generator.produce_to_kafka('test_topic', test_data)
    
    mock_producer.send.assert_called_once_with('test_topic', test_data)