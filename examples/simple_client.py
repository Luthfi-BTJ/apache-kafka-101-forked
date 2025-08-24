#!python

import sys
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

TOPIC_NAME = "test-topic"
BROKER = "localhost:9092"


def run_producer():
    """Produces messages to Kafka.

    Messages are read from stdin and sent to the Kafka topic.
    """
    producer = KafkaProducer(
        bootstrap_servers=[BROKER],
        acks=1,  # Require one ack from leader
        # compression_type="snappy",
        # linger_ms=5000,
        # batch_size=100 * 1024
    )

    try:
        while True:
            msg = input("> ")
            if not msg.strip():
                break
            future = producer.send(TOPIC_NAME, value=msg.encode("utf-8"))
            try:
                record_metadata = future.get(timeout=10)
                print(
                    "Sent to Kafka "
                    f"{record_metadata.topic}:{record_metadata.partition} "
                    f"offset {record_metadata.offset}"
                )
            except KafkaError as e:
                print(f"Send failed: {e}")
    except KeyboardInterrupt:
        print("\nProducer stopped.")
    finally:
        # Blocks until all buffered messages are actually sent to the broker.
        producer.flush()
        producer.close()


def run_consumer(group_id: str):
    """Consumes messages from Kafka.

    Messages are read from Kafka and printed to stdout.
    """

    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[BROKER],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id=group_id,
    )

    try:
        for message in consumer:
            print(message.value.decode("utf-8"))
            consumer.commit()
    except KeyboardInterrupt:
        print("\nConsumer stopped.")
    finally:
        consumer.close()

def run_transformer(group_id: str):
    """Consumes, transforms, and produces messages to a new topic."""
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[BROKER],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id=group_id,
    )
    producer = KafkaProducer(
        bootstrap_servers=[BROKER],
        acks=1,
    )
    TRANSFORMED_TOPIC = "transformed-topic"

    try:
        for message in consumer:
            original = message.value.decode("utf-8")
            # Example transformation: uppercase
            transformed = original.upper()
            # Produce to new topic
            producer.send(TRANSFORMED_TOPIC, value=transformed.encode("utf-8"))
            print(f"Transformed and sent: {transformed}")
            consumer.commit()
    except KeyboardInterrupt:
        print("\nTransformer stopped.")
    finally:
        consumer.close()
        producer.flush()
        producer.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py [producer|consumer <groupId>|transformer]")
        sys.exit(1)

    role = sys.argv[1]

    if role == "producer":
        run_producer()
    elif role == "consumer":
        if len(sys.argv) < 3:
            print("Usage: python app.py consumer <groupId>")
            sys.exit(1)
        run_consumer(sys.argv[2])
    elif role == "transformer":
        if len(sys.argv) < 3:
            print("Usage: python app.py transformer <groupId>")
            sys.exit(1)
        run_transformer(sys.argv[2])
    else:
        print("Unknown role:", role)
