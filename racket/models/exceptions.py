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
