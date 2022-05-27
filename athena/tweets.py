import io
import json
import os

import tweepy

API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET = os.environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]


def get_tweets(keyword, n_tweets):
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    tweets = [
        tweet._json
        for tweet in tweepy.Cursor(api.search_tweets, q=keyword).items(n_tweets)
    ]
    return tweets


if __name__ == "__main__":
    tweets = get_tweets(keyword="S&P500 lang:en", n_tweets=1000)
    with io.open("tweets.dat", "w") as f:
        f.write("\n".join(map(json.dumps, tweets)))
