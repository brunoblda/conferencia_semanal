import logging
import sys
from project.main.adapters.comparar_pi_request_adapter import comparar_pi_request_adapter 
from project.main.composer.comparar_pi_siafi_composer import comparar_pi_siafi_composer
from project.main.composer.comparar_pi_seof_composer import comparar_pi_seof_composer
from project.infra.criar_pastas import CriarPastas
from project.infra.initial_configs import InitialConfigs
from project.errors.error_handler import handle_error
from project.validators.conferencia_data_validator import conferencia_data_validator

class App:

    def __init__(self):
        self.__setup_logger()
        sys.excepthook = self.__handle_exception

    def __setup_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        # Criar um manipulador de arquivo
        fh = logging.FileHandler('error_log.txt')
        fh.setLevel(logging.ERROR)
        
        # Criar um formatador e adicioná-lo ao manipulador
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        # Adicionar o manipulador ao logger
        logger.addHandler(fh)

    def __handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger().error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    def __criar_pastas(self):
        criar_pastas = CriarPastas()
        criar_pastas.execute()

    def __inicializar_configs(self):
        initial_configs = InitialConfigs()
        initial_configs.execute()

    def __comparar_pi_seof(self, input_file_path_principal, data_da_conferencia):
        print(f'Comparar PI com SEOF')
        print()
        input_file_path_secundario = input(f'Digite o caminho do arquivo do SEOF: ')
        print()
        try:
            conferencia_data_validator(data_da_conferencia)
            request_adapted = comparar_pi_request_adapter(input_file_path_principal, input_file_path_secundario, data_da_conferencia)
            comparacao_pi_seof = comparar_pi_seof_composer(request_adapted)
        except Exception as e:
            comparacao_pi_seof = handle_error(e)
        print()
        print(comparacao_pi_seof.message)
        print(comparacao_pi_seof.body)
        print()

    def __comparar_pi_siafi(self, input_file_path_principal, data_da_conferencia):
        print(f'Comparar PI com SIAFI')
        print()
        input_file_path_secundario = input(f'Digite o caminho do arquivo do SIAFI: ')
        print()
        try:
            conferencia_data_validator(data_da_conferencia)
            request_adapted = comparar_pi_request_adapter(input_file_path_principal, input_file_path_secundario, data_da_conferencia)
            comparacao_pi_siafi = comparar_pi_siafi_composer(request_adapted)
        except Exception as e:
            comparacao_pi_siafi = handle_error(e)
        print()
        print(comparacao_pi_siafi.message)
        print(comparacao_pi_siafi.body)
        print()

    def run(self):
        self.__inicializar_configs()
        print('Bem vindo ao comparador de PIs')
        print()
        print('Escolha uma das opções abaixo:')
        print('1 - Comparar PI com SEOF')
        print('2 - Comparar PI com SIAFI')
        print('3 - Sair')
        print()
        option = input('Digite a opção desejada: ')
        if option == '1':
            print()
            data_da_conferencia = input('Digite a data da conferência: ')
            print()
            input_file_path_principal = input(f'Digite o caminho do arquivo do Plano Interno: ')
            print()
            self.__criar_pastas()
            self.__comparar_pi_seof(input_file_path_principal, data_da_conferencia)
            print()
            self.run()

        elif option == '2':
            print()
            data_da_conferencia = input('Digite a data da conferência: ')
            print()
            input_file_path_principal = input(f'Digite o caminho do arquivo do Plano Interno: ')
            print()
            self.__criar_pastas()
            self.__comparar_pi_siafi(input_file_path_principal, data_da_conferencia)
            print()
            self.run()

        elif option == '3':
            print('Até a próxima!')
        else:
            print('Opção inválida')
            self.run()
