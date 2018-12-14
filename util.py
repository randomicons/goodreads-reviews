import os
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

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
