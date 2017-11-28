# https://gist.github.com/yanofsky/5436496

import tweepy #https://github.com/tweepy/tweepy
import csv

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
user_name = "ShawHelp"

#make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(screen_name = user_name,count=50)

#save most recent tweets
alltweets.extend(new_tweets)

# save the id of the oldest tweet less one
oldest = alltweets[-1].id - 1
# oldest = 921869903593848832

while new_tweets[-1].created_at:
	print ("getting tweets before %s" % (oldest))

	#all subsiquent requests use the max_id param to prevent duplicates
	new_tweets = api.user_timeline(screen_name = user_name,count=200,max_id=oldest)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#update the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	print "...%s tweets downloaded so far" % (len(alltweets))

outtweets = []
# transform the tweepy tweets into a 2D array that will populate the csv
for tweet in alltweets:
    try:
        original_tweet = api.get_status(tweet.in_reply_to_status_id)
        outtweets.append([tweet.id_str, tweet.created_at, original_tweet.created_at, tweet.in_reply_to_status_id])
        print(tweet.in_reply_to_status_id)
    except Exception, e:
        print("Exception")
        pass
# outtweets = [[tweet.id_str, tweet.created_at, tweet.in_reply_to_status_id] for tweet in alltweets]

#write the csv
with open('%s___tweets.csv' % user_name, 'wb') as f:
	writer = csv.writer(f)
	writer.writerow(["id","created_at","orig_created_at", "in_reply_to_status_id"])
	writer.writerows(outtweets)
