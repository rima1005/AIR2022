import praw


class RedditApiWrapper(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RedditApiWrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.reddit = praw.Reddit(client_id='JnIW8tASkO5FwWzwu-wjdA', client_secret='HS8pQZh-AMjYQ6KHdbPOzzR2XpKUDg',
                                  redirect_uri='http://www.example.com/unused/redirect/uri', user_agent='agent')
        assert self.reddit.read_only

    def getNewSubmissions(self, subreddit_name, limit=100):
        submissions = []

        subreddit = self.reddit.subreddit(subreddit_name)

        for submission in subreddit.new(limit=limit):
            submissions.append(submission)

        print('{} newest submissions for {} retrieved'.format(len(submissions), subreddit_name))

        return submissions

    def getHotSubmissions(self, subreddit_name, limit=100):
        submissions = []

        subreddit = self.reddit.subreddit(subreddit_name)

        for submission in subreddit.hot(limit=limit):
            submissions.append(submission)

        print('{} hottest submissions for {} retrieved'.format(len(submissions), subreddit_name))

        return submissions
