import tweets
import keywords
import googlesearch

if __name__ == "__main__":
    api = tweets.create_api()
    tweet = tweets.retrieve_tweet(api)
    tweets.save_images(tweet)
    print(f'The tweet text: "{tweet.full_text}"')
    wordlist = keywords.extract_kwords(tweet)
    generated_query = keywords.create_query(wordlist)
    startnum = 1
    while startnum <= 50:
        results = googlesearch.kword_search(generated_query, startnum)
        startnum = results["queries"]["nextPage"][0]['startIndex']
        result_items = results["items"]
        for i, item in enumerate(result_items):
            print(f"Result {i}: {item['title']}]\n")
