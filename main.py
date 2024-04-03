import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from gui import NavGUI
from gui import LoginScreen
from database import Database
from login import User
 
if __name__ == "__main__":
    connection=Database("MailDB.db")
    root=ctk.CTk()
    root.geometry=("200x400")
    root.title=("Mail Database")
    # login=LoginScreen(root, connection)
    user=User("admin", "password", connection) # Delete this before final. Just for testing
    gui=NavGUI(root, connection, user) # Delete this before final. Just for testing. 
    root.mainloop()
    connection.close_connection()
