import re

import pandas as pd

from project.domain.interfaces.mapear.command.pegar_indices import (
    PegarIndices as PegarIndicesInterface,
)


class PegarIndicesPiSeof(PegarIndicesInterface):
    """Pega os indices do PI SEOF"""

    def execute(self, plano_interno_df: pd.DataFrame) -> dict:
        """Executa a busca dos indices do PI SEOF"""
        # pattern para encontrar os planos interno "10-AIMOVEIS"

        pattern_plano_interno_seof = r"(^\d{2}(?:[A-Z]+|-[-A-Z]+(?: [A-Z]+)?))"

        extracted = plano_interno_df[1].str.extract(pattern_plano_interno_seof)
        matched_rows_planos_internos_seof = extracted.notna().any(axis=1)

        # matched_rows_planos_internos_seof = plano_interno_df[1].str.contains(pattern_plano_interno_seof).fillna(False).infer_objects(copy=False)
        # matched_rows_planos_internos_seof = plano_interno_df[1].str.match(pattern_plano_interno_seof).fillna(False)

        indices_planos_internos_seof = plano_interno_df[
            matched_rows_planos_internos_seof
        ].index

        # pattern para encontrar os elementos de despesa
        pattern_elemento_de_despesa_seof = r"^[34]\d{5} - "

        # pattern para encontrar os desdobramentos de despesa
        pattern_desdobramento_elemento_despesa_seof = r"^\d{2}.\d{2}.\d{2}"

        list_indices_planos_internos_seof = list(indices_planos_internos_seof)
        list_indices_planos_internos_verification_seof = (
            list_indices_planos_internos_seof.copy()
        )

        # adicionando o ultimo indice do dataframe para a lista de verificacao
        list_indices_planos_internos_verification_seof.append(
            len(plano_interno_df.index) - 1
        )

        # ic.ic(list_indices_planos_internos_verification_seof)

        dict_planos_internos_seof = {}

        # para i de 0 até o tamanho da lista de indices dos planos internos seof
        for i in range(len(list_indices_planos_internos_seof)):
            # cria um dicionario igual ao valor do item na lista de planos internos de indice i
            dict_planos_internos_seof[list_indices_planos_internos_seof[i]] = []

            # para j de valor igual ao valor da linha até o valor da proxima linha de planos internos fazer a comparacao de regex
            for j in range(
                list_indices_planos_internos_verification_seof[i],
                list_indices_planos_internos_verification_seof[i + 1] + 1,
            ):
                aux_counter = 0

                # Verifica se os patterns de elemento de despesa acontecem
                if re.search(
                    pattern_elemento_de_despesa_seof, str(plano_interno_df[1][j])
                ):
                    dict_elemento_despesa = {}

                    # cria um chave de dicionario com valor do index do elemento de despesa (j) que tera uma lista para armazenar os desdobramentos de despesa
                    dict_elemento_despesa[j] = []

                    # faz o append do elemento de despesa (dicionario) a lista (value) que tem em cada chave de plano interno
                    dict_planos_internos_seof[
                        list_indices_planos_internos_seof[i]
                    ].append(dict_elemento_despesa)

                    # auxiliar para que seja selecionado o item certo da lista que é o value da chava de cada plano interno
                    aux_counter += 1

                    # indice que sera usado para identificar o elemento de despesa
                    indice_elemento_despesa = j

                # Verifica se o patterns de desdobramento de elemento de despesa acontece
                if re.search(
                    pattern_desdobramento_elemento_despesa_seof,
                    str(plano_interno_df[1][j]),
                ):

                    # adiciona na lista value do elemento de despeas, o desdobramento de despesa
                    dict_planos_internos_seof[list_indices_planos_internos_seof[i]][
                        aux_counter - 1
                    ][indice_elemento_despesa].append(j)

        return dict_planos_internos_seof
