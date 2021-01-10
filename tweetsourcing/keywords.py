from rake_nltk import Rake


def extract_kwords(tweet_object):
    r = Rake(max_length=6)
    tweet_text = tweet_object.full_text
    r.extract_keywords_from_text(tweet_text)
    extracted = r.get_ranked_phrases()
    return extracted


def create_query(kword_list):
    query = " OR ".join(kword_list)
    return query