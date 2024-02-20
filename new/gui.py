import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, Toplevel
from idlelib.tooltip import Hovertip
from database import Database
from login import User
from datetime import datetime

class GUI:
    def __init__(self, root, database, user):
        self.root=root
        self.database=database
        self.user=user
        ctk.set_default_color_theme("../themes/CGA.json")
        ctk.set_appearance_mode("dark")
        self.root.resizable(width=0, height=0)

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
            self.root.destroy()
            root=ctk.CTk()
            NavGUI(root, self.database, self.user)
             

class NavGUI(GUI):
    def __init__(self, root, database, user):
        super().__init__(root, database, user)
        self.database=database

        self.nav_bar=ctk.CTkFrame(self.root, fg_color=("#d3d3d3", "#191919"))
        self.nav_bar.pack(side="left", fill="y", pady=10, padx=(10,0))

        self.home_button=ctk.CTkButton(self.nav_bar, text="Home", command=self.show_home)
        self.home_button.pack(side="top", padx=(30), pady=(50,0))
        self.data_button=ctk.CTkButton(self.nav_bar, text="Data", command=self.show_data)
        self.data_button.pack(side="top", padx=(30), pady=(20,0))
        self.reports_button=ctk.CTkButton(self.nav_bar, text="Reports", command=self.show_reports)
        self.reports_button.pack(side="top", padx=(30), pady=(20,0))
        self.settings_button=ctk.CTkButton(self.nav_bar, text="Settings", command=self.show_settings)
        self.settings_button.pack(side="top",  padx=(30), pady=(20,0))

        self.main_frame=ctk.CTkFrame(self.root, width=400, height=300, fg_color=("#d3d3d3","#191919"))
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=(20))

        self.show_home()

    def show_home(self):
        self.clear_main_frame()
        HomeScreen(self.main_frame, self)

    def show_data(self):
        self.clear_main_frame()
        DataScreen(self.main_frame, self)
        
    def show_reports(self):
        self.clear_main_frame()

    def show_settings(self):
        self.clear_main_frame()
        print("SETTINGS TAB HERE")

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

