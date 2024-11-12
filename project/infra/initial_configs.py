import tabula
import os
import sys
import re
from dotenv import load_dotenv

class InitialConfigs:

    def __init__(self) -> None:
        self.project_root = self.__get_project_root()

    def __get_project_root(self) -> str:
        """ Returns project root folder """
        root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if getattr( sys , 'frozen' , False):    # keyword 'frozen' is for setting basedir while in onefile mode in pyinstaller
            root_folder = sys._MEIPASS
        return root_folder 

    def __tabula_configuracao_inicial(self) -> None:
        ''' Set tabula configuration ''' 
        tabula.environment_info.TABULA_JAR = os.path.join(self.project_root,'tabula', 'tabula-1.0.5-jar-with-dependencies.jar')

    def __carregar_variaveis_de_ambiente(self) -> None:
        ''' Load environment variables '''
        extDataDir = os.getcwd()
        if getattr(sys, 'frozen', False):
            extDataDir = sys._MEIPASS
        load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))
    
    def __carregar_certificados_digitais(self) -> None:
        ''' Load digital certificates '''
        basedir = os.getcwd()
        if getattr( sys , 'frozen' , False):    # keyword 'frozen' is for setting basedir while in onefile mode in pyinstaller
            basedir = sys._MEIPASS
        os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(basedir, 'certificados.pem')

    def __carregar_java_home(self) -> None:
        ''' Load JAVA_HOME environment variable '''
        java_base_path = "C:\\Program Files\\Java"
        jre_pattern = re.compile(r'jre.*')
        try:
            jre_dirs = [d for d in os.listdir(java_base_path) if jre_pattern.match(d)]
            if jre_dirs:
                jre_path = os.path.join(java_base_path, jre_dirs[0], 'bin')
                os.environ['PATH'] = jre_path
        except FileNotFoundError:
            pass

    def execute(self) -> None:
        self.__carregar_java_home()
        self.__tabula_configuracao_inicial()
        self.__carregar_variaveis_de_ambiente()
        self.__carregar_certificados_digitais()
