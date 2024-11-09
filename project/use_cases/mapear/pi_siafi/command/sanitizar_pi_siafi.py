from project.domain.interfaces.mapear.command.sanitizar_pi import SanitizarPi as SanitizarPiInterface
import pandas as pd

class SanitizarPiSiafi(SanitizarPiInterface):
    """ Sanitiza o PI Siafi"""
    def execute(self, plano_interno: pd.DataFrame|list[str]) -> pd.DataFrame:
        """ Executa a higienização do PI """

        pi_siafi_df: pd.DataFrame = plano_interno
        
        columns = pi_siafi_df.columns

        columns_list = (list(columns.values))

        pi_siafi_df.drop(columns=columns_list[:10], inplace=True)

        column_headers = list(pi_siafi_df)

        pi_siafi_df = pi_siafi_df.rename(columns={column_headers[0]:1,column_headers[1] :2, column_headers[2]: 3 })

        siafi_pi_dasf_df = pi_siafi_df

        siafi_pi_dasf_df[1] = siafi_pi_dasf_df[1].astype(str)

        siafi_pi_dasf_df[2] = siafi_pi_dasf_df[2].astype(str)

        return siafi_pi_dasf_df