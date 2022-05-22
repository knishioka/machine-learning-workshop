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
        tweet.text
        for tweet in tweepy.Cursor(api.search_tweets, q=keyword).items(n_tweets)
    ]


if __name__ == "__main__":
    get_tweets(keyword="S&P500", n_tweets=10000)
