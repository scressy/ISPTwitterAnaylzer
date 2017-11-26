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
    # grouped = df.groupby(['by_month'])['by_month'].count()
    grouped = df.groupby(['by_month'])['by_month'].count().reset_index(name="count")

    # changes month int to month str, does it from ascending order
    grouped['by_month'] = grouped['by_month'].apply(lambda x: calendar.month_abbr[x])

    if(debug):
        print(grouped)
    return grouped

def get_response(df):

    df['tvalue'] = df.index
    df['by_time'] = pd.to_datetime(df['tweet_date'], errors='coerce')
    df['delta'] = (df['by_time'].shift()-df['by_time']).fillna(pd.to_timedelta("00:00:00"))
    df['delta'] = df['delta'].dt.total_seconds()

    # grouped =  df.groupby(['delta'])['delta'].mean().reset_index(name="average")
    grouped = df['delta'].mean()

    if(debug):
        print(grouped)

    return grouped

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

def plot_response(source,df):
        grouped = get_volume(df)

        fig = grouped.plot.line(kind='bar',rot='horizontal',figsize=(9,6), style='-', legend=False, title="Average Response per Month")
        fig.set_xlabel("Date")
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
    tweets =  pd.read_csv('atShaw_replies.csv', names=['tweet_date', 'text'],encoding='utf-8',skipinitialspace=True)

    # get_volume(tweets)
    get_response(tweets)
    # plot_volume_of_tweets("at_shawHelp",tweets)

volume_of_tweets()
