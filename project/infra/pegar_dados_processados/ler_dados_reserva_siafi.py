""" Class for the LerDadosReservaSiafi use case """

import tabula

from project.use_cases.interfaces.pegar_dados_processados.ler_dados import (
    LerDados as LerDadosInterface,
)

class LerDadosReservaSiafi(LerDadosInterface):
    """Class for the LerDadosReservaSiafi use case"""

    def execute(self, output_path):
        """execute the ler dados"""

        reserva_siafi_list = tabula.read_pdf(
            output_path,
            pages="all",
            lattice=True,
            guess=False,
            area=[86.62, 510.84, 522.22, 700.92],
            pandas_options={"header": None}
        )

        return reserva_siafi_list
