import pandas as pd
from project.domain.interfaces.mapear.command.sanitizar_pi import SanitizarPi as SanitizarPiInterface
from project.domain.interfaces.plano_interno import PlanoInterno as PlanoInternoInterface
from project.errors.types.sanitize_error import SanitizeError 

class SanitizarPi(SanitizarPiInterface):
    """ Sanitiza o PI """
    def execute(self, plano_interno: pd.DataFrame|list[str]) -> pd.DataFrame:
        """ Executa a higienização do PI """
        try:
            pi_df: pd.DataFrame = pd.concat(plano_interno, ignore_index=True)

            # substitui os valores da coluna 3 pela coluna 4, quando a coluna 3 for nula
            pi_df[3] = pi_df[3].combine_first(pi_df[4])
            # drop as colunas 0 e 4
            pi_df = pi_df.drop([0,4], axis=1)

            return pi_df

        except Exception as e:
                raise SanitizeError("Erro ao sanitizar o PI")
        