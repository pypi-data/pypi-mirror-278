# from osbot_github.api.GitHub__API import GitHub__API
# from osbot_github.api.GitHub__Repo import GitHub__Repo
# from osbot_github.dbs.Sqlite__GitHub import Sqlite__GitHub, SQLITE_TABLE__REPOS
# from osbot_github.schemas.Schema__Repo import Schema__Repo
# from osbot_github.schemas.Schema__Repos import Schema__Repos
# from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
# from osbot_utils.decorators.methods.cache_on_self import cache_on_self
#
#
# class Table__GitHub__Repos(Kwargs_To_Self):
#     sqlite__github  : Sqlite__GitHub
#     github_api      : GitHub__API
#
#     def __init__(self):
#         super().__init__()
#         self.github_api.target_repo = REPO__OSBOT_GIT_HUB
#         self.setup()
#
#     def create(self):
#         with self.table() as _:
#             _.row_schema = Schema__Repo     # set the table row's schema
#             if _.exists() is False:
#                 _.create()                  # create if it doesn't exist
#                 return True
#
#     def repo(self, repo_full_name):
#         return  GitHub__Repo(full_name=repo_full_name)
#
#     def setup(self):
#         self.create()
#
#     @cache_on_self
#     def table(self):
#         return self.sqlite__github.table(SQLITE_TABLE__REPOS)
#     # def raw_github_repos(self):
#     #     return self.github_api.repo()