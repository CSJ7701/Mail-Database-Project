import customtkinter as ctk


class Settings(NavGUI):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame
        self.config=self.parent.config

        self.left_frame=ctk.CTkFrame(self.main_frame, width=200, height=400, fg_color=("#d3d3d3", "#000000"))
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        

        self.middle_frame=ctk.CTkFrame(self.main_frame, width=300, height=200, fg_color=("#d3d3d3", "#000000"))
        self.middle_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame=ctk.CTkFrame(self.main_frame, width=300, height=200, fg_color=("#d3d3d3", "#000000"))
        self.right_frame.pack(side="left", fill="y", padx=10, pady=10)

    def ChangeColorMode(self, choice):
        ...
