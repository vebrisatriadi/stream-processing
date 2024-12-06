# Stream Data Processing Project

## Overview
This project demonstrates a comprehensive stream data processing pipeline using:
- PostgreSQL as source and destination database
- Apache Kafka for event streaming
- Apache Flink for stream processing
- Python for implementation
- Docker for containerization

## Architecture
1. **Data Generator**: Produces synthetic user data
2. **Kafka**: Serves as message broker
3. **Flink**: Processes and transforms streaming data
4. **PostgreSQL**: Stores source and processed data

## Setup and Running

### Prerequisites
- Docker
- Docker Compose

### Steps
1. Clone the repository
2. Run `docker-compose up --build`

## Key Components
- `/src`: Source code
- `/docker`: Docker configurations
- `/sql`: Database initialization scripts

## Data Flow
1. Generate user data in PostgreSQL
2. Stream data to Kafka
3. Flink processes data (income categorization)
4. Processed data written back to PostgreSQL
