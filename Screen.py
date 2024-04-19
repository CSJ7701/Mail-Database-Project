import tkinter as tk
from tkinter import messagebox

class Screen:
    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_success(self, message):
        messagebox.showinfo("Success", message)
