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

def sentiment_numbers(ptweets,numNeutral,ntweets):
    dictionary = plt.figure()
    D = {'Positive':len(ptweets), 'Neutral':numNeutral, 'Negative':len(ntweets)}
    plt.bar(range(len(D)), D.values(), align='center')
    plt.xticks(range(len(D)), D.keys())

    plt.show()

# users = ['ShawHelp','ShawInfo']

users = ['ShawHelp']

for user in users:
    tweetCriteria = got.manager.TweetCriteria().setUsername(user).setSince("2017-10-11").setUntil("2017-10-12")
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if get_tweet_sentiment(tweet.text) == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if get_tweet_sentiment(tweet.text) == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    numNeutral = len(tweets)-len(ntweets)-len(ptweets)
    print("Neutral tweets percentage: {} %".format(100*(numNeutral)/len(tweets)))


    # printing first 5 positive tweets
    # print("\n\nPositive tweets:")
    # for tweet in ptweets[:10]:
    #     print(tweet.text)
    # # printing first 5 negative tweets
    # print("\n\nNegative tweets:")
    # for tweet in ntweets[:10]:
    #     print(tweet.text)


    sentiment_numbers(ptweets,numNeutral,ntweets)
