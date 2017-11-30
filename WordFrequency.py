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
    # RegEx for stopwords
    RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
    # replace '|'-->' ' and drop all stopwords

    return (text.str.lower()
               .replace([r'\|', RE_stopwords], [' ', ''], regex=True)
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

    final = pd.DataFrame(Counter(two_words).most_common(top_N), columns=['Biphrase', 'Frequency'])

    return final.set_index('Word')

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

    words = count_words(df['text'])
    two_words = [' '.join(ws) for ws in zip(words, words[1:])]
    # three_words = [' '.join(ws) for ws in zip(words, two_words[1:])]

    word_count = Counter(words)
    two_words_count = Counter(two_words)

    match_dict = {}
    for province in provinces:
        match_dict[province] = 0
        for aword, word_freq in zip(word_count.keys(), word_count.values()):
            if province == 'NL' and (aword == 'newfoundland' or  aword == 'labrador'):
                match_dict[province] += word_freq
            elif province == 'PE' and aword == 'pei':
                match_dict[province] += word_freq
            elif province.lower() == aword or provinces[province].lower() == aword:
                match_dict[province] += word_freq
        for biword, biword_freq in zip(two_words_count.keys(), two_words_count.values()):
            if provinces[province].lower() == biword:
                match_dict[province] += word_freq


    final = pd.DataFrame(match_dict.values(), index=match_dict.keys(), columns=['Frequency'])
    return final;

################################################################################################
# PLOT STUFF
################################################################################################

def plot_word_counts(source,df):
    if not df.empty:
        allCounts = get_most_popular_words(df)

        fig = allCounts.plot.bar(rot=0, figsize=(12,6), width=0.8)

        plt.title('Most Frequent Words', fontsize=18)
        plt.savefig('plots/' + source + '_mostFrequentWords')

        plt.tight_layout()
        plt.show()

def plot_keywords(source,df):
    if not df.empty:
        allCounts = get_keyword_counts(df)

        allCounts.plot.bar(rot=0, figsize=(12,6), width=0.8)

        plt.title('Keyword Counts', fontsize=18)
        plt.savefig('plots/' + source + '_keywordCounts')

        plt.tight_layout()
        plt.show()

def plot_location_counts(source,df):
    if not df.empty:
        allCounts = get_location_counts(df)

        allCounts.plot.bar(rot=0, figsize=(12,6), width=0.8)

        plt.title('Province Counts', fontsize=18)
        plt.savefig('plots/' + source + '_provinceCounts')

        plt.tight_layout()
        plt.show()


################################################################################################
# MAIN STUFF
################################################################################################

users = ['ShawHelp','ShawInfo']

def word_frequency():
    # for user in users:
    #     tweets =  pd.read_csv('datasets/' + user + '_tweets.csv', names=['tweet_date', 'text'],encoding='utf-8',na_values="NaN")
    #     tweets = tweets[pd.notnull(tweets['text'])]
    #
    #     plot_keywords(user,tweets)
    #     plot_word_counts(user,tweets)
    #
    # tweets =  pd.read_csv('datasets/' + users[0] + '_hashtags.csv', names=['tweet_date', 'text'],encoding='utf-8')
    # tweets = tweets[pd.notnull(tweets['text'])]
    #
    # plot_keywords("hastag_shawInternet",tweets)
    # plot_word_counts("hastag_shawInternet",tweets)
    #
    tweets =  pd.read_csv('datasets/atShawHelp.csv', names=['tweet_date', 'text'],encoding='utf-8')
    tweets = tweets[pd.notnull(tweets['text'])]

    plot_keywords("atShawHelp",tweets)
    plot_word_counts("atShawHelp",tweets)
    plot_location_counts("atShawHelp", tweets)

word_frequency()
