import praw
from DataAdapter import convert_to_pandas
import Utils

class RedditApiWrapper(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RedditApiWrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.reddit = praw.Reddit(client_id=Utils.reddit_client_id, client_secret=Utils.reddit_client_secret,
                                  redirect_uri='http://www.example.com/unused/redirect/uri', user_agent='agent')
        assert self.reddit.read_only

    def getNewSubmissions(self, subreddit_name, limit=100):
        submissions = []

        subreddit = self.reddit.subreddit(subreddit_name)

        for submission in subreddit.new(limit=limit):
            submissions.append(submission)

        if Utils.debug:
            print('{} newest submissions for {} retrieved'.format(len(submissions), subreddit_name))

        return convert_to_pandas(submissions)

    def getHotSubmissions(self, subreddit_name, limit=100):
        submissions = []

        subreddit = self.reddit.subreddit(subreddit_name)

        for submission in subreddit.hot(limit=limit):
            submissions.append(submission)

        if Utils.debug:
            print('{} hottest submissions for {} retrieved'.format(len(submissions), subreddit_name))

        return convert_to_pandas(submissions)

    def getInfoByFullname(self, fullnames):
        return self.reddit.info(fullnames=fullnames)
