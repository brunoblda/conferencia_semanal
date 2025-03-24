from abc import ABC, abstractmethod

from pandas import DataFrame


class PegarIndices(ABC):
    @abstractmethod
    def execute(self, plano_interno: DataFrame|list) -> dict:
        """execute the pegar indices"""
        raise NotImplementedError("Method not implemented")
