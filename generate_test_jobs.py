import uuid
import datetime
import random
import json
from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('job_keyspace')

def random_payload():
    task_types = ['email', 'backup', 'sms', 'db_sync', 'report']
    task = random.choice(task_types)
    return json.dumps({
        "task": task,
        "target": f"user{random.randint(1, 100)}@example.com",
        "priority": random.choice(["low", "medium", "high"])
    })

def insert_job(job_id, start_time, payload, periodic_flag, period_time):
    session.execute("""
        INSERT INTO JobExecutionHistory (
            job_id, start_time, payload, status, periodic_flag,
            period_time, retry_count, retry_delay, error_message
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        job_id,
        start_time,
        payload,
        'pending',
        periodic_flag,
        period_time,
        0,
        30,
        None
    ))

def generate_jobs(n=10):
    now = datetime.datetime.utcnow()
    for i in range(n):
        job_id = uuid.uuid4()
        offset_seconds = random.randint(30, 300)  # between 30s and 5 min from now
        start_time = now + datetime.timedelta(seconds=offset_seconds)
        payload = random_payload()
        is_periodic = random.choice([True, False])
        period_time = random.choice([60, 120, 300]) if is_periodic else None

        insert_job(job_id, start_time, payload, is_periodic, period_time)

        print(f"Inserted job {job_id} | start_time: {start_time} | periodic: {is_periodic} | payload: {payload}")

if __name__ == '__main__':
    generate_jobs(15)
