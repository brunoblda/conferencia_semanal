from project.domain.interfaces.mapear.command.pegar_indices import PegarIndices as PegarIndicesInterface
import re
import pandas as pd

class PegarIndicesPi(PegarIndicesInterface):
    """ Pega os indices do PI """
    def execute(self, plano_interno_df: pd.DataFrame) -> dict:
        """ Executa a busca dos indices do PI """
    
        # pattern para encontrar os planos interno "10-AIMOVEIS"

        pattern_plano_interno = r'(^\d{2}(?:[A-Z]+|-[-A-Z]+(?: [A-Z]+)?))'

        extracted = plano_interno_df[1].str.extract(pattern_plano_interno)
        matched_rows_planos_internos = extracted.notna().any(axis=1)

        # matched_rows_planos_internos = plano_interno_df[1].str.contains(pattern_plano_interno).fillna(False).infer_objects(copy=False)
        # matched_rows_planos_internos = plano_interno_df[1].str.match(pattern_plano_interno).fillna(False)

        pattern_elemento_despesa_nome_tipo_1 = r'^[a-zA-Z]'
        pattern_elemento_despesa_codigo_tipo_1 = r'^\d\.\d\.\d{2}\.\d{2}\.\d{2}'
        # Motivo do pattern
        # Serviços de tecnologia da inform. e comunicação - pessoa jurídic3a.3.90.40.00
        # Material de consumo 3.3.90.30.00 
        # Serviços de tecnologia da informação e comunicação - pessoa ju3r.í3d.i9c0a.40.00
        pattern_elemento_despesa_nome_e_codigo_tipo_2 = r'^[a-zA-Z].*\.\d{2}\.\d{2}' 
        pattern_desdobramento_elemento_despesa_codigo = r'^\d{2}\.\d{2}\.\d{2}'

        indices_planos_internos = plano_interno_df[matched_rows_planos_internos].index

        list_indices_planos_internos = list(indices_planos_internos)
        list_indices_planos_internos_verification =list_indices_planos_internos.copy()

        # adicionando o ultimo indice do dataframe para a lista de verificacao
        list_indices_planos_internos_verification.append(len(plano_interno_df.index)-1)

        dict_planos_internos = {}

        # para i de 0 até o tamanho da lista de indices dos planos internos
        for i in range(len(list_indices_planos_internos)):

            # cria um dicionario igual ao valor do item na lista de planos internos de indice i
            dict_planos_internos[list_indices_planos_internos[i]]=[]

            # para j de valor igual ao valor da linha até o valor da proxima linha de planos internos fazer a comparacao de regex
            for j in range(list_indices_planos_internos_verification[i],list_indices_planos_internos_verification[i+1]+1):
                aux_counter = 0
        
                # Verifica se os patterns de elemento de despesa acontecem
                if (re.search(pattern_elemento_despesa_nome_tipo_1, str(plano_interno_df[1][j])) and re.search(pattern_elemento_despesa_codigo_tipo_1,str(plano_interno_df[2][j]))) or (re.search(pattern_elemento_despesa_nome_e_codigo_tipo_2, str(plano_interno_df[1][j]))):

                    dict_elemento_despesa = {}

                    # cria um chave de dicionario com valor do index do elemento de despesa (j) que tera uma lista para armazenar os desdobramentos de despesa
                    dict_elemento_despesa[j] = []

                    # faz o append do elemento de despesa (dicionario) a lista (value) que tem em cada chave de plano interno 
                    dict_planos_internos[list_indices_planos_internos[i]].append(dict_elemento_despesa)

                    # auxiliar para que seja selecionado o item certo da lista que é o value da chava de cada plano interno
                    aux_counter += 1 

                    # indice que sera usado para identificar o elemento de despesa
                    indice_elemento_despesa = j

                # Verifica se o patterns de desdobramento de elemento de despesa acontece    
                if re.search(pattern_desdobramento_elemento_despesa_codigo, str(plano_interno_df[1][j])):

                    # adiciona na lista value do elemento de despeas, o desdobramento de despesa
                    dict_planos_internos[list_indices_planos_internos[i]][aux_counter-1][indice_elemento_despesa].append(j)

                    
        return dict_planos_internos
    