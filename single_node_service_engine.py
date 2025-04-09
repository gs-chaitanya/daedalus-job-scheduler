import datetime
import time
from cassandra.cluster import Cluster
from kafka import KafkaProducer

CASSANDRA_HOSTS = ['127.0.0.1']
KEYSPACE = 'job_keyspace'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TOPIC = 'jobs'
POLL_INTERVAL_SECONDS = 2

cluster = Cluster(CASSANDRA_HOSTS)
session = cluster.connect(KEYSPACE)
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

print("Cassandra and Kafka producers initialized.")

def poll_and_schedule():
    now = datetime.datetime.utcnow()
    query = """
        SELECT job_id, start_time, payload, periodic_flag, period_time
        FROM JobExecutionHistory 
        WHERE status = 'pending' AND start_time <= %s ALLOW FILTERING
    """
    rows = session.execute(query, (now,))
    job_count = 0

    for job in rows:
        job_id = job.job_id
        run_time = job.start_time
        payload = job.payload.encode('utf-8') if job.payload else b''

        print(f"Sending job {job_id} scheduled at {run_time} with payload: {payload.decode()}")
        producer.send(KAFKA_TOPIC, key=str(job_id).encode(), value=payload)
        job_count += 1

        if job.periodic_flag:
            next_run = run_time + datetime.timedelta(seconds=job.period_time)
            session.execute("""
                UPDATE JobExecutionHistory SET start_time=%s, status='pending'
                WHERE job_id=%s
            """, (next_run, job_id))
        else:
            session.execute("""
                UPDATE JobExecutionHistory SET status='queued'
                WHERE job_id=%s
            """, (job_id,))
    
    if job_count == 0:
        print("No jobs found to schedule.")
    else:
        print(f"{job_count} job(s) sent to Kafka.")

def run_scheduler():
    while True:
        try:
            print("Polling Cassandra for jobs...")
            poll_and_schedule()
            producer.flush()
        except Exception as e:
            print("Error:", e)
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == '__main__':
    run_scheduler()
