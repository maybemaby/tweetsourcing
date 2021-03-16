import tweets
import keywords
import googlesearch
import imagematch

if __name__ == "__main__":
    # Taking a tweet url and generating a query based off the keywords.
    api = tweets.create_api()
    tweet = tweets.retrieve_tweet(api)
    image_urls = tweets.save_images(tweet)
    if image_urls:
        imagematch.reverse_image_search(image_urls[0])
    print(f'The tweet text: "{tweet.full_text}"')
    wordlist = keywords.extract_kwords(tweet)
    generated_query = keywords.create_query(wordlist)
    startnum = 1
    # Loop for checking best matches in first 50 search results.
    while int(startnum) <= 50:
        results = googlesearch.kword_search(generated_query, startnum)
        try:
            news = googlesearch.categorize_news(results, wordlist, news)
        except:
            news = googlesearch.categorize_news(results, wordlist)
        for site_dict in news.values():
            if site_dict["title"] == "":
                startnum = news["next_page"]
                break
    
    news.pop("next_page")
    for k, v in news.items():
        if v["title"] != "":
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
