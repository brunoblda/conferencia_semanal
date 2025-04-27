import pandas as pd

import re

from project.domain.interfaces.mapear.command.pegar_indices import (
    PegarIndices as PegarIndicesInterface,
)

from project.use_cases.interfaces.utilities.utils import Utils as UtilsInterface

class PegarIndicesPiSiafi(PegarIndicesInterface):
    """Pega os indices do PI Siafi"""

    def __init__(self, utils: UtilsInterface):
        self.utils = utils

    def execute(self, plano_interno: pd.DataFrame) -> dict:
        """Executa a busca dos indices do PI Siafi"""

        siafi_pi_df_original = pd.concat(plano_interno, ignore_index=True)

        siafi_pi_df = siafi_pi_df_original.copy()

        columns_names_siafi_pi_list = siafi_pi_df.columns.to_list()

        # patterns para encontrar os planos internos
        pattern_plano_interno_column_result_siafi = r'(((?:^|\s)\d{2}[-A-Z]{7,9}(?:\s|$))|((?:^|\s)-8(?:\s|$)))'

        extracted_list = []

        siafi_pi_df = siafi_pi_df.astype(str)

        for i in columns_names_siafi_pi_list:
            extracted = siafi_pi_df[i].str.extract(pattern_plano_interno_column_result_siafi)
            extracted_list.append(extracted)

        matched_rows_planos_internos_siafi_list = [extracted.notna().any(axis=1) for extracted in extracted_list]
    
        matched_rows_planos_internos_siafi_df = pd.concat(matched_rows_planos_internos_siafi_list, axis=1)    

        matched_rows_planos_internos_siafi_df.columns = columns_names_siafi_pi_list

        tuple_list_indices_planos_internos_siafi= self.utils.get_row_and_column(matched_rows_planos_internos_siafi_df)

        # patterns para encontrar os elementos de despesas

        pattern_elemento_de_despesa_siafi = r'(^\d{6})'

        pattetn_total = r'(^Total)'

        extracted_list = []

        for i in columns_names_siafi_pi_list:
            extracted = siafi_pi_df[i].str.extract(pattern_elemento_de_despesa_siafi)
            extracted_list.append(extracted)

        matched_rows_elementos_de_despesa_siafi_list = [extracted.notna().any(axis=1) for extracted in extracted_list]

        matched_rows_elementos_de_despesa_siafi_df = pd.concat(matched_rows_elementos_de_despesa_siafi_list, axis=1)

        matched_rows_elementos_de_despesa_siafi_df.columns = columns_names_siafi_pi_list

        tuple_list_indices_elementos_de_despesa_siafi = self.utils.get_row_and_column(matched_rows_elementos_de_despesa_siafi_df)

        extracted_list = []

        for i in columns_names_siafi_pi_list:
            extracted = siafi_pi_df[i].str.extract(pattetn_total)
            extracted_list.append(extracted)

        matched_rows_total_siafi_list = [extracted.notna().any(axis=1) for extracted in extracted_list]

        matched_rows_total_siafi_df = pd.concat(matched_rows_total_siafi_list, axis=1)

        matched_rows_total_siafi_df.columns = columns_names_siafi_pi_list

        tuple_list_indices_total_siafi = self.utils.get_row_and_column(matched_rows_total_siafi_df)

        list_planos_verified = []

        dict_planos_internos_siafi = {}

        aux_count_indice = 0

        # para cada indice na lista de indices de planos internos
        for i in tuple_list_indices_planos_internos_siafi:

            matched_plano_interno = re.search(pattern_plano_interno_column_result_siafi ,siafi_pi_df[i[1]][i[0]])
            if matched_plano_interno:
                # if matched_plano_interno.group() != '-8' and matched_plano_interno.group() in list_planos_verified:
                if  ('-8' not in matched_plano_interno.group()) and matched_plano_interno.group() in list_planos_verified:

                    continue

            dict_planos_internos_siafi[i[0]] = {'column': i[1], 'totais': []}
    
            # para cada indice de elementos de despesa total
            for j in tuple_list_indices_total_siafi:
                list_j = {j[0]:{'column': j[1], 'elementos de despesa': []}}
                dict_planos_internos_siafi[i[0]]['totais'].append(list_j)

                # para cada indice da lista de indices de elementos de despesa siafi - de 0 até o final da lista
                for k in range(aux_count_indice, len(tuple_list_indices_elementos_de_despesa_siafi)):
            
                    # se o indice do elemento de despesa for maior que o indice de total, break
                    if tuple_list_indices_elementos_de_despesa_siafi[k][0] > j[0]:
                        break
                    elemento_de_depesa_siafi = {tuple_list_indices_elementos_de_despesa_siafi[k][0]: {'column': tuple_list_indices_elementos_de_despesa_siafi[k][1]}}
                    dict_planos_internos_siafi[i[0]]['totais'][0][j[0]]['elementos de despesa'].append(elemento_de_depesa_siafi)
            
                    # a proxima contagem de k começara pelo proximo item, mesmo quando passar para o loop de j, o valor não é reiniciado
                    aux_count_indice += 1
            
                # remove o valor de j, para nao contar no proximo loop    
                tuple_list_indices_total_siafi.remove(j)
                break

            if matched_plano_interno:
                list_planos_verified.append(matched_plano_interno.group())

        return dict_planos_internos_siafi
