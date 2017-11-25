# coding: utf-8

#Twitter Crawler code from
#http: //ipullrank.com/step-step-twitter-sentiment
#-analysis-visualizing-united-airlines-pr-crisis/

import tweepy
import csv
import pandas as pd
import got

####input your credentials here
consumer_key = 'ejCkcbYsjKRCI6e125bJpG49x'
consumer_secret = 'qqEeJUPeFdlZyETjx6hJxfFw6i1gYWCINpQvdwdJzh7rMKttTu'
access_token = '919666743655538688-bCIJ3vxitH4jX1XE7xj1sUniYGR5pjH'
access_token_secret = 'bDrJFwMNPd54FeeMoDMewBoAR5FQoLySc1ILBH9bs8x98'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

users = ['ShawHelp','ShawInfo']
startDate = '2017-11-01'
endDate = '2017-11-11'

for user in users:
    csvFile = open('%s_tweets.csv' % user, "w")
    csvWriter = csv.writer(csvFile)

    tweetCriteria = got.manager.TweetCriteria().setUsername(user).setSince(startDate).setUntil(endDate)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    for tweet in tweets:
        csvWriter.writerow([tweet.date, tweet.text.encode('utf-8')])
