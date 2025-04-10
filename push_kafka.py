import json
import random
import uuid
from datetime import datetime
from confluent_kafka import Producer, Consumer, TopicPartition
from confluent_kafka.admin import AdminClient

# Kafka config
BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC = 'jobs'
GROUP_ID = 'job-worker-group'  # Make sure this matches the consumer group your workers use

producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

def generate_job():
    return {
        "job_id": str(uuid.uuid4()),
        "start_time": datetime.utcnow().isoformat(),
        "payload": f"Job payload {random.randint(1000, 9999)}",
        "status": "PENDING",
        "periodic_flag": random.choice([True, False]),
        "period_time": random.randint(30, 600),
        "retry_count": random.randint(0, 3),
        "retry_delay": random.randint(5, 60),
        "error_message": None
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Job sent to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Produce jobs
N = 10
for _ in range(N):
    job = generate_job()
    job_json = json.dumps(job)
    producer.produce(TOPIC, value=job_json, callback=delivery_report)
    producer.poll(0.1)

producer.flush()
print("🚀 All jobs sent.")

# Reset offsets to 0 for all partitions in the topic for the given group
def reset_offsets_to_zero():
    print("🔁 Resetting consumer group offsets to 0...")

    consumer = Consumer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    })

    metadata = consumer.list_topics(topic=TOPIC, timeout=5)
    partitions = metadata.topics[TOPIC].partitions

    topic_partitions = [TopicPartition(TOPIC, p, 0) for p in partitions]
    consumer.assign(topic_partitions)

    for tp in topic_partitions:
        consumer.seek(tp)
    consumer.commit(offsets=topic_partitions)
    consumer.close()
    print("✅ Offsets reset to 0 for all partitions.")
