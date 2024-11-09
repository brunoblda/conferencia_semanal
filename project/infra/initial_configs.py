import tabula
import os
import sys
from dotenv import load_dotenv

class InitialConfigs:

    def __tabula_configuracao_inicial(self) -> None:
        ''' Set tabula configuration ''' 

        tabula.environment_info.TABULA_JAR = os.path.join(os.path.dirname(__file__), 'tabula', 'tabula-1.0.5-jar-with-dependencies.jar')

    def __carregar_variaveis_de_ambiente(self) -> None:
        ''' Load environment variables '''
        extDataDir = os.getcwd()
        if getattr(sys, 'frozen', False):
            extDataDir = sys._MEIPASS
        load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

    def execute(self) -> None:
        self.__tabula_configuracao_inicial()
        self.__carregar_variaveis_de_ambiente()
        
