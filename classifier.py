import numpy as np
import pandas as pd
from keras import Sequential, regularizers
from keras.layers import Dense
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import KFold, GridSearchCV, train_test_split
from sklearn.svm import SVC

import to_vec
from util import run_or_get_pkl

"""
Run the learning algorithms
"""


def main():
    df = pd.read_csv("data.csv")
    data = run_or_get_pkl("bow_all.p", lambda: to_vec.create_vec_with_all(df))
    y = df['rating'].values
    X, X_test, y_train, y_test = train_test_split(data, y, test_size=0.20)
    logi_reg(X, y, X_test, y_test)
    random_forest(X, y, X_test, y_test)
    svm(X, y, X_test, y_test)
    svm_grid_search(data, y)
    # tokenizer = Tokenizer(num_words=data.shape[1])
    # tokenizer.fit_on_texts(df['review_c'].values)
    #
    # data = tokenizer.texts_to_matrix(df['review_c'].values, mode="tfidf")
    #
    # X, X_test, y, y_test = train_test_split(data, y, test_size=0.10)
    # nn(X, y, X_test, y_test)


def logi_reg(X, y, X_test, y_test):
    """

    :param X: X training data
    :param y: y training data
    :param X_test: X test data
    :param y_test: Y test data
    :return: none
    """
    print("LogisticRegression")
    model = LogisticRegression(class_weight="balanced", multi_class='auto', solver='lbfgs', n_jobs=-1).fit(X, y)
    eval(model.predict(X_test), y_test)


def random_forest(X, y, X_test, y_test):
    """

    :param X: X training data
    :param y: y training data
    :param X_test: X test data
    :param y_test: Y test data
    :return: none
    """
    print("random_forest")
    model = RandomForestClassifier(n_estimators=100).fit(X, y)
    eval(model.predict(X_test), y_test)


def svm(X, y, X_test, y_test):
    """

       :param X: X training data
       :param y: y training data
       :param X_test: X test data
       :param y_test: Y test data
       :return: none
       """
    print("svm")
    model = SVC(kernel="rbf", gamma="scale", C=1, class_weight='balanced').fit(X, y)
    eval(model.predict(X), y)
    eval(model.predict(X_test), y_test)


def svm_grid_search(X, y):
    param_grid = [
        {'C': [1, .01, .05], 'kernel': ['linear']},
        {'C': [1, .01, .05], 'kernel': ['rbf']},
    ]
    svc = SVC(gamma='scale', class_weight='balanced')
    clf = GridSearchCV(svc, param_grid, cv=4, n_jobs=-1, scoring='f1_weighted')
    clf.fit(X, y)
    print(clf.get_params())
    print(clf.score(X, y))


def nn(X, y, X_test, y_test):
    """

       :param X: X training data
       :param y: y training data
       :param X_test: X test data
       :param y_test: Y test data
       :return: none
       """
    # fit Keras model
    print("Neural Net")
    batch_size = 100
    vocab_size = X.shape[1]
    model = Sequential()
    model.add(
        Dense(
            100,
            input_dim=vocab_size,
            kernel_initializer="normal",
            kernel_regularizer=regularizers.l2(10),
            activation="sigmoid",
        )
    )
    model.add(Dense(1, kernel_initializer="normal", activation="sigmoid"))

    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    history = model.fit(
        X, y, batch_size=batch_size, epochs=30, verbose=0, validation_split=0.1
    )
    # evaluate
    print("Training accuracy")
    pred = model.predict_classes(X)
    eval(pred, y)
    print("Test accuracy")
    pred = model.predict_classes(X_test)
    eval(pred, y_test)


def eval(pred, y_test):
    """
    Prints evaluation scores based on predictions and ground truth
    """
    print("accuracy score: ", accuracy_score(y_test, pred))
    print("precision score: ", precision_score(y_test, pred, average='weighted'))
    print("recall score: ", recall_score(y_test, pred, average='weighted'))
    print("weighted f1 score: ", f1_score(y_test, pred, average='weighted'))


def eval_cv(X, y, model):
    """
    Finds training error and then runs K-Fold Cross Validation
    """
    print(" training accuracy: ", model.fit(X, y).score(X, y))
    i = 4
    cv = []
    for train_index, test_index in KFold(n_splits=i).split(X):
        # Create train and test set from KFold split
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        # Calculate test score after fitting decision tree and MLP with given training set
        cv.append(model.fit(X_train, y_train).score(X_test, y_test))

        print("k =", i)
        print("cv accuracy", np.mean(cv))


if __name__ == '__main__':
    main()
