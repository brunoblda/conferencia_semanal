import pandas as pd

from project.domain.interfaces.processar_dados_brutos.processar_dados_brutos import (
    ProcessarDadosBrutos as ProcessarDadosBrutosInterface,
)
from project.use_cases.interfaces.pegar_dados_processados.ler_dados import (
    LerDados as LerDadosInterface,
)

class ProcessarDadosBrutos(ProcessarDadosBrutosInterface):
    """ Class to processar dados brutos """
    def __init__(
        self,
        ler_dados: LerDadosInterface,
       
    ) -> None:
        """Constructor"""

        self.__ler_dados = ler_dados
    
    def execute(
        self, input_path: str 
    ) -> pd.DataFrame | list[str]:
        """ execute the processar dados brutos """

        dados_processados = self.__ler_dados.execute(input_path)

        return dados_processados
