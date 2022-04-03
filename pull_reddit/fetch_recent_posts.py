import os
from typing import Dict

import requests


class RedditAPI:

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


    def fetch_from_url(self, url_subdomain_path: str) -> requests.Response:
        return requests.get(
                f"https://oauth.reddit.com/{url_subdomain_path}",
                headers=self.request_headers,
        )


