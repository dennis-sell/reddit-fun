from datetime import datetime
import os
from typing import Dict, Iterable

import pandas as pd
import requests

class RedditAPI:
    """
    Inspired by code in this article:
    https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
    """

    NUM_POSTS_PER_GET = 100

    def __init__(self):
        self.request_headers = RedditAPI.request_auth_token()


    def request_auth_token() -> Dict:
        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': os.environ['REDDIT_USER_AGENT_NAME']}

        if os.environ.get('REDDIT_ACCESS_TOKEN') is None:
            auth = requests.auth.HTTPBasicAuth(os.environ['REDDIT_APP_NAME'], os.environ['REDDIT_APP_SECRET'])

            data = {'grant_type': 'password',
                    'username': os.environ['REDDIT_USERNAME'],
                    'password': os.environ['REDDIT_PASSWORD']}
            res = requests.post('https://www.reddit.com/api/v1/access_token',
                                auth=auth, data=data, headers=headers)
            # TODO: Can I have this stick around after the python script ends?
            #       Otherwise there is not much of a point to checking if it is already set.
            TOKEN = res.json()['access_token']

            os.environ['REDDIT_ACCESS_TOKEN'] = f"bearer {TOKEN}"
        # add authorization to our headers dictionary
        return {**headers, **{'Authorization': os.environ['REDDIT_ACCESS_TOKEN']}}


    def fetch_from_url(self, url_path_post_domain: str, **kwargs) -> requests.Response:
        return requests.get(
                f"https://oauth.reddit.com/{url_path_post_domain}",
                headers=self.request_headers,
                **kwargs,
        )


    def fetch_posts(self, url_path_post_domain: str, num_posts: int) -> pd.DataFrame:
        if url_path_post_domain[0] == "/":
            url_path_post_domain = url_path_post_domain[1:]
        data = []
        num_posts_left = num_posts
        params = {}
        params['limit'] = min(RedditAPI.NUM_POSTS_PER_GET, num_posts_left)

        while num_posts_left > 0:
            res = self.fetch_from_url(url_path_post_domain, params=params)

            new_df = df_from_response(res.json())
            if new_df.empty:
                print(f"Could not fetch data from {url_path_post_domain}")
                break
            data.append(new_df)

            row = new_df.iloc[len(new_df)-1]
            fullname = row['kind'] + '_' + row['post_id']
            # In the reddit API "after" means earlier posts
            params['after'] = fullname
            params['limit'] = min(RedditAPI.NUM_POSTS_PER_GET, num_posts_left)

            num_posts_left -= RedditAPI.NUM_POSTS_PER_GET

        return pd.concat(data)

    def fetch_posts_from_subreddits(self, *, subreddits: Iterable[str], url_path_post_sub: str, num_posts_per_sub: int) -> pd.DataFrame:
        posts = []
        for subreddit_name in subreddits:
            url_path = f"{subreddit_name}/{url_path_post_sub}"
            try:
                posts.append(self.fetch_posts(url_path, num_posts_per_sub))
            except Exception as e:
                print(f"exception {e} happened while fetching from url: {url_path}")
                raise e
        posts = pd.concat(posts)
        return posts

def df_from_response(reddit_response_json: Dict) -> pd.DataFrame:
    response_posts = reddit_response_json.get('data', {}).get('children')
    if response_posts is None:
        return pd.DataFrame()
    post_data = [
        {
            'post_id': post['data']['id'],
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'post_permalink': post['data']['permalink'],
            'up_votes': post['data']['ups'],
            'down_votes': post['data']['downs'],
            'score': post['data']['score'],
            'link_flair_css_class': post['data']['link_flair_css_class'],
            'created_time_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'author': post['data']['author'],
            'author_fullname': post['data'].get('author_fullname'),
            'kind': post['kind'],
            'fetched_time_utc': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        }
        for post in response_posts
    ]
    return pd.DataFrame(post_data)
