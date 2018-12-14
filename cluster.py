import pickle

import pandas as pd
import umap
from nltk import pos_tag
from nltk import sent_tokenize
from nltk import word_tokenize
from summa import keywords

from util import run_or_get_pkl, plot

num_phrases = 5


def top_phrases_summa(revs):
    rev_combined = "\n".join(revs)
    kws = keywords.keywords(rev_combined, split=True, ratio=.1)
    # Gets only adjectives
    kws = list(
        filter(lambda phrase: any(map(lambda w: w[1].startswith(("JJ", "RB")), pos_tag(word_tokenize(phrase)))), kws))
    return kws


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


if __name__ == "__main__":
    umap_vis_by_book()
