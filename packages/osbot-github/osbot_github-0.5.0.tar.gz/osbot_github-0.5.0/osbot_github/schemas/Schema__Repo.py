from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Schema__Repo(Kwargs_To_Self):
    archived       : bool
    created_at     : int
    default_branch : str
    description    : str
    forks          : int
    full_name      : str
    language       : str
    name           : str
    owner          : str
    organisation   : str
    parent         : str
    private        : bool
    pushed_at      : int
    repo_id        : int
    size           : int
    stars          : int
    updated_at     : int
    url            : str
    visibility     : str
    watchers       : int

    def __init__(self):
        super().__init__()
