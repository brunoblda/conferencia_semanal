import sys
from tkinter import filedialog

import customtkinter as ctk

from project.UI.menu_frame import MenuFrame
from project.UI.reserva_frame import ReservaFrame
from project.UI.controller_app import ControllerApp
from project.UI.plano_interno_frame import PlanoInternoFrame


class JanelaView(ctk.CTk):
    """Classe para a janela principal da aplicação"""

    def __init__(self, controller: ControllerApp) -> None:
        super().__init__()
        self.__setup_janela()
        self.__controller = controller
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.build_frames()
        self.mostrar_tela("Menu")

        
    def __setup_janela(self):
        """Configura a aparência e o tema do customtkinter."""
        ctk.set_appearance_mode("Dark")  # Modos: "Light", "Dark", "System"
        ctk.set_default_color_theme("blue")  # Tema: "blue", "green", "dark-blue"
        self.title("Comparador de PIs")
        self.geometry(self.__CenterWindowToDisplay(795, 775))
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(25, weight=1)

    def __CenterWindowToDisplay(
        self, width: int, height: int, scale_factor: float = 1.0
    ):

        """Centers the window to the main display/monitor"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width / 2) - (width / 2)) * scale_factor)
        y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"

    def mostrar_tela(self, nome):
        for frame in self.__frames.values():
            frame.grid_forget()
        self.__frames[nome].grid(row=0, column=0)

    def __on_closing(self):
        """Função para fechar a aplicação."""
        self.destroy()
        sys.exit()

    def build_frames(self):
        """Constrói os frames da aplicação."""
        self.__plano_interno_frame = PlanoInternoFrame(self, self.__controller)
        self.__menu_frame = MenuFrame(self)
        self.__reserva_frame = ReservaFrame(self, self.__controller)
        self.__frames = {
            "PlanoInterno": self.__plano_interno_frame,
            "Menu": self.__menu_frame,
            "Reserva": self.__reserva_frame,
        }