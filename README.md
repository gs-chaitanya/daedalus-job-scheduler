# Daedulus
Daedalus Job Scheduler is a distributed, fault-tolerant system for scheduling and executing background jobs with retry and periodic execution support.

## Key Features

1) Scheduled and periodic job execution

2) Automatic retries on failure

3) FastAPI-based RESTful API

4) Persistent storage with Apache Cassandra

5) Job queuing via Redis + RQ

6) Dedicated job polling service

7) Fault-tolerant and reliable execution

8) Modular and scalable architecture

9) Supports high-throughput workloads

## Software Architecture

1) FastAPI API Server: Handles job submission, status queries, and user interactions via REST endpoints.

2) Apache Cassandra: Stores job metadata, execution logs, and retry details in a scalable, distributed database.

3) Job Poller: Periodically checks Cassandra for jobs due for execution and pushes them to the Redis queue.

4) Redis + RQ: Acts as the message broker and job queue, decoupling scheduling from execution and enabling retries.

5) RQ Worker: Processes queued jobs, executes them, and updates the results in Cassandra.

  # Installation 

## Option 1 : Manual Installation (if you're not comfortable with using Docker compose)

 Step 1: Pull and run Cassandra with Docker
```bash
docker pull cassandra:latest
docker run --name cassandra-db -p 9042:9042 -d cassandra:latest
docker exec -it cassandra-db cqlsh
```


Step 2: In cqlsh, run the following:
```sql
CREATE KEYSPACE job_keyspace 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE job_keyspace;
```

Step 3: Create table : (optional)

```sql
CREATE TABLE IF NOT EXISTS JobExecutionHistory (
    job_id UUID PRIMARY KEY,
    start_time timestamp,
    payload text,
    status text,
    periodic_flag boolean,
    period_time int,
    retry_count int,
    retry_delay int,
    error_message text,
    user_id text
);

DESCRIBE TABLES;
DESCRIBE TABLE JobExecutionHistory;
```

Step 4: Install Python dependencies
```bash
pip install -r requirements.txt
```

Step 5: Run the FastAPI server (in fastapi_server.py)
```bash
uvicorn fastapi_server:app --reload
```

Step 6: Pull and run Cassandra with Redis
```bash
docker run -d --name redis-test -p 6379:6379 redis:7
```

Step 7: Start Poller
```bash
python poller.py
```

Step 8: Run the Redis Worker to Frontend Websocket
```bash
uvicorn websocket:app --reload --port 8888
```

Step 9: Setting up the Frontend
```bash
npm i
npm build
npm start
```

And voila!

## Option 2 : Using Docker Compose

bash
docker-compose up --build
