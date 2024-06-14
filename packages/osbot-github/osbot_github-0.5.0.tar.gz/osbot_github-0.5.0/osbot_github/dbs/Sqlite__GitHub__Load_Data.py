from osbot_github.api.GitHub__API import GitHub__API
from osbot_github.api.GitHub__Repo import GitHub__Repo
from osbot_github.dbs.Sqlite__GitHub import Sqlite__GitHub


class Sqlite__GitHub__Load_Data:
    sqlite_github : Sqlite__GitHub

    def __init__(self, config_data):
        self.sqlite_github = Sqlite__GitHub(config_data)
        self.github_api    = self.sqlite_github.github_api


    def load_repos(self):
        config_data = self.sqlite_github.config_data()
        name        = config_data.get('name')
        name_type   = config_data.get('name_type')
        table_repos = self.sqlite_github.table_repos()
        if name_type == 'organization':
            repos = self.github_api.repos_from_organization(name)
        elif name_type == 'user':
            repos = self.github_api.repos_from_user(name)
        else:
            repos = []
        for repo in repos:
            full_name   = repo.full_name
            github_repo = GitHub__Repo(full_name=full_name)
            repo_data   = github_repo.repo_data()
            if table_repos.contains(full_name=full_name):
                #print(f'updating repo row: {full_name}')
                table_repos.row_update(repo_data, dict(full_name=full_name))
            else:
                #print(f'creating repo row: {full_name}')
                table_repos.add_row(**repo_data)
        table_repos.commit()
            #return table_repos.schema__by_name_type()
            #return repos