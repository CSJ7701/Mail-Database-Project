import customtkinter as ctk
from HomeTab import HomeScreen
from DataTab import DataScreen
from ManageTab import Manage
from ReportsTab import Reports
from SettingsTab import Settings
from config import Config
from PIL import Image
import os
import sys

class NavGUI():
    """A class for creating the root GUI window."""
    def __init__(self, root, database, user):
        """Initialize the GUI window.

        Args:
            root: The root Tkinter object
            database: The database object
            user: The user object.
        """
        # super().__init__(root, database, user)
        self.root=root
        self.root.protocol("WM_DELETE_WINDOW", root.quit)
        self.user=user
        self.config=Config("config.ini")
        self.database=database
        script_dir=os.path.dirname(os.path.abspath(sys.argv[0]))
        ctk.set_default_color_theme(os.path.join(script_dir, "themes", "CGA.json"))
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
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=(20,20))

        self.show_home()

    def show_home(self):
        """Display the home screen."""
        self.clear_main_frame()
        HomeScreen(self.main_frame, self)

    def show_data(self):
        """Display the data screen."""
        self.clear_main_frame()
        DataScreen(self.main_frame, self)

    def show_manage(self):
        """Display the manage screen."""
        self.clear_main_frame()
        Manage(self.main_frame, self)
        
    def show_reports(self):
        """Display the reports screen."""
        self.clear_main_frame()
        Reports(self.main_frame, self)

    def show_settings(self):
        """Display the settings screen."""
        self.clear_main_frame()
        Settings(self.main_frame, self)

    def logout(self):
        """Logout and reload the login screen."""
        from LoginScreen import LoginScreen
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginScreen(self.root, self.database)

    def clear_main_frame(self):
        """Empty the main frame to load a new one."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()



