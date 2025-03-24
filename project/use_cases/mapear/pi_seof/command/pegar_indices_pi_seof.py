import re

import pandas as pd

from project.domain.interfaces.mapear.command.pegar_indices import (
    PegarIndices as PegarIndicesInterface,
)

from project.use_cases.interfaces.utilities.utils import Utils as UtilsInterface

class PegarIndicesPiSeof(PegarIndicesInterface):
    """Pega os indices do PI SEOF"""

    def __init__(self, utils: UtilsInterface):
        self.utils = utils

    def execute(self, plano_interno: pd.DataFrame) -> dict:
        """Executa a busca dos indices do PI SEOF"""
        # pattern para encontrar os planos interno "10-AIMOVEIS"
        
        plano_interno = pd.concat(plano_interno, ignore_index=True) 

        columns_names_seof_pi_list = plano_interno.columns.to_list()

        # pattern para encontrar os planos interno "10-AIMOVEIS"
        pattern_plano_interno_seof = r'(^\d{2}(?:[A-Z]+|-[-A-Z]+(?: [A-Z]+)?))'

        extracted_list = []

        for i in columns_names_seof_pi_list:
            extracted = plano_interno[i].str.extract(pattern_plano_interno_seof)
            extracted_list.append(extracted)

        matched_rows_planos_internos_seof_list = [extracted.notna().any(axis=1) for extracted in extracted_list]

        matched_rows_planos_internos_seof_df = pd.concat(matched_rows_planos_internos_seof_list, axis=1)

        matched_rows_planos_internos_seof_df.columns = columns_names_seof_pi_list

        tuple_list_indices_planos_internos_seof = self.utils.get_row_and_column(matched_rows_planos_internos_seof_df)

        pattern_nan = r'^nan'

        # pattern para encontrar os elementos de despesa
        pattern_elemento_de_despesa_seof = r'^[34]\d{5} - '

        # pattern para encontrar os desdobramentos de despesa
        pattern_desdobramento_elemento_despesa_seof = r'^\d{2}.\d{2}.\d{2}'


        tuple_list_indices_planos_internos_seof_verification = tuple_list_indices_planos_internos_seof.copy()
        # adicionando o ultimo indice do dataframe para a lista de verificacao

        tuple_list_indices_planos_internos_seof_verification.append((len(plano_interno.index)-1, columns_names_seof_pi_list[-1]))

        # ic.ic(list_indices_planos_internos_verification_seof)

        dict_planos_internos_seof = {}

        # para i de 0 até o tamanho da lista de indices dos planos internos seof
        for i in range(len(tuple_list_indices_planos_internos_seof)):
            # cria um dicionario igual ao valor do item na lista de planos internos de indice i
            dict_planos_internos_seof[tuple_list_indices_planos_internos_seof[i][0]]= {'column': tuple_list_indices_planos_internos_seof[i][1], 'elementos de despesa': []}

            # para j de valor igual ao valor da linha até o valor da proxima linha de planos internos fazer a comparacao de regex
            for j in range(tuple_list_indices_planos_internos_seof_verification[i][0],tuple_list_indices_planos_internos_seof_verification[i+1][0]+1):
                aux_counter = 0

                for k in columns_names_seof_pi_list:
        
                    # Verifica se os patterns de elemento de despesa acontecem
                    if re.search(pattern_elemento_de_despesa_seof, str(plano_interno[k][j])):
                        dict_elemento_despesa = {}

                        # cria um chave de dicionario com valor do index do elemento de despesa (j) que tera uma lista para armazenar os desdobramentos de despesa
                        dict_elemento_despesa[j] = {'column': k, 'desdobramentos de elemento de despesa': []}

                        # faz o append do elemento de despesa (dicionario) a lista (value) que tem em cada chave de plano interno 
                        dict_planos_internos_seof[tuple_list_indices_planos_internos_seof[i][0]]['elementos de despesa'].append(dict_elemento_despesa)

                        # auxiliar para que seja selecionado o item certo da lista que é o value da chava de cada plano interno
                        aux_counter += 1 

                        # indice que sera usado para identificar o elemento de despesa
                        indice_elemento_despesa = j

                    for l in columns_names_seof_pi_list:

                        # Verifica se o patterns de desdobramento de elemento de despesa acontece    
                        if re.search(pattern_desdobramento_elemento_despesa_seof, str(plano_interno[l][j])):

                            dict_desdobramento_elemento_despesa = {}
                            dict_desdobramento_elemento_despesa[j]={"column": l}
            
                            # adiciona na lista value do elemento de despeas, o desdobramento de despesa
                            if dict_desdobramento_elemento_despesa not in dict_planos_internos_seof[tuple_list_indices_planos_internos_seof[i][0]]['elementos de despesa'][aux_counter-1][indice_elemento_despesa]['desdobramentos de elemento de despesa']:
                                dict_planos_internos_seof[tuple_list_indices_planos_internos_seof[i][0]]['elementos de despesa'][aux_counter-1][indice_elemento_despesa]['desdobramentos de elemento de despesa'].append(dict_desdobramento_elemento_despesa)
                    
        return dict_planos_internos_seof