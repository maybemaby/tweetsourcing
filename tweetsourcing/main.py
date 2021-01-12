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
    results = googlesearch.kword_search(generated_query, startnum)
    news = googlesearch.categorize_news(results, wordlist)
    while int(startnum) <= 50:
        for site_dict in news.values():
            if site_dict["title"] == "":
                results = googlesearch.kword_search(generated_query, startnum)
                news = googlesearch.categorize_news(results, wordlist, news)
                startnum = news["next_page"]
                break

    for k, v in news.items():
        try:
            print(
                f"""
            Title: {v['title']}
            Link: {v['link']}
            Keyword Matches: {v['matches']}
            """
            )
        except TypeError:
            break
