""" Module for FileNotFound error. """


class FileNotFound(Exception):
    """Class for FileNotFound error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
