import tweets
import keywords

if __name__ == '__main__':
    api = tweets.create_api()
    tweet = tweets.retrieve_tweet(api)
    tweets.save_images(tweet)
    print(f'The tweet text: "{tweet.full_text}"')
    wordlist = keywords.extract_kwords(tweet)
    print(wordlist)