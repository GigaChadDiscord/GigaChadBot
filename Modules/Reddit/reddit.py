import logging
import requests
import os
from dotenv import load_dotenv
from Utils.dice import Dice

logger = logging.getLogger('gigachad')


class Reddit:
    def __init__(self):
        load_dotenv()

        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        self.auth = requests.auth.HTTPBasicAuth(os.getenv('REDDIT_CLIENT_ID'), os.getenv('REDDIT_SECRET_TOKEN'))

        # here we pass our login method (password), username, and password
        self.data = {'grant_type': 'password',
                     'username': os.getenv('REDDIT_USERNAME'),
                     'password': os.getenv('REDDIT_PASSWORD')}

        self.init_headers()

        logger.info("Reddit initialized")

    def init_headers(self):
        self.headers = {'User-Agent': 'Discord:GigaChad:0.01 (by /u/GigaChadDiscord)'}

        # send our request for an OAuth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=self.auth, data=self.data, headers=self.headers)

        # convert response to JSON and pull access_token value
        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        self.headers = {**self.headers, **{'Authorization': f"bearer {TOKEN}"}}

        # # while the token is valid (~2 hours) we just add headers=headers to our requests
        # requests.get('https://oauth.reddit.com/api/v1/me', headers=self.headers)

    def parse(self, message):
        """
        Parses a message for a subreddit and returns a random meme from that subreddit
        :param message: message to parse
        :return: random meme from subreddit
        """
        params = message.content.split()
        if not self.verify_headers():
            self.init_headers()
            logger.debug("Reddit headers reauthorized")
        if len(params) == 1:
            return None
        elif len(params) == 2:
            fuzzy_subreddit = params[1]
            subreddit = self.get_name_subreddit(fuzzy_subreddit)
            if not subreddit:
                return f"There is no subreddit by the name of {fuzzy_subreddit}"
            post_link = self.get_random_meme_from_subreddit(subreddit)
            return post_link

    def verify_headers(self):
        """
        Verifies that the headers are valid
        :return: True if headers are valid, False otherwise
        """
        res = requests.get('https://oauth.reddit.com/api/v1/me', headers=self.headers)
        if res.status_code == 200:
            return True
        else:
            return False

    def get_name_subreddit(self, query):
        """
        Gets the top post from a subreddit
        :param subreddit: subreddit to get top post from
        :return: top post from subreddit
        """
        # get the top post from the subreddit

        res = requests.get("https://oauth.reddit.com/api/subreddit_autocomplete_v2",
                           headers=self.headers,
                           params={'typeahead_active': 'true', 'query': query, 'limit': 1, 'include_profiles': 'false'}).json()
        if not res['data']['children']:
            return None
        logger.debug(f"got subreddit {res['data']['children'][0]['data']['display_name']}")
        return res['data']['children'][0]['data']['display_name']

    def get_random_meme_from_subreddit(self, subreddit):
        """
        Gets a random post from a subreddit
        :param subreddit: subreddit to get random post from
        :return: random post from subreddit
        """
        # get the top post from the subreddit
        res = requests.get("https://oauth.reddit.com/r/{}/random".format(subreddit), headers=self.headers).json()

        return res[0]['data']['children'][0]['data']['url']
