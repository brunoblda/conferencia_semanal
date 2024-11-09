from project.domain.interfaces.mapear.command.pegar_indices import PegarIndices as PegarIndicesInterface
import pandas as pd
import re

class PegarIndicesPiSiafi(PegarIndicesInterface):
    """ Pega os indices do PI Siafi """
    
    def execute(self, plano_interno_df: pd.DataFrame) -> dict:
        """ Executa a busca dos indices do PI Siafi """

        # patterns para encontrar os planos internos

        pattern_plano_interno_column_result_siafi_dasf = r'(^\d{2}[-A-Z]{7,9})|(^-8)'

        # Extract and update column 1

        extracted = plano_interno_df[1].str.extract(pattern_plano_interno_column_result_siafi_dasf)
        matched_rows_planos_internos_column_1_siafi_dasf = extracted.notna().any(axis=1)
        
        # matched_rows_planos_internos_column_1_siafi_dasf = plano_interno_df[1].str.contains(pattern_plano_interno_column_result_siafi_dasf).fillna(False)

        indices_planos_internos_siafi_dasf = plano_interno_df[matched_rows_planos_internos_column_1_siafi_dasf].index

        # patterns para encontrar os elementos de despesas

        pattern_elemento_de_despesa_siafi_dasf = r'^\d{6}'

        pattern_total_siafi_dasf = r'^Total'

        matched_rows_elementos_de_despesa_siafi_dasf = plano_interno_df[2].str.match(pattern_elemento_de_despesa_siafi_dasf).fillna(False)

        indices_elementos_de_despesa_siafi_dasf = plano_interno_df[matched_rows_elementos_de_despesa_siafi_dasf].index

        matched_rows_elementos_de_despesa_total_siafi_dasf = plano_interno_df[2].str.match(pattern_total_siafi_dasf).fillna(False)

        indices_elementos_de_despesa_total_siafi_dasf = plano_interno_df[matched_rows_elementos_de_despesa_total_siafi_dasf].index

        # ic.ic(indices_planos_internos_siafi_dasf)
        # ic.ic(indices_elementos_de_despesa_siafi_dasf)
        # ic.ic(indices_elementos_de_despesa_total_siafi_dasf)

        list_planos_verified = []

        dict_planos_internos_siafi_dasf = {}

        aux_count_indice = 0

        list_indices_planos_internos_siafi_dasf = indices_planos_internos_siafi_dasf.to_list()
        list_indices_elementos_de_despesa_siafi_dasf = indices_elementos_de_despesa_siafi_dasf.to_list()
        list_indices_elementos_de_despesa_total_siafi_dasf = indices_elementos_de_despesa_total_siafi_dasf.to_list()

        # para cada indice na lista de indices de planos internos
        for i in list_indices_planos_internos_siafi_dasf:
    
            # verifica se o plano interno ja foi verificado, pois as vezes o mesmo plano interno aparece mais de uma vez por conta de quebra de pagina
            # o -8 deve ser ignorado, pois o continue eh somente para pegar os planos internos
            if plano_interno_df[1][i] != '-8' and plano_interno_df[1][i] in list_planos_verified:
                continue
            dict_planos_internos_siafi_dasf[i] = []
    
            # para cada indice de elementos de despesa total
            for j in list_indices_elementos_de_despesa_total_siafi_dasf:
                list_j = {j:[]}
                dict_planos_internos_siafi_dasf[i].append(list_j)

                # para cada indice da lista de indices de elementos de despesa siafi - de 0 até o final da lista
                for k in range(aux_count_indice, len(list_indices_elementos_de_despesa_siafi_dasf)):
            
                    # se o indice do elemento de despesa for maior que o indice de total, break
                    if list_indices_elementos_de_despesa_siafi_dasf[k] > j:
                        break
                    dict_planos_internos_siafi_dasf[i][0][j].append(list_indices_elementos_de_despesa_siafi_dasf[k])
            
                    # a proxima contagem de k começara pelo proximo item, mesmo quando passar para o loop de j, o valor não é reiniciado
                    aux_count_indice += 1
            
                # remove o valor de j, para nao contar no proximo loop    
                list_indices_elementos_de_despesa_total_siafi_dasf.remove(j)
                break
    
            list_planos_verified.append(plano_interno_df[1][i])

        return dict_planos_internos_siafi_dasf
    