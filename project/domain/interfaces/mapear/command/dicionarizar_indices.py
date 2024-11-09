from abc import ABC, abstractmethod
import pandas as pd

class DicionarizarIndices(ABC):
    @abstractmethod
    def execute(self, dict_indices: dict, plano_interno: pd.DataFrame) -> dict:
        """ execute the dicionarizar indices """
        raise NotImplementedError('Method not implemented')
