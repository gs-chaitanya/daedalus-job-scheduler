
## Installation

Job Scheduler

To cassandra db : 

```bash
  docker pull cassandra:latest
  docker run --name cassandra-db -p 9042:9042 -d cassandra:latest
  docker exec -it cassandra-db cqlsh

  
```
In cqlsh run : 
```bash
CREATE KEYSPACE job_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE job_space;

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
    user_id UUID
);                    
DESCRIBE TABLES;
DESCRIBE TABLE JobExecutionHistory;

```

Run server: 
``` bash
pip install -r requirements.txt
flask --app server run
```
