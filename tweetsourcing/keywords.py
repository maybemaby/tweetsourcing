from rake_nltk import Rake


def extract_kwords(tweet_object):
    r = Rake()
    tweet_text = tweet_object.full_text
    r.extract_keywords_from_text(tweet_text)
    extracted = r.get_ranked_phrases()
    return extracted