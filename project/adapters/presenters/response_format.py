""" This file contains the class that will be used to format the response of the API  """


class ResponseFormat:
    def __init__(self, status, message, body):
        self.status = status
        self.message = message
        self.body = body
