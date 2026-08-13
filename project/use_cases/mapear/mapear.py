from abc import ABC, abstractmethod
import pandas as pd

class Mapear(ABC):
    @abstractmethod
    def handle(self, data_processed: pd.DataFrame | list[str]) -> dict:
        """handle the mapping of reserva"""
        raise NotImplementedError("Method not implemented")
