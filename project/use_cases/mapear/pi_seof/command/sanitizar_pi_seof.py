from project.domain.interfaces.mapear.command.sanitizar_pi import SanitizarPi as SanitizarPiInterface
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface
import pandas as pd

class SanitizarPiSeof(SanitizarPiInterface):
    """ Sanitiza o PI Seof"""
    def execute(self, plano_interno: pd.DataFrame|list[str]) -> pd.DataFrame:
        """ Executa a higienização do PI """

        # cada pagina é uma lista, o concat junta todas as listas em um dataframe
        seof_pi_df: pd.DataFrame = pd.concat(plano_interno, ignore_index=True)

        column_headers = list(seof_pi_df)

        seof_pi_df = seof_pi_df.rename(columns={column_headers[0]:1,column_headers[1] :2, column_headers[2]: 3 })

        seof_pi_df[4] = seof_pi_df[2].combine_first(seof_pi_df[3])

        seof_pi_df = seof_pi_df.drop([2,3], axis=1)

        column_headers = list(seof_pi_df)

        seof_pi_df = seof_pi_df.rename(columns={column_headers[0]:1,column_headers[1] :2})

        return seof_pi_df