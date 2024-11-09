""" Class for the LerDadosSiafi use case """

import pandas as pd
from project.use_cases.interfaces.pegar_dados_processados.ler_dados import LerDados as LerDadosInterface

class LerDadosSiafi(LerDadosInterface):
    """ Class for the LerDadosSiafi use case """

    def execute(self, output_path):
        """ execute the ler dados """

        siafi_dasf_df = pd.read_excel(output_path, engine='openpyxl')

        return siafi_dasf_df