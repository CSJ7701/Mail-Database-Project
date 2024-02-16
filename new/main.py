import tkinter as tk
from tkinter import ttk
from gui import GUI
from database import Database

if __name__ == "__main__":
    connection=Database("MailDB.db")
    connection.get_cadet_info("101")
    root=tk.Tk()
    root.geometry=("500x450")
    root.title=("Mail Database")
    gui=GUI(root, connection)
    root.mainloop()
    connection.close_connection()
