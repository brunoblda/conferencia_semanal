from abc import ABC, abstractmethod


class CriarPastas(ABC):
    @abstractmethod
    def execute(self):
        """Cria as pastas"""
        raise NotImplementedError("Method not implemented")
