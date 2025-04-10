import time
import datetime
import logging
import uuid

from cassandra.cluster import Cluster
from kazoo.client import KazooClient, KazooState
from kazoo.recipe.election import Election
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],  # Use container name for Docker network
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)



# ----------------------------
# Configuration and Logging
# ----------------------------
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

CASSANDRA_NODES = ['127.0.0.1']
KEYSPACE = "job_space"
ZOOKEEPER_HOSTS = '127.0.0.1:2181'
ELECTION_PATH = '/election/scheduler'

# Dummy queue for testing
dummy_queue = []



# ----------------------------
# Cassandra Connection
# ----------------------------
cluster = Cluster(CASSANDRA_NODES)
session = cluster.connect(KEYSPACE)

# ----------------------------
# ZooKeeper Setup
# ----------------------------
zk = KazooClient(hosts=ZOOKEEPER_HOSTS)
zk.start()

def zk_listener(state):
    if state == KazooState.LOST:
        logging.warning("ZooKeeper session lost!")
    elif state == KazooState.SUSPENDED:
        logging.warning("ZooKeeper connection suspended!")
    elif state == KazooState.CONNECTED:
        logging.info("ZooKeeper connected or reconnected.")

zk.add_listener(zk_listener)

election = Election(zk, ELECTION_PATH)

# ----------------------------
# Leader Task
# ----------------------------
def leader_task():

    logging.info("🚀 I am the leader now. Starting polling loop...")

    while True:
        now = datetime.datetime.utcnow()
        logging.info(f"Polling for jobs scheduled at or before {now}...")

        # Replace "JobSchedule" with your actual table name and adjust fields accordingly.
        query = "SELECT job_id, start_time FROM jobexecutionhistory WHERE start_time <= %s ALLOW FILTERING"
        rows = session.execute(query, (now,))

        for row in rows:
            job_id = row.job_id
            start_time = row.start_time

            message = f"{job_id}:{start_time}"
            producer.send('job_queue', value=message.encode('utf-8'))
            logging.info(f"✅ Pushed job {job_id} to Kafka: {message}")


            # Optionally, mark job as "scheduled" or remove it if one-time

        if dummy_queue:
            logging.info("Current Dummy Queue:")
            for job in dummy_queue:
                logging.info(f"  - {job}")

        # Sleep for 1 minute
        time.sleep(60)

#


# ----------------------------
# Election Runner
# ----------------------------
def run_election():
    logging.info("Starting leader election...")
    election.run(leader_task)

if __name__ == "__main__":
    try:
        run_election()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        zk.stop()
        zk.close()
