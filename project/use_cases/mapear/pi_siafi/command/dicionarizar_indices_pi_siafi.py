import re

import pandas as pd

from project.domain.interfaces.mapear.command.dicionarizar_indices import (
    DicionarizarIndices as DicionarizarIndicesInterface,
)
from project.use_cases.interfaces.utilities.utils import Utils as UtilsInterface


class DicionarizarIndicesPiSiafi(DicionarizarIndicesInterface):
    """Dicionariza os indices do PI Siafi"""

    def __init__(self, utils: UtilsInterface) -> None:
        self.utils = utils

    def execute(self, dict_indices: dict, plano_interno: pd.DataFrame) -> dict:
        """Executa a diciornarização dos indices do PI Siafi"""

        plano_interno = pd.concat(plano_interno, ignore_index=True)

        dict_resultado_plano_interno_siafi = {}

        columns_names_siafi_pi_list = plano_interno.columns.to_list()
        
        pattern_only_plano_interno_column_result_siafi = r'((?:^|\s)\d{2}[-A-Z\s]{7,9}(?:\s|$))'
        
        # para a chave do plano interno
        for w in dict_indices:

            column_plano_interno_siafi = dict_indices[w]['column']

            # para descartar os -8uu
            if not re.search(r'(-\d)', plano_interno[column_plano_interno_siafi][w]):
            # if not re.search(r'(-\d)', plano_interno[column_plano_interno_siafi][w]).group():
                nome_plano_interno_siafi = re.search(pattern_only_plano_interno_column_result_siafi, plano_interno[column_plano_interno_siafi][w])

                if nome_plano_interno_siafi:
                    nome_plano_interno_siafi = nome_plano_interno_siafi.group().strip()
                else:
                    nome_plano_interno_siafi = plano_interno[column_plano_interno_siafi][w].strip()
        
                # pegar os valores de dotacao do plano interno
                dotacao_plano_interno_siafi = 0
                for o in columns_names_siafi_pi_list:
                    dotacao_plano_interno_por_coluna = self.utils.value_hygienization(plano_interno[o][list(dict_indices[w]['totais'][0].keys())[0]])
                    if dotacao_plano_interno_por_coluna:
                        dotacao_plano_interno_siafi = dotacao_plano_interno_por_coluna
    
                # para pegar os indice da chave que esta na lista do dicionario de cada plano interno
                dict_resultado_plano_interno_siafi[nome_plano_interno_siafi] = {'indice plano interno': w,'indice total': list(dict_indices[w]['totais'][0].keys())[0] ,'valor': dotacao_plano_interno_siafi, 'elementos de despesa': {}}

                # pega os elementos de despesa do plano interno
                totais_key = list(dict_indices[w]['totais'][0].keys())[0]
                elementos_de_despesa_siafi = dict_indices[w]['totais'][0][totais_key]['elementos de despesa']
 
                for elemento_de_depesa_siafi in elementos_de_despesa_siafi:
                    for key, value in elemento_de_depesa_siafi.items():
                    
                        # para pegar o valor dentro da lista que esta dentro da lista, dentro o dicionario total, o x é o indice da lista, não o valor
                        nome_elemento_despesa_siafi = plano_interno[value['column']][key]
                        nome_elemento_despesa_siafi = nome_elemento_despesa_siafi[:1] + '.' + nome_elemento_despesa_siafi[1:2] + '.' + nome_elemento_despesa_siafi[2:4] + '.' + nome_elemento_despesa_siafi[4:]
                        for o in columns_names_siafi_pi_list:
                            dotacao_elemento_despesa_por_coluna = self.utils.value_hygienization(plano_interno[o][key])
                            if dotacao_elemento_despesa_por_coluna:
                                dotacao_elemento_despesa_siafi = dotacao_elemento_despesa_por_coluna
            
                        dict_resultado_plano_interno_siafi[nome_plano_interno_siafi]['elementos de despesa'][nome_elemento_despesa_siafi] = {'indice': key, 'valor': dotacao_elemento_despesa_siafi}

        return dict_resultado_plano_interno_siafi
