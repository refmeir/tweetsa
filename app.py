from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api
import json
import threading

from tweets.tweets_repository import TweetsRepository

'''
Web service entry point
'''
flatten = lambda l: [item for sublist in l for item in sublist]

tweet_repository = TweetsRepository('tweets.db')
app = Flask(__name__)
api = Api(app)


@app.route('/')
def pie():
    hourly_stat = tweet_repository.get_hourly_statistics()
    daily_stat = tweet_repository.get_daily_statistics()
    weekly_stat = tweet_repository.get_weekly_statistics()
    if (not hourly_stat) and (not daily_stat) and (not weekly_stat):
        return '<h1>No tweets been found…</h1>'

    # Preparing data for UI
    nchart_types = 3
    chart_type = []
    chart_type += nchart_types * ['hourly']
    chart_type += nchart_types * ['daily']
    chart_type += nchart_types * ['weekly']

    labels = ["Negative", "Neutral", "Positive"]
    labels = labels + labels + labels

    hourly_stat_val = []
    if not hourly_stat:
        hourly_stat_val = [0, 0, 0]
    else:
        hourly_stat_val = list(flatten(hourly_stat)[i] for i in [1, 3, 5])

    daily_stat_val = []
    if not hourly_stat:
        daily_stat_val = [0, 0, 0]
    else:
        daily_stat_val = list(flatten(daily_stat)[i] for i in [1, 3, 5])

    weekly_stat_val = []
    if not weekly_stat:
        weekly_stat_val = [0, 0, 0]
    else:
        weekly_stat_val = list(flatten(weekly_stat)[i] for i in [1, 3, 5])

    values = list(hourly_stat_val + daily_stat_val + weekly_stat_val)

    colors = ["#FF0000", "#FFFF00", "#008000"]
    colors = colors + colors + colors

    return render_template('dashboard.html', title='Sentiment Distribution Dashboard', set=zip(values, labels, colors))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


