from kafka import KafkaConsumer
import threading
import json

'''
Consumer: consuming messages from kafka using dedicated thread context
'''
class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=['192.168.99.100:9092'],
                                 auto_offset_reset='earliest',
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe(['my-topic'])
        for message in consumer:
            print(message)
