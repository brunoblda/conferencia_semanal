""" class to compare Reservas """

from abc import ABC, abstractmethod

import pandas as pd


class CompararReservas(ABC):
    """Compare Reservas"""

    @abstractmethod
    def get_status(self) -> str:
        """Get the status of the comparison"""
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update_status(self, status: str) -> None:
        """Update the status of the comparison"""
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def execute(self, reserva_principal: pd.DataFrame, reserva_secundaria: pd.DataFrame):
        """Execute the comparison of the reserva PI with the reserva SEOF or reserva SIAFI"""
        raise NotImplementedError("Method not implemented")