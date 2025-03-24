import re

import pandas as pd

from project.domain.interfaces.mapear.command.dicionarizar_indices import (
    DicionarizarIndices as DicionarizarIndicesInterface,
)
from project.use_cases.interfaces.utilities.utils import Utils as UtilsInterface


class DicionarizarIndicesPiSeof(DicionarizarIndicesInterface):
    """Dicionaria os indices do PI Seof"""

    def __init__(self, utils: UtilsInterface):
        self.utils = utils

    def execute(self, dict_indices: dict, plano_interno: pd.DataFrame) -> dict:
        """Executa a diciornarização dos indices do PI Seof"""
        
        plano_interno = pd.concat(plano_interno, ignore_index=True) 

        columns_names_plano_interno = plano_interno.columns.to_list()

        pattern_plano_interno_seof = r"^\d{2}(?:[A-Z]+|-[-A-Z]+(?: [A-Z]+)?)"
        pattern_desdobramento_elemento_despesa_seof = r"^\d{2}.\d{2}.\d{2}"

        dict_resultado_plano_interno_seof = {}

        # para cada chave de plano interno
        for w in dict_indices:
            # ic.ic(plano_interno[2][w])
            # ic.ic(dict_indices[w])
            # ic.ic(plano_interno[1][w])

            # nome_plano_interno_seof = plano_interno[1][w].split(' ',1)[0]
            column_plano_interno_seof = dict_indices[w]['column']
            nome_plano_interno_seof = re.search(pattern_plano_interno_seof, plano_interno[column_plano_interno_seof][w]).group()
    
            dotacao_plano_interno_seof = 0
            for o in columns_names_plano_interno:
                dotacao_plano_interno_por_coluna = self.utils.value_hygienization(plano_interno[o][w])
                if dotacao_plano_interno_por_coluna:
                    dotacao_plano_interno_seof = dotacao_plano_interno_por_coluna

            dict_resultado_plano_interno_seof[nome_plano_interno_seof] = {'indice': w, 'valor': dotacao_plano_interno_seof, 'elementos de despesa': {}}

            # para cada item da lista de value de cada chave de plano interno
            for z in dict_indices[w]['elementos de despesa']:

                # para cada chave de elemento de despesa
                for y in z:
                    # ic.ic(plano_interno[2][y])
                    # ic.ic(plano_interno[1][y])
           
                    column_elemento_despesa_seof = z[y]['column']
                    nome_elemento_despesa_seof = plano_interno[column_elemento_despesa_seof][y].split(' ',1)[0]
                    nome_elemento_despesa_seof = nome_elemento_despesa_seof[:1]+"."+nome_elemento_despesa_seof[1:2]+"."+nome_elemento_despesa_seof[2:4]+"."+nome_elemento_despesa_seof[4:]

                    dotacao_elemento_despesa_seof = 0

                    for o in columns_names_plano_interno:
                        dotacao_elemento_despesa_por_coluna = self.utils.value_hygienization(plano_interno[o][y])
                        if dotacao_elemento_despesa_por_coluna:
                            dotacao_elemento_despesa_seof = dotacao_elemento_despesa_por_coluna

                    dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof] = {'indice': y, 'valor': dotacao_elemento_despesa_seof, 'desdobramentos de despesa': {}}

                    # para cada item da lista de value da chave de elemento de despesa
                    for x in z[y]['desdobramentos de elemento de despesa']:
                        # ic.ic(plano_interno[2][x])
                        # ic.ic(plano_interno[1][x])

                        for k in x:

                            column_desdobramento_elemento_despesa_seof = x[k]['column']
                    
                            nome_desdobramento_despesa_seof = re.search(pattern_desdobramento_elemento_despesa_seof, plano_interno[column_desdobramento_elemento_despesa_seof][k])[0]

                            dotacao_desdobramento_despesa_seof = 0
                            for o in columns_names_plano_interno:
                                dotacao_desdobramento_despesa_por_coluna = self.utils.value_hygienization(plano_interno[o][k])
                                if dotacao_desdobramento_despesa_por_coluna:
                                    dotacao_desdobramento_despesa_seof = dotacao_desdobramento_despesa_por_coluna 

                            # versão anterior
                            # dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa'][nome_desdobramento_despesa_seof] = {'indices': [k], 'valor': dotacao_desdobramento_despesa_seof}

                            if nome_desdobramento_despesa_seof not in dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa']:
                                dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa'][nome_desdobramento_despesa_seof] = {'indice': [k], 'valor': dotacao_desdobramento_despesa_seof}
                            else:
                                dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa'][nome_desdobramento_despesa_seof]['indice'].append(k)
                                dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa'][nome_desdobramento_despesa_seof]['valor']

        return dict_resultado_plano_interno_seof

