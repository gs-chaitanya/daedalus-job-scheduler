import time
import json
import random
from kafka import KafkaConsumer
from cassandra.cluster import Cluster

CASSANDRA_HOSTS = ['127.0.0.1']
KEYSPACE = 'job_keyspace'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TOPIC = 'jobs'

cluster = Cluster(CASSANDRA_HOSTS)
session = cluster.connect(KEYSPACE)

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='worker-group'
)

print("Worker started. Listening to Kafka...")

def execute_job(job_id, payload):
    print(f"Executing job {job_id} with payload: {payload}")
    try:
        data = json.loads(payload)
        time.sleep(random.uniform(0.5, 2.0))  # simulate execution
        if random.random() < 0.2:  # simulate failure 20% of time
            raise Exception("Simulated execution failure")
        print(f"Job {job_id} executed successfully.")
        return 'done', None
    except Exception as e:
        print(f"Job {job_id} failed: {e}")
        return 'failed', str(e)

def update_status(job_id, result, error_msg=None):
    job = session.execute("SELECT retry_count, retry_delay FROM JobExecutionHistory WHERE job_id=%s", (job_id,)).one()
    if not job:
        print(f"Job {job_id} not found in DB.")
        return

    if result == 'done':
        session.execute("""
            UPDATE JobExecutionHistory SET status='done', error_message=%s WHERE job_id=%s
        """, (None, job_id))
    elif job.retry_count > 0:
        session.execute("""
            UPDATE JobExecutionHistory SET status='pending', retry_count=%s WHERE job_id=%s
        """, (job.retry_count - 1, job_id))
        print(f"Retrying job {job_id} in next cycle. Remaining retries: {job.retry_count - 1}")
    else:
        session.execute("""
            UPDATE JobExecutionHistory SET status='failed', error_message=%s WHERE job_id=%s
        """, (error_msg, job_id))
        print(f"Job {job_id} permanently failed after retries.")

for message in consumer:
    job_id = message.key.decode()
    payload = message.value.decode()
    result, error_msg = execute_job(job_id, payload)
    update_status(job_id, result, error_msg)
