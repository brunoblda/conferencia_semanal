import pandas as pd
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface

class PlanoInternoSiafi(PlanoInternoInterface):
    
    def set(self, plano_interno: pd.DataFrame) -> None:
        self.plano_interno: pd.DataFrame = plano_interno
    
    def set_dict(self, dict_plano_interno: dict) -> None:
        self.dict_plano_interno: dict = dict_plano_interno

    def get_dict(self) -> dict:
        return self.dict_plano_interno
    
    def get(self) -> pd.DataFrame:
        return self.plano_interno
