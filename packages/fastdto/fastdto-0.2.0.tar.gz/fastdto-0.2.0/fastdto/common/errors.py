"""File contains all possible errors that FastDTO can raise."""


class FastDTOError(Exception):
    """Base class for other Errors."""

    ...


class DirectoryAlreadyExistsError(FastDTOError):
    """Error for `init` command."""

    ...


class DirectoryCreateError(FastDTOError):
    """Error for `init` command."""

    ...
