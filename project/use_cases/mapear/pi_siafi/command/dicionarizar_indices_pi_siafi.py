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

        dict_resultado_plano_interno_siafi_dasf = {}

        # para a chave do plano interno
        for w in dict_indices:
            # para descartar os -8
            if not re.match(r"-\d", plano_interno[1][w]):
                nome_plano_interno_siafi_dasf = plano_interno[1][w]

                # para pegar os indice da chave que esta na lista do dicionario de cada plano interno
                dotacao_plano_interno_siafi_dasf = self.utils.value_hygienization(
                    plano_interno[3][list(dict_indices[w][0].keys())[0]]
                )

                dict_resultado_plano_interno_siafi_dasf[
                    nome_plano_interno_siafi_dasf
                ] = {
                    "indice plano interno": w,
                    "indice total": list(dict_indices[w][0].keys())[0],
                    "valor": dotacao_plano_interno_siafi_dasf,
                    "elementos de despesa": {},
                }

                # para cada item da lista de value de cada chave de plano interno que é [0]
                for z in dict_indices[w]:

                    # para cada chave de dicionario que é o indice do total
                    for y in z:

                        # para indice dentro da lista que é o valor da chave do indice total
                        for x in range(len(z[y])):

                            # para pegar o valor dentro da lista que esta dentro da lista, dentro o dicionario total, o x é o indice da lista, não o valor
                            nome_elemento_despesa_siafi_dasf = plano_interno[2][
                                dict_indices[w][0][y][x]
                            ]
                            nome_elemento_despesa_siafi_dasf = (
                                nome_elemento_despesa_siafi_dasf[:1]
                                + "."
                                + nome_elemento_despesa_siafi_dasf[1:2]
                                + "."
                                + nome_elemento_despesa_siafi_dasf[2:4]
                                + "."
                                + nome_elemento_despesa_siafi_dasf[4:]
                            )
                            dotacao_elemento_despesa_siafi_dasf = (
                                self.utils.value_hygienization(
                                    plano_interno[3][dict_indices[w][0][y][x]]
                                )
                            )

                            dict_resultado_plano_interno_siafi_dasf[
                                nome_plano_interno_siafi_dasf
                            ]["elementos de despesa"][
                                nome_elemento_despesa_siafi_dasf
                            ] = {
                                "indice": z[y][x],
                                "valor": dotacao_elemento_despesa_siafi_dasf,
                            }

        return dict_resultado_plano_interno_siafi_dasf
