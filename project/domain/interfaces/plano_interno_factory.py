from abc import ABC, abstractmethod
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface

class PlanoInternoFactory(ABC):
    @abstractmethod
    def create(self) -> PlanoInternoInterface:
        raise NotImplementedError('Method not implemented')