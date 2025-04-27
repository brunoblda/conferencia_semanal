""" Class for the LerDadosSiafi use case """

import tabula

from project.use_cases.interfaces.pegar_dados_processados.ler_dados import (
    LerDados as LerDadosInterface,
)


class LerDadosSiafi(LerDadosInterface):
    """Class for the LerDadosSiafi use case"""

    def execute(self, output_path):
        """execute the ler dados"""

        siafi_dasf_df = tabula.read_pdf(
            output_path,
            pages="all",
            stream=True,
            guess=False,
            area=[82.58, 554.45, 523.41, 753.30],
            pandas_options={"header": None}
        )

        return siafi_dasf_df
