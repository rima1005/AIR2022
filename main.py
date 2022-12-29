import torch
import getopt
import argparse
import datetime
from datetime import timezone

import Utils
from RedditApiWrapper import RedditApiWrapper
from OpenAiWrapper import OpenAiWrapper
from DataPreprocessor import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reddit_client_id",
                        help="The secret key obtained by adding an application on your reddit account")
    parser.add_argument("reddit_client_secret",
                        help="The secret key obtained by adding an application on your reddit account")
    parser.add_argument("openAi_api_key",
                        help="A generated API Key for your OpenAI Account")

    args = parser.parse_args()

    if Utils.debug:
        print("Args parsed successfully")

    # Initialize Reddit Api
    Utils.reddit_client_id = args.reddit_client_id
    Utils.reddit_client_secret = args.reddit_client_secret
    Utils.openAi_api_key = args.openAi_api_key

    api = RedditApiWrapper()

    # get n newest submission from r/***
    subreddits = ["conspiracy", "conspiracytheories", "skeptic", "actualconspiracies"]
    # Date to start collecting data - COVID-19 pandemic - 11. März 2020
    start_date = datetime.date(2020, 3, 11)
    # 1583881200 utc timestamp
    timestamp = 1583881200

    # ------------------------------------------------------------------------------------------------------------------
    # New Submissions
    # ------------------------------------------------------------------------------------------------------------------
    data = api.getNewSubmissions(subreddits[0], timestamp, 5000)
    data.to_csv("dataframes/praw_new_submissions.csv")
    if Utils.debug:
        print(data[Utils.col_title])

    # ------------------------------------------------------------------------------------------------------------------
    # Hot Submissions
    # ------------------------------------------------------------------------------------------------------------------
    hot_data = api.getHotSubmissions(subreddits[0], timestamp, 5000)
    print(hot_data)
    hot_data.to_csv("dataframes/praw_hot_submissions.csv")
    if Utils.debug:
        print(hot_data[Utils.col_title])
    # Preprocess the title_column (reddits in consipratard subreddit only are allowed with link and therefore
    # there is no body but only a title
    # Preprocessing includes spell correction, stopword- and punctuation-removal and stemming
    data[Utils.col_title_tokens] = data[Utils.col_title].apply(preprocess)

    if Utils.debug:
        print(data[Utils.col_title_tokens])

    data[Utils.col_title_token_string] = data[Utils.col_title_tokens].apply(lambda x: ' '.join(x))

    if Utils.debug:
        print(data[Utils.col_title_token_string])

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data[Utils.col_title_token_string].tolist())

    openAi = OpenAiWrapper()
    vectors = openAi.getEmbeddingVector(vectorizer.get_feature_names())

    pass


if __name__ == '__main__':
    main()
