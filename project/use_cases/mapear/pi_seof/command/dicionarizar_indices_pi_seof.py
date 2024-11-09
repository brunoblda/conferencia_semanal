import re
from project.domain.interfaces.mapear.command.dicionarizar_indices import DicionarizarIndices as DicionarizarIndicesInterface
from project.use_cases.interfaces.utilities.utils import Utils as UtilsInterface
import pandas as pd

class DicionarizarIndicesPiSeof(DicionarizarIndicesInterface):
    """ Dicionaria os indices do PI Seof """
    
    def __init__ (self, utils: UtilsInterface):
        self.utils = utils
        
    def execute(self, dict_indices: dict, plano_interno: pd.DataFrame) -> dict:
        """ Executa a diciornarização dos indices do PI Seof """

        pattern_desdobramento_elemento_despesa_seof = r'^\d{2}.\d{2}.\d{2}' 

        dict_resultado_plano_interno_seof = {}

        for w in dict_indices:
            # ic.ic(plano_interno[2][w])
            # ic.ic(dict_indices[w])
            # ic.ic(plano_interno[1][w])

            nome_plano_interno_seof = plano_interno[1][w].split(' ',1)[0]
    
            dotacao_plano_interno_seof = self.utils.value_hygienization(plano_interno[2][w])
    
            dict_resultado_plano_interno_seof[nome_plano_interno_seof] = {'indice': w, 'valor': dotacao_plano_interno_seof, 'elementos de despesa': {}}

            # para cada item da lista de value de cada chave de plano interno
            for z in dict_indices[w]:

                # para cada chave de elemento de despesa
                for y in z:
                    # ic.ic(plano_interno[2][y])
                    # ic.ic(plano_interno[1][y])
            
                    nome_elemento_despesa_seof = plano_interno[1][y].split(' ',1)[0]
                    nome_elemento_despesa_seof = nome_elemento_despesa_seof[:1]+"."+nome_elemento_despesa_seof[1:2]+"."+nome_elemento_despesa_seof[2:4]+"."+nome_elemento_despesa_seof[4:]

                    dotacao_elemento_despesa_seof = self.utils.value_hygienization(plano_interno[2][y])

                    dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof] = {'indice': y, 'valor': dotacao_elemento_despesa_seof, 'desdobramentos de despesa': {}}

                    # para cada item da lista de value da chave de elemento de despesa
                    for x in z[y]:
                        # ic.ic(plano_interno[2][x])
                        # ic.ic(plano_interno[1][x])
                
                        nome_desdobramento_despesa_seof = re.search(pattern_desdobramento_elemento_despesa_seof, plano_interno[1][x])[0]

                
                        dotacao_desdobramento_despesa_seof = self.utils.value_hygienization(plano_interno[2][x])

                        # versão anterior
                        # dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa'][nome_desdobramento_despesa_seof] = {'indices': [x], 'valor': dotacao_desdobramento_despesa_seof}

                        if nome_desdobramento_despesa_seof not in dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa']:
                            dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa'][nome_desdobramento_despesa_seof] = {'indices': [x], 'valor': dotacao_desdobramento_despesa_seof}
                        else:
                            dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa'][nome_desdobramento_despesa_seof]['indices'].append(x)
                            dict_resultado_plano_interno_seof[nome_plano_interno_seof]['elementos de despesa'][nome_elemento_despesa_seof]['desdobramentos de despesa'][nome_desdobramento_despesa_seof]['valor']+=dotacao_desdobramento_despesa_seof

        return dict_resultado_plano_interno_seof
