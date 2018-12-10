import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


def remove_non_english(df):
    # Remove redundant column headers
    df = df[df['book'] != 'book']
    # Does the same as: (but this cannot do exceptions)
    # df = df[df.apply(lambda x: detect(x['review']) == 'en', axis=1)]
    keep_index = []
    for i in range(len(df)):
        try:
            keep_index.append(detect(df.iloc[i]['review']) == 'en')
        except LangDetectException:
            keep_index.append(False)
    return df[keep_index]


def remove_html_tags(df):
    from bs4 import BeautifulSoup as bs
    df['review'] = df.apply(lambda x: bs(x['review']).get_text(separator=" ", strip=True), axis=1)
    return df


if __name__ == '__main__':
    df = pd.read_csv("data.csv", index_col=['index'])
    df = remove_html_tags(remove_non_english(df))
    df.to_csv("data.csv")
