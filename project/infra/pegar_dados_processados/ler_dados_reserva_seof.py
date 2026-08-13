""" Class for the LerDadosReservaSeof use case """

import tabula

from project.use_cases.interfaces.pegar_dados_processados.ler_dados import (
    LerDados as LerDadosInterface,
)

class LerDadosReservaSeof(LerDadosInterface):
    """Class for the LerDadosReservaSeof use case"""

    def execute(self, output_path):
        """execute the ler dados"""

        reserva_seof_list = tabula.read_pdf(
            output_path,
            stream=True,
            pages="all",
            area=[137.96, 34.95, 732.96, 565.99],
            pandas_options={"header": None}
        )

        return reserva_seof_list
