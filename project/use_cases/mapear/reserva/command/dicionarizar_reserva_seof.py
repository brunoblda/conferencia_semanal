import re

import pandas as pd

from project.use_cases.mapear.reserva.command.dicionarizar_reserva import (
    DicionarizarReserva as dicionarizarReservaInterface,
)
from project.services.utilities.utils import Utils

class DicionarizarReservaSeof(dicionarizarReservaInterface):
    """Dicionariza a reserva do SEOF"""

    def __init__(self, utils: Utils):
        self.utils = utils

    def execute(self, seof_plano_interno_reserva_list: list) -> dict:
        """execute the dicionarizar reserva """

        seof_pi_reserva_df = pd.concat(seof_plano_interno_reserva_list, ignore_index=True)

        columns_names_seof_pi_reserva_list = seof_pi_reserva_df.columns.to_list()

        pattern_despesas_correntes = r'^Despesas Correntes$'

        pattern_cabecalho_reserva_seof = r'^(Identificador|Plano Interno)'

        pattern_seof_po_reserva = r'(^PO [A-Z0-9]{4})'

        pattern_natureza_seof = r'(3\.1\.\d{2}\.\d{2}\.\d{1}$|3\.3\.\d{2}\.\d{2}\.\d{1}$|4\.\d{1}\.\d{2}\.\d{2}\.\d{1}$)'

        num_columns_pi_reserva_list = seof_pi_reserva_df.columns.to_list()

        dict_seof_pos_reserva = {}

        po_atual = None
        item_atual = None

        for i in range(len(seof_pi_reserva_df)):
            for j in range(len(columns_names_seof_pi_reserva_list)):

                celula = str(seof_pi_reserva_df.iloc[i, j])

                # verifica se encontra o patterm de despesas correntes, pois os POs estão na linha acima
                match_despesas_correntes = re.search(pattern_despesas_correntes, celula)

                if match_despesas_correntes:

                    indice = i-1

                    po_atual = 'PO 0000 - ' + str(seof_pi_reserva_df.iloc[indice, j])
            
                    match_cabecalho_reserva_seof = re.search(pattern_cabecalho_reserva_seof, str(seof_pi_reserva_df.iloc[indice, j]))
            
                    if match_cabecalho_reserva_seof:
                        indice = i-2
                        po_atual = 'PO 0000 - ' + str(seof_pi_reserva_df.iloc[indice, j])
                

                    # procura o po para aqueles que estao no padrão PO - XXXXX
                    match_seof_po_reserva = re.search(pattern_seof_po_reserva, str(seof_pi_reserva_df.iloc[indice, j]))

                    if match_seof_po_reserva:

                        po_atual = seof_pi_reserva_df.iloc[indice, j]

                    dict_seof_pos_reserva[po_atual] = {'posicao': (indice, j), '3.3': {'itens': [], 'valor': 0}, '3.1': {'itens': [], 'valor': 0}, '4.4': {'itens': [], 'valor': 0}}
                    item_atual = None

                    # procura o valor do po em cada coluna da linha
                    for col_scan in range(len(num_columns_pi_reserva_list)):
                        if self.utils.is_numero(seof_pi_reserva_df.iloc[indice, col_scan]):
                            dict_seof_pos_reserva[po_atual]['valor'] = self.utils.value_hygienization(seof_pi_reserva_df.iloc[indice, col_scan])
                            break


                # verifica se o po atual ja foi inserido no dicionario
                if po_atual in dict_seof_pos_reserva:

                    match_natureza_seof = re.search(pattern_natureza_seof, celula)

                    # identifica a natureza de despesa, toda string do item contém a natureza
                    if match_natureza_seof:
                        natureza_atual = match_natureza_seof.group()
                        if natureza_atual[:3] == '3.1':
                            natureza_atual = '3.1'
                        elif natureza_atual[:3] == '3.3':
                            natureza_atual = '3.3'
                        elif natureza_atual[:3] == '4.4':
                            natureza_atual = '4.4' 

                        valor_item = None

                        # procura o valor do item em cada coluna da linha
                        for col_scan in range(len(num_columns_pi_reserva_list)):
                            if self.utils.is_numero(seof_pi_reserva_df.iloc[i, col_scan]):
                                valor_item = self.utils.value_hygienization(seof_pi_reserva_df.iloc[i, col_scan])
                            elif not str(seof_pi_reserva_df.iloc[i, col_scan]).strip() == 'nan':
                                has_string = re.sub(r"\d\.\d\.\d{2}\.\d{2}\.\d$", "", str(seof_pi_reserva_df.iloc[i, col_scan]))
                                if has_string:
                                    item_atual = re.sub(r"\s+\d\.\d\.\d{2}\.\d{2}\.\d$", "", str(seof_pi_reserva_df.iloc[i, col_scan])).strip()

                        # Salva o valor no item 
                        dict_seof_pos_reserva[po_atual][natureza_atual]['itens'].append({'item': item_atual, 'posicao': (i, j), 'valor': valor_item})

                        if valor_item is not None:
                            # Salva o valor do item na natureza correspondente
                            dict_seof_pos_reserva[po_atual][natureza_atual]['valor'] = round(dict_seof_pos_reserva[po_atual][natureza_atual]['valor'] + float(valor_item), 2)

                    
        return dict_seof_pos_reserva
            