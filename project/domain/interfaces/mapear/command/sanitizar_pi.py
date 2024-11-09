import pandas as pd
from abc import ABC, abstractmethod
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface

class SanitizarPi(ABC):
    @abstractmethod
    def execute(self, plano_interno: pd.DataFrame|list[str]) -> pd.DataFrame:
        """ execute the sanitizar pi """
        raise NotImplementedError('Method not implemented')
