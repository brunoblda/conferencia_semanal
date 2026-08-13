import pandas as pd
    
from project.use_cases.mapear.mapear import Mapear
from project.use_cases.mapear.reserva.command.dicionarizar_reserva import (
    DicionarizarReserva as DicionarizarReservaInterface,
)

class MapearReserva(Mapear):
    """Mapeia a reserva"""

    def __init__(
        self,
        dicionarizar_reserva: DicionarizarReservaInterface,
    ) -> None:
        self.dicionarizar_reserva = dicionarizar_reserva

    def handle(self, reserva_processed: pd.DataFrame | list[str]) -> dict:
        """Executa o mapeamento da reserva"""
        reserva_df = reserva_processed
        dict_reserva = self.dicionarizar_reserva.execute(reserva_df)
        return dict_reserva