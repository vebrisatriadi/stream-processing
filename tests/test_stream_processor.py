import pytest
from unittest.mock import Mock, patch
from src.flink_jobs.stream_processor import UserEventProcessor

def test_income_categorization():
    processor = UserEventProcessor()
    
    test_cases = [
        (30000, 'LOW_INCOME'),
        (75000, 'MIDDLE_INCOME'),
        (150000, 'HIGH_INCOME')
    ]
    
    for income, expected_category in test_cases:
        result = processor._categorize_income(income)
        assert result == expected_category

@patch('pyflink.table.StreamTableEnvironment')
def test_setup_kafka_source(mock_table_env):
    processor = UserEventProcessor()
    processor.setup_kafka_source()
    
    mock_table_env.connect.assert_called_once()

@patch('pyflink.table.StreamTableEnvironment')
def test_setup_postgres_sink(mock_table_env):
    processor = UserEventProcessor()
    processor.setup_postgres_sink()
    
    mock_table_env.connect.assert_called_once()