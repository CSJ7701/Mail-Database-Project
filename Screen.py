import tkinter as tk
import customtkinter as ctk

class Screen:
    def show_error(self, message):
        tk.messagebox.showerror("Error", message)
