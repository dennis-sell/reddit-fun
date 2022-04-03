import pandas as pd

from reddit_api import RedditAPI
from subreddits import get_popular_subreddits, DEFAULT_SUBREDDITS


# This was generated from https://frontpagemetrics.com/top-sfw-subreddits/offset/
# as of 2022-04-03
popular_subreddits: pd.DataFrame = get_popular_subreddits()
# default subs don't really count
popular_subreddits = popular_subreddits[~popular_subreddits.subreddit.isin(DEFAULT_SUBREDDITS)]

reddit = RedditAPI()
top_monthly_posts = []
for subreddit_name in popular_subreddits.subreddit.head(2):
    top_monthly_posts.append(reddit.fetch_posts(f"{subreddit_name}/top/?t=month", 100))
top_monthly_posts = pd.concat(top_monthly_posts)


#if __name__ == "__main__":
#    fetch_top_posts()