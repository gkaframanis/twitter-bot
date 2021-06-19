import tweepy
import time
from env_variables import *

# We need to authenticate to verify our account | we get from the app we created
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# We use the tweepy.API to authenticate and now we have access to the API.
api = tweepy.API(auth)

# # Get the tweets of your twitter timeline
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

# # My twitter's account information
# print(api.me())

# My twitter handler
# user = api.me()
# print(user.screen_name)


# Always follow back the people that follow you using the tweepy.Cursor. 
# cursor is a generator | limit handler function to handle the number of hits allowed to the Twitter API in a period of time.
def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        time.sleep(1000)
    except StopIteration:
        return 1


for follower in limit_handler(tweepy.Cursor(api.followers).items()):
    try:
        follower.follow()
    except StopIteration:
        print("You have no followers...")
        break


# Love certain number of tweets based on specific words.
search_string = "python"
number_of_tweets = 2

for tweet in limit_handler(tweepy.Cursor(api.search, search_string).items(number_of_tweets)):
    try:
        # We can also retweet instead of liking some tweets.
        # tweet.retweet()
        tweet.favorite()
        print("I liked that tweet")
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        print("No tweet was found...")
        break