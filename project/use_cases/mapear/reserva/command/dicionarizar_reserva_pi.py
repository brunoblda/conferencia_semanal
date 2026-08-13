import re

import pandas as pd

from project.use_cases.mapear.reserva.command.dicionarizar_reserva import (
    DicionarizarReserva as dicionarizarReservaInterface,
)
from project.services.utilities.utils import Utils

class DicionarizarReservaPi(dicionarizarReservaInterface):
    """Dicionariza a reserva do PI"""

    def __init__(self, utils: Utils):
        self.utils = utils

    def execute(self, pi_reserva_list: list) -> dict:
        """execute the dicionarizar reserva """

        pi_reserva_df = pd.concat(pi_reserva_list, ignore_index=True)

        columns_names_pi_reserva_list = pi_reserva_df.columns.to_list() 

        # cache: guarda o primeiro valor numérico de cada linha
        primeiro_valor_numerico_por_linha = {}

        # pattern para encontrar as ações 03.062.0031.4261.0053
        pattern_codigo_acao_reserva= r'(^\d{2}\.\d{3}\.\d{4}\.[A-Z0-9]{4}\.\d{4})'

        # pattern para encontrar os POs da reserva
        pattern_PO_reserva = r'(^PO [A-Z0-9]{4})'

        # pattern para encontrar os PTRES da reserva
        pattern_PTREs_reserva = r' - (\d{6}$)'

        # pattern nan
        pattern_nan = r'^nan'

        # pattern -
        pattern_traco = r'^-'

        pattern_natureza = r'(3\.1\.\d{2}\.\d{2}\.\d{2}$|3\.3\.\d{2}\.\d{2}\.\d{2}$|4\.\d{1}\.\d{2}\.\d{2}\.\d{2}$)'

        pattern_cabecalho_reserva = r'^(ATIVIDADE\/PROJETO\/ PLANO INTERNO Natureza|ATIVIDADE\/PROJETO\/ PLANO INTERNO|Natureza|da|Despesa|nan|Interno|Plano)$'

        def get_primeiro_valor_numerico(i):
            if i in primeiro_valor_numerico_por_linha:
                return primeiro_valor_numerico_por_linha[i]

            valor = 0
            for col_scan in range(len(columns_names_pi_reserva_list)):
                cel = pi_reserva_df.iloc[i, col_scan]
                if self.utils.is_numero(cel):
                    valor = self.utils.value_hygienization(cel)
                    break

            primeiro_valor_numerico_por_linha[i] = valor
            return valor

        def get_nome_po_acao_com_po(i,j):
            nome = str(pi_reserva_df.iloc[i, j])
            nome = nome[10:]
            if re.search(pattern_PTREs_reserva, nome):
                nome = re.sub(pattern_PTREs_reserva, '', nome)
    
            else:
                nome += ' ' + str(pi_reserva_df.iloc[i+1, j])
                nome = re.sub(pattern_PTREs_reserva, '', nome)
    
            return nome

        dict_acoes_reserva_pi = {}

        acao_atual = None
        po_atual = None
        ptres_atual = None
        natureza_atual = None
        item_atual = None

        for i in range(len(pi_reserva_df)):
            for j in range(len(columns_names_pi_reserva_list)):

                celula = str(pi_reserva_df.iloc[i, j])

                match_acao = re.search(pattern_codigo_acao_reserva, celula) 

                if match_acao:
                    acao_atual = match_acao.group()
                    dict_acoes_reserva_pi[acao_atual] = {'posicao':(i,j), 'POs': {}}
                    po_atual = None
                    ptres_atual = None
                    natureza_atual = None
                    item_atual = None
                    for col_scan in range(len(columns_names_pi_reserva_list)):
                        if self.utils.is_numero(pi_reserva_df.iloc[i+1, col_scan]):
                            dict_acoes_reserva_pi[acao_atual]['valor'] = get_primeiro_valor_numerico(i+1)
                            break
        
                if acao_atual in dict_acoes_reserva_pi:

                    match_po = re.search(pattern_PO_reserva, celula) 

                    if match_po:
                        po_atual = match_po.group()
                        dict_acoes_reserva_pi[acao_atual]['POs'][po_atual] = {'posicao':(i,j), 'PTRES': {}}
                        dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['nome'] = get_nome_po_acao_com_po(i,j)
                        for col_scan in range(len(columns_names_pi_reserva_list)):
                            if self.utils.is_numero(pi_reserva_df.iloc[i, col_scan]):
                                dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['valor'] = get_primeiro_valor_numerico(i)
                                break
            
                    match_ptres = re.search(pattern_PTREs_reserva, celula) 

                    if match_ptres:

                        if not po_atual:
                            valor_po = None
                            for col_scan in range(len(columns_names_pi_reserva_list)):
                                linha_da_acao = dict_acoes_reserva_pi[acao_atual]['posicao'][0]
                                if self.utils.is_numero(pi_reserva_df.iloc[linha_da_acao+1, col_scan]):
                                    valor_po = get_primeiro_valor_numerico(linha_da_acao+1)
                                    break

                            po_atual = 'PO 0000'
                            dict_acoes_reserva_pi[acao_atual]['POs'][po_atual] = {'posicao':(i,j), 'PTRES': {}}
                            if valor_po:
                                dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['valor'] = valor_po
                            dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['nome'] = pi_reserva_df.iloc[i+1, j]


                        ptres_atual = match_ptres.group(1)
                        dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['PTRES'][ptres_atual] = {'posicao':(i,j), 'valor': dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['valor'], 'naturezas': {}}
                        natureza_atual = None
                        item_atual = None
                
                    if po_atual in dict_acoes_reserva_pi[acao_atual]['POs'] and ptres_atual in dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['PTRES']:
                
                        match_natureza = re.search(pattern_natureza, celula)

                        if match_natureza:
                            natureza_atual = match_natureza.group()
                            dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['PTRES'][ptres_atual]['naturezas'][natureza_atual] = {'posicao':(i,j), 'itens':[]}

                            item_atual = None
                
                            for col_scan in range(len(columns_names_pi_reserva_list)):
                                if self.utils.is_numero(pi_reserva_df.iloc[i, col_scan]):
                                    dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['PTRES'][ptres_atual]['naturezas'][natureza_atual]['valor'] = get_primeiro_valor_numerico(i)
                                    break
                    
                            continue
                
                        if natureza_atual in dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['PTRES'][ptres_atual]['naturezas']:

                            match_nan = re.search(pattern_nan, celula)
                            match_traco = re.search(pattern_traco, celula)
                            match_cabecalho = re.search(pattern_cabecalho_reserva, celula)

                            if not match_nan and not match_traco and not match_cabecalho and not self.utils.is_numero(celula): 
                                item_atual = celula
                                dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['PTRES'][ptres_atual]['naturezas'][natureza_atual]['itens'].append({'item': item_atual, 'posicao':(i,j)})
                                for col_scan in range(len(columns_names_pi_reserva_list)):
                                    if self.utils.is_numero(pi_reserva_df.iloc[i, col_scan]):
                                        dict_acoes_reserva_pi[acao_atual]['POs'][po_atual]['PTRES'][ptres_atual]['naturezas'][natureza_atual]['itens'][-1]['valor'] = get_primeiro_valor_numerico(i)
                                        break
                    
        return dict_acoes_reserva_pi
