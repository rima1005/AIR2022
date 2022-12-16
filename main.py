import torch
from RedditApiWrapper import RedditApiWrapper


def main():
    api = RedditApiWrapper()
    for submission in api.getNewSubmissions("conspiratard", limit=20):
        print(submission.title)

    pass


if __name__ == '__main__':
    main()
