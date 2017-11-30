import re
import tweepy
from collections import Counter
from tweepy import OAuthHandler
from textblob import TextBlob
from datetime import datetime, timedelta
from dateutil import relativedelta as rdelta
import calendar

import nltk
from nltk.corpus import stopwords # Import the stop word list
from nltk.tokenize import wordpunct_tokenize

import pandas as pd
import matplotlib.pyplot as plt

import numpy as np

import csv
import json
import got

plt.style.use('ggplot')

################################################################################################
# HELPER STUFF
################################################################################################

# Source: http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def get_tweet_sentiment(tweet):
    analysis = TextBlob(tweet)
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

    grouped = grouped.reindex(columns=['positive','neutral','negative'])

    return grouped

def get_sentiment_by_month(df):
    df['sentiment'] = df.apply(lambda x: get_tweet_sentiment(x['text']), axis=1)
    df['tweet_date'] = pd.to_datetime(df['tweet_date'])
    df['month_index'] = pd.to_datetime(df['tweet_date'], errors='coerce').dt.month

    df['by_month'] = df['month_index'].apply(lambda x: calendar.month_abbr[x])
    df.sort_values('month_index', inplace=True)
    df['num_days'] = df['tweet_date'].apply(lambda x: calendar.monthrange(x.year,x.month)[1])

    df = df.drop(['month_index','text'],axis=1)

    grouped = df.groupby(['sentiment','by_month','num_days'], sort=False)['by_month'].count().unstack('sentiment').fillna(0)
    sentiments = ['positive','neutral','negative']
    grouped = grouped.reindex(columns=sentiments)

    num_days = grouped.index.get_level_values('num_days')
    i = 0
    for s in sentiments:
        grouped[s] = grouped.apply(lambda x: x[s] / num_days[i], axis=1)
        i = i + 1

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
        sentiments = counts.keys()

        order = ["positive","neutral","negative"]
        d = {k:v for v,k in enumerate(order)}
        sentiments.sort(key=d.get)

        fig = plt.figure(figsize=(6,6))

        plt.axis("equal")

        patches, texts, autotexts = plt.pie(vals, labels=sentiments, autopct=make_autopct(vals))
        plt.title('Percentage of Tweets by Sentiment', fontsize=18)

        for t in texts:
            t.set_size(16)
        for t in autotexts:
            t.set_size(14)

        fig.savefig('plots/' + source + '_sentiment_numbers', bbox_inches='tight')

        plt.tight_layout()
        plt.show()

# Creates a bar chart for the TOTAL number of tweets by sentiment for each day of the week
def plot_sentiment_per_day(source,df):
    if not df.empty:
        grouped = get_sentiment_by_day(df)

        fig = grouped.plot(kind='bar',stacked=True,rot='horizontal',figsize=(9,6), title='Number of Tweets by Sentiment')
        fig.set_xlabel("Day of the Week")
        fig.set_ylabel("Total Number of Tweets")

        plt.title('Total Number of Tweets by Sentiment', fontsize=18)
        plt.savefig('plots/' + source + '_sentiment_by_week', bbox_inches='tight')

        plt.tight_layout()
        plt.show()

def plot_num_per_month(source,df):
    if not df.empty:
        grouped = get_sentiment_by_month(df)

        # total = len(grouped.axes[0])

        fig = grouped.plot.line(figsize=(9,6), title='Number of Tweets by Sentiment')
        plt.xticks(np.arange(12), calendar.month_abbr[1:13])

        fig.set_xlabel("Month")
        fig.set_ylabel("Average Number of Tweets (per day)")

        plt.title('Average Number of Tweets by Sentiment', fontsize=18)
        plt.savefig('plots/' + source + '_sentiment_by_month', bbox_inches='tight')

        plt.tight_layout()
        plt.show()

################################################################################################
# MAIN STUFF
################################################################################################

users = ['ShawHelp','ShawInfo']

def sentiment_analysis():
    for user in users:
        tweets =  pd.read_csv('datasets/' + user + '_tweets.csv', names=['tweet_date', 'text'],encoding='utf-8',na_values="NaN")
        tweets = tweets[pd.notnull(tweets['text'])]

        plot_sentiment_numbers(user,tweets)
        plot_sentiment_per_day(user,tweets)
        plot_num_per_month(user,tweets)

    tweets =  pd.read_csv('datasets/' + users[0] + '_hashtags.csv', names=['tweet_date', 'text'],encoding='utf-8')
    tweets = tweets[pd.notnull(tweets['text'])]

    plot_sentiment_numbers("hastag_shawInternet",tweets)
    plot_sentiment_per_day("hastag_shawInternet",tweets)
    plot_num_per_month("hastag_shawInternet",tweets)

    tweets =  pd.read_csv('datasets/atShawHelp.csv', names=['tweet_date', 'text'],encoding='utf-8')
    tweets = tweets[pd.notnull(tweets['text'])]

    plot_sentiment_numbers("atShawHelp",tweets)
    plot_sentiment_per_day("atShawHelp",tweets)
    plot_num_per_month("atShawHelp",tweets)

sentiment_analysis()
