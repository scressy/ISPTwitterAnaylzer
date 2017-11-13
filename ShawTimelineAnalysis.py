import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

import pandas as pd
import matplotlib.pyplot as plt

import numpy as np

import csv
import json
import got

consumer_key = 'ejCkcbYsjKRCI6e125bJpG49x'
consumer_secret = 'qqEeJUPeFdlZyETjx6hJxfFw6i1gYWCINpQvdwdJzh7rMKttTu'
access_token = '919666743655538688-bCIJ3vxitH4jX1XE7xj1sUniYGR5pjH'
access_token_secret = 'bDrJFwMNPd54FeeMoDMewBoAR5FQoLySc1ILBH9bs8x98'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Source: http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Source: https://stackoverflow.com/questions/6170246/how-do-i-use-matplotlib-autopct
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

# Reference: https://plot.ly/matplotlib/bar-charts/#matplotlib-bar-chart-with-dates
# Creates a pie chart of postive/negative/neutral for tweets
def plot_sentiment_numbers(source,tweets):
    ptweets = len([tweet for tweet in tweets if get_tweet_sentiment(tweet.text) == 'positive'])
    ntweets = len([tweet for tweet in tweets if get_tweet_sentiment(tweet.text) == 'negative'])
    numNeutral = len(tweets)-ntweets-ptweets

    vals = [ptweets, numNeutral, ntweets ]
    sentiments = 'Positive','Neutral','Negative'

    fig = plt.figure(figsize=(6,6))

    plt.axis("equal")
    patches, texts, autotexts = plt.pie(vals, labels=sentiments, autopct=make_autopct(vals))
    plt.title('Number of Tweets by Sentiment', fontsize=18)

    for t in texts:
        t.set_size(14)
    for t in autotexts:
        t.set_size(16)

    fig.savefig('plots/' + source + '_sentiment_numbers')

    plt.tight_layout()
    plt.show()

def plot_sentiment_per_day(source,tweets):
    dates = []
    sentiments = []
    for tweet in tweets:
        dates.append(tweet.date)
        sentiments.append(get_tweet_sentiment(tweet.text))

    df = pd.DataFrame({'tweet_date':dates,'sentiment':sentiments})

    if not df.empty:
        df['tweet_date'] = pd.to_datetime(df['tweet_date'])
        df['day_of_week'] = df['tweet_date'].dt.weekday_name
        df['week_index'] = df['tweet_date'].dt.weekday

        df.sort_values('week_index', inplace=True)
        grouped = df.groupby(['sentiment','day_of_week'], sort=False)['day_of_week'].count().unstack('sentiment').fillna(0)

        fig = grouped.plot(kind='bar',stacked=True,rot='horizontal',figsize=(9,6), title='Number of Tweets by Sentiment')
        fig.set_xlabel("Day of the Week")
        fig.set_ylabel("Total Number of Tweets")

        plt.title('Number of Tweets by Sentiment', fontsize=18)
        plt.savefig('plots/' + source + '_sentiment_by_week')

        plt.tight_layout()
        plt.show()

users = ['ShawHelp','ShawInfo']
startDate = '2017-11-01'
endDate = '2017-11-11'

def sentiment_analysis():
    for user in users:
        tweetCriteria = got.manager.TweetCriteria().setUsername(user).setSince(startDate).setUntil(endDate)
        shawTweets = got.manager.TweetManager.getTweets(tweetCriteria)

        plot_sentiment_numbers(user,shawTweets)

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#ShawInternet').setSince(startDate).setUntil(endDate)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    plot_sentiment_numbers("hastag_shawInternet",tweets)

def avg_tweets_per_day():
    for user in users:
        tweetCriteria = got.manager.TweetCriteria().setUsername(user).setSince(startDate).setUntil(endDate)
        shawTweets = got.manager.TweetManager.getTweets(tweetCriteria)

        plot_sentiment_per_day(user,shawTweets)

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#ShawInternet').setSince(startDate).setUntil(endDate)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    plot_sentiment_per_day("hastag_shawInternet",tweets)

avg_tweets_per_day()
