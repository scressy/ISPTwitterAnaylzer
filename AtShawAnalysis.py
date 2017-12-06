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

    # get rid of invalid date values (Nan, NaT, etc)
    df = df[df.orig_created_at.notnull()]

    # getting the time delta and converting to day, hours, min, seconds
    df['delta'] = (df['created_at']-df['orig_created_at']).fillna(pd.to_timedelta("00:00:00"))
    df['delta'] = df['delta'].dt.total_seconds()

    maxDelta = df.loc[df['delta'].idxmax()]
    maxDeltaTime = timedelta(seconds=maxDelta['delta'])

    print("***********************************************")
    print(df)
    print("Number of replies: " + str(len(df.index)))
    print("Max delta: \n" + str(maxDelta))
    print("maxDeltaTime: " + str(maxDeltaTime))

    # find the average
    mean = df['delta'].mean()
    mean = timedelta(seconds=mean)
    return mean

def get_response_range(df, start, end):
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['orig_created_at'] = pd.to_datetime(df['orig_created_at'], errors='coerce')

    startDate = pd.to_datetime(start, format="%Y-%m-%d")
    endDate = pd.to_datetime(end, format="%Y-%m-%d")
    mask = (df['created_at'] > startDate) & (df['created_at'] <= endDate)
    df = df.loc[mask]

    # get rid of invalid date values (Nan, NaT, etc)
    df = df[df.orig_created_at.notnull()]

    # getting the time delta and converting to day, hours, min, seconds
    df['delta'] = (df['created_at']-df['orig_created_at']).fillna(pd.to_timedelta("00:00:00"))
    df['delta'] = df['delta'].dt.total_seconds()

    maxDelta = df.loc[df['delta'].idxmax()]
    maxDeltaTime = timedelta(seconds=maxDelta['delta'])

    print("***********************************************")
    print(df)
    print("Number of replies: " + str(len(df.index)))
    print("Max delta: \n" + str(maxDelta))
    print("maxDeltaTime: " + str(maxDeltaTime))

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
# users = ['ShawHelp']
startDate = '2017-10-27'
endDate = '2017-11-27'

def volume_of_tweets():
    tweets =  pd.read_csv('datasets/atShaw_replies.csv', names=['tweet_date', 'text'],encoding='utf-8',skipinitialspace=True)
    get_volume(tweets)
    plot_volume_of_tweets("at_shawHelp",tweets)

# get average response time over the whole csv
def response_time():
    for user in users:
        tweets =  pd.read_csv('datasets/%s_tweets_replied_to.csv' % user, names=['created_at', 'orig_created_at'],encoding='utf-8',skipinitialspace=True)
        print("Average response time from @" + user + ": " + str(get_response(tweets)))

# used to get dataset for only one month (see dates above)
def response_time_range():
    for user in users:
        tweets =  pd.read_csv('datasets/%s_tweets_replied_to.csv' % user, names=['created_at', 'orig_created_at'],encoding='utf-8',skipinitialspace=True)
        print("Average response time from range @" + user + ": " + str(get_response_range(tweets, startDate, endDate)))

# volume_of_tweets()
response_time()
response_time_range()
