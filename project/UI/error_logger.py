import logging
import sys

class ErrorLogger:

    def run(self):
        self.__setup_logger()
        sys.excepthook = self.__handle_exception

    def __setup_logger(self):
        """Configura o logger para registrar erros em um arquivo."""
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # Criar um manipulador de arquivo
        fh = logging.FileHandler("error_log.txt")
        fh.setLevel(logging.ERROR)

        # Criar um formatador e adicioná-lo ao manipulador
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # Adicionar o manipulador ao logger
        logger.addHandler(fh)

    def __handle_exception(self, exc_type, exc_value, exc_traceback):
        """Captura exceções não tratadas e registra no logger."""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger().error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
