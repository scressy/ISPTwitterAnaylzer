# coding: utf-8

import tweepy
import csv
import pandas as pd
import got
import numpy as np
import matplotlib.pyplot as plt

####input your credentials here
consumer_key = 'ejCkcbYsjKRCI6e125bJpG49x'
consumer_secret = 'qqEeJUPeFdlZyETjx6hJxfFw6i1gYWCINpQvdwdJzh7rMKttTu'
access_token = '919666743655538688-bCIJ3vxitH4jX1XE7xj1sUniYGR5pjH'
access_token_secret = 'bDrJFwMNPd54FeeMoDMewBoAR5FQoLySc1ILBH9bs8x98'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

##################################
# Helper functions
##################################
def find_report_dates(rdates, csv_name):
    t =  pd.read_csv(csv_name, names=['tweet_date', 'text'],encoding='utf-8')
    tweets = t['text']
    dates = t['tweet_date']
    count = 0
    for tweet in tweets:
        if 'outage' in tweet or 'Outage' in tweet:
            date = dates[count].split(' ')
            if (date[0] not in rdates):
                rdates.append(date[0])
        count = count + 1

def find_official_report_dates(rdates):
    t =  pd.read_csv('ShawHelp_tweets.csv', names=['tweet_date', 'text'],encoding='utf-8')
    tweets = t['text']
    dates = t['tweet_date']
    count = 0
    for tweet in tweets:
        if 'outage' in tweet or 'Outage' in tweet:
            if ('Not' not in tweet and 'not' not in tweet and 'no' not in tweet and 'n\'t' not in tweet):
                date = dates[count].split(' ')
                if (date[0] not in rdates):
                    rdates.append(date[0])
        count = count + 1

def find_missed_report_dates(rdates, officialrdates, misseddates):
    for rdate in rdates:
        if rdate not in officialrdates:
            misseddates.append(rdate)

##################################
# Plot functions
##################################

def plot_outage_report_numbers(source,df):
    if not df.empty:
        fig = df.iloc[0].plot(kind='bar',rot='horizontal',figsize=(9,6), title='Total Number of Official/Unofficial Outage Reports', ylim=[0,15])
        fig.set_xlabel("Reports")
        fig.set_ylabel("Total Number of Outage Reports")
        
        plt.title('Total Number of Official/Unofficial Outage Reports', fontsize=18)
        plt.savefig('plots/' + source + '_outage_report_numbers')
        
        plt.tight_layout()
        plt.show()

def plot_missed_reports(source,df):
    if not df.empty:
        fig = df.iloc[0].plot.pie(figsize=(7,7), title='Officially Reported vs Unreported Outages', autopct='%.2f', colors=['c','y'], fontsize=16)
        fig.set_aspect('equal')
        fig.set_xlabel(" ")
        fig.set_ylabel(" ")
        
        plt.title('Officially Reported vs Unreported Outages', fontsize=18)
        plt.savefig('plots/' + source + '_outage_missed_reports')
        
        plt.tight_layout()
        plt.show()


##################################
# Main
##################################
#find unofficial outage reports
report_dates = []
find_report_dates(report_dates, 'shawtags.csv')
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
plot_outage_report_numbers('Shaw',df)
md = {'Reported': [officialrdate_num], 'Unreported': [missedrdate_num]}
mdf = pd.DataFrame(md)
plot_missed_reports('Shaw',mdf)