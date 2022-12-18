import torch
from RedditApiWrapper import RedditApiWrapper
import pandas as pd


def main():
    api = RedditApiWrapper()
    data = api.getNewSubmissions('conspiratard', 50)
    print(data.head(3))

    pass


if __name__ == '__main__':
    main()
