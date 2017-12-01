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
alltweets = []

#######################################################################
# INITIALIZE USERS, DATES, SEARCH QUERIES
#######################################################################
user_name = "ShawHelp"
date_start = "2017-11-20"
date_end = "2017-11-30"				# this date is NOT included in timeline csv
searchQuery = "from:%s" % user_name

#make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(screen_name = user_name,count=5)

#save most recent tweets
alltweets.extend(new_tweets)

# save the id of the oldest tweet less one
oldest = alltweets[-1].id - 1
print("Oldest: " + str(oldest))

# using getoldtweets to grab tweet timeline
csvFile = open("%s_timeline.csv" % user_name, "w")
csvWriter = csv.writer(csvFile)
tweetCriteria = got.manager.TweetCriteria().setQuerySearch(searchQuery).setSince(date_start).setUntil(date_end)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
for tweet in tweets:
	csvWriter.writerow([tweet.id])
    # csvWriter.writerow([tweet.id, tweet.date, tweet.text.encode('utf-8')])
csvFile.close()

# from csv: grab the first tweet and last tweet (from the start and end date of a timeline)
# we only need to get the tweet status ID
csvFileList = []
with open("%s_timeline.csv" % user_name, "rb") as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		csvFileList.append(row)

# get tweet status ID
startTweet = int(csvFileList[0][0])
endTweet = int(csvFileList[-1][0])

print("startTweet: " + str(startTweet) + " | endTweet: " + str(endTweet))

count_by = 5
count_to_cutoff = count_by	# the number of tweets to chop off at the end of the csv
stop = False
while (len(new_tweets) > 0 and not stop):
	print ("getting tweets before %s" % (oldest))

	#all subsiquent requests use the max_id param to prevent duplicates
	new_tweets = api.user_timeline(screen_name = user_name,count=count_by,max_id=oldest)

	for tweet in new_tweets:
		if (tweet.id == endTweet):
			stop = True
			break
		else:
			print("tweet id: " + str(tweet.id))
			count_to_cutoff = count_to_cutoff-1

	# remove the tweets after the end time
	if(count_to_cutoff > 0):
		new_tweets = new_tweets[:-count_to_cutoff or None]

	#save most recent tweets
	alltweets.extend(new_tweets)

	#update the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	print("Oldest #: " + str(oldest))

	print "...%s tweets downloaded so far" % (len(alltweets))
	count_to_cutoff = count_by

outtweets = []

# remove the tweets before the start time (at the top of the csv)
stop = False
count_to_cutoff = 0

for tweet in alltweets:
	if (tweet.id == startTweet):
		break
	else:
		count_to_cutoff = count_to_cutoff + 1

if(count_to_cutoff > 0):
	alltweets = alltweets[count_to_cutoff:]

# this code is for testing
# outtweets = [[tweet.id_str, tweet.created_at, tweet.in_reply_to_status_id] for tweet in alltweets]

# transform the tweepy tweets into a 2D array that will populate the csv
for tweet in alltweets:
    try:
        original_tweet = api.get_status(tweet.in_reply_to_status_id)
        # outtweets.append([tweet.id_str, tweet.created_at, original_tweet.created_at, tweet.in_reply_to_status_id]) # use to debug
        outtweets.append([tweet.created_at, original_tweet.created_at])
        print(tweet.in_reply_to_status_id)
    except Exception, e:
        print("Exception")
        pass

# write the csv
# the resultant CSV file only contains the tweet reply date, and the original tweet date.
# use this _tweets_replied_to csv for the response time-delta
with open('%s_tweets_replied_to.csv' % user_name, 'wb') as f:
	writer = csv.writer(f)
	# writer.writerow(["created_at","orig_created_at"])
	writer.writerows(outtweets)
