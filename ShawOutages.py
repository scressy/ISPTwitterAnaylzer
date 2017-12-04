# coding: utf-8

import tweepy
import csv
import pandas as pd
import got
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from collections import Counter

plt.style.use('ggplot')

all_unofficial_dates = []
all_official_dates   = []

##################################
# Helper functions
##################################
def find_report_dates(rdates, csv_name):
    t =  pd.read_csv(csv_name, header=0, names=['tweet_date', 'text'],converters={'tweet_date':str,'text':str})
    tweets = t['text']
    dates = t['tweet_date']
    count = 0
    for tweet in tweets:
        if 'outage' in tweet or 'Outage' in tweet or 'down' in tweet:
            date = dates[count].split(' ')
            all_unofficial_dates.append(date[0])
            if (date[0] not in rdates):
                rdates.append(date[0])
        count = count + 1

def find_official_report_dates(rdates):
    t =  pd.read_csv('datasets/ShawHelp_tweets.csv', names=['tweet_date', 'text'],encoding='utf-8')
    t = t[pd.notnull(t['text'])]
    t = t[pd.notnull(t['tweet_date'])]
    tweets = t['text']
    dates = t['tweet_date']

    count = 0
    for tweet in tweets:
        if 'outage' in tweet or 'Outage' in tweet or 'down ' in tweet:
            if ('Not' not in tweet and 'not' not in tweet and 'no' not in tweet and 'n\'t' not in tweet):
                date = dates[count].split(' ')
                all_official_dates.append(date[0])
                if (date[0] not in rdates):
                    rdates.append(date[0])
        count = count + 1

def find_missed_report_dates(rdates, officialrdates, misseddates):
    for rdate in rdates:
        if rdate not in officialrdates:
            misseddates.append(rdate)

def find_corresponding_tweets(outage_dates, csv_name, outage_tweets):
    t =  pd.read_csv(csv_name, header=0, names=['tweet_date', 'text'],converters={'tweet_date':str,'text':str})
    tweets = t['text']
    dates = t['tweet_date']
    count = 0
    for tweet in tweets:
        date = dates[count].split(' ')
        if (date[0] in outage_dates):
            unitweet = unicode(tweet, 'utf-8')
            outage_tweets.append(unitweet)
        count = count + 1

def find_lag_dates(rdates, csv_name):
    t =  pd.read_csv(csv_name, header=0, names=['tweet_date', 'text'],converters={'tweet_date':str,'text':str})
    tweets = t['text']
    dates = t['tweet_date']
    count = 0
    for tweet in tweets:
        if 'lag' in tweet or 'Lag' in tweet or 'problem' in tweet or 'slow' in tweet or 'Slow' in tweet:
            date = dates[count].split(' ')
            if (date[0] not in rdates):
                rdates.append(date[0])
        count = count + 1

#SENTIMENT ANALYSIS FUNCTIONS FROM OTHER FILE
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


def findOutagesByDayofWeek(dateList):
    df = pd.DataFrame(Counter(dateList).most_common(5), columns=['Date', 'Frequency'])
    df = df.set_index('Date')

    print(df)


##################################
# Plot functions
##################################

def plot_outage_report_numbers(source,df):
    if not df.empty:
        fig = df.iloc[0].plot(kind='bar',rot='horizontal',figsize=(9,6), title='Total Number of Official/Unofficial Outage Reports')
        fig.set_xlabel("Reports")
        fig.set_ylabel("Total Number of Outage Reports")

        plt.title('Total Number of Official/Unofficial Outage Reports', fontsize=18)
        plt.savefig('plots/' + source + '_outage_report_numbers')

        plt.tight_layout()
        plt.show()

def plot_missed_reports(source,df):
    if not df.empty:
        fig = df.iloc[0].plot.pie(figsize=(7,5), title='Officially Reported vs Unreported Outages', autopct='%.2f', fontsize=14)
        fig.set_aspect('equal')
        fig.set_xlabel(" ")
        fig.set_ylabel(" ")

        plt.title('Officially Reported vs Unreported Outages', fontsize=18)
        plt.savefig('plots/' + source + '_outage_missed_reports')

        plt.tight_layout()
        plt.show()

#SENTIMENT ANALYSIS CHART
# Reference: https://plot.ly/matplotlib/bar-charts/#matplotlib-bar-chart-with-dates
# Creates a pie chart of postive/negative/neutral for tweets
def plot_sentiment_numbers(source,df):
    if not df.empty:
        df['sentiment'] = df.apply(lambda x: get_tweet_sentiment(x['text']), axis=1)
        counts = df['sentiment'].value_counts().to_dict()

        vals = counts.values()
        sentiments = counts.keys()

        fig = plt.figure(figsize=(8,6))

        plt.axis("equal")

        patches, texts, autotexts = plt.pie(vals, labels=sentiments, autopct=make_autopct(vals))
        plt.title('Average Sentiment on Outage Dates', fontsize=18)

        for t in texts:
            t.set_size(16)
        for t in autotexts:
            t.set_size(14)

        fig.savefig('plots/' + source + '_sentiment_numbers')

        plt.tight_layout()
    plt.show()

##################################
# Main
##################################
#find unofficial outage reports
report_dates = []
find_report_dates(report_dates, 'datasets/ShawInternet_hashtags.csv')
find_report_dates(report_dates, 'datasets/atShawHelp.csv')
rdate_num = len(report_dates)

#find official outage reports
official_reported_dates = []
find_official_report_dates(official_reported_dates)
officialrdate_num = len(official_reported_dates)

#find missed report dates
missed_dates = []
find_missed_report_dates(report_dates, official_reported_dates, missed_dates)
missedrdate_num = len(missed_dates)

#set up data frame
d = {'Official': [officialrdate_num], 'Unofficial': [rdate_num]}
df = pd.DataFrame(d)
# plot_outage_report_numbers('Shaw',df)
md = {'Reported': [officialrdate_num], 'Unreported': [missedrdate_num]}
mdf = pd.DataFrame(md)
# plot_missed_reports('Shaw',mdf)

#Get tweets corresponding to outage dates
outage_tweets = []
outage_dates = []
outage_dates.extend(official_reported_dates)
outage_dates.extend(missed_dates)
find_corresponding_tweets(outage_dates, 'datasets/ShawInternet_hashtags.csv', outage_tweets)
find_corresponding_tweets(outage_dates, 'datasets/atShawHelp.csv', outage_tweets)

#set up dataframe
sd = {'text': outage_tweets}
sdf = pd.DataFrame(sd)
# plot_sentiment_numbers('ShawOutages',sdf)

#lag analysis
lag_dates = []
find_lag_dates(lag_dates, 'datasets/ShawInternet_hashtags.csv')
find_lag_dates(lag_dates, 'datasets/atShawHelp.csv')
print('Number of days lag or internet problems were reported: ', len(lag_dates)) #the number is 376



print("\n=================================================================")
print("Finding most common dates...")
print("=================================================================")
print("\n************** Unreported **************")
findOutagesByDayofWeek(all_unofficial_dates)
print("\n************** Reported **************")
findOutagesByDayofWeek(all_official_dates)
