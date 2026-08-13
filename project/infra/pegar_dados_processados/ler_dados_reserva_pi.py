""" Class for the LerDadosReservaPi use case """

import tabula

from project.use_cases.interfaces.pegar_dados_processados.ler_dados import (
    LerDados as LerDadosInterface,
)


class LerDadosReservaPi(LerDadosInterface):
    """Class for the LerDadosReservaPi use case"""

    def execute(self, output_path):
        """execute the ler dados"""

        reserva_pi_list = tabula.read_pdf(
            output_path,
            pages="all",
            stream=True,
            guess=False,
            area=[31.60, 124.95, 781.30, 470.79],
            pandas_options={"header": None}
        )

        return reserva_pi_list

