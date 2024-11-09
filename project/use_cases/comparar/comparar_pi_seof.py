""" Module to compare PI with SEOF """
from project.domain.interfaces.comparar.comparar_pis import CompararPis as CompararPisInterface
import pandas as pd

class CompararPiSeof(CompararPisInterface):
    """ Compare PIs """

    def execute(self, pi_principal: pd.DataFrame, pi_secundario: pd.DataFrame) -> str:
        """ Execute the comparison of the PI with the PI Seof """

        pi = pi_principal 
        pi_seof = pi_secundario

        col_1 = "PLANO INTERNO"
        col_2 = "ELEMENTO - ITEM"
        col_3 = "VALOR PI"
        col_4 = "VALOR SEOF"
        col_5 = "DIF.: PI - SEOF"
        response = f"|{col_1:^15}|{col_2:^17}|{col_3:^15}|{col_4:^15}|{col_5:^17}|\n"
        response += f"|{'':-^15}|{'':-^17}|{'':-^15}|{'':-^15}|{'':-^17}|\n"

        for n in pi:

            # se o plano interno estiver no dicionario de planos internos do seof
            if n in pi_seof:
                if pi[n]['valor'] != pi_seof[n]['valor']:
                    response += (
                        f"|{n:^15}|{'':^17}|{pi[n]['valor']:^15,.2f}|{pi_seof[n]['valor']:^15,.2f}|{pi[n]['valor'] - pi_seof[n]['valor']:^17,.2f}|\n"
                    )

                # para cada elemento de despesa no dicionario de elementos de despesa do plano interno
                for m in pi[n]['elementos de despesa']:

                    # se o elemento de despesa estiver no dicionario de elementos de despesa do plano interno do seof
                    if m in pi_seof[n]['elementos de despesa']:
                        if pi[n]['elementos de despesa'][m]['valor'] != pi_seof[n]['elementos de despesa'][m]['valor']:
                            response += (
                                f"|{n:^15}|{m:^17}|{pi[n]['elementos de despesa'][m]['valor']:^15,.2f}|{pi_seof[n]['elementos de despesa'][m]['valor']:^15,.2f}|{pi[n]['elementos de despesa'][m]['valor'] - pi_seof[n]['elementos de despesa'][m]['valor']:^17,.2f}|\n"
                            )
                
                        # para cada desdobramento de despesa no dicionario de desdobramentos de despesa do elemento de despesa
                        for o in pi[n]['elementos de despesa'][m]['desdobramentos de despesa']:

                            # se o desdobramento de despesa estiver no dicionario de desdobramentos de despesa do elemento de despesa do plano interno do seof
                            if o in pi_seof[n]['elementos de despesa'][m]['desdobramentos de despesa']:
                                if pi[n]['elementos de despesa'][m]['desdobramentos de despesa'][o]['valor'] != pi_seof[n]['elementos de despesa'][m]['desdobramentos de despesa'][o]['valor']:
                                    response += (
                                        f"|{n: ^15}|{m+o[2:]:^17}|{pi[n]['elementos de despesa'][m]['desdobramentos de despesa'][o]['valor']:^15,.2f}|{pi_seof[n]['elementos de despesa'][m]['desdobramentos de despesa'][o]['valor']:^15,.2f}|{pi[n]['elementos de despesa'][m]['desdobramentos de despesa'][o]['valor'] - pi_seof[n]['elementos de despesa'][m]['desdobramentos de despesa'][o]['valor']:^17,.2f}|\n"
                                    )
                    
                            # se o desdobramento de despesa não estiver no dicionario de desdobramentos de despesa do elemento de despesa do plano interno        
                            else:
                                response += (
                                    f"|{n:^15}|{m+o[2:]:^17}|{pi[n]['elementos de despesa'][m]['desdobramentos de despesa'][o]['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                                )

                    # se o elemento de despesa não estiver no dicionario de elementos de despesa do plano interno do seof            
                    else:
                        response += (
                            f"|{n:^15}|{m:^17}|{pi[n]['elementos de despesa'][m]['valor']:^15,.2f}|{'':^15}|{'Não encontrado':^17}|\n"
                        )
            # se o plano interno não estiver no dicionario de planos internos do seof            
            else:
                response += (f"|{n:^15}|{'':^17}|{pi[n]['valor']:^15}|{'':^15}|{'Não encontrado':^17}|\n")

        return response