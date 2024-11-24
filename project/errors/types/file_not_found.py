''' Module for FileNotFound error. '''

class FileNotFound(Exception):
    ''' Class for FileNotFound error. '''
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)