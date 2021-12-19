#!/usr/bin/env python
# coding: utf-8
from flask import send_file
import os
import tweepy as tw
from tweepy import OAuthHandler
import pandas as pd
from wordcloud import WordCloud , STOPWORDS , ImageColorGenerator
import matplotlib.pyplot as plt
import re
import os
import config
import collections
import itertools
import base64
import io
import dill 

auth = tw.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

def tweets(term, num):
    txt='Serch for '+ term +' tweets. Number of tweets: '+ str(num)
    return txt

def twtImg(term,num):
    tw_num= int(num)
    hashtag = term
    query = hashtag + ' -filter:retweets'
    tweets = tw.Cursor(api.search_tweets,q=query,lang="en").items(tw_num)
    tweet_text = [tweet.text for tweet in tweets]
    tw_link = []
    tw2 = []
    for tweet in tweet_text:
        tweet_link=tweet.split()[-1]
        tw_link.append(tweet_link)
        tw22 = tweet.split()[:-1]
        tw2.append(" ".join(tw22))
    tweet_df = pd.DataFrame({'Tweets':tw2 , 'Link':tw_link})
    tweet_df2 = pd.DataFrame({'Tweets':tweet_text})    
    tweet_defined=tweet_df["Tweets"].tolist()
    full_tweet = " ".join(tweet_text)
    tweets=full_tweet.split()[1:]
    full_tweetss = " ".join(tweets)
    def clean_data(tweet):
        tweet = " ".join(re.sub("@[\w]*", "", tweet).split())
        tweet = " ".join(re.sub("https://[A-Za-z0-9./]", "", tweet).split())
        tweet = " ".join(re.sub("\n", "", tweet).split())
        tweet = " ".join(re.sub("&amp", "", tweet).split())
        tweet = " ".join(re.sub("#", "", tweet).split())
        tweet = " ".join(re.sub(r"[^\w]", ' ', tweet ).split())
        return tweet
    tweet_2 = [clean_data(tweet) for tweet in tweet_text]
    tweet_3 = [word.lower() for word in tweet_2]
    tweet_4 = [tweet.split() for tweet in tweet_3]
    tweet_5 = list(itertools.chain(*tweet_4))
    noise_words_set = {'https' , 'COVID' , 'TWEET', 'CO' , 'COVIDIOT'
                       , 'VIRUS', 'COVID19' , 'CORONAVIRUS', 'covid19','covid_19','çom'}
    tweet_6 = [' '.join(w for w in place.split() if w.lower() not in noise_words_set)
             for place in tweet_5 ]
    while("" in tweet_6) : 
        tweet_6.remove("")
    unique_string=(" ").join(tweet_6)
    wordcloud = WordCloud(width = 800, height = 800, background_color="white")
    wordcloud.generate(unique_string)
    p = plt.figure(figsize = (12, 12), facecolor = None) 
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(hashtag) 
    F = p.savefig('static/'+hashtag+'.png')   
    
    twt= hashtag + '.png'
    return twt 




