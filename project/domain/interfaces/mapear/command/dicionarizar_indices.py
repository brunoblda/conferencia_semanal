from abc import ABC, abstractmethod

from pandas import DataFrame


class DicionarizarIndices(ABC):
    @abstractmethod
    def execute(self, dict_indices: dict, plano_interno: DataFrame|list) -> dict:
        """execute the dicionarizar indices"""
        raise NotImplementedError("Method not implemented")
