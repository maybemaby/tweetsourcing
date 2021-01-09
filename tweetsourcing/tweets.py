import tweepy, requests
from credentials import *


def create_api():
    auth = tweepy.OAuthHandler(api_key, secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def retrieve_tweet():
    tweet_url = input("Enter the URL of the tweet you would like analyzed.\n")
    tweet_id = tweet_url.split("/status/")[1]
    return api.get_status(tweet_id)


def save_images(tweet_object):
    tweet_images = tweet_object.entities["media"]
    image_url = set()
    for image in tweet_images:
        image_url.add(image["media_url"])
        try:
            res = requests.get(image["media_url"])
            res.raise_for_status()
        except:
            return print("No picture found.")
        image_file = open("image1.jpg", "wb")
        image_file.write(res.content)
        image_file.close()


if __name__ == "__main__":
    api = create_api()
    tweet = retrieve_tweet()
    tweet_body = tweet.text
    save_images(tweet)
