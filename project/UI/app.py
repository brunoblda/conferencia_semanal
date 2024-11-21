from project.UI.error_logger import ErrorLogger
from project.UI.janela_view import JanelaView
from project.UI.controller_app import ControllerApp
import sys

class App:
    def __init__(self) -> None:
        self.__error_logger = ErrorLogger()
        self.__error_logger.run()
        self.__controller = ControllerApp()  # Inicializa o ControllerApp
        self.__view = JanelaView(self.__controller) # Inicializa a JanelaView
        self.__view.protocol("WM_DELETE_WINDOW", self.on_closing)  # Sobrescreve o comportamento de fechamento da janela
    
    def run(self) -> None:
        self.__controller.inicializar_configs()
        self.__view.mainloop()

    def on_closing(self):
        """Método chamado quando a janela é fechada."""
        self.__controller.stop()
        self.__view.destroy()
        sys.exit()
