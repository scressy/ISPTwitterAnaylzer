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

# #####Shaw ISP
# # Open/Create a file to append data
# csvFile = open("atShaw_replies.csv", "w")
# #Use csv Writer
# csvWriter = csv.writer(csvFile)
#
# searchQuery = ['@ShawHelp -filter:nativeretweets -from:ShawHelp',
#     '@ShawInfo -filter:nativeretweets -from:ShawInfo',
#     'from:ShawHelp filter:replies']
# # for search queries, use
# # http://www.followthehashtag.com/help/hidden-twitter-search-operators-extra-power-followthehashtag/
# tweetCriteria = got.manager.TweetCriteria().setQuerySearch(searchQuery[2]).setSince("2017-11-20").setUntil("2017-11-22")
# tweets = got.manager.TweetManager.getTweets(tweetCriteria)
# for tweet in tweets:
#     csvWriter.writerow([tweet.date, tweet.text.encode('utf-8')])


#####Shaw ISP test
# tweet = api.statuses_lookup(['643389532105256961'])
# (a1[0].text)
# print(tweet.date)
try:
    tweet = api.get_status(934107406207926272)
    print tweet.created_at
except Exception, e:
    pass
