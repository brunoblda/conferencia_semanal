import re

import pandas as pd

from project.services.utilities.utils import Utils

from project.use_cases.mapear.reserva.command.dicionarizar_reserva import (
    DicionarizarReserva as dicionarizarReservaInterface
)

class DicionarizarReservaSiafi(dicionarizarReservaInterface):
    """Dicionariza a reserva do SIAFI"""

    def __init__(self, utils: Utils):
        self.utils = utils
        

    def execute(self, siafi_credito_disponivel_sem_fonte_list: list) -> dict:
        """execute the dicionarizar reserva """

        siafi_reserva_df = pd.concat(siafi_credito_disponivel_sem_fonte_list, ignore_index=True)

        columns_names_siafi_reserva_list = siafi_reserva_df.columns.to_list()

        pattern_8 = r'(^-8)'

        naturezas = r'319000|319100|335000|339000|339100|449000'

        pattern_natureza_reserva = rf'^(?:{naturezas})$'

        pattern_PTRES_reserva = rf'^(?!(?:{naturezas})$)\d{{6}}$'

        pattern_total = r'(^Total)'

        num_columns_siafi_reserva = siafi_reserva_df.shape[1]

        num_rows_siafi_reserva = siafi_reserva_df.shape[0]

        ptres_atual = None

        natureza_atual = None

        oito_atual = None

        dict_ptres_reserva_siafi = {}

        for i in range(num_rows_siafi_reserva):
            for j in range(num_columns_siafi_reserva):
                cell_value = siafi_reserva_df.iloc[i, j]

                if re.match(pattern_8, str(cell_value)):

                    oito_atual = cell_value

                    for k in range(num_columns_siafi_reserva):
                        if re.match(pattern_PTRES_reserva, str(siafi_reserva_df.iloc[i, k])):
                            ptres_atual = siafi_reserva_df.iloc[i, k]
                            dict_ptres_reserva_siafi[ptres_atual] = {'posicao': (i, k), 'naturezas': {}}
                
                        if re.match(pattern_natureza_reserva, str(siafi_reserva_df.iloc[i, k])):
                            natureza_atual = siafi_reserva_df.iloc[i, k]
                            dict_ptres_reserva_siafi[ptres_atual]['naturezas'][natureza_atual] = {'posicao': (i, k)}

                        if ',' in str(siafi_reserva_df.iloc[i, k]):
                            valor = self.utils.value_hygienization(siafi_reserva_df.iloc[i, k])
                            dict_ptres_reserva_siafi[ptres_atual]['naturezas'][natureza_atual]['valor'] = valor

                    break

                if oito_atual is not None and ptres_atual is not None:

                    if re.match(pattern_natureza_reserva, str(siafi_reserva_df.iloc[i, j])):
                        natureza_atual = siafi_reserva_df.iloc[i, j]
                        dict_ptres_reserva_siafi[ptres_atual]['naturezas'][natureza_atual] = {'posicao': (i, j)}
                

                    if ',' in str(siafi_reserva_df.iloc[i, j]):
                        valor = self.utils.value_hygienization(siafi_reserva_df.iloc[i, j])
                        dict_ptres_reserva_siafi[ptres_atual]['naturezas'][natureza_atual]['valor'] = valor

                    if re.match(pattern_total, str(cell_value)):

                        for k in range(num_columns_siafi_reserva):
                            if ',' in str(siafi_reserva_df.iloc[i, k]):
                                valor = self.utils.value_hygienization(siafi_reserva_df.iloc[i, k])
                                dict_ptres_reserva_siafi[ptres_atual]['valor'] = valor
            
                        oito_atual = None
                        ptres_atual = None
                        natureza_atual = None

        return dict_ptres_reserva_siafi   
        