from abc import ABC, abstractmethod

class PdfConversor(ABC):
    @abstractmethod
    def execute(self, credentials_env, input_path):
        """ execute the pdf conversor """
        raise NotImplementedError('Method not implemented')