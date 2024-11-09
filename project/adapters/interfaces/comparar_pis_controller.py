from abc import ABC, abstractmethod

class CompararPisController(ABC):
    @abstractmethod
    def handle_request(self, tipo_pi_principal: str, input_file_path_principal: str, tipo_pi_secundario: str, input_file_path_secundario: str) -> str:
        raise NotImplementedError('Method not implemented')

