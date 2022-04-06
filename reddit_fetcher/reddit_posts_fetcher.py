import os

from sqlalchemy import create_engine

from reddit_api import RedditAPI
from subreddits import get_popular_subreddits

POPULAR_SUBREDDITS = set(get_popular_subreddits().subreddit)

# DB table_name => fetch_configuration
CONFIG = {
    'reddit_top_posts': {'url_path': "top/?t=month", 'subreddits': POPULAR_SUBREDDITS, 'num_posts':100, 'freq': 'monthly'},
}

def fetch_and_save_posts():
    reddit = RedditAPI()
    db_engine = create_engine(os.environ['DATABASE_URL'])
    for table_name, config in CONFIG.items():
        posts = reddit.fetch_posts_from_subreddits(
            subreddits=config['subreddits'],
            url_path=config['url_path'],
            num_posts_per_sub=config['num_posts'],
        )
        posts.to_sql(table_name, db_engine, if_exists='append')

if __name__ == "__main__":
    fetch_and_save_posts()
