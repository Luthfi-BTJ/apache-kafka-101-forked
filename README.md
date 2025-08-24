# How to Run

- Clone the repo
    ```
    git clone https://github.com/ammfat/apache-kafka-101.git
    ```

- Start the docker containers
    ```
    docker-compose up -d
    docker ps
    ```

- Access the Kafka UI at http://localhost:8080


# Kafka CLI Commands

- Open a shell inside the container
    ```
    docker exec -it kafka bash
    ```

- List topics
    ```
    kafka-topics.sh --bootstrap-server localhost:19092 --list
    ```

- Create a topic
    ```
    kafka-topics.sh --bootstrap-server localhost:19092 --create \
    --topic test-topic \
    --partitions 3 \
    --replication-factor 1
    ```

- Describe the topic
    ```
    kafka-topics.sh --bootstrap-server localhost:19092 --describe --topic test-topic
    ```

- Produce messages
    ```
    kafka-console-producer.sh --bootstrap-server localhost:19092 --topic test-topic
    ```

- Consume messages
    ```
    kafka-console-consumer.sh --bootstrap-server localhost:19092 --topic test-topic --from-beginning
    ```

    or with specific group
    ```
    kafka-console-consumer.sh --bootstrap-server localhost:19092 --topic test-topic --group test-group-cli --from-beginning
    ```


# Kafka Python Client (Simple Producer, Consumer, and Transformer)
Open a terminal in the project directory and run the following commands as needed:

- Install the dependencies
    ```
    pip install -r requirements.txt
    ```

- Run the producer
    ```
    python examples\simple_client.py producer
    ```
    Type messages and press Enter to send. Press Enter on an empty line or Ctrl+C to stop.

- Run the consumer
    ```
    python examples\simple_client.py consumer [your TOPIC_NAME name]
    ```
    This will read messages from `test-topic`

- Run the transformer
    ```
    python examples\simple_client.py transformer [your TRANSFORMED_TOPIC name]
    ```
    This will read from `test-topic`, transform messages into uppercase, and send them to `transformed-topic`.

