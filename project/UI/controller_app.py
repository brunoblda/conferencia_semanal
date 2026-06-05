import logging
import threading
from datetime import date

import jpype

from project.errors.error_handler import handle_error
from project.infra.criar_pastas import CriarPastas
from project.infra.initial_configs import InitialConfigs
from project.main.adapters.comparar_pi_request_adapter import comparar_pi_request_adapter
from project.main.composer.comparar_pi_seof_composer import comparar_pi_seof_composer
from project.main.composer.comparar_pi_siafi_composer import comparar_pi_siafi_composer


class ControllerApp:

    def __init__(self):
        self._stop_event = threading.Event()
        self.threads = []

    def __run_in_thread(self, target, callback, *args):
        """Executa uma função em um thread e captura exceções."""
        self.__cleanup_finished_threads()
        thread = threading.Thread(
            target=self.__thread_wrapper,
            args=(target, callback, *args),
            daemon=True,
        )
        thread.start()
        self.threads.append(thread)

    def __cleanup_finished_threads(self):
        """Remove da lista as threads que já terminaram."""
        self.threads = [thread for thread in self.threads if thread.is_alive()]

    def __thread_wrapper(self, target, callback, *args):
        """Wrapper para executar a função alvo e capturar exceções."""
        result = None
        try:
            if not self._stop_event.is_set():
                result = target(*args)
        except Exception as e:
            logging.getLogger().error("Exception in thread", exc_info=True)
            result = handle_error(e)
        finally:
            if callback:
                callback(result)
                
    def calculate_data_conferencia(self):
        """ Calcula a data da conferência. """
        today = date.today()
        today_str = today.strftime("%d/%m/%Y")
        return today_str

    def __comparar_pi(
        self,
        composer,
        input_file_path_principal,
        input_file_path_secundario,
        data_da_conferencia,
    ):
        """Compara PI usando o composer informado (SEOF ou SIAFI)."""
        request_adapted = comparar_pi_request_adapter(
            input_file_path_principal, input_file_path_secundario, data_da_conferencia
        )
        return composer(request_adapted)

    def on_compare_seof(
        self,
        input_file_path_principal,
        input_file_path_secundario,
        data_da_conferencia,
        callback,
    ):
        self.__run_in_thread(
            self.__comparar_pi,
            callback,
            comparar_pi_seof_composer,
            input_file_path_principal,
            input_file_path_secundario,
            data_da_conferencia,
        )

    def on_compare_siafi(
        self,
        input_file_path_principal,
        input_file_path_secundario,
        data_da_conferencia,
        callback,
    ):
        self.__run_in_thread(
            self.__comparar_pi,
            callback,
            comparar_pi_siafi_composer,
            input_file_path_principal,
            input_file_path_secundario,
            data_da_conferencia,
        )

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
        self.__cleanup_finished_threads()
        for thread in self.threads:
            thread.join(timeout=3)
            if thread.is_alive():
                logging.getLogger().warning("Thread não finalizou dentro do timeout")
        self.threads.clear()
        self.__shutdown_jvm()

    def __shutdown_jvm(self):
        """Encerra a JVM do JPype para liberar o processo Python no fechamento."""
        try:
            if jpype.isJVMStarted():
                jpype.shutdownJVM()
        except Exception:
            logging.getLogger().warning("Falha ao encerrar JVM do JPype", exc_info=True)
