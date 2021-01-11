from googleapiclient.discovery import build
from credentials import cse_api_key, cse_id
from newspaper import Article
from rake_nltk import Rake


def kword_search(query, startnum):
    """Performs google customsearch.

    Inputs
    -------
    str: query (list of keywords)
    int: Starting search result index
    Returns
    -------
    google customsearch Results object.
    """
    service = build("customsearch", "v1", developerKey=cse_api_key)
    res = service.cse().list(q=query, cx=cse_id, start=startnum).execute()
    return res


def categorize_news(results_object, tweet_kwords):
    result_items = results_object["items"]
    news = {
        "apnews.com": {"title": "", "link": "", "matches": 0},
        "abcnews.go.com": {"title": "", "link": "", "matches": 0},
        "www.cnn.com": {"title": "", "link": "", "matches": 0},
        "www.foxnews.com": {"title": "", "link": "", "matches": 0},
        "www.msnbc.com": {"title": "", "link": "", "matches": 0},
        "www.nationalreview.com": {"title": "", "link": "", "matches": 0},
        "www.nytimes.com": {"title": "", "link": "", "matches": 0},
        "www.reuters.com": {"title": "", "link": "", "matches": 0},
        "www.theepochtimes.com": {"title": "", "link": "", "matches": 0},
        "www.washingtonpost.com": {"title": "", "link": "", "matches": 0},
    }
    for items in result_items:
        article_link = items["link"]
        article_site = items["displayLink"]
        article_kwords = extract_article(article_link)
        kword_matches = keyword_compare(tweet_kwords, article_kwords)
        if kword_matches > news[article_site]["matches"]:
            news[article_site]["title"] = items["title"]
            news[article_site]["link"] = article_link
            news[article_site]["matches"] = kword_matches
    return news


def extract_article(url):
    article = Article(url)
    article.download()
    article.parse()
    r = Rake()
    r.extract_keywords_from_text(article.text)
    article_kwords = r.get_ranked_phrases()
    return article_kwords


def keyword_compare(kwords1, kwords2):
    matches = 0
    for kword in kwords1:
        for kword2 in kwords2:
            if kword in kword2:
                matches += 1
    return matches


if __name__ == "__main__":
    query = "charlotte rookie lamello ball OR youngest player OR nba history OR record"
    kword_search(query, 1)
