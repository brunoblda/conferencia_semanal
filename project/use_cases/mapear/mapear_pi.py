import pandas as pd

from project.domain.interfaces.mapear.command.dicionarizar_indices import (
    DicionarizarIndices as DicionarizarIndicesInterface,
)
from project.domain.interfaces.mapear.command.pegar_indices import (
    PegarIndices as PegarIndicesInterface,
)
from project.domain.interfaces.mapear.mapear_pi import MapearPi as MapearPiInterface


class MapearPi(MapearPiInterface):
    """Mapeia o PI"""

    def __init__(
        self,
        dicionarizar_indices: DicionarizarIndicesInterface,
        pegar_indices: PegarIndicesInterface,
    ) -> None:
        self.dicionarizar_indices = dicionarizar_indices
        self.pegar_indices = pegar_indices

    def handle(self, plano_interno_processed: pd.DataFrame | list[str]) -> dict:
        """Executa o mapeamento do PI"""
        plano_interno_df = plano_interno_processed
        dict_indices_plano_interno = self.pegar_indices.execute(plano_interno_df)
        dict_plano_interno = self.dicionarizar_indices.execute(
            dict_indices_plano_interno, plano_interno_df
        )
        return dict_plano_interno
