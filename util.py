import os
import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import umap

plt.rc("font", size=16)
sns.set_style("white")


def run_or_get_pkl(filename, func):
    """
    If the filename is not found, runs the function and saves a pickle to the
    filename ( but this has been commented out for submission)
    :return the output of the function
    """
    if not os.path.isfile(filename):
        # with open(filename, "wb") as file:
        #     mat = func()
        #     # pickle.dump(mat, file, protocol=pickle.HIGHEST_PROTOCOL)
        #     return mat
        return func()
    else:
        return pickle.load(open(filename, "rb"))


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


def plot(frame):
    """
    Takes a plottable frame with labels and plots a scatter graph
    """
    sns.lmplot(
        data=frame,
        x="x",
        y="y",
        hue="label",
        fit_reg=False,
        legend=True,
        legend_out=True,
        scatter_kws={"alpha": 0.8, "s": 50},
    )
    plt.show()
