from abc import ABC, abstractmethod

import pandas as pd


class SanitizarPi(ABC):
    @abstractmethod
    def execute(self, plano_interno: pd.DataFrame | list[str]) -> pd.DataFrame:
        """execute the sanitizar pi"""
        raise NotImplementedError("Method not implemented")
