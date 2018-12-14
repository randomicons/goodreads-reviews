import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import matplotlib.pyplot as plt


def svm():

    data = pd.read_csv("Data/data.csv")
    x = data.drop('rating', axis=1)
    y = data['rating']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
    svclassifier = SVC(kernel='linear')
    svclassifier.fit(x_train, y_train)

    clf = SVC(gamma='scale', decision_function_shape='ovo')
    clf.fit(x, y)



if __name__ == 'main' :
    svm()