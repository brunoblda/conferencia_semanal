""" Module for FileStillOpened error. """


class FileStillOpened(Exception):
    """Class for FileStillOpened error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
