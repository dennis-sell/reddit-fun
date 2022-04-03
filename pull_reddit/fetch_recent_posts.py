from datetime import datetime
import os
from typing import Dict

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


    def fetch_from_url(self, url_subdomain_path: str, **kwargs) -> requests.Response:
        return requests.get(
                f"https://oauth.reddit.com/{url_subdomain_path}",
                headers=self.request_headers,
                **kwargs,
        )


    def fetch_posts(self, url_subdomain_path: str, num_posts: int) -> pd.DataFrame:
        data = pd.DataFrame()
        num_posts_left = num_posts
        params = {}
        params['limit'] = min(RedditAPI.NUM_POSTS_PER_GET, num_posts_left)


        while num_posts_left > 0:
            res = self.fetch_from_url(url_subdomain_path, params=params)

            new_df = df_from_response(res.json())
            row = new_df.iloc[len(new_df)-1]
            fullname = row['kind'] + '_' + row['id']
            # In the reddit API "after" means earlier posts
            params['after'] = fullname
            params['limit'] = min(RedditAPI.NUM_POSTS_PER_GET, num_posts_left)

            data = data.append(new_df, ignore_index=True)

            num_posts_left -= RedditAPI.NUM_POSTS_PER_GET

        return data


def df_from_response(reddit_response_json: Dict) -> pd.DataFrame:
    df = pd.DataFrame()

    # loop through each post pulled from res and append to df
    for post in reddit_response_json['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'link_flair_css_class': post['data']['link_flair_css_class'],
            'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id'],
            'kind': post['kind']
        }, ignore_index=True)

    return df
