
from sqlite3 import IntegrityError


class NotInitializedError(Exception):
    ...


class VersionError(Exception):
    ...


class CLIError(Exception):
    ...


class ModelNotFoundError(Exception):
    ...


class DuplicateException(IntegrityError):
    message = 'At least one of the inputs provided has a the same id as one already in the database.'


class TFSError(Exception):
    ...


def validate_config(fn):
    from racket.managers.project import ProjectManager

    def wrapper(*args, **kwargs):
        if ProjectManager.get_config() is None:
            raise CLIError('No configuration found. Are you sure you have a racket.yaml file in your current directory?'
                           'Run racket init to start a new project')
        return fn(*args, **kwargs)
    return wrapper
