import tweepy, requests
from credentials import *


def create_api():
    """Creates api object from tweepy
    using api auth credentials.
    """
    auth = tweepy.OAuthHandler(api_key, secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def retrieve_tweet(api_object):
    """Used to get a tweet object from authorized
    api object.

    Inputs
    ------
    Tweepy api object
    Returns
    -------
    Tweepy tweet object in extended mode.
    """
    tweet_url = input("Enter the URL of the tweet you would like analyzed.\n")
    tweet_id = tweet_url.split("/status/")[1]
    return api_object.get_status(tweet_id, tweet_mode="extended")


def save_images(tweet_object):
    """Used to save any images from desired tweet.

    Inputs
    ------
    Tweepy tweet object
    Returns
    -------
    Saved images in the project folder.
    """
    try:
        tweet_images = tweet_object.entities["media"]
        image_url = set()
    except KeyError:
        return print("No picture found.")
    for image in tweet_images:
        image_url.add(image["media_url"])
        try:
            res = requests.get(image["media_url"])
            res.raise_for_status()
        except:
            return print("No picture found.")
    return image_url
        # image_file = open("image1.jpg", "wb")
        # image_file.write(res.content)
        # image_file.close()


if __name__ == "__main__":
    api = create_api()
    tweet = retrieve_tweet(api)
    tweet_body = print(tweet.full_text)
    save_images(tweet)
