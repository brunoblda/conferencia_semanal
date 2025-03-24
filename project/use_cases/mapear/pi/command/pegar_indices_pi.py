import re

import pandas as pd

from project.domain.interfaces.mapear.command.pegar_indices import (
    PegarIndices as PegarIndicesInterface,
)

from project.use_cases.interfaces.utilities.utils import Utils as UtilsInterface

class PegarIndicesPi(PegarIndicesInterface):
    """Pega os indices do PI"""

    def __init__(self, utils: UtilsInterface) -> None:
        self.utils = utils

    def execute(self, plano_interno: list) -> dict:
        """Executa a busca dos indices do PI"""
        pi_df = pd.concat(plano_interno, ignore_index=True)

        columns_names_pi_list = pi_df.columns.to_list() 

        # pattern para encontrar os planos interno "10-AIMOVEIS"

        # pattern_plano_interno = r'^\d{2}[-A-Z]'
        pattern_plano_interno = r'(^\d{2}(?:[A-Z]+|-[-A-Z]+(?: [A-Z]+)?))'
        # matched_rows_planos_internos = pi_df[1].str.match(pattern_plano_interno).fillna(False)

        extracted_list = []

        for i in columns_names_pi_list:
            extracted = pi_df[i].str.extract(pattern_plano_interno)
            extracted_list.append(extracted)

        matched_rows_planos_internos_list = [extracted.notna().any(axis=1) for extracted in extracted_list]

        matched_rows_planos_internos_df = pd.concat(matched_rows_planos_internos_list, axis=1)

        tuple_list_indices_planos_internos = self.utils.get_row_and_column(matched_rows_planos_internos_df)

        pattern_nan = r'^nan'

        pattern_elemento_despesa_nome_tipo_1 = r'^[a-zA-Z]'
        pattern_elemento_despesa_codigo_tipo_1 = r'^\d\.\d\.\d{2}\.\d{2}\.\d{2}'
        # Motivo do pattern
        # Serviços de tecnologia da inform. e comunicação - pessoa jurídic3a.3.90.40.00
        # Material de consumo 3.3.90.30.00 
        # Serviços de tecnologia da informação e comunicação - pessoa ju3r.í3d.i9c0a.40.00
        pattern_elemento_despesa_nome_e_codigo_tipo_2 = r'^[a-zA-Z].*\.\d{2}\.\d{2}' 
        pattern_desdobramento_elemento_despesa_codigo = r'^\d{2}\.\d{2}\.\d{2}'

        tuple_list_indices_planos_internos_verification =tuple_list_indices_planos_internos.copy()

        # adicionando o ultimo indice do dataframe para a lista de verificacao
        tuple_list_indices_planos_internos_verification.append((len(pi_df.index)-1, columns_names_pi_list[-1]))

        dict_planos_internos = {}

        # ic.ic(tuple_list_indices_planos_internos)

        # para i de 0 até o tamanho da lista de indices dos planos internos
        for i in range(len(tuple_list_indices_planos_internos)):

            # cria um dicionario igual ao valor do item na lista de planos internos de indice i
            dict_planos_internos[tuple_list_indices_planos_internos[i][0]] = {'column': tuple_list_indices_planos_internos[i][1], 'elementos de despesa': []}

            # para j de valor igual ao valor da linha até o valor da proxima linha de planos internos fazer a comparacao de regex
            for j in range(tuple_list_indices_planos_internos_verification[i][0],tuple_list_indices_planos_internos_verification[i+1][0]+1):
                aux_counter = 0
       
                # para cada coluna do dataframe 
                for k in columns_names_pi_list:
            
                    if re.search(pattern_elemento_despesa_nome_e_codigo_tipo_2, str(pi_df[k][j])) and not re.search(pattern_nan, str(pi_df[k][j])):
                        dict_elemento_despesa = {}

                        # cria um chave de dicionario com valor do index do elemento de despesa (j) que tera uma lista para armazenar os desdobramentos de despesa
                        dict_elemento_despesa[j] = {'column': k, 'desdobramentos de elemento de despesa': []}

                        # faz o append do elemento de despesa (dicionario) a lista (value) que tem em cada chave de plano interno 
                        dict_planos_internos[tuple_list_indices_planos_internos[i][0]]['elementos de despesa'].append(dict_elemento_despesa)

                        # auxiliar para que seja selecionado o item certo da lista que é o value da chava de cada plano interno
                        aux_counter += 1 

                        # indice que sera usado para identificar o elemento de despesa
                        indice_elemento_despesa = j
            
                    # Verifica se os patterns de elemento de despesa acontecem
                    if re.search(pattern_elemento_despesa_codigo_tipo_1, str(pi_df[k][j])):
                        for m in columns_names_pi_list:
                            if re.search(pattern_elemento_despesa_nome_tipo_1, str(pi_df[m][j])) and not re.search(pattern_nan, str(pi_df[m][j])):

                                dict_elemento_despesa = {}

                                # cria um chave de dicionario com valor do index do elemento de despesa (j) que tera uma lista para armazenar os desdobramentos de despesa
                                dict_elemento_despesa[j] = {'column': k, 'desdobramentos de elemento de despesa': []}

                                # faz o append do elemento de despesa (dicionario) a lista (value) que tem em cada chave de plano interno 
                                dict_planos_internos[tuple_list_indices_planos_internos[i][0]]['elementos de despesa'].append(dict_elemento_despesa)

                                # auxiliar para que seja selecionado o item certo da lista que é o value da chava de cada plano interno
                                aux_counter += 1 

                                # indice que sera usado para identificar o elemento de despesa
                                indice_elemento_despesa = j

                    for l in columns_names_pi_list:

                        # Verifica se o patterns de desdobramento de elemento de despesa acontece    
                        if re.search(pattern_desdobramento_elemento_despesa_codigo, str(pi_df[l][j])):
                    
                            dict_desdobramento_elemento_despesa = {}
                            dict_desdobramento_elemento_despesa[j]={"column": l}

                            # adiciona na lista value do elemento de despeas, o desdobramento de despesa
                            if dict_desdobramento_elemento_despesa not in dict_planos_internos[tuple_list_indices_planos_internos[i][0]]['elementos de despesa'][aux_counter-1][indice_elemento_despesa]['desdobramentos de elemento de despesa']:
                                dict_planos_internos[tuple_list_indices_planos_internos[i][0]]['elementos de despesa'][aux_counter-1][indice_elemento_despesa]['desdobramentos de elemento de despesa'].append(dict_desdobramento_elemento_despesa)
                
        return dict_planos_internos
    