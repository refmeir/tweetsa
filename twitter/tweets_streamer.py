
import json
import csv
import re
from twython import TwythonStreamer

import logging

from messaging.producer import Producer

'''
TweetsStreamer: fetch tweets from twitter and foreword these tweets through kafaka messaging broker
'''


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TweetsStreamer(TwythonStreamer):
    def __init__(self):
        # Load credentials from json file
        with open("twitter/twitter_credentials.json", "r") as file:
            creds = json.load(file)
            TwythonStreamer.__init__(self, creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'], creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

        self.tweet_producer = Producer()

    def on_success(self, data):
        if data['lang'] == 'en':
            tweet_data = TweetsStreamer.tweet_format(data)
            logger.info(tweet_data)
            self.tweet_producer.send('tweet-topic', tweet_data)
            # TweetsStreamer.to_csv(tweet_data)

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

    @staticmethod
    def clean_tweet(tweet):
        # removing links and special characters
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    @staticmethod
    def tweet_format(tweet):
        tf = {}
        tf['created_at'] = tweet['created_at']
        tf['text'] = TweetsStreamer.clean_tweet(tweet['text'])
        return tf

    @staticmethod
    def to_csv(tweet):
        try:
            with open(r'tweets1.csv', 'a') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"')
                writer.writerow(list(tweet.values()))
        except:
            print(tweet)

