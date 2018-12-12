import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import umap

from util import run_or_get_pkl

plt.rc("font", size=16)
sns.set_style("white")


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
        scatter_kws={"alpha": 0.8, "s": 4},
    )
    plt.show()


def umap_vis():
    with open('bow_all.p', "rb") as file:
        X = pickle.load(file)

    df = pd.read_csv("data.csv", index_col='index')
    umap_feats = run_or_get_pkl(
        "umap_bow_all.p",
        lambda: umap.UMAP(n_neighbors=10, min_dist=0.001, n_components=2).fit_transform(
            X
        ),
    )
    frame = pd.DataFrame({"x": umap_feats[:, 0], 'y': umap_feats[:, 1], "label": df['rating'].values})
    plot(frame)


if __name__ == "__main__":
    umap_vis()
