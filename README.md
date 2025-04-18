# Game Analytics

This project is a game analytics platform that processes and analyzes game event data using a microservices architecture. It includes services for event ingestion, processing, and storage, leveraging technologies like Kafka, PostgreSQL, Spark, and Python.

## Prerequisites

Before running the project, ensure you have the following installed on your system:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Getting Started

Follow these steps to set up and run the project:

### 1. Clone the Repository
```
git clone https://github.com/Buratii/game-analytics.git
cd game-analytics
```

### 2. Build and Start the Services
Run the following command to build and start all services defined in the docker-compose.yml file:

```bash
docker-compose up --build
```

This will start the following services:

- **Zookeeper**: Required for Kafka.
- **Kafka**: Message broker for event streaming.
- **Python App**: Handles event ingestion and publishes events to Kafka.
- **Spark App**: Processes events from Kafka and stores results in PostgreSQL.
- **PostgreSQL**: Database for storing processed analytics data.

### 3. Populate Kafka with Events
The Python app includes a route to populate Kafka with events. Once the services are running, you can use the following HTTP endpoint to send event files to Kafka:

- **Endpoint**: POST /send-event
- **URL**: http://localhost:8000/event/import-file

You need to upload a file containing the event data. You can use tools like Postman or curl to send requests. Example using curl:

```bash
curl -X POST http://localhost:8000/event/import-file \
-F "file=@/path/to/your/event_data.json"
```

### 4. Database Initialization
The PostgreSQL database is automatically initialized with the schema defined in sql/init.sql. This includes tables for storing event counts, unique users, and average time between events.

### 5. Accessing the Services
- **Python App**: Accessible at http://localhost:8000
- **PostgreSQL**: Accessible at localhost:5432 with the following credentials:
  - Username: postgres
  - Password: postgres
  - Database: game_analytics

## Project Structure
- **python/**: Contains the Python app for event ingestion.
- **spark/**: Contains the Spark app for event processing.
- **sql/**: Contains the SQL initialization script for PostgreSQL.
- **docker-compose.yml**: Defines the services and their configurations.

## Stopping the Services
To stop all running services, use:

```bash
docker-compose down
```