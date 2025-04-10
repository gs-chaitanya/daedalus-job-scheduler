import datetime
import time
import json
import logging
from cassandra.cluster import Cluster
from kafka import KafkaProducer
from kazoo.client import KazooClient, KazooState
from kazoo.recipe.election import Election

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Configuration
CASSANDRA_HOSTS = ['127.0.0.1']
KEYSPACE = 'job_keyspace'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TOPIC = 'jobs'
POLL_INTERVAL_SECONDS = 5
ZOOKEEPER_HOSTS = '127.0.0.1:2182'  # Dedicated ZK container
ELECTION_PATH = '/election/scheduler'

# Cassandra
cluster = Cluster(CASSANDRA_HOSTS)
session = cluster.connect(KEYSPACE)

# Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8')
)

# ZooKeeper
zk = KazooClient(hosts=ZOOKEEPER_HOSTS)
zk.start()

def zk_listener(state):
    if state == KazooState.LOST:
        logging.warning("ZooKeeper session lost")
    elif state == KazooState.SUSPENDED:
        logging.warning("ZooKeeper connection suspended")
    elif state == KazooState.CONNECTED:
        logging.info("Connected to ZooKeeper")

zk.add_listener(zk_listener)
election = Election(zk, ELECTION_PATH)

# Main job polling logic (only run by leader)
def poll_and_schedule():
    now = datetime.datetime.utcnow()
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

        logging.info(f"Enqueuing job {job_id} scheduled at {int(run_time.timestamp())}")
        producer.send(KAFKA_TOPIC, key=job_id, value=job_data)
        job_count += 1

        if job.periodic_flag:
            next_run = run_time + datetime.timedelta(seconds=job.period_time)
            session.execute("""
                UPDATE JobExecutionHistory SET start_time=%s, status='pending'
                WHERE job_id=%s
            """, (next_run, job.job_id))
        else:
            session.execute("""
                UPDATE JobExecutionHistory SET status='queued'
                WHERE job_id=%s
            """, (job.job_id,))

    if job_count:
        logging.info(f"{job_count} job(s) sent to Kafka.")
    else:
        logging.info("No jobs to schedule.")

# Leader-only loop
def leader_task():
    logging.info("Elected as leader. Starting scheduling loop...")
    while True:
        try:
            poll_and_schedule()
            producer.flush()
        except Exception as e:
            logging.error("Error during scheduling: %s", e)
        time.sleep(POLL_INTERVAL_SECONDS)

# Election start
def run_election():
    logging.info("Starting leader election...")
    election.run(leader_task)

if __name__ == '__main__':
    try:
        run_election()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        zk.stop()
        zk.close()
