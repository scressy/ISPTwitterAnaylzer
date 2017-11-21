import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from datetime import datetime, timedelta

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
    grouped = df.groupby(['by_month'])['by_month'].count()
    if(debug):
        print(grouped.to_string())

    # separate into month and count

    return grouped

################################################################################################
# PLOT STUFF
################################################################################################

# Creates line graph
def plot_volume_of_tweets(source,df):
    if not df.empty:
        grouped = get_volume(df)

        fig = grouped.plot()
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
    tweets =  pd.read_csv('atShaw.csv', names=['tweet_date', 'text'],encoding='utf-8',skipinitialspace=True)

    # get_volume(tweets)
    plot_volume_of_tweets("at_shawHelp",tweets)

volume_of_tweets()
