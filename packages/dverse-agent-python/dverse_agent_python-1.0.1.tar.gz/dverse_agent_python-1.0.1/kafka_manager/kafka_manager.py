import json
import os
import threading
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic
from dotenv import load_dotenv

load_dotenv()


class KafkaManager:
    def __init__(self, group_id="default"):
        config = {
            'bootstrap.servers': os.environ.get("KAFKA_BOOTSTRAP_SERVER"),
            'security.protocol': os.environ.get("KAFKA_SECURITY_PROTOCOL"),
            'sasl.mechanisms': os.environ.get("KAFKA_SASL_MECHANISMS"),
            'sasl.username': os.environ.get("KAFKA_SASL_USERNAME"),
            'sasl.password': os.environ.get("KAFKA_SASL_PASSWORD"),
        }

        self.admin = AdminClient(config)
        self.producer = Producer(config)

        config['group.id'] = group_id
        config['auto.offset.reset'] = 'earliest'

        self.consumer = Consumer(config)
        self.subscriptions = {}

    def send_message(self, topic, message, key=None):
        """
        Sends a message to a Kafka topic

        Args:
            topic (str): The Kafka topic to send the message to
            message (dict[str, str]): The message to send
            key (str): The UI key to use for the message
        """

        self.__create_non_existing_topics(topic)

        headers = {'requestId': key}
        if isinstance(message, dict):
            message = str(message)
        self.producer.produce(topic, value=message.encode('utf-8'), headers=headers)
        self.producer.flush()

    def start_consuming(self):
        """
        Start consuming messages from the subscribed topics
        """

        for topic, callback in self.subscriptions.items():
            threading.Thread(target=self.__consume_messages, args=(topic, callback)).start()

    def subscribe(self, topic, callback):
        """
        Subscribes to a Kafka topic and adds a callback to the subscriptions dictionary

        Args:
            topic (str): The Kafka topic to subscribe to
            callback (func): The callback function to call when a message is received
        """

        self.__create_non_existing_topics(topic)

        self.subscriptions[topic] = callback

    def __list_topics(self):
        """
        Lists all Kafka topics

        Returns:
            list: A list of Kafka topics
        """

        return self.admin.list_topics().topics

    def __create_topic(self, topic, partitions=1, replication=3):
        """
        Creates a new Kafka topic

        Args:
            topic (str): The name of the topic to create
            partitions (int): The number of partitions for the topic
            replication (int): The number of replicas for the topic
        """

        new_topic = NewTopic(topic, num_partitions=partitions, replication_factor=replication)
        fs = self.admin.create_topics([new_topic])

        for topic, f in fs.items():
            try:
                f.result()
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")

    def __create_non_existing_topics(self, topic):
        """
        Creates the specified topics if they do not already exist

        Args:
            topic (str): The Kafka topic to create
        """

        if "^" not in topic:
            if topic not in self.__list_topics():
                self.__create_topic(topic)

    def __consume_messages(self, topic, callback):
        """
        Consumes messages from a Kafka topic and calls the callback function

        Args:
            topic (str): The Kafka topic to consume messages from
            callback (func): The callback function to call when a message is received
        """

        self.consumer.subscribe([topic])
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None or msg.error():
                continue

            x = msg.value().decode('utf-8')
            x = x.replace("'", "\"")
            message = json.loads(x)
            callback(message)
