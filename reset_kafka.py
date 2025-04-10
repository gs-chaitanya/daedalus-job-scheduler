from confluent_kafka.admin import AdminClient, NewTopic
import time

# Kafka config
BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_NAME = 'jobs'
NUM_PARTITIONS = 3
REPLICATION_FACTOR = 1

admin = AdminClient({'bootstrap.servers': BOOTSTRAP_SERVERS})

# Step 1: Delete the topic if it exists
def delete_topic(topic_name):
    print(f"🗑️ Deleting topic '{topic_name}'...")
    fs = admin.delete_topics([topic_name], operation_timeout=30)
    for topic, f in fs.items():
        try:
            f.result()
            print(f"✅ Topic '{topic}' deleted.")
        except Exception as e:
            print(f"⚠️ Could not delete topic '{topic}': {e}")

# Step 2: Wait until topic is fully deleted
def wait_for_deletion(topic_name, timeout=10):
    print("⏳ Waiting for topic to be fully removed...")
    for _ in range(timeout):
        metadata = admin.list_topics(timeout=5)
        if topic_name not in metadata.topics:
            print(f"✅ Topic '{topic_name}' is fully deleted.")
            return
        time.sleep(1)
    print("⚠️ Timeout: Topic still appears in metadata.")

# Step 3: Recreate the topic
def create_topic(topic_name, num_partitions, replication_factor):
    print(f"🆕 Creating topic '{topic_name}' with {num_partitions} partitions...")
    new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    fs = admin.create_topics([new_topic])
    for topic, f in fs.items():
        try:
            f.result()
            print(f"✅ Topic '{topic}' created successfully.")
        except Exception as e:
            print(f"❌ Failed to create topic '{topic}': {e}")

# Run full reinitialization
delete_topic(TOPIC_NAME)
wait_for_deletion(TOPIC_NAME)
create_topic(TOPIC_NAME, NUM_PARTITIONS, REPLICATION_FACTOR)
