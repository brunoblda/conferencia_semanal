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

    def execute(self, dict_indices: dict, plano_interno: pd.DataFrame) -> dict:
        """Executa a dicionarização dos indices"""

        pattern_plano_interno = r"^\d{2}(?:[A-Z]+|-[-A-Z]+(?: [A-Z]+)?)"
        pattern_desdobramento_elemento_despesa_codigo = r"^\d{2}\.\d{2}\.\d{2}"
        dict_resultado_plano_interno = {}

        # para cada chave de plano interno
        for w in dict_indices:

            nome_plano_interno = re.search(
                pattern_plano_interno, plano_interno[1][w]
            ).group()

            dotacao_plano_interno = self.utils.value_hygienization(plano_interno[3][w])

            dict_resultado_plano_interno[nome_plano_interno] = {
                "indice": w,
                "valor": dotacao_plano_interno,
                "elementos de despesa": {},
            }

            # para cada item da lista de value de cada chave de plano interno
            for z in dict_indices[w]:

                # para cada chave de elemento de despesa
                for y in z:

                    nome_elemento_despesa = re.sub(
                        r"[a-zA-ZÀ-ü\s\-\/]", "", plano_interno[1][y].strip()
                    )
                    if nome_elemento_despesa:
                        nome_elemento_despesa = re.search(
                            r"\d\.\d\.\d{2}\.\d{2}\.\d{2}", nome_elemento_despesa
                        )
                        if nome_elemento_despesa:
                            nome_elemento_despesa = nome_elemento_despesa[0]
                    if not nome_elemento_despesa:
                        nome_elemento_despesa = re.sub(
                            r"[a-zA-ZÀ-ü\s\-\/]", "", plano_interno[2][y]
                        )
                    nome_elemento_despesa = nome_elemento_despesa[:9]

                    # Eliminar os elementos de despesa que não possuem desdobramentos de despesas, para nao serem carregados no dicionario
                    if not z[y]:
                        continue

                    dotacao_elemento_despesa = self.utils.value_hygienization(
                        plano_interno[3][y]
                    )

                    dict_resultado_plano_interno[nome_plano_interno][
                        "elementos de despesa"
                    ][nome_elemento_despesa] = {
                        "indice": y,
                        "valor": dotacao_elemento_despesa,
                        "desdobramentos de despesa": {},
                    }

                    # para cada item da lista de value da chave de elemento de despesa
                    for x in z[y]:

                        nome_desdobramento_despesa = re.search(
                            pattern_desdobramento_elemento_despesa_codigo,
                            plano_interno[1][x],
                        )[0]
                        dotacao_desdobramento_despesa = self.utils.value_hygienization(
                            plano_interno[3][x]
                        )

                        dict_resultado_plano_interno[nome_plano_interno][
                            "elementos de despesa"
                        ][nome_elemento_despesa]["desdobramentos de despesa"][
                            nome_desdobramento_despesa
                        ] = {
                            "indice": x,
                            "valor": dotacao_desdobramento_despesa,
                        }

        return dict_resultado_plano_interno
