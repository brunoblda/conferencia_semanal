from abc import ABC, abstractmethod

import pandas as pd


class LerDados(ABC):
    @abstractmethod
    def execute(self, output_path: str) -> pd.DataFrame | list[str]:
        """execute the ler dados"""
        raise NotImplementedError("Method not implemented")
