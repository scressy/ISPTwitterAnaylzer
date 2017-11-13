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

####input your credentials here
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

# Reference: https://plot.ly/matplotlib/bar-charts/#matplotlib-bar-chart-with-dates
def sentiment_numbers(user,tweets):
    ptweets = len([tweet for tweet in tweets if get_tweet_sentiment(tweet.text) == 'positive'])
    ntweets = len([tweet for tweet in tweets if get_tweet_sentiment(tweet.text) == 'negative'])
    numNeutral = len(tweets)-ntweets-ptweets

    vals = [ptweets, numNeutral, ntweets ]
    sentiments = 'Positive','Neutral','Negative'

    fig = plt.figure(figsize=(6,6))

    plt.axis("equal")
    patches, texts, autotexts = plt.pie(vals, labels=sentiments, autopct='%1.1f%%')
    plt.title('Number of Tweets by Sentiment', fontsize=18)

    for t in texts:
        t.set_size(14)
    for t in autotexts:
        t.set_size(16)

    fig.savefig('plots/' + user + '_sentiment_numbers')

    plt.tight_layout()
    plt.show()

# users = ['ShawHelp','ShawInfo']

users = ['ShawHelp']

for user in users:
    tweetCriteria = got.manager.TweetCriteria().setUsername(user).setSince("2017-10-11").setUntil("2017-10-12")
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    sentiment_numbers(user,tweets)
