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
    res = service.cse().list(q=query, cx=cse_id, lr="lang_en", start=startnum).execute()
    return res


def categorize_news(results_object, tweet_kwords, *args):
    """Categorizes search results with most matches
    based on the news source they came from.

    Inputs
    ------
    Google search results object
    Keyword list from tweet
    optional: Existing news dict.
    Returns
    --------
    Nested dictionary for each news source with the title
    and link to the article with the most keyword matches.
    """
    result_items = results_object["items"]
    next_page = results_object["queries"]["nextPage"][0]["startIndex"]
    if len(args) > 0:
        news = args[0]
    else:
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
        if article_site in news:
            article_kwords = extract_article(article_link)
        else:
            continue
        kword_matches = keyword_compare(tweet_kwords, article_kwords)
        if kword_matches > news[article_site]["matches"]:
            news[article_site]["title"] = items["title"]
            news[article_site]["link"] = article_link
            news[article_site]["matches"] = kword_matches
    news["next_page"] = next_page
    return news


def extract_article(url):
    """Extracts article text and keywords from url.

    Inputs
    ------
    article url
    Returns
    -------
    Keywords extracted with RAKE
    """
    article = Article(url)
    article.download()
    article.parse()
    r = Rake()
    r.extract_keywords_from_text(article.text)
    article_kwords = r.get_ranked_phrases()
    return article_kwords


def keyword_compare(kwords1, kwords2):
    """Counts matches of keywords in kwords1 to
    keywords in kwords2.

    Inputs
    ------
    list kwords1: Keywords to search for within kwords2.
    list kwords2: Keywords to search from.
    Returns
    -------
    float matches: number of times keyword in kwords1 shows up in kwords2.
    """
    matches = 0
    for kword in set(kwords1):
        match_list = [match for match in set(kwords2) if kword in match]
        matches += len(match_list)
    return matches / len(kwords2)


if __name__ == "__main__":
    query = "charlotte rookie lamello ball OR youngest player OR nba history OR record"
    kword_search(query, 1)
