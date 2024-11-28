from abc import ABC, abstractmethod

import pandas as pd


class MapearPi(ABC):
    @abstractmethod
    def handle(self, plano_interno_processed: pd.DataFrame | list[str]):
        """handle the mapear pi"""
        raise NotImplementedError("Method not implemented")
