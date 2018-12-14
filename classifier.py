import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from util import run_or_get_pkl


def svm():

    data = run_or_get_pkl("bow_all.p")
    rating = pd.read_csv("data.csv")
    x = data
    y = rating['rating']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
    svclassifier = SVC(gamma='scale', decision_function_shape='ovo', kernel='rbf')
    svclassifier.fit(x_train, y_train)


if __name__ == 'main' :
    svm()