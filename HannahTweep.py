# -*- coding: utf-8 -*-

import tweepy
import csv
import pandas as pd

####input your credentials here
consumer_key = 'ejCkcbYsjKRCI6e125bJpG49x'
consumer_secret = 'qqEeJUPeFdlZyETjx6hJxfFw6i1gYWCINpQvdwdJzh7rMKttTu'
access_token = '919666743655538688-bCIJ3vxitH4jX1XE7xj1sUniYGR5pjH'
access_token_secret = 'bDrJFwMNPd54FeeMoDMewBoAR5FQoLySc1ILBH9bs8x98'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#####Shaw ISP
# Open/Create a file to append data
csvFile = open('shaw.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

users = ['ShawHelp','ShawInfo']
#
for user in users:
    user = api.get_user(screen_name = user)
    csvWriter.writerow([user.screen_name,
                        user.id, user.followers_count,
                        user.description.encode('utf-8')])
    print (user.id)
#
# for tweet in tweepy.Cursor(api.get_user,screen_name = 'ShawHelp').items():
#     print (tweet.created_at, tweet.text)
#     csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
