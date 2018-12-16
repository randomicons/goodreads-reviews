import pickle

import pandas as pd
import umap
from nltk import pos_tag, BigramCollocationFinder, BigramAssocMeasures
from nltk.corpus import stopwords
from nltk import sent_tokenize
from nltk import word_tokenize
from summa import keywords
from util import run_or_get_pkl, plot

num_phrases = 5


def top_phrases_summa(revs):
    rev_combined = "\n".join(revs)
    kws = keywords.keywords(rev_combined, split=True, ratio=.5)
    # Gets only adjectives
    kws = list(
        filter(lambda phrase: any(map(lambda w: not w[1].startswith(("NN")), pos_tag(word_tokenize(phrase)))), kws))
    kws = list(filter(lambda phrase: len(word_tokenize(phrase)) > 1, kws))
    return kws


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


def umap_vis():
    with open('bow_all.p', "rb") as file:
        X = pickle.load(file)

    df = pd.read_csv("data.csv", index_col='index')
    umap_feats = run_or_get_pkl(
        "umap_bow_all.p",
        lambda: umap.UMAP(n_neighbors=10, min_dist=0.001, n_components=2).fit_transform(X),
    )
    frame = pd.DataFrame({"x": umap_feats[:, 0], 'y': umap_feats[:, 1], "label": df['rating'].values})
    plot(frame)


def umap_vis_by_book():
    with open('bow_book.p', "rb") as file:
        x_list = pickle.load(file)
    for title, rest in pd.read_csv("data.csv", index_col='index').groupby('book'):
        umap_feats = umap.UMAP(n_neighbors=10, min_dist=0.001, n_components=2).fit_transform(x_list[title])
        frame = pd.DataFrame({"x": umap_feats[:, 0], 'y': umap_feats[:, 1], "label": rest['rating']})
        plot(frame)


def main():
    df = pd.read_csv("data.csv", index_col='index')
    book_sent_map = {}
    for title, revs in df.groupby('book'):
        revs = revs['review'].values
        phrases = top_phrases_summa(revs)[:5]
        book_sent_map[title] = sents_of_phrase(revs, phrases)
    print(book_sent_map)


if __name__ == "__main__":
    main()
