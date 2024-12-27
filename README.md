# Stream Processing Infrastructure

This project sets up a complete stream processing infrastructure using Docker Compose, combining Apache Kafka, Apache Flink, PostgreSQL, and a custom data generator.

## Architecture Components

- **PostgreSQL**: Database server for persistent storage
- **Apache Kafka & Zookeeper**: Message broker system for stream processing
- **Apache Flink**: Distributed stream processing framework
- **Custom Data Generator**: Application for generating sample data

## Prerequisites

- Docker
- Docker Compose

## Configuration

The infrastructure consists of the following services:

### PostgreSQL
- Database: `streamdb`
- User: `streamuser`
- Port: `5432`
- Includes initialization scripts in `./sql/`

### Apache Kafka
- Broker Port: `9092`
- Depends on Zookeeper
- Uses Wurstmeister Kafka image (version 2.13-2.7.0)

### Apache Flink
- JobManager UI Port: `8081`
- Includes both JobManager and TaskManager
- Uses Flink version 1.14.4 with Scala 2.12

### Data Generator
- Custom built from local Dockerfile
- Mounts local `./src` directory into container

## Getting Started

1. Clone this repository
2. Start the infrastructure:

### Steps
1. Clone the repository
2. Run `docker-compose up --build`

3. Access the services:
   - Flink Dashboard: `http://localhost:8081`
   - PostgreSQL: `localhost:5432`
   - Kafka: `localhost:9092`

## Volumes

- `postgres_data`: Persistent volume for PostgreSQL data

## Notes

- The data generator will automatically start generating data once the Kafka and PostgreSQL services are available
- SQL initialization scripts should be placed in the `./sql` directory
- Source code for the data generator should be in the `./src` directory

## Data Flow
1. Generate user data in PostgreSQL
2. Stream data to Kafka
3. Flink processes data (income categorization)
4. Processed data written back to PostgreSQL
