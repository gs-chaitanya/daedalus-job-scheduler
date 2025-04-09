
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

USE job_keyspace;

CREATE TABLE JobExecutionHistory (
    job_id UUID,
    execution_id timeuuid,
    start_time timestamp,
    end_time timestamp,
    worker_id text,
    status text,
    error_message text,
    PRIMARY KEY ((job_id), execution_id)
) WITH CLUSTERING ORDER BY (execution_id DESC);

```

Run server: 
``` bash
pip install -r requirements.txt
flask --app server run
```
