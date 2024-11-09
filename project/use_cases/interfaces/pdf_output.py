from abc import ABC, abstractmethod

class PdfOutput(ABC):
    @abstractmethod
    def write_pdf(self, data: str, output_name: str) -> None:
        ''' write data to a file '''
        raise NotImplementedError('Method not implemented')