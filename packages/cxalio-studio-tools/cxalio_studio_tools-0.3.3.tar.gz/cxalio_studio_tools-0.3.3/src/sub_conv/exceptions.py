class SourceFileError(IOError):
    pass


class TargetFileError(IOError):
    pass


class NoLoaderError(SourceFileError):
    pass


class TargetConflictError(TargetFileError):
    pass


class TargetExistsError(TargetFileError):
    pass


class NoSaverError(TargetFileError):
    pass


class UserCancelError(Exception):
    pass
