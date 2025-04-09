from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'jobs',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    consumer_timeout_ms=10000  # stop after 10s of no messages
)

print("Listening to Kafka 'jobs' topic...")
for message in consumer:
    print(f"[Kafka] job_id = {message.key.decode()} | payload = {message.value.decode()}")
