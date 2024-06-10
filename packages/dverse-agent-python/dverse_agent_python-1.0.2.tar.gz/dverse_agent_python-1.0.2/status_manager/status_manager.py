import threading
import time


class StatusManager:
    def __init__(self, kafka_manager, name):
        """
        Initialize the status manager.

        Args:
            kafka_manager (KafkaManager): The Kafka manager to use for communication.
            name (str): The name of the agentDVerse.
        """
        self.kafka_manager = kafka_manager
        self.name = name

    def start_looping(self):
        """
        Start the status loop.
        """
        threading.Thread(target=self.send_status).start()

    def send_status(self):
        """
        Send the status to the Kafka topic.
        """
        while True:
            self.kafka_manager.send_message("agents.status", {self.name: "ok"})
            time.sleep(5)
