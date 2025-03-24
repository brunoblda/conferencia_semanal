from abc import ABC, abstractmethod

import pandas as pd


class ProcessarDadosBrutos(ABC):
    @abstractmethod
    def execute(
        self, input_path: str, output_file_path: str
    ) -> pd.DataFrame | list[str]:
        """execute the processar dados brutos"""
        raise NotImplementedError("Method not implemented")
