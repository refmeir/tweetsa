from kafka   import KafkaProducer
import threading
import json
import time


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Producer: produce message for a given topic using kafka messaging broker
'''

class Producer():
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['192.168.99.100:9092'],
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def send(self, topic, message):
        logger.info(message)
        self.producer.send(topic, message)
        self.producer.flush()


