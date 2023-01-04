import pandas as pd
import praw
from DataAdapter import convert_to_pandas
import Utils

# importing our error - for http error - subreddit is private eg.
from prawcore.exceptions import Forbidden


class RedditApiWrapper(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RedditApiWrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.reddit = praw.Reddit(client_id=Utils.reddit_client_id, client_secret=Utils.reddit_client_secret,
                                  redirect_uri='http://www.example.com/unused/redirect/uri', user_agent='agent')
        assert self.reddit.read_only

    def getNewSubmissions(self, subreddit_name, start_date, limit):
        submissions = []

        subreddit = self.reddit.subreddit(subreddit_name)

        for submission in subreddit.new(limit=limit):
            submissions.append(submission)

        if Utils.debug:
            print('{} newest submissions for {} retrieved'.format(len(submissions), subreddit_name))

        return convert_to_pandas(submissions, start_date)

    def getHotSubmissions(self, subreddit_name, start_date, limit):
        submissions = []

        subreddit = self.reddit.subreddit(subreddit_name)

        for submission in subreddit.hot(limit=limit):
            submissions.append(submission)

        if Utils.debug:
            print('{} hottest submissions for {} retrieved'.format(len(submissions), subreddit_name))

        return convert_to_pandas(submissions, start_date)

    def getInfoByFullname(self, fullnames):
        return self.reddit.info(fullnames=fullnames)

    def getNewSubmissionsOfRedditor(self, redditor, start_date, limit):
        submissions = []
        try:
            for submission in self.reddit.redditor(str(redditor)).submissions.new(limit=limit):
                submissions.append(submission)
            if Utils.debug:
                print('{} newest submissions for {} retrieved'.format(len(submissions), redditor))
        except Exception as e:
            print("---------------\nError Handling! Submissions\n---------------")
            print(e)
        return convert_to_pandas(submissions, start_date)

    def getHotSubmissionsOfRedditor(self, redditor_name, start_date, limit):
        submissions = []
        redditor = self.reddit.redditor(redditor_name)
        try:
            for submission in self.reddit.redditor(str(redditor)).submissions.hot(limit=limit):
                # print(submission.subreddit)
                submissions.append(submission)
            if Utils.debug:
                print('{} hottest submissions for {} retrieved'.format(len(submissions), redditor))
        except Exception as e:
            print("---------------\nError Handling! Submissions\n---------------")
            print(e)
        return convert_to_pandas(submissions, start_date)

    def getNewCommentsOfRedditor(self, redditor_name, start_date, limit):
        comments = []
        redditor = self.reddit.redditor(redditor_name)
        try:
            for comment in self.reddit.redditor(str(redditor)).comments.new(limit=limit):
                comments.append(comment)
            if Utils.debug:
                print('{} newest comments for {} retrieved'.format(len(comments), redditor))
        except Exception as e:
            print("---------------\nError Handling! Comments\n---------------")
            print(e)
        return convert_to_pandas(comments, start_date)

    def getHotCommentsOfRedditor(self, redditor_name, start_date, limit):
        comments = []
        redditor = self.reddit.redditor(redditor_name)
        try:
            for comment in self.reddit.redditor(str(redditor)).comments.hot(limit=limit):
                comments.append(comment)
            if Utils.debug:
                print('{} hottest comments for {} retrieved'.format(len(comments), redditor))
        except Exception as e:
            print("---------------\nError Handling! Comments\n---------------")
            print(e)
        return convert_to_pandas(comments, start_date)

    def getHotCommentsOfSubmissions(self, submissions, limit):
        sorted_submissions = submissions.sort_values("num_comments", ascending=False)
        submission_comments = {}
        for index, submission in sorted_submissions[0:limit].iterrows():
            submission_obj = self.reddit.submission(str(submission["id"]))
            comments = []
            try:
                submission_obj.comments.replace_more(limit=0)
                for top_level_comment in submission_obj.comments:
                    print(top_level_comment.body)
                    comments.append(top_level_comment.body)
                submission_comments[submission["id"]] = str(comments)
            except Exception as e:
                print("---------------\nError Handling! Comments\n---------------")
                print(e)

        if Utils.debug:
            print('{} comments for submissions retrieved'.format(len(comments)))

        return pd.DataFrame.from_dict(submission_comments, orient='index')
