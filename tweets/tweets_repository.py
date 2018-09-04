from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import pandas as pd
from textblob import TextBlob
import datetime
import threading

from tweets.tweets_listener import TweetsListener
'''
TweetsRepository: Persist incoming tweets, calculate sentiment analysis for each tweet, 
retrieve sentiment distribution for last hour, day and week 
'''


Base = declarative_base()

# Declaration of tweet table
class Tweet(Base):
    __tablename__ = 'tweet_table'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    tweet_text = Column(String)
    sentiment = Column(Integer)


class TweetsRepository:
    def __init__(self, db_filename):
        self.engine = create_engine('sqlite:///' + db_filename)
        session_factory = sessionmaker()
        session_factory.configure(bind=self.engine, expire_on_commit=False, autoflush=False)
        Base.metadata.create_all(self.engine)
        self.session = scoped_session(session_factory)

        # Activate tweets listener thread
        self.tweets_listener = TweetsListener(kwargs={'tweets_repository': self})
        self.tweets_listener.start()
        # primitive lock object
        self.lock = threading.Lock()

    def add_tweet(self, tweet_data):
        with self.lock:
            timestamp = datetime.datetime.strptime(tweet_data['created_at'], '%a %b %d %H:%M:%S %z %Y')
            tweet_text = tweet_data['text']
            if tweet_text is None:
                return
            sentiment = TweetsRepository.analyze_sentiment(tweet_text)
            tweet_rec = Tweet(timestamp=timestamp, tweet_text = tweet_text, sentiment= sentiment)
            self.session.add(tweet_rec)
            self.session.commit()

    def get_tweets(self):
        with self.lock:
            return pd.read_sql_table(table_name=Tweet.__tablename__, con=self.engine, index_col='timestamp')

    def get_sentiment_statistics(self, nhours):
        with self.lock:
            dt = datetime.timedelta(hours=nhours)
            now = datetime.datetime.utcnow()
            since = now - dt
            query_res = self.session.query(Tweet.sentiment, func.count()).filter((Tweet.timestamp >= since) & (Tweet.timestamp <= now)).group_by(Tweet.sentiment)
            return query_res.all()

    def get_hourly_statistics(self):
        return self.get_sentiment_statistics(nhours=12)

    def get_daily_statistics(self):
        return self.get_sentiment_statistics(nhours=24)

    def get_weekly_statistics(self):
        return self.get_sentiment_statistics(nhours=7*24)

    def load_tweets_from_csv(self, csv_fn):
        df = pd.read_csv(csv_fn, parse_dates=True, index_col='timestamp', header=None, names=['timestamp', 'tweet_text'])
        # Remove empty text records
        df = df[pd.notnull(df['tweet_text'])]

        # Perform sentiment analysis for each tweet
        df['sentiment'] = None
        for index, row in df.iterrows():
            print(index, row['tweet_text'], TweetsRepository.analyze_sentiment(row['tweet_text']))
            row['sentiment'] = TweetsRepository.analyze_sentiment(row['tweet_text'])

        df.to_sql(con=self.engine, name=Tweet.__tablename__, if_exists='replace')

    @staticmethod
    # Calculate sentiment analysis for a given tweet
    def analyze_sentiment(tweet_text):
        if isinstance(tweet_text, str):
            analysis = TextBlob(tweet_text)
            if analysis.sentiment.polarity > 0:
                return 1
            elif analysis.sentiment.polarity == 0:
                return 0
            else:
                return -1
        else:
            return None


