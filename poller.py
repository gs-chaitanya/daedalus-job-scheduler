import datetime
import time
import json
from cassandra.cluster import Cluster
from redis import Redis
from rq import Queue
from rq import Queue, Retry
from jobs import execute_job
from datetime import datetime, timezone, timedelta


CASSANDRA_HOSTS = ['127.0.0.1']
KEYSPACE = 'job_keyspace'
POLL_INTERVAL_SECONDS = 5

cluster = Cluster(CASSANDRA_HOSTS)
session = cluster.connect(KEYSPACE)

redis_conn = Redis(host='localhost', port=6379)
queue = Queue(connection=redis_conn)

print("Cassandra and Redis queue initialized.")

def poll_and_schedule():
    now = datetime.now()
    query = """
        SELECT job_id, start_time, payload, periodic_flag, period_time, retry_count, retry_delay
        FROM JobExecutionHistory 
        WHERE status = 'pending' AND start_time <= %s ALLOW FILTERING
    """
    rows = session.execute(query, (now,))
    job_count = 0

    for job in rows:
        job_id = str(job.job_id)
        run_time = job.start_time
        job_data = {
            "job_id": job_id,
            "start_time": int(run_time.timestamp()),
            "payload": job.payload,
            "periodic_flag": job.periodic_flag,
            "period_time": job.period_time,
            "retry_count": job.retry_count,
            "retry_delay": job.retry_delay
        }

        print(f"Enqueuing job {job_id} scheduled at {run_time}")
        queue.enqueue(
            execute_job,
            args=(job_data,),
            retry=Retry(max=max(1,job.retry_count), interval=job.retry_delay)
        )

        job_count += 1

        if job.periodic_flag:
            next_run = run_time + timedelta(seconds=job.period_time)
            session.execute("""
                UPDATE JobExecutionHistory SET start_time=%s, status='pending'
                WHERE job_id=%s
            """, (next_run, job.job_id))
        else:
            session.execute("""
                UPDATE JobExecutionHistory SET status='queued'
                WHERE job_id=%s
            """, (job.job_id,))
    
    print(f"{job_count} job(s) enqueued." if job_count else "No jobs to schedule.")

def run_scheduler():
    while True:
        try:
            print("Polling Cassandra for jobs...")
            poll_and_schedule()
        except Exception as e:
            print("Error:", e)
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == '__main__':
    run_scheduler()
