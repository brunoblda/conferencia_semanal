from abc import ABC, abstractmethod

class VerificarExistenciaDeArquivo(ABC):
    @abstractmethod
    def execute(self, file_path: str) -> bool:
        """ Verifica se o arquivo existe """
        raise NotImplementedError('Method not implemented')
