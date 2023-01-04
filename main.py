import torch
import getopt
import argparse
import datetime
from datetime import timezone
import os
# import spacy
import numpy as np
from ast import literal_eval

# for error handling - for http error - subreddit is private eg.
from prawcore.exceptions import Forbidden

import Utils
from RedditApiWrapper import RedditApiWrapper
from OpenAiWrapper import OpenAiWrapper
from DataPreprocessor import preprocess
from DataPreprocessor import replaceNan
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
    if not os.path.exists("dataframes/praw_new_submissions.csv"):
        data = api.getNewSubmissions(subreddits[0], timestamp, 5000)
        data.to_csv("dataframes/praw_new_submissions.csv")
        if Utils.debug:
            print(data[Utils.col_title])

    # ------------------------------------------------------------------------------------------------------------------
    # Hot Submissions
    # ------------------------------------------------------------------------------------------------------------------
    if not os.path.exists("dataframes/praw_new_submissions.csv"):
        hot_data = api.getHotSubmissions(subreddits[0], timestamp, 5000)
        print(hot_data)
        hot_data.to_csv("dataframes/praw_hot_submissions.csv")
        if Utils.debug:
            print(hot_data[Utils.col_title])

    # ------------------------------------------------------------------------------------------------------------------
    # Comments of the top 100 hot submissions
    # ------------------------------------------------------------------------------------------------------------------
    if not os.path.exists("dataframes/praw_hot_comments.csv"):
        hot_data = pd.read_csv('dataframes/praw_hot_submissions.csv')
        hot_comments = api.getHotCommentsOfSubmissions(hot_data, 100)
        hot_comments.to_csv("dataframes/praw_hot_comments.csv")
        if Utils.debug:
            print(hot_comments)
    # ------------------------------------------------------------------------------------------------------------------
    #                                          SUBMISSIONS AND COMMENTS
    #                                             of UNIQUE AUTHORS
    # ------------------------------------------------------------------------------------------------------------------
    unique_authors = pd.read_csv('dataframes/unique_authors.csv')
    # ------------------------------------------------------------------------------------------------------------------
    # SUBMISSIONS
    # ------------------------------------------------------------------------------------------------------------------
    if not os.path.exists("dataframes/praw_redditor_submissions.csv"):
        redditor_subs = pd.DataFrame()
        count = 1
        for redditor in unique_authors['author_name']:
            if Utils.debug:
                print('Processing Submissions {} Redditor of {}.'.format(count, len(unique_authors['author_name'])))
            # new_data = api.getNewSubmissionsOfRedditor(redditor, timestamp, 5000)
            # pd.concat([redditor_subs, new_data])
            hot_data = api.getHotSubmissionsOfRedditor(redditor, timestamp, 100)
            redditor_subs = pd.concat([redditor_subs, hot_data])
            print(redditor_subs)
            count += 1
        redditor_subs.to_csv("dataframes/praw_redditor_submissions.csv")
    # ------------------------------------------------------------------------------------------------------------------
    # COMMENTS - Might be to overkill
    # ------------------------------------------------------------------------------------------------------------------
    # if not os.path.exists("dataframes/praw_redditor_comments.csv"):
    #     redditor_coms = pd.DataFrame()
    #     count = 1
    #     for redditor in unique_authors['author_name']:
    #         if Utils.debug:
    #             print('Processing Comments {} Redditor of {}.'.format(count, len(unique_authors['author_name'])))
    #         # new_data = api.getNewCommentsOfRedditor(redditor, timestamp, 5000)
    #         # pd.concat([redditor_coms, new_data])
    #         hot_data = api.getHotCommentsOfRedditor(redditor, timestamp, 100)
    #         redditor_coms = pd.concat([redditor_coms, hot_data])
    #         print(redditor_coms)
    #         count += 1
    #     redditor_coms.to_csv("dataframes/praw_redditor_comments.csv")
    # Preprocess the title_column (reddits in consipratard subreddit only are allowed with link and therefore
    # there is no body but only a title
    # Preprocessing includes spell correction, stopword- and punctuation-removal and stemming

    data = None
    if os.path.exists("dataframes/praw_new_submissions.csv"):
        data = pd.read_csv("dataframes/praw_new_submissions.csv")

    if os.path.exists("dataframes/praw_new_submissions_preprocessed.csv"):
        data = pd.read_csv("dataframes/praw_new_submissions.csv")
    else:
        data[Utils.col_title_tokens] = data[Utils.col_title].apply(preprocess)

        if Utils.debug:
            print(data[Utils.col_title_tokens])

        data[Utils.col_title_token_string] = data[Utils.col_title_tokens].apply(lambda x: ' '.join(x))

        if Utils.debug:
            print(data[Utils.col_title_token_string])

        data.to_csv("dataframes/praw_new_submissions_preprocessed.csv")


    if os.path.exists("dataframes/praw_hot_submissions.csv"):
        data = pd.read_csv("dataframes/praw_hot_submissions.csv")

    if os.path.exists("dataframes/praw_hot_submissions_preprocessed.csv"):
        data = pd.read_csv("dataframes/praw_hot_submissions_preprocessed.csv")
    else:
        data[Utils.col_title_tokens] = data[Utils.col_title].apply(preprocess)
        data[Utils.col_text_tokens] = data[Utils.col_text].apply(preprocess)

        if Utils.debug:
            print(data[Utils.col_title_tokens])

        data[Utils.col_title_token_string] = data[Utils.col_title_tokens].apply(lambda x: ' '.join(x))
        data[Utils.col_text_token_string] = data[Utils.col_text_tokens].apply(lambda x: ' '.join(x))

        data[Utils.col_title_token_string] = data[Utils.col_title_token_string].replace(np.nan, '')
        data[Utils.col_text_token_string] = data[Utils.col_text_token_string].replace(np.nan, '')

        data[Utils.col_title_tokens] = data[Utils.col_title_tokens].apply(replaceNan)
        data[Utils.col_text_tokens] = data[Utils.col_text_tokens].apply(replaceNan)

        if Utils.debug:
            print(data[Utils.col_title_token_string])

        data.to_csv("dataframes/praw_hot_submissions_preprocessed.csv")

    pass


if __name__ == '__main__':
    main()
