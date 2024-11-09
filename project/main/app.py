from project.main.composer.comparar_pi_siafi_composer import comparar_pi_siafi_composer
from project.main.composer.comparar_pi_seof_composer import comparar_pi_seof_composer
from project.infra.criar_pastas import CriarPastas

class App:

    def __criar_pastas(self):
        criar_pastas = CriarPastas()
        criar_pastas.execute()

    def __comparar_pi_seof(self, input_file_path_principal, data_da_conferencia):
        print(f'Comparar PI com SEOF')
        input_file_path_secundario = input(f'Digite o caminho do arquivo do SEOF: ')
        comparacao_pi_seof = comparar_pi_seof_composer(input_file_path_principal, input_file_path_secundario, data_da_conferencia)
        print()
        print(comparacao_pi_seof)
        print()

    def __comparar_pi_siafi(self, input_file_path_principal, data_da_conferencia):
        print(f'Comparar PI com SIAFI')
        input_file_path_secundario = input(f'Digite o caminho do arquivo do SIAFI: ')
        comparacao_pi_siafi = comparar_pi_siafi_composer(input_file_path_principal, input_file_path_secundario, data_da_conferencia)
        print()
        print(comparacao_pi_siafi)
        print()

    def run(self):
        print('Bem vindo ao comparador de PIs')
        print('Escolha uma das opções abaixo:')
        print('1 - Comparar PI com SEOF e Comparar PI com SIAFI')
        print('2 - Sair')
        option = input('Digite a opção desejada: ')
        if option == '1':
            data_da_conferencia = input('Digite a data da conferência: ')
            input_file_path_principal = input(f'Digite o caminho do arquivo do Plano Interno: ')
            self.__criar_pastas()
            self.__comparar_pi_seof(input_file_path_principal, data_da_conferencia)
            print()
            print()
            self.__comparar_pi_siafi(input_file_path_principal, data_da_conferencia)
        elif option == '2':
            print('Até a próxima!')
        else:
            print('Opção inválida')
            self.run()

