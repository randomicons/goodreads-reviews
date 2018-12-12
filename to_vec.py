import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def create_vec_with_all(df):
    with open("bow_all.p", 'wb') as file:
        pickle.dump(TfidfVectorizer().fit_transform(df['review'].values.astype('U')), file,
                    protocol=pickle.HIGHEST_PROTOCOL)


def create_vec_by_book(df):
    with open("bow_book.p", 'wb') as file:
        vecs = {name: TfidfVectorizer().fit_transform(revs['review'].values.astype('U')) for name, revs in
                df.groupby('book')}
        pickle.dump(vecs, file, protocol=pickle.HIGHEST_PROTOCOL)


def main():
    df = pd.read_csv('data.csv', index_col='index')
    create_vec_with_all(df)
    create_vec_by_book(df)


if __name__ == '__main__':
    main()
