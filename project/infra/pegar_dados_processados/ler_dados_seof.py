""" Class for the LerDadosSeof use case """

import tabula
from project.use_cases.interfaces.pegar_dados_processados.ler_dados import LerDados as LerDadosInterface

class LerDadosSeof(LerDadosInterface):
    """ Class for the LerDadosSeof use case """
    
    def execute(self, output_path):
        """ execute the ler dados """

        seof_pi_df = tabula.read_pdf(output_path, pages='all', guess=False)
        
        return seof_pi_df