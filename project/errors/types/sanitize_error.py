""" Module for KeyErrorSanitize error. """


class SanitizeError(Exception):
    """Class for KeyErrorSanitize error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
