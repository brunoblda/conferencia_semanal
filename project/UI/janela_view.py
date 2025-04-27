import sys
from tkinter import filedialog

import customtkinter as ctk

from project.adapters.presenters.response_format import ResponseFormat
from project.UI.controller_app import ControllerApp
from project.UI.pop_up_loading import PopUpLoading


class JanelaView(ctk.CTk):
    """Classe para a janela principal da aplicação"""

    def __init__(self, controller: ControllerApp) -> None:
        super().__init__()
        self.__controller = controller
        self.__setup_janela()
        self.__view_janela()
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.pop_up_loading = None

    def __setup_janela(self):
        """Configura a aparência e o tema do customtkinter."""
        ctk.set_appearance_mode("Dark")  # Modos: "Light", "Dark", "System"
        ctk.set_default_color_theme("blue")  # Tema: "blue", "green", "dark-blue"
        self.title("Comparador de PIs")
        self.geometry(self.__CenterWindowToDisplay(640, 720))
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(21, weight=1)

    def __CenterWindowToDisplay(
        self, width: int, height: int, scale_factor: float = 1.0
    ):

        """Centers the window to the main display/monitor"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width / 2) - (width / 2)) * scale_factor)
        y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"

    def __view_janela(self):
        """Cria os widgets da janela principal."""
        self.__radio_button_seof_siafi()
        self.__label_plano_interno()
        self.__label_seof()
        self.__label_siafi()
        self.__label_data_da_conferencia()
        self.__button_comparar()
        self.__response_message()
        self.__show_app_version()

    def __radio_button_seof_siafi(self):
        """Cria os radio buttons para escolher entre comparar PI X SEOF ou PI X SIAFI."""
        self.radio_var = ctk.IntVar(value=0)
        self.radio_button_pi_seof = ctk.CTkRadioButton(
            self,
            text="Comparar PI X SEOF",
            font=("default", 22),
            variable=self.radio_var,
            command=self.__on_radio_button,
            value=1,
        )
        self.radio_button_pi_seof.grid(
            row=1, column=0, padx=(50, 26), pady=30, sticky="e"
        )
        self.radio_button_pi_siafi = ctk.CTkRadioButton(
            self,
            text="Comparar PI X SIAFI",
            font=("default", 22),
            variable=self.radio_var,
            command=self.__on_radio_button,
            value=2,
        )
        self.radio_button_pi_siafi.grid(
            row=1, column=1, padx=(26, 50), pady=30, sticky="w"
        )

    def __label_plano_interno(self):
        """Cria os labels e entrys para o caminho do arquivo do Plano Interno."""
        self.plano_interno_label_text = ctk.CTkLabel(
            self, text="Caminho do Arquivo do Plano Interno:", font=("default", 22)
        )
        self.plano_interno_label_text.grid(row=2, column=0, pady=(5, 0), columnspan=2)
        self.entry_plano_interno = ctk.CTkEntry(self, width=400, font=("default", 20))
        self.entry_plano_interno.grid(row=3, column=0, pady=5, columnspan=2)
        self.plano_interno_select_button = ctk.CTkButton(
            self,
            text="Selecionar Arquivo",
            font=("default", 22),
            command=self.__select_file_plano_interno,
        )
        self.plano_interno_select_button.grid(row=4, column=0, pady=5, columnspan=2)

    def __label_seof(self):
        """Cria os labels e entrys para o caminho do arquivo do SEOF."""
        self.seof_label_text = ctk.CTkLabel(
            self, text="Caminho do Arquivo do SEOF:", font=("default", 22)
        )
        self.seof_label_text.grid(row=6, column=0, pady=(24, 0), columnspan=2)
        self.entry_seof = ctk.CTkEntry(self, width=400, font=("default", 22))
        self.entry_seof.grid(row=7, column=0, pady=5, columnspan=2)
        self.seof_button = ctk.CTkButton(
            self,
            text="Selecionar Arquivo",
            font=("default", 22),
            command=self.__select_file_seof,
        )
        self.seof_button.grid(row=8, column=0, pady=5, columnspan=2)
        if self.radio_var.get() == 2:
            self.entry_seof.configure(state="disabled")
            self.seof_button.configure(state="disabled")

    def __label_siafi(self):
        """Cria os labels e entrys para o caminho do arquivo do SIAFI."""
        self.siafi_label_text = ctk.CTkLabel(
            self, text="Caminho do Arquivo do SIAFI:", font=("default", 22)
        )
        self.siafi_label_text.grid(row=10, column=0, pady=(24, 0), columnspan=2)
        self.entry_siafi = ctk.CTkEntry(self, width=400, font=("default", 22))
        self.entry_siafi.grid(row=11, column=0, pady=5, columnspan=2)
        self.siafi_button = ctk.CTkButton(
            self,
            text="Selecionar Arquivo",
            font=("default", 22),
            command=self.__select_file_siafi,
        )
        self.siafi_button.grid(row=12, column=0, pady=5, columnspan=2)

    def __label_data_da_conferencia(self):
        """Cria os labels e entrys para a data da conferência."""
        self.data_conferencia_label_text = ctk.CTkLabel(
            self, text="Data da Conferência:", font=("default", 22)
        )
        self.data_conferencia_label_text.grid(
            row=14, column=0, pady=(22, 0), columnspan=2, sticky="s"
        )
        self.data_conferencia_label_data= ctk.CTkLabel(
            self, text="", font=("default", 22)
        )
        self.data_conferencia_label_data.grid(
            row=15, column=0, pady=(22, 0), columnspan=2, sticky="s"
        )
        
        self.__on_label_data_conferencia()

    def __button_comparar(self):
        """Cria o botão para comparar os arquivos."""
        self.comparar_button = ctk.CTkButton(
            self,
            text="Comparar",
            fg_color="green",
            hover_color="darkgreen",
            font=("default", 22),
            command=self.__on_compare,
        )
        self.comparar_button.grid(row=18, column=0, pady=(20, 0), columnspan=2)

    def __response_message(self):
        """Cria o label para exibir a mensagem de resposta."""
        self.response_message = ctk.CTkLabel(
            self, text="", font=("default", 22), text_color="orange"
        )
        self.response_message.grid(row=20, column=0, pady=(24, 0), columnspan=2)

    def __show_app_version(self):
        """Cria o label para exibir a versão da aplicação."""
        self.app_version = ctk.CTkLabel(
            self, text="Versão 2.1.7", font=("default", 10), text_color="white"
        )
        self.app_version.grid(row=21, column=0, pady=(20, 0), columnspan=2, sticky="s")

    def __on_radio_button(self):
        """Desabilita os campos de entrada de acordo com o radio button selecionado."""
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

    def __on_compare(self):
        """Função para comparar os arquivos."""
        if self.radio_var.get() == 0:
            self.response_message.configure(
                text="Por favor, selecione o tipo de comparação"
            )
        else:
            self.__controller.criar_pastas()
            self.__open_pop_up_loading(
                "Comparador de PIs", "Carregando, por favor aguarde..."
            )
            if self.radio_var.get() == 1:
                self.__controller.on_compare_seof(
                    self.entry_plano_interno.get(),
                    self.entry_seof.get(),
                    self.data_conferencia_label_data.cget("text"),
                    self.__handle_compare_result,
                )
            elif self.radio_var.get() == 2:
                self.__controller.on_compare_siafi(
                    self.entry_plano_interno.get(),
                    self.entry_siafi.get(),
                    self.data_conferencia_label_data.cget("text"),
                    self.__handle_compare_result,
                )

    def __handle_compare_result(self, result: ResponseFormat):
        """Função para lidar com o resultado da comparação."""
        self.__close_pop_up_loading()
        if result.status == "error":
            self.response_message.configure(text=result.message, text_color="yellow")
        elif result.status == "success - sem erro":
            self.response_message.configure(text=result.message, text_color="green")
        elif result.status == "success - com erro":
            self.response_message.configure(text=result.message, text_color="red")
        else:
            self.response_message.configure(text=result.message, text_color="orange")

    def __on_label_data_conferencia(self):
        """ Função para inserir a data da conferência."""
        self.data_conferencia_label_data.configure(text=self.__controller.calculate_data_conferencia())
    
    def __select_file_plano_interno(self):
        """Função para selecionar o arquivo do Plano Interno."""
        file_path = filedialog.askopenfilename(
            title="Selecione o Arquivo do Plano Interno"
        )
        if file_path:
            self.entry_plano_interno.delete(0, ctk.END)
            self.entry_plano_interno.insert(0, file_path)

    def __select_file_seof(self):
        """Função para selecionar o arquivo do SEOF."""
        file_path = filedialog.askopenfilename(title="Selecione o Arquivo do SEOF")
        if file_path:
            self.entry_seof.delete(0, ctk.END)
            self.entry_seof.insert(0, file_path)

    def __select_file_siafi(self):
        """Função para selecionar o arquivo do SIAFI."""
        file_path = filedialog.askopenfilename(title="Selecione o Arquivo do SIAFI")
        if file_path:
            self.entry_siafi.delete(0, ctk.END)
            self.entry_siafi.insert(0, file_path)

    def __open_pop_up_loading(self, title, mensagem: str):
        """Função para abrir a janela de loading."""
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
        self.__disable_widget()

    def __close_pop_up_loading(self):
        """Função para fechar a janela de loading."""
        if self.pop_up_loading is not None and self.pop_up_loading.winfo_exists():
            self.pop_up_loading.destroy()
            self.pop_up_loading = None
        self.__enable_widget()

    def __on_closing(self):
        """Função para fechar a aplicação."""
        self.destroy()
        sys.exit()

    def __disable_widget(self):
        """Função para desabilitar os widgets da janela principal."""
        for widget in self.winfo_children():
            widget.configure(state="disabled")

    def __enable_widget(self):
        """Função para habilitar os widgets da janela principal."""
        for widget in self.winfo_children():
            widget.configure(state="normal")
        self.__on_radio_button()
