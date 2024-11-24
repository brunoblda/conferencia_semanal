from project.main.adapters.comparar_pi_request_adapter import comparar_pi_request_adapter
from project.main.composer.comparar_pi_siafi_composer import comparar_pi_siafi_composer
from project.main.composer.comparar_pi_seof_composer import comparar_pi_seof_composer
from project.errors.error_handler import handle_error
from project.validators.conferencia_data_validator import conferencia_data_validator
import threading
import logging
from project.infra.criar_pastas import CriarPastas
from project.infra.initial_configs import InitialConfigs
import os
import signal

class ControllerApp:

    def __init__(self):
        self._stop_event = threading.Event()
        self.threads = []

    def __run_in_thread(self, target, callback, *args):
        """ Executa uma função em um thread e captura exceções."""
        thread = threading.Thread(target=self.__thread_wrapper, args=(target, callback, *args))
        thread.start()
        self.threads.append(thread)
        
    def __thread_wrapper(self, target, callback, *args):
        """Wrapper para executar a função alvo e capturar exceções."""
        result = None
        try:
            if not self._stop_event.is_set():
                data_da_conferencia = args[-1]
                conferencia_data_validator(data_da_conferencia)
                result = target(*args)
        except Exception as e:
            logging.getLogger().error("Exception in thread", exc_info=True)
            result = handle_error(e)
        finally:
            if callback:
                callback(result)

    def __comparar_pi_seof(self, input_file_path_principal, input_file_path_secundario, data_da_conferencia):
        """Compara PI com SEOF."""
        request_adapted = comparar_pi_request_adapter(input_file_path_principal, input_file_path_secundario, data_da_conferencia)
        pi_seof_comparado = comparar_pi_seof_composer(request_adapted)
        return pi_seof_comparado

    def __comparar_pi_siafi(self, input_file_path_principal, input_file_path_secundario, data_da_conferencia):
        """Compara PI com SIAFI."""
        request_adapted = comparar_pi_request_adapter(input_file_path_principal, input_file_path_secundario, data_da_conferencia)
        pi_siafi_comparado = comparar_pi_siafi_composer(request_adapted)
        return pi_siafi_comparado

    def on_compare_seof(self, input_file_path_principal, input_file_path_secundario, data_da_conferencia, callback):
        self.__run_in_thread(self.__comparar_pi_seof, callback, input_file_path_principal, input_file_path_secundario, data_da_conferencia)

    def on_compare_siafi(self, input_file_path_principal, input_file_path_secundario, data_da_conferencia, callback):
        self.__run_in_thread(self.__comparar_pi_siafi, callback, input_file_path_principal, input_file_path_secundario, data_da_conferencia)

    def criar_pastas(self):
        """Cria as pastas necessárias para o funcionamento do aplicativo."""
        criar_pastas = CriarPastas()
        criar_pastas.execute()

    def inicializar_configs(self):
        """Inicializa as configurações do aplicativo."""
        initial_configs = InitialConfigs()
        initial_configs.execute()

    def stop(self):
        """Método para parar todos os threads."""
        self._stop_event.set()
        for thread in self.threads:
            thread.join()
        self.threads.clear()
        PID = os.getpid()
        os.kill(PID, signal.SIGTERM)
