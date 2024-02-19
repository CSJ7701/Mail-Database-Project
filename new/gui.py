import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, Toplevel
from idlelib.tooltip import Hovertip
from database import Database
from login import User

class GUI:
    def __init__(self, root, database, user):
        self.root=root
        self.database=database
        self.user=user
        ctk.set_default_color_theme("../themes/CGA.json")
        ctk.set_appearance_mode("dark")

    def add_package(self):
        box=self.package_box.get()
        track=self.package_number.get()
        self.database.add_package(box, track)

    def populate_table(self):
        name=self.search_name.get()
        box=self.search_box.get()
        track=self.search_track.get()
        results=self.database.populate_table(name=name, box=box, track=track)
        self.table.delete(*self.table.get_children())
        for data in results:
            self.table.insert('', 'end', values=(data[1], data[2], data[3], data[4]))

    def item_select(self, _):
        for i in self.table.selection():
            print(self.table.item(i)['values'])

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

class LoginScreen(GUI):
    def __init__(self, root, database):
        super().__init__(root, database, None)
        self.root=root
        self.database=database

        ctk.CTkLabel(self.root, text="USCGA Mailroom", font=("Helvetica",20)).pack(pady=20)

        self.frame=ctk.CTkFrame(master=self.root, width=30, height=30)
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)

        ctk.CTkLabel(master=self.frame, text="Enter Login").pack(pady=12, padx=10)

        self.usern=ctk.CTkEntry(master=self.frame, placeholder_text="Username")
        self.usern.pack(pady=12, padx=10)
        self.passw=ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.passw.pack(pady=12, padx=10)
        self.button=ctk.CTkButton(master=self.frame, text='Login', command=self.login)
        self.button.pack(pady=12, padx=10)

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
            self.root.destroy()
            root=ctk.CTk()
            NavGUI(root, self.database, self.user)
             

class NavGUI(GUI):
    def __init__(self, root, database, user):
        super().__init__(root, database, user)

        self.nav_bar=ctk.CTkFrame(self.root)
        self.nav_bar.pack(side="left", fill="y")

        self.home_button=ctk.CTkButton(self.nav_bar, text="Home", command=self.show_home)
        self.home_button.pack(side="top", padx=(30,20), pady=20)

        self.main_frame=ctk.CTkFrame(self.root, width=400, height=300, fg_color=("#d3d3d3","#191919"))
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.show_home()

    def show_home(self):
        self.clear_main_frame()
        home_label=ctk.CTkLabel(self.main_frame, text=f"Welcome {self.user.username}", font=("Helvetica", 18))
        home_label.pack(pady=50)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
