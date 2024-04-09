from os.path import expanduser
from sre_constants import AT_END
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, Toplevel
from customtkinter.windows.widgets import image
from idlelib.tooltip import Hovertip
from database import Database
from LoginBackend import User
from HomeTab import HomeScreen
from DataTab import DataScreen
from ManageTab import Manage
from ReportsTab import Reports
from SettingsTab import Settings
from LoginScreen import LoginScreen
from datetime import datetime
from config import Config
import CTkListbox
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class GUI:
    def __init__(self, root, database, user):

        self.root=root
        self.database=database
        self.user=user
        self.config=Config("./config.ini")
        ctk.set_default_color_theme("themes/CGA.json")
        ctk.set_appearance_mode(self.config.appearance('color_mode'))


        # self.root.resizable(width=0, height=0)

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



class NavGUI(GUI):
    def __init__(self, root, database, user):
        super().__init__(root, database, user)
        self.database=database
        ctk.set_default_color_theme("themes/CGA.json")
        ctk.set_appearance_mode(self.config.appearance('color_mode'))


        self.nav_bar=ctk.CTkFrame(self.root, fg_color=("#d3d3d3", "#191919"))
        self.nav_bar.pack(side="left", fill="y", pady=10, padx=(10,0))

        self.logo_ref=ctk.CTkImage(light_image=Image.open("Assets/USCGA.png"), size=(130,130))
        self.logo=ctk.CTkLabel(self.nav_bar, image=self.logo_ref, text="")
        self.logo.pack(pady=(0,0))

        self.home_button=ctk.CTkButton(self.nav_bar, text="Home", command=self.show_home)
        self.home_button.pack(side="top", padx=(30), pady=(50,0))
        self.data_button=ctk.CTkButton(self.nav_bar, text="Data", command=self.show_data)
        self.data_button.pack(side="top", padx=(30), pady=(20,0))
        self.reports_button=ctk.CTkButton(self.nav_bar, text="Reports", command=self.show_reports)
        self.manage_button=ctk.CTkButton(self.nav_bar, text="Manage DB", command=self.show_manage)
        self.manage_button.pack(side="top", padx=(30), pady=(20,0))
        self.reports_button.pack(side="top", padx=(30), pady=(20,0))
        self.settings_button=ctk.CTkButton(self.nav_bar, text="Settings", command=self.show_settings)
        self.settings_button.pack(side="top",  padx=(30), pady=(20,0))
        self.logout_button=ctk.CTkButton(self.nav_bar, text="Logout", command=self.logout)
        self.logout_button.pack(side="bottom", padx=(30), pady=(20,20))

        self.main_frame=ctk.CTkFrame(self.root, width=400, height=300, fg_color=("#d3d3d3","#191919"))
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=(60,20))

        self.show_home()

    def show_home(self):
        self.clear_main_frame()
        HomeScreen(self.main_frame, self)

    def show_data(self):
        self.clear_main_frame()
        DataScreen(self.main_frame, self)

    def show_manage(self):
        self.clear_main_frame()
        Manage(self.main_frame, self)
        
    def show_reports(self):
        self.clear_main_frame()
        Reports(self.main_frame, self)

    def show_settings(self):
        self.clear_main_frame()
        Settings(self.main_frame, self)

    def logout(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginScreen(self.root, self.database)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()



