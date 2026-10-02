""" Módulo de comparação entre reserva PI e SIAFI """

import pandas as pd

from project.domain.interfaces.comparar.comparar_reservas import (
    CompararReservas as CompararReservasInterface,
)
from project.services.types.response_data_comparar_reservas import ResponseData
from project.services.utilities.utils import Utils

class CompararReservaPiSiafi(CompararReservasInterface):
    """Compare Reservas"""

    def __init__(self, utils: Utils):
        self.utils = utils
        self.status = "sem erro"

    def get_status(self) -> str:
        """Get the status of the comparison"""
        return self.status

    def update_status(self, status: str) -> None:
        """Update the status of the comparison"""
        self.status = status

    def execute(
        self, reserva_principal: pd.DataFrame, reserva_secundaria: pd.DataFrame
    ) -> ResponseData:
        """Execute the comparison of the reserva PI with the reserva SIAFI"""

        update_status_com_erro = "com erro"

        reserva_pi = reserva_principal
        reserva_siafi = reserva_secundaria

        col_1 = "PTRES"
        col_2 = "ELEMENTO - ITEM"
        col_3 = "RESERVA PI"
        col_4 = "RESERVA SIAFI"
        col_5 = "DIF.: PI - SIAFI"
        response = f"|{col_1:^7}|{col_2:^25}|{col_3:^15}|{col_4:^15}|{col_5:^17}|\n"
        response += f"|{'':-^7}|{'':-^25}|{'':-^15}|{'':-^15}|{'':-^17}|\n"
        
        dict_acoes_reserva_pi = reserva_pi
        dict_ptres_reserva_siafi = reserva_siafi

        for codigo_acao_reserva_pi, dados_acao_reserva_pi in dict_acoes_reserva_pi.items():

            for codigo_po_reserva_pi, dados_po_reserva_pi in dados_acao_reserva_pi['POs'].items():

                for codigo_ptres_reserva_pi, dados_ptres_reserva_pi in dados_po_reserva_pi['PTRES'].items():

                    if codigo_ptres_reserva_pi in dict_ptres_reserva_siafi:

                        if dados_ptres_reserva_pi['valor'] != dict_ptres_reserva_siafi[codigo_ptres_reserva_pi]['valor']:
                            self.update_status(update_status_com_erro)
                            diferenca_valor = dados_ptres_reserva_pi['valor'] - dict_ptres_reserva_siafi[codigo_ptres_reserva_pi]['valor']
                            response += f"|{codigo_ptres_reserva_pi:^7}|{'':^25}|" + self.utils.replace_commas_and_dots(
                                f"{dados_ptres_reserva_pi['valor']:^15,.2f}|{dict_ptres_reserva_siafi[codigo_ptres_reserva_pi]['valor']:^15,.2f}|{diferenca_valor:^17,.2f}|\n"
                            )

                        for codigo_natureza_reserva_pi, dados_natureza_reserva_pi in dados_ptres_reserva_pi['naturezas'].items():
                            codigo_natureza_reserva_pi_formatado = codigo_natureza_reserva_pi.replace('.', '')[:6]

                            if codigo_natureza_reserva_pi_formatado in dict_ptres_reserva_siafi[codigo_ptres_reserva_pi]['naturezas']:

                                if dados_natureza_reserva_pi['valor'] != dict_ptres_reserva_siafi[codigo_ptres_reserva_pi]['naturezas'][codigo_natureza_reserva_pi_formatado]['valor']:
                                    self.update_status(update_status_com_erro)
                                    diferenca_valor_natureza = dados_natureza_reserva_pi['valor'] - dict_ptres_reserva_siafi[codigo_ptres_reserva_pi]['naturezas'][codigo_natureza_reserva_pi_formatado]['valor']
                                    response += f"|{codigo_ptres_reserva_pi:^7}|{codigo_natureza_reserva_pi:^25}|" + self.utils.replace_commas_and_dots(
                                        f"{dados_natureza_reserva_pi['valor']:^15,.2f}|{dict_ptres_reserva_siafi[codigo_ptres_reserva_pi]['naturezas'][codigo_natureza_reserva_pi_formatado]['valor']:^15,.2f}|{diferenca_valor_natureza:^17,.2f}|\n"
                                    )

                            else:
                                response += f"|{codigo_ptres_reserva_pi:^7}|{codigo_natureza_reserva_pi:^25}|" + self.utils.replace_commas_and_dots(
                                    f"{dados_natureza_reserva_pi['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                                )
                                if not dados_natureza_reserva_pi['valor']:
                                    self.update_status(update_status_com_erro)
            
                    else:
                        response += f"|{codigo_ptres_reserva_pi:^7}|{'':^25}|" + self.utils.replace_commas_and_dots(
                            f"{dados_ptres_reserva_pi['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                        )
                        if not dados_ptres_reserva_pi['valor']:
                            self.update_status(update_status_com_erro)
                            
        data: ResponseData = {"response": response, "status": self.get_status()}
        
        return data
