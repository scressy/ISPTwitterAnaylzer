# coding: utf-8

#Twitter Crawler code from
#http: //ipullrank.com/step-step-twitter-sentiment
#-analysis-visualizing-united-airlines-pr-crisis/

import tweepy
import csv
import pandas as pd
import got

startDate = '2016-11-01'
endDate = '2017-11-27'

#######################################################################
# SHAW TIMELINES
#######################################################################

users = ['ShawHelp','ShawInfo']

for user in users:
    csvFile = open('datasets/%s_tweets.csv' % user, "w")
    csvWriter = csv.writer(csvFile)

    print("Gathering timeline of " + user + "...")
    tweetCriteria = got.manager.TweetCriteria().setUsername(user).setSince(startDate).setUntil(endDate)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    for tweet in tweets:
        csvWriter.writerow([tweet.date, tweet.text.encode('utf-8')])
    print("Done!")

#######################################################################
# AT SHAW HELP
#######################################################################

csvFile = open("datasets/atShawHelp.csv", "w")
csvWriter = csv.writer(csvFile)

searchQuery = ['@ShawHelp -filter:nativeretweets -from:ShawHelp',
    '@ShawInfo -filter:nativeretweets -from:ShawInfo',
    'from:ShawHelp filter:replies']

print("Gathering @ShawHelp tweets...")
tweetCriteria = got.manager.TweetCriteria().setQuerySearch(searchQuery[0]).setSince(startDate).setUntil(endDate)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
for tweet in tweets:
    csvWriter.writerow([tweet.date, tweet.text.encode('utf-8')])

csvFile = open("datasets/atShawHelp_hashtags.csv", "w")
csvWriter = csv.writer(csvFile)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
for tweet in tweets:
    csvWriter.writerow([tweet.date, tweet.hashtags])
print("Done!")


#######################################################################
# HASHTAG SHAW
#######################################################################

hashtags = ['ShawHelp','ShawInfo','ShawInternet']

for hashtag in hashtags:
    csvFile = open('datasets/%s_hashtags.csv' % hashtag, "w")
    csvWriter = csv.writer(csvFile)

    print("Gathering #" + hashtag + " tweets...")
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#%s' % hashtag).setSince(startDate).setUntil(endDate)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    for tweet in tweets:
        csvWriter.writerow([tweet.date, tweet.text.encode('utf-8')])
    print("Done!")
