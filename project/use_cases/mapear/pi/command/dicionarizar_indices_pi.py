import re

import pandas as pd

from project.domain.interfaces.mapear.command.dicionarizar_indices import (
    DicionarizarIndices as DicionarizarIndicesInterface,
)
from project.use_cases.interfaces.utilities.utils import Utils as UtilsInterface


class DicionarizarIndices(DicionarizarIndicesInterface):
    def __init__(self, utils: UtilsInterface):
        self.utils = utils

    """ Dicionaria os indices do PI """

    def execute(self, dict_indices: dict, plano_interno: list) -> dict:
        """Executa a dicionarização dos indices"""

        plano_interno_df = pd.concat(plano_interno, ignore_index=True)
        columns_names_pi_list = plano_interno_df.columns.to_list() 
        pattern_plano_interno = r'(^\d{2}(?:[A-Z]+|-[-A-Z]+(?: [A-Z]+)?))'
        pattern_desdobramento_elemento_despesa_codigo = r'^\d{2}\.\d{2}\.\d{2}'
        dict_resultado_plano_interno = {}

        # para cada chave de plano interno
        for w in dict_indices:
            # ic.ic(plano_interno_df[3][w])
            # ic.ic(dict_indices[w])

            # nome_plano_interno = plano_interno_df[1][w].split(' ',1)[0]
            column_plano_interno = dict_indices[w]['column']
            nome_plano_interno = re.search(pattern_plano_interno, plano_interno_df[column_plano_interno][w]).group()

            # calcula o valor da dotação para cada coluna da linha e caso encontre ele se torna o valor da dotação do plano interno
            dotacao_plano_interno = 0
            for o in columns_names_pi_list:
                if plano_interno_df[o][w] == '-':
                    dotacao_plano_interno = 0
                else:
    
                    dotacao_plano_interno_por_coluna = self.utils.value_hygienization(plano_interno_df[o][w])
                    if dotacao_plano_interno_por_coluna:
                        dotacao_plano_interno = dotacao_plano_interno_por_coluna

            dict_resultado_plano_interno[nome_plano_interno] = {'indice': w, 'valor': dotacao_plano_interno, 'elementos de despesa': {}}

            # para cada item da lista de value de cada chave de plano interno
            for z in dict_indices[w]['elementos de despesa']:

                # para cada chave de elemento de despesa
                for y in z:
            
                    # Eliminar os elementos de despesa que não possuem desdobramentos de despesas, para nao serem carregados no dicionario 
                    if not z[y]['desdobramentos de elemento de despesa']:
                        continue

                    column_elemento_despesa = z[y]['column']
                    nome_elemento_despesa = re.sub(r'[a-zA-ZÀ-ü\s\-\/]', '', plano_interno_df[column_elemento_despesa][y].strip())
                    if nome_elemento_despesa:
                        nome_elemento_despesa = re.search(r'\d\.\d\.\d{2}\.\d{2}\.\d{2}', nome_elemento_despesa)
                        if nome_elemento_despesa:
                            nome_elemento_despesa = nome_elemento_despesa[0]
                    if not nome_elemento_despesa:
                        nome_elemento_despesa = re.sub(r'[a-zA-ZÀ-ü\s\-\/]', '', plano_interno_df[column_elemento_despesa][y].strip())
                    nome_elemento_despesa = nome_elemento_despesa[:9]
           
                    # calcula o valor da dotação para cada coluna da linha e caso encontre ele se torna o valor da dotação do plano interno
                    dotacao_elemento_despesa = 0
                    for o in columns_names_pi_list:

                        if plano_interno_df[o][y] == '-':
                            dotacao_elemento_despesa = 0
                        else:
                            dotacao_elemento_despesa_por_coluna = self.utils.value_hygienization(plano_interno_df[o][y])
                
                            if dotacao_elemento_despesa_por_coluna:
                                dotacao_elemento_despesa = dotacao_elemento_despesa_por_coluna

                    dict_resultado_plano_interno[nome_plano_interno]['elementos de despesa'][nome_elemento_despesa] = {'indice': y, 'valor': dotacao_elemento_despesa, 'desdobramentos de despesa': {}}
            
                    # para cada item da lista de value da chave de elemento de despesa
                    for x in z[y]['desdobramentos de elemento de despesa']:
                        # ic.ic(plano_interno_df[3][x])

                        for k in x:
                            column_desdobramento_elemento_despesa = x[k]['column']
                            nome_desdobramento_despesa = re.search(pattern_desdobramento_elemento_despesa_codigo, plano_interno_df[column_desdobramento_elemento_despesa][k])[0] 

                            # calcula o valor da dotação para cada coluna da linha e caso encontre ele se torna o valor da dotação do plano interno
                            dotacao_desdobramento_despesa = 0
                            for o in columns_names_pi_list:
                                if plano_interno_df[o][k] == '-':
                                    dotacao_desdobramento_despesa = 0
                                else:
                                    dotacao_desdobramento_despesa_por_coluna = self.utils.value_hygienization(plano_interno_df[o][k])
                                    if dotacao_desdobramento_despesa_por_coluna:
                                        dotacao_desdobramento_despesa = dotacao_desdobramento_despesa_por_coluna
                
                            dict_resultado_plano_interno[nome_plano_interno]['elementos de despesa'][nome_elemento_despesa]['desdobramentos de despesa'][nome_desdobramento_despesa] = {'indice': k, 'valor': dotacao_desdobramento_despesa}

        return dict_resultado_plano_interno
  