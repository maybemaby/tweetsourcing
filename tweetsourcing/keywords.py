from rake_nltk import Rake


def extract_kwords(tweet_object):
    """Uses RAKE algorithm to extract keywords from
    a tweet.

    Inputs
    ------
    Tweepy tweet object
    Returns
    -------
    List of keywords.
    """
    r = Rake()
    tweet_text = tweet_object.full_text
    r.extract_keywords_from_text(tweet_text)
    extracted = r.get_ranked_phrases()
    return extracted


def create_query(kword_list):
    """Takes keyword list and joins them
    to be used in google search"""
    query = " OR ".join(kword_list)
    return query
