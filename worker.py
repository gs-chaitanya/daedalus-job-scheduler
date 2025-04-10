from confluent_kafka import Consumer, KafkaException, KafkaError
import sys
import signal

BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC = 'jobs'
GROUP_ID = 'job-worker-group-debug-1'

conf = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',  # Start from beginning if no committed offsets
    'enable.auto.commit': True
}

# Optional: Handle Ctrl+C
def handle_sigint(sig, frame):
    print("🛑 Received interrupt, closing consumer...")
    consumer.close()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

print(f"🚀 Starting Kafka consumer in group '{GROUP_ID}'...")
consumer = Consumer(conf)

def on_assign(consumer, partitions):
    print(f"📦 Assigned partitions: {[f'{p.topic}-{p.partition}' for p in partitions]}")
    # Uncomment to always start at offset 0 (optional)
    # for p in partitions:
    #     p.offset = 0
    # consumer.assign(partitions)

def on_revoke(consumer, partitions):
    print(f"❌ Partitions revoked: {[f'{p.topic}-{p.partition}' for p in partitions]}")

print(f"📡 Subscribing to topic '{TOPIC}'...")
consumer.subscribe([TOPIC], on_assign=on_assign, on_revoke=on_revoke)

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            print("⏳ No message received in this poll.")
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"📭 End of partition {msg.partition()} at offset {msg.offset()}")
            else:
                print(f"❌ Error while consuming: {msg.error()}")
                raise KafkaException(msg.error())
        else:
            print(f"✅ Received message from topic '{msg.topic()}' partition {msg.partition()} offset {msg.offset()}")
            print(f"   ➕ Payload: {msg.value().decode('utf-8')}")

except Exception as e:
    print(f"💥 Unexpected error: {e}")

finally:
    print("👋 Closing Kafka consumer.")
    consumer.close()
