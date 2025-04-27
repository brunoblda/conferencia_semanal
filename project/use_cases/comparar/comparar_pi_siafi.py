""" Module to compare PIs """

import pandas as pd

from project.domain.interfaces.comparar.comparar_pis import (
    CompararPis as CompararPisInterface,
)
from project.services.types.response_data_comparar_pis import ResponseData
from project.use_cases.interfaces.utilities.utils import Utils as UtilsInterface


class CompararPiSiafi(CompararPisInterface):
    """Compare PIs"""

    def __init__(self, utils: UtilsInterface):
        self.utils = utils
        self.status = "sem erro"

    def get_status(self) -> str:
        """Get the status of the comparison"""
        return self.status

    def update_status(self, status: str) -> None:
        """Update the status of the comparison"""
        self.status = status

    def execute(
        self, pi_principal: pd.DataFrame, pi_secundário: pd.DataFrame
    ) -> ResponseData:
        """Execute the comparison of the PI with the PI Siafi"""

        update_status_com_erro = "com erro"

        pi = pi_principal
        pi_siafi = pi_secundário

        col_1 = "PLANO INTERNO"
        col_2 = "ELEMENTO - ITEM"
        col_3 = "VALOR PI"
        col_4 = "VALOR SIAFI"
        col_5 = "DIF.: PI - SIAFI"
        response = f"|{col_1:^15}|{col_2:^17}|{col_3:^15}|{col_4:^15}|{col_5:^17}|\n"
        response += f"|{'':-^15}|{'':-^17}|{'':-^15}|{'':-^15}|{'':-^17}|\n"

        # para cada plano interno no dicionario de planos internos
        for n in pi:

            # se o plano interno estiver no dicionario de planos internos do siafi
            if n in pi_siafi:
                if pi[n]["valor"] != pi_siafi[n]["valor"]:
                    self.update_status(update_status_com_erro)
                    response += f"|{n:^15}|{'':^17}|" + self.utils.replace_commas_and_dots(
                        f"{pi[n]['valor']:^15,.2f}|{pi_siafi[n]['valor']:^15,.2f}|{pi[n]['valor'] - pi_siafi[n]['valor']:^17,.2f}|\n"
                    )

                # para cada elemento de despesa no dicionario de elementos de despesa do plano interno
                for m in pi[n]["elementos de despesa"]:

                    # se o elemento de despesa estiver no dicionario de elementos de despesa do plano interno do siafi
                    if m in pi_siafi[n]["elementos de despesa"]:
                        if (
                            pi[n]["elementos de despesa"][m]["valor"]
                            != pi_siafi[n]["elementos de despesa"][m]["valor"]
                        ):
                            self.update_status(update_status_com_erro)
                            response += (
                                f"|{n:^15}|{m:^17}|"
                                + self.utils.replace_commas_and_dots(
                                    f"{pi[n]['elementos de despesa'][m]['valor']:^15,.2f}|{pi_siafi[n]['elementos de despesa'][m]['valor']:^15,.2f}|{pi[n]['elementos de despesa'][m]['valor'] - pi_siafi[n]['elementos de despesa'][m]['valor']:^17,.2f}|\n"
                                )
                            )

                    # se o elemento de despesa não estiver no dicionario de elementos de despesa do plano interno do siafi
                    else:
                        response += f"|{n:^15}|{m:^17}|" + self.utils.replace_commas_and_dots(
                            f"{pi[n]['elementos de despesa'][m]['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                        )

            # se o plano interno não estiver no dicionario de planos internos do siafi
            else:
                response += f"|{n:^15}|{'':^17}|" + self.utils.replace_commas_and_dots(
                    f"{pi[n]['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                )

                # mostrar os 0 dos elementos de despesa
                for m in pi[n]["elementos de despesa"]:
                    response += f"|{n:^15}|{m:^17}|" + self.utils.replace_commas_and_dots(
                        f"{pi[n]['elementos de despesa'][m]['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                    )

        data: ResponseData = {"response": response, "status": self.get_status()}

        return data
