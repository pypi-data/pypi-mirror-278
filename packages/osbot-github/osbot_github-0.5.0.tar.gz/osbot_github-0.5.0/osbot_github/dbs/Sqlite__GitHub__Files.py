from osbot_github.api.GitHub__Repo import GitHub__Repo
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Files import Sqlite__DB__Files
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set

SQLITE_DB_NAME = 'github_files__{repo_full_name}.sqlite'

class Sqlite__GitHub__Files(Sqlite__DB__Files, GitHub__Repo):

    def __init__(self, repo_full_name, db_path=None):
        db_name = SQLITE_DB_NAME.format(repo_full_name=repo_full_name)
        Sqlite__DB__Files.__init__(self, db_path=db_path, db_name=db_name)
        GitHub__Repo     .__init__(self, full_name=repo_full_name)

    def add_github_files_to_db(self , path, add_all=False):
        if add_all:
            files = self.all_files   (path=path)
        else:
            files = self.folder_files(path=path)

        rows_added = []
        for file in files:
            path     = file.get('path'    )
            contents = file.get('content' )
            metadata = file.get('metadata')
            row_obj = self.add_file(path=path, contents=contents, metadata=metadata)
            rows_added.append(row_obj)
        return rows_added


    # def all_folders_and_files(self, initial_path='/'):
    #     return self.all_folders_and_files(initial_path)