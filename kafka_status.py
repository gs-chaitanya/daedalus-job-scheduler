from kafka import KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient
import argparse

def print_topic_status(bootstrap_servers, topic_name, group_id=None):
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
    partitions = consumer.partitions_for_topic(topic_name)

    if partitions is None:
        print(f"Topic '{topic_name}' does not exist.")
        return

    partitions = [TopicPartition(topic_name, p) for p in partitions]
    consumer.assign(partitions)

    beginning_offsets = consumer.beginning_offsets(partitions)
    end_offsets = consumer.end_offsets(partitions)

    print(f"\n📊 Kafka Topic Status: '{topic_name}'\n")
    print(f"{'Partition':<10}{'Start Offset':<15}{'End Offset':<15}{'Lag':<10}")
    print("-" * 50)

    for tp in partitions:
        start = beginning_offsets[tp]
        end = end_offsets[tp]
        lag = end - start

        if group_id:
            group_consumer = KafkaConsumer(
                bootstrap_servers=bootstrap_servers,
                group_id=group_id
            )
            committed = group_consumer.committed(tp)
            if committed is not None:
                lag = end - committed
            else:
                committed = 'N/A'
                lag = 'N/A'
            group_consumer.close()
        else:
            committed = 'N/A'

        print(f"{tp.partition:<10}{start:<15}{end:<15}{lag:<10}")

    consumer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootstrap', default='localhost:9092', help='Kafka bootstrap servers')
    parser.add_argument('--topic', required=True, help='Kafka topic name')
    parser.add_argument('--group', help='Consumer group ID (optional)')
    args = parser.parse_args()

    print_topic_status(args.bootstrap, args.topic, args.group)
