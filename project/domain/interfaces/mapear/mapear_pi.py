from abc import ABC, abstractmethod
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface
from project.domain.interfaces.mapear.command.sanitizar_pi import SanitizarPi as SanitizarPiInterface
from project.domain.interfaces.mapear.command.pegar_indices import PegarIndices as PegarIndicesInterface
from project.domain.interfaces.mapear.command.dicionarizar_indices import DicionarizarIndices as DicionarizarIndicesInterface
import pandas as pd

class MapearPi(ABC):
    @abstractmethod
    def handle(self, plano_interno_processed: pd.DataFrame|list[str]):
        """ handle the mapear pi """
        raise NotImplementedError('Method not implemented')
