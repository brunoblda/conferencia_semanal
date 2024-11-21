import customtkinter as ctk

class PopUpLoading(ctk.CTkToplevel):
    def __init__(self, title, mensagem):
        super().__init__()
        self.geometry(self.CenterWindowToDisplay(400, 100))
        self.title(title)
        self.label = ctk.CTkLabel(self, text=mensagem, font=('default', 20))
        self.grid_columnconfigure(0, weight=1)
        self.label.grid(row=0, column=0, padx=20, pady=20)

    def CenterWindowToDisplay(self, width: int, height: int, scale_factor: float = 1.0):
        """Centers the window to the main display/monitor"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width/2) - (width/2)) * scale_factor)
        y = int(((screen_height/2) - (height/1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"
