import os
import re
import sys

import tabula
from dotenv import load_dotenv


class InitialConfigs:

    def __init__(self) -> None:
        self.project_root = self.__get_project_root()

    def __get_project_root(self) -> str:
        """Returns project root folder"""
        root_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        if getattr(
            sys, "frozen", False
        ):  # keyword 'frozen' is for setting basedir while in onefile mode in pyinstaller
            root_folder = sys._MEIPASS
        return root_folder

    def __tabula_configuracao_inicial(self) -> None:
        """Set tabula configuration"""
        tabula.environment_info.TABULA_JAR = os.path.join(
            self.project_root, "tabula", "tabula-1.0.5-jar-with-dependencies.jar"
        )

    def __carregar_variaveis_de_ambiente(self) -> None:
        """Load environment variables"""
        extDataDir = os.getcwd()
        if getattr(sys, "frozen", False):
            extDataDir = sys._MEIPASS
        load_dotenv(dotenv_path=os.path.join(extDataDir, ".env"))

    def __carregar_certificados_digitais(self) -> None:
        """Load digital certificates"""
        basedir = os.getcwd()
        if getattr(
            sys, "frozen", False
        ):  # keyword 'frozen' is for setting basedir while in onefile mode in pyinstaller
            basedir = sys._MEIPASS
        os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(basedir, "certificados.pem")

    def __carregar_java_home(self) -> None:
        """Load JAVA_HOME environment variable"""
        java_base_paths = ["C:\\Program Files\\Java", "C:\\Program Files (x86)\\Java"]
        jre_pattern = re.compile(r"jre.*")
        jdk_pattern = re.compile(r"jdk.*")

        def find_java_path(base_path, pattern):
            try:
                dirs = [d for d in os.listdir(base_path) if pattern.match(d)]
                if dirs:
                    return os.path.join(base_path, dirs[0])
            except FileNotFoundError:
                return None
            return None

        java_path = None
        for base_path in java_base_paths:
            java_path = find_java_path(base_path, jre_pattern)
            if java_path:
                break
            java_path = find_java_path(base_path, jdk_pattern)
            if java_path:
                break

        if java_path:
            os.environ["JAVA_HOME"] = java_path
            os.environ["PATH"] = os.path.join(java_path, "bin")

    def __carregar_local_java_home(self) -> None:
        """Load JAVA_HOME environment variable"""
        extDataDir = os.getcwd()
        if getattr(sys, "frozen", False):
            extDataDir = sys._MEIPASS
        java_local_path = os.path.join(extDataDir, "jre1.8.0_421", "bin")
        os.environ["PATH"] = java_local_path
        java_home_path = os.path.join(extDataDir, "jre1.8.0_421")
        os.environ["JAVA_HOME"] = java_home_path

    def execute(self) -> None:
        self.__carregar_local_java_home()
        # self.__carregar_java_home()
        self.__tabula_configuracao_inicial()
        self.__carregar_variaveis_de_ambiente()
        self.__carregar_certificados_digitais()
