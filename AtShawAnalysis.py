import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from datetime import datetime, timedelta
import calendar

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

################################################################################################
# HELPER STUFF
################################################################################################

debug = True

# reference https://plot.ly/pandas/line-charts/
def get_volume(df):
    df['by_month'] = pd.to_datetime(df['tweet_date'], errors='coerce').dt.month

    # separate into month and count
    grouped = df.groupby(['by_month'])['by_month'].count().reset_index(name="count")

    # changes month int to month str
    grouped['by_month'] = grouped['by_month'].apply(lambda x: calendar.month_abbr[x])

    if(debug):
        print(grouped)
    return grouped

# get_response takes in a dataframe and returns the mean response time of the dataframe
def get_response(df):
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['orig_created_at'] = pd.to_datetime(df['orig_created_at'], errors='coerce')

    # getting the time delta and converting to day, hours, min, seconds
    df['delta'] = (df['created_at']-df['orig_created_at']).fillna(pd.to_timedelta("00:00:00"))
    df['delta'] = df['delta'].dt.total_seconds()

    # find the average
    mean = df['delta'].mean()
    mean = timedelta(seconds=mean)
    return mean

################################################################################################
# PLOT STUFF
################################################################################################

# Creates line graph
def plot_volume_of_tweets(source,df):
    if not df.empty:
        grouped = get_volume(df)

        fig = grouped.plot.line(x='by_month', y='count', style='-', legend=False, title="Number of Tweets per Month")
        fig.set_xlabel("Months")
        fig.set_ylabel("Number of Tweets")

        # used to save the file
        plt.savefig('plots/' + source + '_volume')

        plt.tight_layout()
        plt.show()

# Reference: https://plot.ly/matplotlib/bar-charts/#matplotlib-bar-chart-with-dates


################################################################################################
# MAIN STUFF
################################################################################################

users = ['ShawHelp','ShawInfo']
startDate = '2017-01-01'
endDate = '2017-11-11'

def volume_of_tweets():
    # tweets =  pd.read_csv('atShaw_replies.csv', names=['tweet_date', 'text'],encoding='utf-8',skipinitialspace=True)
    # get_volume(tweets)
    tweets =  pd.read_csv('ShawInfo_tweets_replied_to.csv', names=['created_at', 'orig_created_at'],encoding='utf-8',skipinitialspace=True)

    print(get_response(tweets))
    # plot_volume_of_tweets("at_shawHelp",tweets)

def look_up(id):
    try:
        tweet = api.get_status(id)
        print tweet.created_at
    except Exception, e:
        pass


volume_of_tweets()
