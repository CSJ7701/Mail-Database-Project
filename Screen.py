import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk

class Screen:
    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_success(self, message):
        messagebox.showinfo("Success", message)


    def Treeview_style(self):
        mode=ctk.get_appearance_mode()
        if mode == "Dark":
            bg_color="#1e1e1e"
            text_color="#888888"
            selected_color="#f2531b"
            bg_select="#545454"
        else:
            bg_color="#e0e0e0"
            text_color="#000000"
            selected_color="#e04200"
            bg_select="#d3d3d3"
        treestyle=ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=1)
        treestyle.configure("Treeview.Heading", foreground=text_color, background=bg_color)
        treestyle.map('Treeview', background=[('selected', bg_select)], foreground=[('selected', selected_color)])
