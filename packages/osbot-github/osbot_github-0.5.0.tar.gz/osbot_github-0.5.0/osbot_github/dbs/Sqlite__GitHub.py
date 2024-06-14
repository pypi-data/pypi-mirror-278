from os import environ

from osbot_github.api.GitHub__API                            import GitHub__API
from osbot_github.schemas.Schema__Repo                       import Schema__Repo
from osbot_utils.decorators.methods.cache_on_self            import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Database             import Sqlite__Database
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Config import Sqlite__Table__Config
from osbot_utils.utils.Files                                 import current_temp_folder, path_combine, folder_create
from osbot_utils.utils.Str                                   import str_safe

DB_NAME__GIT_HUB          = 'github__{type}__{name}.sqlite'
ENV_NAME_PATH_LOCAL_DBS   = 'PATH_LOCAL_DBS'
FOLDER_NAME__GIT_HUB_DBS  = 'github_dbs'
SQLITE_TABLE__REPOS       = 'repos'


class Sqlite__GitHub(Sqlite__Database):

    github_api : GitHub__API

    def __init__(self, config_data: dict):
        super().__init__(db_path=self.path_sqlite_github(config_data))
        self.setup(config_data)

    def config_data(self):
        return self.table_config().data()

    def path_db_folder(self):
        return environ.get(ENV_NAME_PATH_LOCAL_DBS) or current_temp_folder()

    def path_github_dbs(self):
        return path_combine(self.path_db_folder(), FOLDER_NAME__GIT_HUB_DBS)

    def path_sqlite_github(self, config_data):
        name = config_data.get('name'     )
        type = config_data.get('name_type')
        if not name or not type:
            raise ValueError("In Sqlite__GitHub, config.name and config.type values must be set")
        db_filename = str_safe(DB_NAME__GIT_HUB.format(type=type, name=name))
        return path_combine(self.path_github_dbs(), db_filename)

    @cache_on_self
    def table_config(self):
        return Sqlite__Table__Config(database=self).setup()

    def setup(self, config_data):
        folder_create(self.path_db_folder())
        folder_create(self.path_github_dbs())
        self.table_repos__create()
        self.table_config().set_config_data(config_data)
        return self

    @cache_on_self
    def table_repos(self):
        return self.table(SQLITE_TABLE__REPOS)

    def table_repos__create(self):
        with self.table_repos() as _:
            _.row_schema = Schema__Repo                        # set the table row's schema
            if _.exists() is False:
                _.create()                                          # create if it doesn't exist
                return True
        return False


