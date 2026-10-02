""" Module to compare reserva PI with reserva SEOF """

import pandas as pd

from rapidfuzz import fuzz

from project.domain.interfaces.comparar.comparar_reservas import (
    CompararReservas as CompararReservasInterface,
)
from project.services.types.response_data_comparar_reservas import ResponseData
from project.services.utilities.utils import Utils

class CompararReservaPiSeof(CompararReservasInterface):
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
        """Execute the comparison of the reserva PI with the reserva SEOF"""

        update_status_com_erro = "com erro"

        reserva_pi = reserva_principal
        reserva_seof = reserva_secundaria

        col_1 = "PTRES"
        col_2 = "ELEMENTO - ITEM"
        col_3 = "RESERVA PI"
        col_4 = "RESERVA SEOF"
        col_5 = "DIF.: PI - SEOF"
        response = f"|{col_1:^7}|{col_2:^25}|{col_3:^15}|{col_4:^15}|{col_5:^17}|\n"
        response += f"|{'':-^7}|{'':-^25}|{'':-^15}|{'':-^15}|{'':-^17}|\n"

        def calcular_similaridade(nome_pi, list_nomes_seof):
    
            best_nome_seof = None
            best_score = 50
    
            for nome_seof in list_nomes_seof:
                score = fuzz.ratio(nome_pi, nome_seof)
                if score > best_score:
                    best_score = score
                    best_nome_seof = nome_seof

            return best_nome_seof
    
        list_po_seof_reserva = list(reserva_seof.keys())

        for codigo_acao_pi, dados_acao_pi in reserva_pi.items():
            for codigo_po_pi, dados_po_pi in dados_acao_pi['POs'].items():
                nome_po_pi = dados_po_pi['nome']

                best_nome_po_seof = calcular_similaridade(nome_po_pi, list_po_seof_reserva)
        
                if best_nome_po_seof in reserva_seof:
                    if dados_po_pi['valor'] != reserva_seof[best_nome_po_seof]['valor']:
                        self.update_status(update_status_com_erro)
                        PTRES = list(dados_po_pi['PTRES'].keys())[0]  # Pega o primeiro PTRES da reserva PI
                        diferenca_valor = dados_po_pi['valor'] - reserva_seof[best_nome_po_seof]['valor']
                        response += f"|{PTRES:^7}|{'':^25}|" + self.utils.replace_commas_and_dots(
                            f"{dados_po_pi['valor']:^15,.2f}|{reserva_seof[best_nome_po_seof]['valor']:^15,.2f}|{diferenca_valor:^17,.2f}|\n"
                        )

                    for codigo_ptres, dados_ptres_pi in dados_po_pi['PTRES'].items():
                        for codigo_natureza_pi, dados_natureza_pi in dados_ptres_pi['naturezas'].items():
                    
                            if codigo_natureza_pi[:3] in reserva_seof[best_nome_po_seof]:
                                list_itens_reserva_pi = dados_natureza_pi['itens']

                                if dados_natureza_pi["valor"] != reserva_seof[best_nome_po_seof][codigo_natureza_pi[:3]]["valor"]:
                                    self.update_status(update_status_com_erro)
                                    diferenca_valor_natureza = dados_natureza_pi["valor"] - reserva_seof[best_nome_po_seof][codigo_natureza_pi[:3]]["valor"]
                                    response += f"|{codigo_ptres:^7}|{codigo_natureza_pi:^25}|" + self.utils.replace_commas_and_dots(
                                        f"{dados_natureza_pi['valor']:^15,.2f}|{reserva_seof[best_nome_po_seof][codigo_natureza_pi[:3]]['valor']:^15,.2f}|{diferenca_valor_natureza:^17,.2f}|\n"
                                    )
                        
                                for item in list_itens_reserva_pi:
                                    item_nome_reserva_pi = item['item']
                                    item_valor_reserva_pi = item['valor']

                                    # Encontrar o melhor item correspondente no SEOF
                            
                                    if item_valor_reserva_pi != 0:

                                        list_nome_itens_reserva_seof = [seof_item['item'] for seof_item in reserva_seof[best_nome_po_seof][codigo_natureza_pi[:3]]['itens']]
                            
                                        best_item_seof = calcular_similaridade(item_nome_reserva_pi, list_nome_itens_reserva_seof)

                                        if best_item_seof in [seof_item['item'] for seof_item in reserva_seof[best_nome_po_seof][codigo_natureza_pi[:3]]['itens']]:
                                            seof_item_valor = next(
                                                seof_item['valor']
                                                for seof_item in reserva_seof[best_nome_po_seof][codigo_natureza_pi[:3]]['itens']
                                                if seof_item['item'] == best_item_seof
                                            )

                                            if item_valor_reserva_pi != seof_item_valor:
                                                self.update_status(update_status_com_erro)
                                                diferenca_valor_item = item_valor_reserva_pi - seof_item_valor
                                                response += f"|{codigo_ptres:^7}|{item_nome_reserva_pi[:25]:^25}|" + self.utils.replace_commas_and_dots(
                                                    f"{item_valor_reserva_pi:^15,.2f}|{seof_item_valor:^15,.2f}|{diferenca_valor_item:^17,.2f}|\n"
                                                )

                                        else:
                                            response += f"|{codigo_ptres:^7}|{item_nome_reserva_pi[:25]:^25}|" + self.utils.replace_commas_and_dots(
                                                f"{item_valor_reserva_pi:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                                            )
                                            if not item_valor_reserva_pi:
                                                self.update_status(update_status_com_erro)
                                    
                            else:
                                response += f"|{codigo_ptres:^7}|{codigo_natureza_pi:^25}|" + self.utils.replace_commas_and_dots(
                                    f"{dados_natureza_pi['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                                )
                                if not dados_natureza_pi['valor']:
                                    self.update_status(update_status_com_erro)
                        
                else:
                    PTRES = list(dados_po_pi['PTRES'].keys())[0]  # Pega o primeiro PTRES da reserva PI
                    response += f"|{PTRES:^7}|{'':^25}|" + self.utils.replace_commas_and_dots(
                        f"{dados_po_pi['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                    )
                    if not dados_po_pi['valor']:
                        self.update_status(update_status_com_erro)

        data: ResponseData = {"response": response, "status": self.get_status()}
        
        return data
