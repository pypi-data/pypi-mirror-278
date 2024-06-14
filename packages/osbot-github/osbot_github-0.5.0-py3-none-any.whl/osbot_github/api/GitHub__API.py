from os import getenv

import requests
from github import Github

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Python_Logger              import logger_info
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

GIT_HUB__ACCESS_TOKEN   = "GIT_HUB__ACCESS_TOKEN"
GIT_HUB__REPO_PATH      = 'https://raw.githubusercontent.com/'
GIT_HUB__DEFAULT_BRANCH = 'main'
GIT_HUB__DEFAULT_REPO   = 'owasp-sbot/OSBot-GitHub'


class GitHub__API:

    def __init__(self):
        self.log_info = logger_info()
        self.session  = requests.Session()

    def access_token(self):
        return getenv(GIT_HUB__ACCESS_TOKEN)

    # def file_download(self, repo, branch, file_path):
    #     download_url = f'{GIT_HUB__REPO_PATH}/{repo}/{branch}/{file_path}'
    #     pprint(download_url)
    #     headers  = {'Authorization'  : f'token {self.access_token()}',
    #                 'Accept-Encoding': 'gzip'}
    #     response = self.session.get(download_url, headers=headers)
    #     return response.text

    def github(self):
        return Github(self.access_token())

    @cache_on_self
    def organization(self, org_name):
        return self.github().get_organization(org_name)

    @cache_on_self
    def user(self, user_name):
        return self.github().get_user(user_name)

    def repo(self, repo_full_name):
        return self.github().get_repo(repo_full_name)

    def repos_from_user(self, user_name):
        user = self.user(user_name=user_name)
        return user.get_repos()

    def repos_from_organization(self, org_name):
        return self.organization(org_name=org_name).get_repos()
