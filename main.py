import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from gui import NavGUI
from LoginScreen import LoginScreen
from database import Database
from LoginBackend import User
from config import Config
 
if __name__ == "__main__":
    config=Config('config.ini')
    connection=Database(config.system('db'))
    root=ctk.CTk()
    root.geometry=("200x400")
    root.title=("Mail Database")
    login=LoginScreen(root, connection)
    # user=User("admin", "password", connection) # Delete this before final. Just for testing
    # gui=NavGUI(root, connection, user) # Delete this before final. Just for testing. 
    root.mainloop()
    connection.close_connection()
