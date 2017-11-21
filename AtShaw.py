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

#####Shaw ISP
# Open/Create a file to append data
csvFile = open("atShaw.csv", "w")
#Use csv Writer
csvWriter = csv.writer(csvFile)

tweetCriteria = got.manager.TweetCriteria().setQuerySearch('@ShawHelp').setSince("2015-10-21").setUntil("2015-10-22")
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
for tweet in tweets:
    csvWriter.writerow([tweet.date, tweet.text.encode('utf-8')])

# searchQuery = '@ShawHelp'
# retweet_filter='-filter:retweets'       # skips retweets
# q=searchQuery+retweet_filter            # query parameter
# tweetsPerQry = 100
# fName = 'atShaw.csv'
# sinceId = None
#
# max_id = -1L
# maxTweets = 50                          # max number of tweets to put in file
#
# tweetCount = 0
# print("Downloading max {0} tweets".format(maxTweets))
# with open(fName, 'w') as f:
#     while tweetCount < maxTweets:
#         try:
#             if (max_id <= 0):
#                 if (not sinceId):
#                     new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
#                 else:
#                     new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
#                                             since_id=sinceId)
#             else:
#                 if (not sinceId):
#                     new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
#                                             max_id=str(max_id - 1))
#                 else:
#                     new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
#                                             max_id=str(max_id - 1),
#                                             since_id=sinceId)
#             if not new_tweets:
#                 print("No more tweets found")
#                 break
#             for tweet in new_tweets:
#                 # write function goes here
#                 # outtweets = [tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")]
#                 # f.write(outtweets)
#                 # f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
#                 #         '\n')
#             tweetCount += len(new_tweets)
#             print("Downloaded {0} tweets".format(tweetCount))
#             max_id = new_tweets[-1].id
#         except tweepy.TweepError as e:
#             # Just exit if any error
#             print("some error : " + str(e))
#             break
#
# print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
