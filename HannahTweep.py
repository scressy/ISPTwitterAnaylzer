import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import csv

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'ejCkcbYsjKRCI6e125bJpG49x'
        consumer_secret = 'qqEeJUPeFdlZyETjx6hJxfFw6i1gYWCINpQvdwdJzh7rMKttTu'
        access_token = '919666743655538688-bCIJ3vxitH4jX1XE7xj1sUniYGR5pjH'
        access_token_secret = 'bDrJFwMNPd54FeeMoDMewBoAR5FQoLySc1ILBH9bs8x98'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, user):
        alltweets = []
        tweets = []
        user_name = user;

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.api.user_timeline(screen_name = user_name,count=200)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
        	print ("getting tweets before %s" % (oldest))

        	#all subsiquent requests use the max_id param to prevent duplicates
        	new_tweets = self.api.user_timeline(screen_name = user_name,count=200,max_id=oldest)

        	#save most recent tweets
        	alltweets.extend(new_tweets)

        	#update the id of the oldest tweet less one
        	oldest = alltweets[-1].id - 1

        	print "...%s tweets downloaded so far" % (len(alltweets))

        for tweet in alltweets:
            # empty dictionary to store required params of a tweet
            parsed_tweet = {}

            # saving text of tweet
            parsed_tweet['text'] = tweet.text
            # saving sentiment of tweet
            parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

            # appending parsed tweet to tweets list
            if tweet.retweet_count > 0:
                # if tweet has retweets, ensure that it is appended only once
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

        # return parsed tweets
        return tweets



def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    # users = ['ShawHelp','ShawInfo']

    users = ['ShawHelp']
    for user in users:
        tweets = api.get_tweets(user=user)

        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # percentage of negative tweets
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
        # percentage of neutral tweets
        print("Neutral tweets percentage: {} %".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))

        # printing first 5 positive tweets
        print("\n\nPositive tweets:")
        for tweet in ptweets[:10]:
            print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])


        # #transform the tweepy tweets into a 2D array that will populate the csv
        # outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]
        #
        # #write the csv
        # with open('%s_tweets.csv' % user, 'wb') as f:
        # 	writer = csv.writer(f)
        # 	writer.writerow(["id","created_at","text"])
        # 	writer.writerows(outtweets)


if __name__ == "__main__":
    # calling main function
    main()

# # -*- coding: utf-8 -*-
#
# import tweepy
# import csv
# import pandas as pd
#
# ####input your credentials here
# consumer_key = 'ejCkcbYsjKRCI6e125bJpG49x'
# consumer_secret = 'qqEeJUPeFdlZyETjx6hJxfFw6i1gYWCINpQvdwdJzh7rMKttTu'
# access_token = '919666743655538688-bCIJ3vxitH4jX1XE7xj1sUniYGR5pjH'
# access_token_secret = 'bDrJFwMNPd54FeeMoDMewBoAR5FQoLySc1ILBH9bs8x98'
#
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth,wait_on_rate_limit=True)
#
# #####Shaw ISP
# # Open/Create a file to append data
# csvFile = open('shaw.csv', 'w')
# #Use csv Writer
# csvWriter = csv.writer(csvFile)
#
# users = ['ShawHelp','ShawInfo']
#
# for user in users:
#     user = api.get_user(screen_name = user)
#     csvWriter.writerow([user.screen_name,
#                         user.id, user.statuses_count,
#                         user.description.encode('utf-8')])
#     print (user.id)
