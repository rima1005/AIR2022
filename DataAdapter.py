import pandas as pd
from praw.reddit import Submission
import RedditApiWrapper
import Utils


def convert_to_pandas(submissions: list):
    submission_df = pd.DataFrame(columns=[Utils.col_id,
                                          Utils.col_name,
                                          Utils.col_created,
                                          Utils.col_title,
                                          Utils.col_text,
                                          Utils.col_score,
                                          Utils.col_upvote_ratio,
                                          Utils.col_over_18,
                                          # Utils.col_comments,
                                          Utils.col_num_comments,
                                          Utils.col_author_id,
                                          Utils.col_author_name
                                          # Utils.col_author_submissions,
                                          # Utils.col_author_comments,
                                          ])

    ids, names, created, title, text, score, upvotes, over_18, comments, num_comments, \
    author_ids, author_names, author_submissions, author_comments = [], [], [], [], [], [], [], [], [], [], [], [], [], []

    fullnames = [submission.name for submission in submissions]

    # Todo The reddit api offers possibility to request up to 100 items in one batch which should speed up things
    # This usage of the Info request does not seem to be correct because there is no speedup with regard to single retrieval
    api = RedditApiWrapper.RedditApiWrapper()
    infos = api.getInfoByFullname(fullnames)

    for count, submission in enumerate(infos):
        if Utils.debug:
            print(F"Collecting data ... [{count + 1} / {len(submissions)}]")
        ids.append(submission.id)
        names.append(submission.name)
        created.append(submission.created_utc)
        title.append(submission.title)
        text.append(submission.selftext)
        score.append(submission.score)
        upvotes.append(submission.upvote_ratio)
        over_18.append(submission.over_18)
        # comments.append(submission.comments)
        num_comments.append(submission.num_comments)
        author = submission.author
        author_ids.append(author.id)
        author_names.append(author.name)
        # author_submissions.append(author.submissions)
        # author_comments.append(author.comments)

    submission_df[Utils.col_id] = ids
    submission_df[Utils.col_name] = names
    submission_df[Utils.col_created] = created
    submission_df[Utils.col_title] = title
    submission_df[Utils.col_text] = text
    submission_df[Utils.col_score] = score
    submission_df[Utils.col_upvote_ratio] = upvotes
    submission_df[Utils.col_over_18] = over_18
    # submission_df[Utils.col_comments] = comments
    submission_df[Utils.col_num_comments] = num_comments
    submission_df[Utils.col_author_id] = author_ids
    submission_df[Utils.col_author_name] = author_names
    # ubmission_df[Utils.col_author_submissions] = author_submissions
    # submission_df[Utils.col_author_comments] = author_comments

    return submission_df
