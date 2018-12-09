import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


def clean(df):
    # Remove redundant column headers
    df = df[df['book'] != 'book']
    keep_index = []
    for i in range(len(df)):
        try:
            keep_index.append(detect(df.iloc[i]['review']) == 'en')
        except LangDetectException:
            keep_index.append(False)
    df = df[keep_index]



if __name__ == '__main__':
    df = pd.read_csv("data.csv", index_col=['index'])
    clean(df)
