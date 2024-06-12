# web_monitor/kafka_producer.py
from kafka import KafkaProducer
import json


class KafkaProducerWrapper:
    def __init__(self, kafka_server, kafka_topic):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.kafka_topic = kafka_topic

    def send(self, message):
        self.producer.send(self.kafka_topic, message)
        self.producer.flush()
