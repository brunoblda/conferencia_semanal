from abc import ABC, abstractmethod
from pandas import DataFrame

class PegarIndices(ABC):
    @abstractmethod
    def execute(self, plano_interno_df: DataFrame) -> dict:
        """ execute the pegar indices """
        raise NotImplementedError('Method not implemented')