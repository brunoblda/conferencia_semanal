"""
from project.UI.controller_app import ControllerApp
from tkinter import filedialog
import customtkinter as ctk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from project.UI.janela_view import JanelaView

class JanelaCommands:
    def __init__(self, janela_view: 'JanelaView', controller: ControllerApp):
        self.janela_view = janela_view
        self.controller = controller

    def on_radio_button(self):
        estado_seof = 'normal'
        estado_siafi = 'normal'

        if self.janela_view.radio_var.get() == 1:
            estado_siafi = 'disabled'
        elif self.janela_view.radio_var.get() == 2:
            estado_seof = 'disabled'

        self.janela_view.siafi_button.configure(state=estado_siafi)
        self.janela_view.entry_siafi.configure(state=estado_siafi)
        self.janela_view.seof_button.configure(state=estado_seof)
        self.janela_view.entry_seof.configure(state=estado_seof)

    def on_compare_seof(self):
        input_file_path_principal = self.janela_view.entry_plano_interno.get()
        input_file_path_secundario = self.janela_view.entry_seof.get()
        data_da_conferencia = self.janela_view.entry_data.get()
        self.controller.on_compare_seof(input_file_path_principal, input_file_path_secundario, data_da_conferencia)

    def on_compare_siafi(self):
        input_file_path_principal = self.janela_view.entry_plano_interno.get()
        input_file_path_secundario = self.janela_view.entry_siafi.get()
        data_da_conferencia = self.janela_view.entry_data.get()
        self.controller.on_compare_siafi(input_file_path_principal, input_file_path_secundario, data_da_conferencia)

    def select_file_plano_interno(self):
        file_path = filedialog.askopenfilename(title="Selecione o Arquivo do Plano Interno")
        if file_path:
            self.janela_view.entry_plano_interno.delete(0, ctk.END)
            self.janela_view.entry_plano_interno.insert(0, file_path)

    def select_file_seof(self):
        file_path = filedialog.askopenfilename(title="Selecione o Arquivo do SEOF")
        if file_path:
            self.janela_view.entry_seof.delete(0, ctk.END)
            self.janela_view.entry_seof.insert(0, file_path)

    def select_file_siafi(self):
        file_path = filedialog.askopenfilename(title="Selecione o Arquivo do SIAFI")
        if file_path:
            self.janela_view.entry_siafi.delete(0, ctk.END)
            self.janela_view.entry_siafi.insert(0, file_path)
"""