import pprint

import pandas as pd
from nltk import pos_tag, BigramCollocationFinder, BigramAssocMeasures
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import stopwords
from rake_nltk import Rake
from summa import keywords

num_phrases = 5


def top_phrases_summa(revs):
    rev_combined = "\n".join(revs)
    kws = keywords.keywords(rev_combined, split=True, ratio=.5)
    # Gets only adjectives
    kws = list(
        filter(lambda phrase: any(map(lambda w: not w[1].startswith(("NN")), pos_tag(word_tokenize(phrase)))), kws))
    kws = list(filter(lambda phrase: len(word_tokenize(phrase)) > 1, kws))
    return kws


def top_phrases_rake(revs):
    rake = Rake(max_length=2)
    rake.extract_keywords_from_text("\n".join(revs))
    return rake.get_ranked_phrases()


def assess_polarity1(tokens):
    """
    sum polarities and divide by number of tokens
    :param tokens:
    :return: scores
    """
    polarity = 0.0
    for token in tokens:
        syn = list(swn.senti_synsets(token))
        if syn:
            syn = syn[0]
            polarity += syn.neg_score()
            polarity += syn.pos_score()
    return polarity / len(tokens)


def top_phrases_nltk(revs):
    revs = '.\n'.join(revs)
    bigram_measures = BigramAssocMeasures()
    tokens = word_tokenize(revs)
    finder = BigramCollocationFinder.from_words(tokens)
    finder.apply_freq_filter(3)
    finder.apply_word_filter(lambda w: len(w) < 2 or w in stopwords.words("english"))
    colloc = []
    for tup in finder.nbest(bigram_measures.pmi, 50):
        pos = pos_tag(tup)
        if pos[0][1].startswith(("JJ", "RB")) or pos[1][1].startswith(("JJ", "RB")):
            colloc.append(tup)
    return colloc


def revs_of_phrase(revs, phrases):
    return list(filter(lambda rev: any(map(lambda phr: phr in rev, phrases)), revs))


def sents_of_phrase(revs, phrases):
    sents = [sent for rev in revs for sent in sent_tokenize(rev)]
    phr_sents = {}
    for phr in phrases:
        phr_sents[phr] = [sent for sent in sents if phr in sent]

    return phr_sents


def main():
    df = pd.read_csv("data.csv", index_col='index')
    # book_sent_map = {}
    book_phrase_map = {}
    for title, revs in df.groupby('book'):
        revs = revs['review'].values
        phrases = top_phrases_summa(revs)
        phrases = sorted(phrases, key=lambda toks: assess_polarity1(word_tokenize(toks)))[:5]
        # book_sent_map[title] = sents_of_phrase(revs, phrases)
        book_phrase_map[title] = phrases
    pprint.pprint(book_phrase_map)


if __name__ == "__main__":
    main()