class HomeScreen(NavGUI):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame
        home_label=ctk.CTkLabel(self.main_frame, text=f"Welcome {self.parent.user.username}", font=("Helvetica", 18))
        home_label.pack(pady=(50,0))

        datestring=datetime.now()
        datestring=datestring.strftime("%B %dth %Y")
        date_label=ctk.CTkLabel(self.main_frame, text=datestring)
        date_label.pack()
        
        data_frame=ctk.CTkFrame(self.main_frame, width=380, height=200, fg_color=("#d3d3d3","#191919"),border_width=2,border_color=("#F2531B", "#E04200"))
        data_frame.pack(expand=True, fill="both", padx=20, pady=20)

        data_top_frame=ctk.CTkFrame(data_frame, width=380, height=10, fg_color=("#d3d3d3", "#191919"))
        data_top_frame.pack(side="top", fill="x", padx=5, pady=5)
        unretrieved_package_count_label=ctk.CTkLabel(data_top_frame, text=self.unretrieved_package_count())
        unretrieved_package_count_label.pack(side="left", padx=(20,0))
        retrieved_package_count_label=ctk.CTkLabel(data_top_frame, text=self.retrieved_package_count())
        retrieved_package_count_label.pack(side="right", padx=(0,20))

        data_bottom_frame=ctk.CTkFrame(data_frame, width=380, height=10, fg_color=("#d3d3d3", "#191919"))
        data_bottom_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        data_bottom_left_frame=ctk.CTkFrame(data_bottom_frame, width=190, height=10)#, fg_color=("#d3d3d3", "#191919"))
        data_bottom_left_frame.pack(side="left", fill="both", padx=5, pady=5)
        data_bottom_right_frame=ctk.CTkFrame(data_bottom_frame, width=190, height=10)#, fg_color=("#d3d3d3","#191919"))
        data_bottom_right_frame.pack(side="right", fill="both", padx=5, pady=5)

        unretrieved_tree=ttk.Treeview(data_bottom_left_frame, columns=("addressee", "received"))
        unretrieved_tree.heading("#1", text="Name")
        unretrieved_tree.heading("#2", text="Received")
        unretrieved_tree['show']='headings'
        unretrieved_tree.pack(side="left")
        retrieved_tree=ttk.Treeview(data_bottom_right_frame, columns=("addressee", "picked_up"))
        retrieved_tree.heading("#1", text="Name")
        retrieved_tree.heading("#2", text="Retrieved")
        retrieved_tree['show']='headings'
        retrieved_tree.pack(side="right")

        self.populate_treeview(unretrieved_tree, self.unretrieved_packages())
        self.populate_treeview(retrieved_tree, self.retrieved_packages())
        self.Treeview_style()

    def unretrieved_packages(self):
        self.parent.database.cursor.execute("SELECT * FROM packages WHERE picked_up IS NULL")
        results=self.parent.database.cursor.fetchall()
        return results
    def unretrieved_package_count(self):
        package_count=self.parent.database.cursor.execute("SELECT COUNT(*) FROM packages WHERE picked_up IS NULL")
        package_count=package_count.fetchone()
        if package_count:
            package_count=package_count[0]
            if package_count==1:
                package_count_string="There is currently 1 unretrieved package."
            else:
                package_count_string=f"There are currently {package_count} unretrieved packages."
        else:
            package_count=0
            package_count_string="There are currently no unretrieved packages."
        return package_count_string

    def retrieved_packages(self):
        self.parent.database.cursor.execute("SELECT * FROM packages WHERE DATE(picked_up) = DATE('now')")
        results=self.parent.database.cursor.fetchall()
        return results
    def retrieved_package_count(self):
        package_count=self.parent.database.cursor.execute("SELECT COUNT(*) FROM packages WHERE DATE(picked_up) = DATE('now')")
        package_count=package_count.fetchone()
        if package_count:
            package_count=package_count[0]
            if package_count==1:
                package_count_string="1 Package has been picked up today."
            else:
                package_count_string=f"{package_count} Packages have been picked up today"
        else:
            package_count=0
            package_count_string="No packages have been picked up today"
        return package_count_string

    def populate_treeview(self, treeview, data):
        treeview.delete(*treeview.get_children())
        for row in data:
            treeview.insert("", "end", values=row)

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

class DataScreen(NavGUI):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame

        input_frame=ctk.CTkFrame(self.main_frame, width=300, height=400, fg_color=("#d3d3d3", "#191919"))
        input_frame.pack(side="left", fill="y")

        input_add_frame=ctk.CTkFrame(input_frame, height=200)
        input_add_frame.pack(fill="y", expand=True, padx=10, pady=10)
        input_search_frame=ctk.CTkFrame(input_frame, height=200)
        input_search_frame.pack(fill="y", expand=True, padx=10, pady=10)

        tree_frame=ctk.CTkFrame(self.main_frame, width=600, height=400, fg_color=("#d3d3d3", "#191919"))
        tree_frame.pack(side="right")

        name_search_input=ctk.CTkEntry(input_search_frame, placeholder_text="Cadet Name")
        name_search_input.pack(side="top", padx=10, pady=10)
        box_search_input=ctk.CTkEntry(input_search_frame, placeholder_text="Box Number")
        box_search_input.pack(side="top", padx=10, pady=10)
        track_search_input=ctk.CTkEntry(input_search_frame, placeholder_text="Tracking Number")
        track_search_input.pack(side="top", padx=10, pady=10)
        search_button=ctk.CTkButton(input_search_frame, text="Search", command=self.search)
        search_button.pack(padx=10, pady=(10,0))

        box_add_input=ctk.CTkEntry(input_add_frame, placeholder_text="Box Number")
        box_add_input.pack(side="top", padx=10, pady=10)
        track_add_input=ctk.CTkEntry(input_add_frame, placeholder_text="Tracking Number")
        track_add_input.pack(side="top", padx=10, pady=10)
        add_button=ctk.CTkButton(input_add_frame, text="Add", command=self.add)
        add_button.pack(padx=10, pady=(10,0))

    def search(self):
        print("Search for something")

    def add(self):
        print("Add Something")

        
        
