""" class to compare PIs """

from abc import ABC, abstractmethod

import pandas as pd


class CompararPis(ABC):
    """Compare PIs"""

    @abstractmethod
    def execute(self, pi_principal: pd.DataFrame, pi_secundario: pd.DataFrame):
        """Execute the comparison of the PI with the PI Seof"""
        raise NotImplementedError("Method not implemented")
