""" Class for the LerDadosPi use case """

import tabula

from project.use_cases.interfaces.pegar_dados_processados.ler_dados import (
    LerDados as LerDadosInterface,
)


class LerDadosPi(LerDadosInterface):
    """Class for the LerDadosPi use case"""

    def execute(self, output_path):
        """execute the ler dados"""

        pi_list = tabula.read_pdf(
            output_path,
            pages="all",
            stream=True,
            guess=False,
            area=[46.48, 120.48, 790.23, 471.53],
            pandas_options={"header": None}
        )

        return pi_list
