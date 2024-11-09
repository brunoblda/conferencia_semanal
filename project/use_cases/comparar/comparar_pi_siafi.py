""" Module to compare PIs """
from project.domain.interfaces.comparar.comparar_pis import CompararPis as CompararPisInterface
import pandas as pd

class CompararPiSiafi(CompararPisInterface):
    """ Compare PIs """

    def execute(self, pi_principal: pd.DataFrame, pi_secundário: pd.DataFrame) -> str:
        """ Execute the comparison of the PI with the PI Siafi """

        pi = pi_principal
        pi_siafi = pi_secundário

        col_1 = "PLANO INTERNO"
        col_2 = "ELEMENTO - ITEM"
        col_3 = "VALOR PI"
        col_4 = "VALOR SIAFI"
        col_5 = "DIF.: PI - SIAFI"
        response = f"|{col_1:^15}|{col_2:^17}|{col_3:^15}|{col_4:^15}|{col_5:^17}|\n"
        response += f"|{'':-^15}|{'':-^17}|{'':-^15}|{'':-^15}|{'':-^17}|\n"
        
        # para cada plano interno no dicionario de planos internos
        for n in pi:
    
            # se o plano interno estiver no dicionario de planos internos do siafi
            if n in pi_siafi:
                if pi[n]['valor'] != pi_siafi[n]['valor']:
                    response += (f"|{n:^15}|{'':^17}|{pi[n]['valor']:^15,.2f}|{pi_siafi[n]['valor']:^15,.2f}|{pi[n]['valor'] - pi_siafi[n]['valor']:^17,.2f}|\n")

                # para cada elemento de despesa no dicionario de elementos de despesa do plano interno
                for m in pi[n]['elementos de despesa']:

                    # se o elemento de despesa estiver no dicionario de elementos de despesa do plano interno do siafi
                    if m in pi_siafi[n]['elementos de despesa']:
                        if pi[n]['elementos de despesa'][m]['valor'] != pi_siafi[n]['elementos de despesa'][m]['valor']:
                            response += (f"|{n:^15}|{m:^17}|{pi[n]['elementos de despesa'][m]['valor']:^15,.2f}|{pi_siafi[n]['elementos de despesa'][m]['valor']:^15,.2f}|{pi[n]['elementos de despesa'][m]['valor'] - pi_siafi[n]['elementos de despesa'][m]['valor']:^17,.2f}|\n")

                    # se o elemento de despesa não estiver no dicionario de elementos de despesa do plano interno do siafi
                    else:
                        response += (f"|{n:^15}|{m:^17}|{pi[n]['elementos de despesa'][m]['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n")

            # se o plano interno não estiver no dicionario de planos internos do siafi
            else:
                response += (f"|{n:^15}|{'':^17}|{pi[n]['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n")
        
        return response

 