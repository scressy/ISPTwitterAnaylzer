# https://gist.github.com/yanofsky/5436496

#######################################################################
# Introduction: Please read
#######################################################################
# This file produces two csv files:
# (1) username_timeline.csv and (2) username_tweets_replied_to.csv
#
# The two csv files contain:
# (1) gives the whole timeline (needed for (2))
# (2) contains the tweet status IDs of the reply and the original tweet
# (however, (2) does not contain tweets with zero replies).
#
# Please edit the part that says "initialize users and dates".
#
# Use "username_timeline.csv" file and run it under the get_response(csvfile) function
# to see the average time between an original tweet, and a reply to that tweet!

import tweepy #https://github.com/tweepy/tweepy
import csv
import got

#Twitter API credentials
consumer_key = 'ejCkcbYsjKRCI6e125bJpG49x'
consumer_secret = 'qqEeJUPeFdlZyETjx6hJxfFw6i1gYWCINpQvdwdJzh7rMKttTu'
access_token = '919666743655538688-bCIJ3vxitH4jX1XE7xj1sUniYGR5pjH'
access_token_secret = 'bDrJFwMNPd54FeeMoDMewBoAR5FQoLySc1ILBH9bs8x98'

#Twitter only allows access to a users most recent 3240 tweets with this method
#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#initialize a list to hold all the tweepy Tweets
outtweets = []
tweet_date = []
original = []
curr_tweet = []
#######################################################################
# INITIALIZE USERS, DATES, SEARCH QUERIES
#######################################################################
users = ["ShawHelp", "ShawInfo"]
user_name = users[0]
date_start = '2016-11-01'
date_end = '2017-11-27'				# this date is NOT included in timeline csv
searchQuery = "from:%s filter:replies" % user_name

# using getoldtweets to grab tweet timeline
# csvFile = open("%s_timeline.csv" % user_name, "w")
# csvWriter = csv.writer(csvFile)
# tweetCriteria = got.manager.TweetCriteria().setQuerySearch(searchQuery).setSince(date_start).setUntil(date_end)
# tweets = got.manager.TweetManager.getTweets(tweetCriteria)
# for tweet in tweets:
# 	csvWriter.writerow([tweet.id])
#     # csvWriter.writerow([tweet.id, tweet.date, tweet.text.encode('utf-8')])
# csvFile.close()

# put tweet status ID in list
csvFileList = []
with open("%s_timeline.csv" % user_name, "rb") as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		individ = row[0]
		csvFileList.append(individ)

# separate list of tweets into sublist
# each chunk has 100 tweet IDs in it
chunks = [csvFileList[x:x+100] for x in xrange(0, len(csvFileList), 100)]

size = len(chunks)
for i in range(0, size):
	# looks up chunks of tweet IDs
	tweets = api.statuses_lookup(chunks[i])
	tweets.sort(key=lambda tweet: tweet.created_at, reverse=True)

	for tweet in tweets:
		try:
			original_tweet = tweet.in_reply_to_status_id
			curr_tweet.append([tweet.created_at,original_tweet])
			original.append(original_tweet)
			# print("tweet id: " + str(tweet.id) + " created at: " + str(tweet.created_at) + " original_tweet: " + str(original_tweet))
			# outtweets.append([tweet.created_at, original_tweet.created_at])
		except Exception, e:
			pass
	if(i % 5 == 0):
		print(i)

# clear chunks
del chunks[:]

# get chunks of original tweet IDs
chunks = [original[x:x+100] for x in xrange(0, len(original), 100)]
#
# # clear original
del original[:]
orig_date = []

size = len(chunks)
for i in range(0, size):
	# looks up chunks of tweet IDs
	tweets = api.statuses_lookup(chunks[i])

	for tweet in tweets:
		try:
			orig_date.append([tweet.id,tweet.created_at])
			# print("orig_date: " + str(tweet.created_at))
			# outtweets.append([tweet.created_at, original_tweet.created_at])
		except Exception, e:
			pass
	if(i % 5 == 0):
		print(i)


for i in range(0,len(orig_date)):
	for j in range(0,len(orig_date)):
		if(curr_tweet[i][1]==orig_date[j][0]):
			del curr_tweet[i][1]
			curr_tweet[i].append(orig_date[j][1])
			# outtweets[i].append([curr_tweet[i][0], orig_date[j][1]])
			# outtweets[i].append(orig_date[j][1])

# get rid of the attributes with "None"
things_to_remove = []
for i in range(0,len(outtweets)):
	if(len(outtweets[i]) != 2):
		things_to_remove.append(i)

# delete the random blanks
for i in sorted(things_to_remove, reverse=True):
    del curr_tweet[i]

# get tweet status ID

# id = int(csvFileList[0][0])
# tweet = api.get_status(id)
# original_tweet = api.get_status(tweet.in_reply_to_status_id)
# print(id)
#
# size = len(csvFileList)
#
# # get tweet in_reply_to_status_id
# for i in range(0, size):
# 	try:
# 		id = int(csvFileList[i][0])
# 		tweet = api.get_status(id)
# 		original_tweet = api.get_status(tweet.in_reply_to_status_id)
# 		# transform the tweepy tweets into a 2D array that will populate the csv
# 		outtweets.append([tweet.created_at, original_tweet.created_at])
# 	except Exception, e:
# 		pass
# 	if(i % 100 == 0):
# 		print(i)
# print(outtweets)

# write the csv
# the resultant CSV file only contains the tweet reply date, and the original tweet date.
# use this _tweets_replied_to csv for the response time-delta
with open('%s_tweets_replied_to.csv' % user_name, 'wb') as f:
	writer = csv.writer(f)
	# writer.writerow(["created_at","orig_created_at"])
	writer.writerows(curr_tweet)
