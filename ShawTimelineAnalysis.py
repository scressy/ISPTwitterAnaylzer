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



# users = ['ShawHelp','ShawInfo']

users = ['ShawHelp']


tweetCriteria = got.manager.TweetCriteria().setUsername('ShawHelp').setSince("2017-10-01").setUntil("2017-10-12")
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
print("Neutral tweets percentage: {} %".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))
#
# # printing first 5 positive tweets
# print("\n\nPositive tweets:")
# for tweet in ptweets[:10]:
#     print(tweet['text'])
# # printing first 5 negative tweets
# print("\n\nNegative tweets:")
# for tweet in ntweets[:10]:
#     print(tweet['text'])

#transform the tweepy tweets into a 2D array that will populate the csv
# outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]

    # #write the csv
    # with open('%s_tweets.csv' % user, 'wb') as f:
    # 	writer = csv.writer(f)
    # 	writer.writerow(["id","created_at","text"])
    # 	writer.writerows(outtweets)
