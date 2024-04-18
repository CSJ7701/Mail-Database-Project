import customtkinter as ctk
from gui import NavGUI 
from LoginBackend import User
from Screen import Screen
from config import Config
import os
import sys

class LoginScreen(Screen):
    def __init__(self, root, database):
        # super().__init__(root, database, None)
        self.root=root
        self.database=database
        self.config=Config("config.ini")
        script_dir=os.path.dirname(os.path.abspath(sys.argv[0]))
        ctk.set_default_color_theme(os.path.join(script_dir, "themes", "CGA.json"))
        ctk.set_appearance_mode(self.config.appearance('color_mode'))

        ctk.CTkLabel(self.root, text="USCGA Mailroom", font=("Helvetica",20)).pack(pady=20)

        self.frame=ctk.CTkFrame(master=self.root, width=30, height=30)
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)

        ctk.CTkLabel(master=self.frame, text="Enter Login").pack(pady=12, padx=10)

        self.usern=ctk.CTkEntry(master=self.frame, placeholder_text="Username")
        self.usern.bind('<Return>', self.event_login)
        self.usern.pack(pady=12, padx=10)
        self.passw=ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.passw.bind('<Return>', self.event_login)
        self.passw.pack(pady=12, padx=10)
        self.button=ctk.CTkButton(master=self.frame, text='Login', command=self.login)
        self.button.pack(pady=12, padx=10)

    def event_login(self, event):
        self.login()
        

    def login(self):
        uname=self.usern.get()
        passw=self.passw.get()
        self.user=User(uname, passw, self.database)
        if not uname:
            self.show_error("Please enter a username")
            return
        if not passw:
            self.show_error("Please enter a password")
            return
        validate=self.user.check_pass(passw)
        print(validate)
        if validate==-1:
            self.show_error("Password Incorrect")
        elif validate==-2:
            self.show_error("Username not recognized")
        elif validate==1:
            for widget in self.root.winfo_children():
                widget.destroy()
            NavGUI(self.root, self.database, self.user)
             
