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

# Source: http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet)
    # print(tweet)
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

def get_sentiment_by_day(df):
    df['sentiment'] = df.apply(lambda x: get_tweet_sentiment(x['text']), axis=1)
    df['tweet_date'] = pd.to_datetime(df['tweet_date'])
    df['day_of_week'] = df['tweet_date'].dt.weekday_name
    df['week_index'] = df['tweet_date'].dt.weekday

    df.sort_values('week_index', inplace=True)
    df = df.drop(['week_index','text'],axis=1)
    grouped = df.groupby(['sentiment','day_of_week'], sort=False)['day_of_week'].count().unstack('sentiment').fillna(0)

    return grouped


################################################################################################
# PLOT STUFF
################################################################################################

# Reference: https://plot.ly/matplotlib/bar-charts/#matplotlib-bar-chart-with-dates
# Creates a pie chart of postive/negative/neutral for tweets
def plot_sentiment_numbers(source,df):
    if not df.empty:
        df['sentiment'] = df.apply(lambda x: get_tweet_sentiment(x['text']), axis=1)
        counts = df['sentiment'].value_counts().to_dict()

        vals = counts.values()
        sentiments = 'Positive','Neutral','Negative'

        fig = plt.figure(figsize=(6,6))

        plt.axis("equal")
        patches, texts, autotexts = plt.pie(vals, labels=sentiments, autopct=make_autopct(vals))
        plt.title('Number of Tweets by Sentiment', fontsize=18)

        for t in texts:
            t.set_size(16)
        for t in autotexts:
            t.set_size(14)

        fig.savefig('plots/' + source + '_sentiment_numbers')

        plt.tight_layout()
        plt.show()

# Creates a bar chart for the TOTAL number of tweets by sentiment for each day of the week
def plot_sentiment_per_day(source,df):
    if not df.empty:
        grouped = get_sentiment_by_day(df)

        fig = grouped.plot(kind='bar',stacked=False,rot='horizontal',figsize=(9,6), title='Number of Tweets by Sentiment')
        fig.set_xlabel("Day of the Week")
        fig.set_ylabel("Total Number of Tweets")

        plt.title('Number of Tweets by Sentiment', fontsize=18)
        plt.savefig('plots/' + source + '_sentiment_by_week')

        plt.tight_layout()
        plt.show()

# Creates a bar chart for the AVERAGE number of tweets by sentiment for each day of the week
def plot_avg_per_day(source,df):
    if not df.empty:
        grouped = get_sentiment_by_day(df)

        print(grouped)

        df.sort_values('tweet_date', inplace=True)
        monday1 = (df.tweet_date[0] - timedelta(days=df.tweet_date[0].weekday()))
        monday2 = (df.tweet_date[len(df.index) - 1] - timedelta(days=df.tweet_date[len(df.index) - 1].weekday()))
        total_weeks = float ((monday1 - monday2).days / 7)

        sentiments = ['positive','neutral','negative']
        for s in sentiments:
            grouped[s] = grouped.apply(lambda x: x[s] / total_weeks, axis=1)

        print(grouped)

        fig = grouped.plot(kind='bar',stacked=False,rot='horizontal',figsize=(9,6), title='Number of Tweets by Sentiment')
        fig.set_xlabel("Day of the Week")
        fig.set_ylabel("Average Number of Tweets")

        plt.title('Number of Tweets by Sentiment', fontsize=18)
        plt.savefig('plots/' + source + '_avg_by_week')

        plt.tight_layout()
        plt.show()


################################################################################################
# MAIN STUFF
################################################################################################

users = ['ShawHelp','ShawInfo']
startDate = '2017-01-01'
endDate = '2017-11-11'

def sentiment_analysis():
    for user in users:
        tweets =  pd.read_csv(user + '_tweets.csv', names=['tweet_date', 'text'],encoding='utf-8')
        plot_sentiment_numbers(user,tweets)

    tweets =  pd.read_csv('shawtags.csv', names=['tweet_date', 'text'],encoding='utf-8')
    plot_sentiment_numbers("hastag_shawInternet",tweets)

def avg_tweets_per_day():
    for user in users:
        tweets =  pd.read_csv(user + '_tweets.csv', names=['tweet_date', 'text'],encoding='utf-8')
        plot_avg_per_day(user,tweets)

    tweets =  pd.read_csv('shawtags.csv', names=['tweet_date', 'text'],encoding='utf-8')
    plot_avg_per_day("hastag_shawInternet",tweets)

def total_tweets_per_day():
    for user in users:
        tweets =  pd.read_csv(user + '_tweets.csv', names=['tweet_date', 'text'],encoding='utf-8')
        plot_sentiment_per_day(user,tweets)

    # tweets =  pd.read_csv('shawtags.csv', names=['tweet_date', 'text'],encoding='utf-8')
    # plot_sentiment_per_day("hastag_shawInternet",tweets)
#
# sentiment_analysis()
avg_tweets_per_day()
# total_tweets_per_day()
