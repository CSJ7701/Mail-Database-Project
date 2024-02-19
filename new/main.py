import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from gui import NavGUI
from gui import LoginScreen
from database import Database

if __name__ == "__main__":
    connection=Database("MailDB.db")
    connection.get_cadet_info("101")
    root=ctk.CTk()
    root.geometry=("200x400")
    root.title=("Mail Database")
    login=LoginScreen(root, connection)
    # gui=NavGUI(root, connection)
    root.mainloop()
    connection.close_connection()
