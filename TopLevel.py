import customtkinter

class TopLevel(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x500")
        self.title("string")

        self.label=customtkinter.CTkLabel(self, text="TopLevelWindow")
        self.label.pack(padx=20, pady=20)
