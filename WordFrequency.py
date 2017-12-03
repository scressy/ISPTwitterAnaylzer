import re
import tweepy
from collections import Counter
from tweepy import OAuthHandler
from textblob import TextBlob
from datetime import datetime, timedelta
from dateutil import relativedelta as rdelta
import calendar

import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords # Import the stop word list
from nltk.tokenize import wordpunct_tokenize

import pandas as pd
import matplotlib.pyplot as plt

import numpy as np

import csv
import json
import got

plt.style.use('ggplot')

################################################################################################
# HELPER STUFF
################################################################################################

def clean_tweet(tweet):
    cleanedTweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])(\w+:\/\/\S+)(')", " ", tweet).split())
    removedPunctuation = ''.join(re.sub(r'[^\w\s]','',cleanedTweet))
    return removedPunctuation

def count_words(text):
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.append('https')
    stopwords.append('http')
    stopwords.append('im')
    stopwords.append('# ')
    # RegEx for stopwords
    RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
    # replace '|'-->' ' and drop all stopwords

    return (text.str.lower()
               .replace([r'\|', RE_stopwords], [' ', ''], regex=True)
               .str.cat(sep=' ')
               .split())

def count_words_uppercase(text):
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.append('https')
    stopwords.append('http')
    stopwords.append('im')
    # RegEx for stopwords
    RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
    # replace '|'-->' ' and drop all stopwords

    return (text.replace([r'\|', RE_stopwords], [' ', ''], regex=True)
               .str.cat(sep=' ')
               .split())

def get_most_popular_words(df):
    top_N = 10

    df['text'] = df['text'].apply(lambda x: clean_tweet(x))

    words = count_words(df['text'])
    final = pd.DataFrame(Counter(words).most_common(top_N), columns=['Word', 'Frequency'])

    return final.set_index('Word')

def get_most_popular_lengthtwo(df):
    top_N = 10

    df['text'] = df['text'].apply(lambda x: clean_tweet(x))

    words = count_words(df['text'])
    two_words = [' '.join(ws) for ws in zip(words, words[1:])]

    final = pd.DataFrame(Counter(two_words).most_common(top_N), columns=['Words', 'Frequency'])
    final = final.set_index('Words')

    print("\n************** Top 10 Words (of Length 2) **************")
    print(final)


def get_most_popular_lengththree(df):
    top_N = 10

    df['text'] = df['text'].apply(lambda x: clean_tweet(x))

    words = count_words(df['text'])
    two_words = [' '.join(ws) for ws in zip(words, words[1:])]
    three_words = [' '.join(ws) for ws in zip(words, two_words[1:])]

    final = pd.DataFrame(Counter(three_words).most_common(top_N), columns=['Words', 'Frequency'])
    final = final.set_index('Words')

    print("\n************** Top 10 Words (of Length 3) **************")
    print(final)


def get_most_popular_hashtags(df):
    top_N = 10

    df['hashtags'] = df['hashtags'].apply(lambda x: clean_tweet(x))

    hashtags = count_words(df['hashtags'])
    final = pd.DataFrame(Counter(hashtags).most_common(top_N), columns=['Hashtag', 'Frequency'])
    final = final.set_index('Hashtag')

    print("\n************** Top 10 Hashtags **************")
    print(final)

def get_keyword_counts(df):
    keywords = ['out','lag','slow','down','switch']

    df['text'] = df['text'].apply(lambda x: clean_tweet(x))

    words = count_words(df['text'])
    word_count = Counter(words)

    match_dict = {}
    for keyword in keywords:
        match_dict[keyword] = 0
        for aword, word_freq in zip(word_count.keys(), word_count.values()):
            if keyword == "out":
                match_dict[keyword] = word_freq
            elif keyword in aword:
                match_dict[keyword] += word_freq

    final = pd.DataFrame(match_dict.values(), index=match_dict.keys(), columns=['Frequency'])
    return final;

def get_location_counts(df):
    provinces = {
        'AB': 'Alberta',
        'BC': 'British Columbia',
        'MB': 'Manitoba',
        'NB': 'New Brunswick',
        'NL': 'Newfoundland and Labrador',
        'NS': 'Nova Scotia',
        'ON': 'Ontario',
        'PE': 'Prince Edward Island',
        'QC': 'Quebec',
        'SK': 'Saskatchewan'
    }

    df['text'] = df['text'].apply(lambda x: clean_tweet(x))

    words = count_words_uppercase(df['text'])
    two_words = [' '.join(ws) for ws in zip(words, words[1:])]
    # three_words = [' '.join(ws) for ws in zip(words, two_words[1:])]

    word_count = Counter(words)
    two_words_count = Counter(two_words)

    match_dict = {}
    for province in provinces:
        match_dict[provinces[province]] = 0
        for aword, word_freq in zip(word_count.keys(), word_count.values()):
            if province == 'NL' and (aword.lower() == 'newfoundland' or aword.lower() == 'labrador'):
                match_dict[provinces[province]] += word_freq
            elif province == 'PE' and aword.lower() == 'pei':
                match_dict[provinces[province]] += word_freq
            elif province == aword or provinces[province].lower() == aword.lower():
                match_dict[provinces[province]] += word_freq
        for biword, biword_freq in zip(two_words_count.keys(), two_words_count.values()):
            if provinces[province].lower() == biword.lower():
                match_dict[provinces[province]] += biword_freq

    final = pd.DataFrame(match_dict.values(), index=match_dict.keys(), columns=['Frequency'])

    print("\n************** Counts of Locations **************")
    print(final);


################################################################################################
# PLOT STUFF
################################################################################################

def plot_word_counts(source,df):
    if not df.empty:
        allCounts = get_most_popular_words(df)

        fig = allCounts.plot.bar(rot=0, figsize=(10,6), width=0.8)

        plt.title('Most Frequent Words', fontsize=18)
        plt.savefig('plots/' + source + '_mostFrequentWords', bbox_inches='tight')

        plt.tight_layout()
        plt.show()

def plot_keywords(source,df):
    if not df.empty:
        allCounts = get_keyword_counts(df)

        allCounts.plot.bar(rot=0, figsize=(10,6), width=0.8)

        plt.title('Keyword Counts', fontsize=18)
        plt.savefig('plots/' + source + '_keywordCounts', bbox_inches='tight')

        plt.tight_layout()
        plt.show()

################################################################################################
# MAIN STUFF
################################################################################################

users = ['ShawHelp','ShawInfo']

def word_frequency():
    print("\n=================================================================")
    print("Word Frequency Analysis of Tweets from ShawHelp")
    print("=================================================================")

    tweets =  pd.read_csv('datasets/' + users[0] + '_tweets.csv', names=['tweet_date', 'text'],encoding='utf-8',na_values="NaN")
    tweets = tweets[pd.notnull(tweets['text'])]

    get_most_popular_lengthtwo(tweets)
    get_most_popular_lengththree(tweets)

    print("\n=================================================================")
    print("Word Frequency Analysis of Tweets @ShawHelp")
    print("=================================================================")
    tweets = pd.read_csv('datasets/atShawHelp.csv', names=['tweet_date', 'text'],encoding='utf-8')
    tweets = tweets[pd.notnull(tweets['text'])]

    plot_keywords("atShawHelp",tweets)
    plot_word_counts("atShawHelp",tweets)
    get_location_counts(tweets)
    get_most_popular_lengthtwo(tweets)
    get_most_popular_lengththree(tweets)

    tweets = pd.read_csv('datasets/atShawHelp_hashtags.csv', names=['tweet_date', 'hashtags'],encoding='utf-8')
    tweets = tweets[pd.notnull(tweets['hashtags'])]
    get_most_popular_hashtags(tweets)

word_frequency()
