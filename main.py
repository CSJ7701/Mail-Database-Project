import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from gui import NavGUI
from LoginScreen import LoginScreen
from database import Database
from LoginBackend import User
from config import Config
 
if __name__ == "__main__":
    # Define variables to pass to GUI
    config=Config('config.ini')
    connection=Database(config.system('db'))

    # Define GUI variables
    root=ctk.CTk()
    root.geometry=("200x400")
    root.title=("Mail Database")
    login=LoginScreen(root, connection)
    
    # Display the GUI
    root.mainloop()
    # Close the connection to the database once the GUI is closed
    connection.close_connection()
