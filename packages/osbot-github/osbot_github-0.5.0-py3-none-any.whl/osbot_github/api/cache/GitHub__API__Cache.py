from github.Requester                                      import Requester

from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Patch import Sqlite__Cache__Requests__Patch

SQLITE_DB_NAME__GIT_HUB_API_CACHE = 'github_api_cache.sqlite'
SQLITE_TABLE__GITHUB_API_REQUESTS = 'github_api_requests'


class GitHub__API__Cache(Sqlite__Cache__Requests__Patch):
    db_name             : str                = SQLITE_DB_NAME__GIT_HUB_API_CACHE
    table_name          : str                = SQLITE_TABLE__GITHUB_API_REQUESTS
    print_requests      : bool = False

    def __init__(self, db_path=None):
        self.target_function      = Requester._Requester__requestRaw
        self.target_class         = Requester
        self.target_function_name = "_Requester__requestRaw"
        super().__init__(db_path=db_path)

    def invoke_target(self, target, target_args, target_kwargs):
        if self.print_requests:
            patched_self, cnx, verb, url, requestHeaders, input = target_args
            print(f'> http call to : {verb} {url}')
        return super().invoke_target(target, target_args, target_kwargs)

    def request_data(self, *args, **kwargs):
        patched_self, cnx, verb, url, requestHeaders, input = args
        request_data = {'verb': verb, 'url': url}
        if self.print_requests:
            print(f'# call to : {verb} {url}')
        return request_data

    # def transform_raw_response(self, raw_response):
    #     pprint(raw_response)
    #     return raw_response
    # def target_kwargs(self, *args, **kwargs):
    #     return {'args': args}

