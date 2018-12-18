import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


def remove_non_english(df):
    """

    :param df: dataframes of reviews
    :return: dataframes that are written in only English
    """
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
    """

    :param df: dataframes of reviews
    :return: dataframes without html tags
    """
    from bs4 import BeautifulSoup as bs
    df['review'] = df.apply(lambda x: bs(x['review']).get_text(separator=" ", strip=True), axis=1)
    return df


def remove_punct_digit(df):
    """

    :param df: dataframes of reviews
    :return: reviews without special characters
    """
    import re
    df['review_c'] = df['review'].apply(lambda x: re.sub(r"['.*&^%$#@<>+=_~`?!,:;()\-\n\"]", ' ', x.lower()))
    df['review_c'] = df['review_c'].apply(lambda x: re.sub(r"\d+", 'num', x.lower()))
    df['review_c'] = df['review_c'].apply(lambda x: re.sub(r"  +", ' ', x))
    return df


def main():
    df = pd.read_csv("data.csv", index_col=['index'])
    df['review'] = df['review'].astype(str)
    df = remove_html_tags(remove_non_english(df))
    df = remove_punct_digit(df)
    df.to_csv("data.csv")


if __name__ == '__main__':
    main()
