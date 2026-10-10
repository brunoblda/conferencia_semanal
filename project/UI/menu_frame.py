import customtkinter as ctk

class MenuFrame(ctk.CTkFrame):
    """Classe para o frame do menu da aplicação"""

    def __init__(self, master, app_version_text) -> None:
        super().__init__(master)
        self.app_version_text = app_version_text
        self.view_janela()
    
    def view_janela(self):
        self.__label_menu()
        self.__button_plano_interno()
        self.__button_reserva()
        self.__show_app_version()

    def __label_menu(self):
        self.label = ctk.CTkLabel(self, text="Menu", font=("default", 26))
        self.label.grid(row=0, column=0, pady=(200,40), padx=368, columnspan=2)
        
    def __button_plano_interno(self):
        self.button1 = ctk.CTkButton(
            self,
            text="Comparar Planos Internos",
            font=("default", 22),
            width=300,
            command=self.__on_button_plano_interno
        )
        self.button1.grid(row=1, column=0, pady=20, padx=20, columnspan=2)

    def __button_reserva(self):
        self.button2 = ctk.CTkButton(
            self,
            text="Comparar Reservas",
            font=("default", 22),
            width=300,
            command=self.__on_button_reserva
        )
        self.button2.grid(row=2, column=0, pady=(20,330), padx=20, columnspan=2)
    
    def __on_button_plano_interno(self):
        self.master.mostrar_tela("PlanoInterno")
        
    def __on_button_reserva(self):
        self.master.mostrar_tela("Reserva")
    
    def __show_app_version(self):
        """Cria o label para exibir a versão da aplicação."""
        self.app_version = ctk.CTkLabel(
            self, text=self.app_version_text, font=("default", 10), text_color="white"
        )
        self.app_version.grid(row=3, column=0, pady=(20,10), columnspan=2, sticky="s")
