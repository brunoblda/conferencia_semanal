import sys
from tkinter import filedialog

import customtkinter as ctk

from project.adapters.presenters.response_format import ResponseFormat
from project.UI.controller_app import ControllerApp
from project.UI.pop_up_loading import PopUpLoading


class JanelaView(ctk.CTk):

    def __init__(self, controller: ControllerApp) -> None:
        super().__init__()
        self.__controller = controller
        self.__setup_janela()
        self.__view_janela()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.pop_up_loading = None

    def __setup_janela(self):
        """Configura a aparência e o tema do customtkinter."""
        ctk.set_appearance_mode("Dark")  # Modos: "Light", "Dark", "System"
        ctk.set_default_color_theme("blue")  # Tema: "blue", "green", "dark-blue"
        self.title("Comparador de PIs")
        self.geometry(self.CenterWindowToDisplay(600, 640))
        self.grid_columnconfigure(0, weight=1)

    def CenterWindowToDisplay(self, width: int, height: int, scale_factor: float = 1.0):
        """Centers the window to the main display/monitor"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width / 2) - (width / 2)) * scale_factor)
        y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"

    def __view_janela(self):
        self.__radio_button_seof_siafi()
        self.__label_plano_interno()
        self.__label_seof()
        self.__label_siafi()
        self.__label_data_da_conferencia()
        self.__button_comparar()
        self.__response_message()

    def __radio_button_seof_siafi(self):
        self.radio_var = ctk.IntVar(value=0)
        self.radio_button_pi_seof = ctk.CTkRadioButton(
            self,
            text="Comparar PI X SEOF",
            font=("default", 20),
            variable=self.radio_var,
            command=self.__on_radio_button,
            value=1,
        )
        self.radio_button_pi_seof.grid(
            row=1, column=0, padx=(70, 0), pady=20, sticky="w"
        )
        self.radio_button_pi_siafi = ctk.CTkRadioButton(
            self,
            text="Comparar PI X SIAFI",
            font=("default", 20),
            variable=self.radio_var,
            command=self.__on_radio_button,
            value=2,
        )
        self.radio_button_pi_siafi.grid(
            row=1, column=1, padx=(0, 70), pady=20, sticky="e"
        )

    def __label_plano_interno(self):
        self.plano_interno_label_text = ctk.CTkLabel(
            self, text="Caminho do Arquivo do Plano Interno:", font=("default", 20)
        )
        self.plano_interno_label_text.grid(row=2, column=0, pady=(0, 0), columnspan=2)
        self.entry_plano_interno = ctk.CTkEntry(self, width=400, font=("default", 20))
        self.entry_plano_interno.grid(row=3, column=0, pady=5, columnspan=2)
        self.plano_interno_select_button = ctk.CTkButton(
            self,
            text="Selecionar Arquivo",
            font=("default", 20),
            command=self.select_file_plano_interno,
        )
        self.plano_interno_select_button.grid(row=4, column=0, pady=5, columnspan=2)

    def __label_seof(self):
        self.seof_label_text = ctk.CTkLabel(
            self, text="Caminho do Arquivo do SEOF:", font=("default", 20)
        )
        self.seof_label_text.grid(row=6, column=0, pady=(20, 0), columnspan=2)
        self.entry_seof = ctk.CTkEntry(self, width=400, font=("default", 20))
        self.entry_seof.grid(row=7, column=0, pady=5, columnspan=2)
        self.seof_button = ctk.CTkButton(
            self,
            text="Selecionar Arquivo",
            font=("default", 20),
            command=self.select_file_seof,
        )
        self.seof_button.grid(row=8, column=0, pady=5, columnspan=2)
        if self.radio_var.get() == 2:
            self.entry_seof.configure(state="disabled")
            self.seof_button.configure(state="disabled")

    def __label_siafi(self):
        self.siafi_label_text = ctk.CTkLabel(
            self, text="Caminho do Arquivo do SIAFI:", font=("default", 20)
        )
        self.siafi_label_text.grid(row=10, column=0, pady=(20, 0), columnspan=2)
        self.entry_siafi = ctk.CTkEntry(self, width=400, font=("default", 20))
        self.entry_siafi.grid(row=11, column=0, pady=5, columnspan=2)
        self.siafi_button = ctk.CTkButton(
            self,
            text="Selecionar Arquivo",
            font=("default", 20),
            command=self.select_file_siafi,
        )
        self.siafi_button.grid(row=12, column=0, pady=5, columnspan=2)

    def __label_data_da_conferencia(self):
        self.data_conferencia_label_text = ctk.CTkLabel(
            self, text="Data da Conferência:", font=("default", 20)
        )
        self.data_conferencia_label_text.grid(
            row=14, column=0, pady=(20, 0), columnspan=2, sticky="s"
        )
        self.entry_data = ctk.CTkEntry(
            self,
            width=400,
            justify="center",
            font=("default", 20),
            placeholder_text="DD-MM-AAAA",
        )
        self.entry_data.grid(row=16, column=0, pady=5, columnspan=2)

    def __button_comparar(self):
        self.comparar_button = ctk.CTkButton(
            self, text="Comparar", font=("default", 20), command=self.on_compare
        )
        self.comparar_button.grid(row=18, column=0, pady=(20, 0), columnspan=2)

    def __response_message(self):
        self.response_message = ctk.CTkLabel(
            self, text="", font=("default", 20), text_color="red"
        )
        self.response_message.grid(row=20, column=0, pady=(20, 0), columnspan=2)

    def __on_radio_button(self):
        estado_seof = "normal"
        estado_siafi = "normal"

        if self.radio_var.get() == 1:
            estado_siafi = "disabled"
        elif self.radio_var.get() == 2:
            estado_seof = "disabled"

        self.siafi_button.configure(state=estado_siafi)
        self.entry_siafi.configure(state=estado_siafi)
        self.seof_button.configure(state=estado_seof)
        self.entry_seof.configure(state=estado_seof)

    def on_compare(self):
        if self.radio_var.get() == 0:
            self.response_message.configure(
                text="Por favor, selecione o tipo de comparação"
            )
        else:
            self.__controller.criar_pastas()
            self.open_pop_up_loading(
                "Comparador de PIs", "Carregando, por favor aguarde..."
            )
            if self.radio_var.get() == 1:
                self.__controller.on_compare_seof(
                    self.entry_plano_interno.get(),
                    self.entry_seof.get(),
                    self.entry_data.get(),
                    self.handle_compare_result,
                )
            elif self.radio_var.get() == 2:
                self.__controller.on_compare_siafi(
                    self.entry_plano_interno.get(),
                    self.entry_siafi.get(),
                    self.entry_data.get(),
                    self.handle_compare_result,
                )

    def handle_compare_result(self, result: ResponseFormat):
        self.close_pop_up_loading()
        self.response_message.configure(text=result.message)

    def select_file_plano_interno(self):
        file_path = filedialog.askopenfilename(
            title="Selecione o Arquivo do Plano Interno"
        )
        if file_path:
            self.entry_plano_interno.delete(0, ctk.END)
            self.entry_plano_interno.insert(0, file_path)

    def select_file_seof(self):
        file_path = filedialog.askopenfilename(title="Selecione o Arquivo do SEOF")
        if file_path:
            self.entry_seof.delete(0, ctk.END)
            self.entry_seof.insert(0, file_path)

    def select_file_siafi(self):
        file_path = filedialog.askopenfilename(title="Selecione o Arquivo do SIAFI")
        if file_path:
            self.entry_siafi.delete(0, ctk.END)
            self.entry_siafi.insert(0, file_path)

    def open_pop_up_loading(self, title, mensagem: str):
        self.response_message.configure(text="")
        if self.pop_up_loading is None or not self.pop_up_loading.winfo_exists():
            self.pop_up_loading = PopUpLoading(
                title, mensagem
            )  # create window if its None or destroyed
            self.pop_up_loading.focus()  # if window exists focus it
            self.pop_up_loading.attributes("-topmost", True)
        else:
            self.pop_up_loading.focus()  # if window exists focus it
            self.pop_up_loading.attributes("-topmost", True)
        self.disable_widget()

    def close_pop_up_loading(self):
        if self.pop_up_loading is not None and self.pop_up_loading.winfo_exists():
            self.pop_up_loading.destroy()
            self.pop_up_loading = None
        self.enable_widget()

    def on_closing(self):
        self.destroy()
        sys.exit()

    def disable_widget(self):
        for widget in self.winfo_children():
            widget.configure(state="disabled")

    def enable_widget(self):
        for widget in self.winfo_children():
            widget.configure(state="normal")
        self.__on_radio_button()
