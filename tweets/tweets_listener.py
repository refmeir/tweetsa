from kafka import KafkaConsumer
import threading
import json
import time

''''
TweetsListener: fetch tweets data from kafka messaging broker using dedicated thread context
'''


class TweetsListener(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)

        self.stop_event = threading.Event()

        self.daemon = True

        # Save tweets repository instance
        self.tweets_repository = kwargs['tweets_repository']

    def run(self):
        tweets_consumer = KafkaConsumer(bootstrap_servers=['192.168.99.100:9092'],
                                        auto_offset_reset='earliest',
                                        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                        session_timeout_ms=300000)

        tweets_consumer.subscribe(['tweet-topic'])
        while not self.stop_event.is_set():
            for tweet_data in tweets_consumer:
                print(tweet_data.value)
                self.tweets_repository.add_tweet(tweet_data.value)
                if self.stop_event.is_set():
                    break

                time.sleep(1)
        tweets_consumer.close()

    def stop(self):
        self.stop_event.set()

