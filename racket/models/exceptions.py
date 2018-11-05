from sqlite3 import IntegrityError


class NotInitializedError(Exception):
    pass


class DuplicateException(IntegrityError):
    message = 'At least one of the inputs provided has a the same id as one already in the database.'
