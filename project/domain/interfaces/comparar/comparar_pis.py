""" class to compare PIs """

from abc import ABC, abstractmethod

import pandas as pd


class CompararPis(ABC):
    """Compare PIs"""

    @abstractmethod
    def get_status(self) -> str:
        """Get the status of the comparison"""
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def update_status(self, status: str) -> None:
        """Update the status of the comparison"""
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def execute(self, pi_principal: pd.DataFrame, pi_secundario: pd.DataFrame):
        """Execute the comparison of the PI with the PI Seof"""
        raise NotImplementedError("Method not implemented")
