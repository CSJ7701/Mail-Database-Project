from os.path import expanduser
from sre_constants import AT_END
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, Toplevel
from customtkinter.windows.widgets import image
from idlelib.tooltip import Hovertip
from database import Database
from login import User
from datetime import datetime
from config import Config
from PIL import Image

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
            for widget in self.root.winfo_children():
                widget.destroy()
            NavGUI(self.root, self.database, self.user)
             

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

class HomeScreen(NavGUI):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame
        home_label=ctk.CTkLabel(self.main_frame, text=f"Welcome {self.parent.user.username}", font=("Helvetica", 18))
        home_label.pack(pady=(50,0))

        datestring=datetime.now()
        datestring=datestring.strftime("%B %d %Y")
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
        data_bottom_frame.pack(side="bottom", fill="both", padx=5, pady=5, expand=True)
        data_bottom_left_frame=ctk.CTkFrame(data_bottom_frame, width=190, height=10)#, fg_color=("#d3d3d3", "#191919"))
        data_bottom_left_frame.pack(side="left", fill="both", padx=5, pady=5, expand=True)
        data_bottom_right_frame=ctk.CTkFrame(data_bottom_frame, width=190, height=10)#, fg_color=("#d3d3d3","#191919"))
        data_bottom_right_frame.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        unretrieved_tree=ttk.Treeview(data_bottom_left_frame, columns=("addressee", "received"))
        unretrieved_tree.heading("#1", text="Name")
        unretrieved_tree.heading("#2", text="Date Received")
        unretrieved_tree['show']='headings'
        unretrieved_tree.pack(side="left", fill="both", expand=True)
        retrieved_tree=ttk.Treeview(data_bottom_right_frame, columns=("addressee", "picked_up"))
        retrieved_tree.heading("#1", text="Name")
        retrieved_tree.heading("#2", text="Date Retrieved")
        retrieved_tree['show']='headings'
        retrieved_tree.pack(side="right", fill="both", expand=True)

        self.populate_treeview(unretrieved_tree, self.unretrieved_packages())
        self.populate_treeview(retrieved_tree, self.retrieved_packages())
        self.Treeview_style()

    def unretrieved_packages(self):
        self.parent.database.cursor.execute("SELECT adressee,received FROM packages WHERE picked_up IS NULL")
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
        self.parent.database.cursor.execute("SELECT adressee, picked_up FROM packages WHERE DATE(picked_up) = DATE('now')")
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

        self.input_frame=ctk.CTkFrame(self.main_frame, width=300, height=400, fg_color=("#d3d3d3", "#191919"))
        self.input_frame.pack(side="left", fill="y")

        self.input_add_frame=ctk.CTkFrame(self.input_frame, height=200)
        self.input_add_frame.pack(fill="y", expand=True, padx=10, pady=10)
        self.input_search_frame=ctk.CTkFrame(self.input_frame, height=200)
        self.input_search_frame.pack(fill="y", expand=True, padx=10, pady=10)

        self.tree_frame=ctk.CTkFrame(self.main_frame, width=600, height=400, fg_color=("#d3d3d3", "#191919"))
        self.tree_frame.pack(side="right", fill="both", expand=True)
        self.tree=ttk.Treeview(self.tree_frame, columns=('track', 'name', 'received', 'picked', 'fragile'), show='headings', height=15)
        self.tree.heading("#1", text="Tracking Number")
        self.tree.heading("#2", text="Name")
        self.tree.heading("#3", text="Date Received")
        self.tree.heading("#4", text="Date Picked Up")
        self.tree.heading("#5", text="Fragile")
        self.tree.pack(padx=(0,10), pady=10, fill="both", expand=True)
        

        self.name_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Cadet Name")
        self.name_search_input.pack(side="top", padx=10, pady=10)
        self.box_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Box Number")
        self.box_search_input.pack(side="top", padx=10, pady=10)
        self.track_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Tracking Number")
        self.track_search_input.pack(side="top", padx=10, pady=10)
        self.search_button=ctk.CTkButton(self.input_search_frame, text="Search", command=self.search)
        self.search_button.pack(padx=10, pady=(10,10))
        self.pickup_button=ctk.CTkButton(self.input_search_frame, text="Pickup", command=self.pickup)
        self.pickup_button.pack(padx=10, pady=10, side="bottom")

        self.box_add_input=ctk.CTkEntry(self.input_add_frame, placeholder_text="Box Number")
        self.box_add_input.pack(side="top", padx=10, pady=10)
        self.track_add_input=ctk.CTkEntry(self.input_add_frame, placeholder_text="Tracking Number")
        self.track_add_input.pack(side="top", padx=10, pady=10)
        self.add_button=ctk.CTkButton(self.input_add_frame, text="Add", command=self.add)
        self.add_button.pack(padx=10, pady=(10,10))
        self.is_fragile=tk.IntVar(self.input_add_frame, 0)
        self.fragile_check=ctk.CTkCheckBox(self.input_add_frame, text="Fragile", variable=self.is_fragile, onvalue=1, offvalue=0)
        self.fragile_check.pack(padx=(0,10), pady=(10))

        # Preview the NAME associated with the box number input.
        # This is an Elwakil Suggestion - Couldn't implement autocomplete, so this is the best I could do
        self.preview_name_label=ctk.CTkLabel(self.input_add_frame, text="Box Owner: ")
        self.preview_name_entry=ctk.CTkLabel(self.input_add_frame, text="")
        self.box_add_input.bind('<KeyRelease>', self.preview_box)

        self.track_search_input.get()
        self.search()


    def preview_box(self, event):
        box=self.box_add_input.get()
        if box:
            self.preview_name_label.pack(side="top", padx=10, pady=(20,0))
            self.preview_name_entry.pack(side="top", padx=10, pady=(0,10))

            query=f"SELECT name FROM cadets WHERE box_number IS {box}"
            self.parent.database.cursor.execute(query)
            result=self.parent.database.cursor.fetchone()
            if result:
                self.preview_name_entry.configure(text=result)
            else:
                self.preview_name_entry.configure(text="Not Found")
        else:
            self.preview_name_label.pack_forget()
            self.preview_name_entry.pack_forget()

        
    def search(self):
        print("Search for something")
        self.tree.delete(*self.tree.get_children())
        name=self.name_search_input.get()
        box=self.box_search_input.get()
        track=self.track_search_input.get()
        query="SELECT * FROM packages WHERE 1=1"
        if name:
            query+=f" AND adressee LIKE '%{name}%'"
        if track:
            query+=f" AND tracking_number LIKE '%{track}%'"
        if box:
            name=self.parent.database.cursor.execute(f"SELECT name FROM cadets WHERE box_number IS '%{box}%'")
            query+=f" AND adressee LIKE '%{name}%'"
        query+=" AND picked_up IS NULL"
        results=self.parent.database.cursor.execute(query)
        results=self.parent.database.cursor.fetchall()
        for data in results:
            self.tree.insert('', 'end', values=(data[1], data[2], data[3], data[4], data[5]))
# Fix the search func
    def add(self):
        box=self.box_add_input.get()
        track=self.track_add_input.get()
        name, email=self.get_cadet_info(box)
        fragile=self.is_fragile.get()
        print(f"Name:{name}")
        print(f"Email:{email}")
        date=datetime.today().strftime('%Y-%m-%d')
        query="INSERT INTO packages(tracking_number, adressee, received, fragile) VALUES (?,?,?,?)"
        self.parent.database.cursor.execute(query, (track, name, date, fragile))
        # self.parent.database.cursor.execute("INSERT INTO packages(tracking_number,adressee,received) VALUES ({track}, '{name}','{date}')".format(track=track, name=name, date=date))
        self.parent.database.conn.commit()
        self.search()

    def get_cadet_info(self, box):
        name = self.parent.database.cursor.execute("SELECT name FROM cadets WHERE box_number = ?", (box,))
        names=self.parent.database.cursor.fetchone()
        if names:
            names=names[0]
        #     names=''.join(item for item in names if item.isalnum())
        #     print(f"Name results from database:{names}")
        else:
            print("No Names")
        email=self.parent.database.cursor.execute("SELECT email FROM cadets WHERE box_number = ?", (box,))
        emails=email.fetchone()
        emails=emails[0]
        return names, emails

    def pickup(self):
        selection=self.tree.selection()
        for item in selection:
            details=self.tree.item(item).get("values")
            track_num=details[0]
            date=datetime.now().strftime('%Y-%m-%d').upper()
            query='''
                  UPDATE packages
                  SET picked_up = ?
                  WHERE tracking_number = ?
                  '''
            self.parent.database.cursor.execute(query, (date, track_num))
        self.parent.database.conn.commit()
        self.search()


class Manage(NavGUI):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame

        self.input_frame=ctk.CTkFrame(self.main_frame, width=300, height=400, fg_color=("#d3d3d3", "#191919"))
        self.input_frame.pack(side="left", fill="y")

        self.input_search_frame=ctk.CTkFrame(self.input_frame, height=200)
        self.input_search_frame.pack(fill="y", expand=True, padx=10, pady=10)
        self.input_action_frame=ctk.CTkFrame(self.input_frame, height=200)
        self.input_action_frame.pack(fill="y", expand=True, padx=10, pady=10)

        self.tree_frame=ctk.CTkFrame(self.main_frame, width=600, height=400, fg_color=("#d3d3d3", "#191919"))
        self.tree_frame.pack(side="right", fill="both", expand=True)

        # Package Tree 
        self.package_tree=ttk.Treeview(self.tree_frame, columns=('track', 'name', 'received', 'picked', 'fragile'), show='headings', height=15)
        self.package_tree.heading("#1", text="Tracking Number")
        self.package_tree.heading("#2", text="Name")
        self.package_tree.heading("#3", text="Date Received")
        self.package_tree.heading("#4", text="Date Picked Up")
        self.package_tree.heading("#5", text="Fragile")
        self.package_tree.pack(padx=(0,10), pady=10, fill="both", expand=True)

        # Package View
        self.name_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Cadet Name")
        self.name_search_input.pack(side="top", padx=10, pady=10)
        self.box_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Box Number")
        self.box_search_input.pack(side="top", padx=10, pady=10)
        self.track_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Tracking Number")
        self.track_search_input.pack(side="top", padx=10, pady=10)
        self.search_packages_button=ctk.CTkButton(self.input_search_frame, text="Search", command=self.search_packages)
        self.search_packages_button.pack(padx=10, pady=(10,10))

        # Cadet Tree
        self.cadet_tree=ttk.Treeview(self.tree_frame, columns=('name', 'box', 'email', 'grad', 'company'), show='headings', height=15)
        self.cadet_tree.heading("#1", text="Name")
        self.cadet_tree.heading("#2", text="Box Num.")
        self.cadet_tree.heading("#3", text="Email")
        self.cadet_tree.heading("#4", text="Grad. Date")
        self.cadet_tree.heading("#5", text="Company")

        # Cadet View
        self.c_name_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Cadet Name")
        self.c_box_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Box Number")
        self.c_email_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Email")
        self.c_grad_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Grad. Date")
        self.c_company_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Company")
        self.search_cadets_button=ctk.CTkButton(self.input_search_frame, text="Search", command=self.search_cadets)

        

        self.edit_button=ctk.CTkButton(self.input_action_frame, text="Edit Item", command=self.edit_item)
        self.delete_button=ctk.CTkButton(self.input_action_frame, text="Delete Item", command=self.delete_item)
        
        self.save_button=ctk.CTkButton(self.input_action_frame, text="Save Edits", command=self.save_edits)
        self.close_edit_button=ctk.CTkButton(self.input_action_frame, text="Close Edits", command=self.close_edits)
        self.delete_button.pack(padx=10, pady=10)
        self.edit_button.pack(padx=10, pady=10)

        self.switch_tree_button=ctk.CTkButton(self.input_action_frame, text="Switch View", command=self.switch_tree)
        self.switch_tree_button.pack(side="bottom", padx=10, pady=10)
        
        self.search_packages()
        self.search_cadets()

        # Edit Frame
        self.edit_frame=ctk.CTkFrame(self.tree_frame, fg_color=("#d3d3d3", "#191919"))

        self.edit_package=ctk.CTkFrame(self.edit_frame)
        self.package_label=ctk.CTkLabel(self.edit_package, text="Package Info")
        self.pack_track_label=ctk.CTkLabel(self.edit_package, text="Tracking Number")
        self.pack_track=ctk.CTkEntry(self.edit_package)
        self.pack_pick_label=ctk.CTkLabel(self.edit_package, text="Retrieved Date")
        self.pack_addr_label=ctk.CTkLabel(self.edit_package, text="Addressee")
        self.pack_addr=ctk.CTkEntry(self.edit_package)
        self.pack_rec_label=ctk.CTkLabel(self.edit_package, text="Received Date")
        self.pack_rec=ctk.CTkEntry(self.edit_package)
        self.pack_pick=ctk.CTkEntry(self.edit_package)
        self.pack_fragile=ctk.CTkCheckBox(self.edit_package, text="Fragile")

        self.edit_cadet=ctk.CTkFrame(self.edit_frame)
        self.cadet_label=ctk.CTkLabel(self.edit_cadet, text="Cadet Info")
        self.cadet_name_label=ctk.CTkLabel(self.edit_cadet, text="Name")
        self.cadet_name=ctk.CTkEntry(self.edit_cadet)
        self.cadet_box_label=ctk.CTkLabel(self.edit_cadet, text="Box Number")
        self.cadet_box=ctk.CTkEntry(self.edit_cadet)
        self.cadet_email_label=ctk.CTkLabel(self.edit_cadet, text="Email")
        self.cadet_email=ctk.CTkEntry(self.edit_cadet)
        self.cadet_grad_label=ctk.CTkLabel(self.edit_cadet, text="Graduation Date")
        self.cadet_grad=ctk.CTkEntry(self.edit_cadet)
        self.cadet_company_label=ctk.CTkLabel(self.edit_cadet, text="Company")
        self.cadet_company=ctk.CTkEntry(self.edit_cadet)

    def search_packages(self):
        print("Search for something")
        self.package_tree.delete(*self.package_tree.get_children())
        name=self.name_search_input.get()
        box=self.box_search_input.get()
        track=self.track_search_input.get()
        query="SELECT * FROM packages WHERE 1=1"
        if name:
            query+=f" AND adressee LIKE '%{name}%'"
        if track:
            query+=f" AND tracking_number LIKE '%{track}%'"
        if box:
            name=self.parent.database.cursor.execute(f"SELECT name FROM cadets WHERE box_number IS '%{box}%'")
            query+=f" AND adressee LIKE '%{name}%'"
        results=self.parent.database.cursor.execute(query)
        results=self.parent.database.cursor.fetchall()
        for data in results:
            self.package_tree.insert('', 'end', values=(data[1], data[2], data[3], data[4], data[5]))

    def search_cadets(self):
        self.cadet_tree.delete(*self.cadet_tree.get_children())
        name=self.c_name_search_input.get()
        box=self.c_box_search_input.get()
        email=self.c_email_search_input.get()
        grad=self.c_grad_search_input.get()
        company=self.c_company_search_input.get()
        query="SELECT * FROM cadets WHERE 1=1"
        if name:
            query+=f" AND name LIKE '%{name}%'"
        if box:
            query+=f" AND box_number LIKE '%{box}%'"
        if email:
            query+=f" AND email LIKE '%{email}%'"
        if grad:
            query+=f" AND graduation_date LIKE '%{grad}%'"
        if company:
            query+=f" AND company LIKE '%{company}%'"
        results=self.parent.database.cursor.execute(query)
        results=self.parent.database.cursor.fetchall()
        for data in results:
            self.cadet_tree.insert('', 'end', values=(data[1], data[2], data[3], data[4], data[5]))

    def delete_item(self):
        selection=self.package_tree.selection()
        for item in selection:
            details=self.package_tree.item(item).get("values")
            track_num=details[0]
            query='''
                  DELETE FROM packages
                  WHERE tracking_number = ?
                  '''
            self.parent.database.cursor.execute(query,(track_num,))
        self.parent.database.conn.commit()

        if self.edit_frame.winfo_ismapped():
            self.close_edits()
        self.search_packages()

    def edit_item(self):
        if self.package_tree.winfo_ismapped():
            self.edit_cadet.pack_forget()

            selected_items=self.package_tree.selection()
            num_selected=len(selected_items)
            if num_selected > 1:
                self.show_error("Too many items selected.")
                return
            if num_selected < 1:
                self.show_error("No items selected.")
                return
            self.edit_button.pack_forget()
            self.save_button.pack(padx=10, pady=10)
            self.close_edit_button.pack(padx=10, pady=10)
            selected_item=selected_items[0]
            values=self.package_tree.item(selected_item, "values")
            self.package_tree.pack_forget()
            self.edit_frame.pack(fill="both", expand=True)
            self.edit_package.pack(side="left", fill="both", expand=True, padx=(10,5), pady=10)
            # Package Info
            self.package_label.pack(side="top", padx=10, pady=10)
            
            self.pack_track_label.pack(side="top", padx=10, pady=(20,0), fill="x")
            self.pack_track.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.pack_track.delete(0,'end')
            self.pack_track.insert(0,values[0])

            self.pack_addr_label.pack(side="top", padx=10, pady=(10,0), fill="x")
            self.pack_addr.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.pack_addr.delete(0,'end')
            self.pack_addr.insert(0,values[1])

            self.pack_rec_label.pack(side="top", padx=10, pady=(10,0), fill="x")
            self.pack_rec.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.pack_rec.delete(0,'end')
            self.pack_rec.insert(0,values[2])

            self.pack_pick_label.pack(side="top", padx=10, pady=(10,0), fill="x")
            self.pack_pick.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.pack_pick.delete(0,'end')
            self.pack_pick.insert(0,values[3])

            self.pack_fragile.pack(side="top", padx=10, pady=(20,0), fill="x")
            if values[4] == '0':
                self.pack_fragile.deselect()
            else:
                self.pack_fragile.select()



        elif self.cadet_tree.winfo_ismapped():
            self.edit_package.pack_forget()

            selected_items=self.cadet_tree.selection()
            num_selected=len(selected_items)
            if num_selected > 1:
                self.show_error("Too many items selected.")
                return
            if num_selected < 1:
                self.show_error("No items selected")
                return
            self.edit_button.pack_forget()
            self.save_button.pack(padx=10, pady=10)
            self.close_edit_button.pack(padx=10, pady=10)
            selected_item=selected_items[0]
            values=self.cadet_tree.item(selected_item, "values")
            self.cadet_tree.pack_forget()

            
            # Cadet Info
            self.edit_frame.pack(fill="both", expand=True)
            self.edit_cadet.pack(side="right", fill="both", expand=True, padx=(5,10), pady=10)
            self.cadet_label.pack(side="top", padx=10, pady=10)
            
            self.cadet_name_label.pack(side="top", padx=10, pady=(10,0), fill="x")
            self.cadet_name.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.cadet_name.delete(0,'end')
            self.cadet_name.insert(0, values[0])
            
            self.cadet_box_label.pack(side="top", padx=10, pady=(10,0), fill="x")
            self.cadet_box.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.cadet_box.delete(0,'end')
            self.cadet_box.insert(0,values[1])
            
            self.cadet_email_label.pack(side="top", padx=10, pady=(10,0), fill="x")
            self.cadet_email.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.cadet_email.delete(0,'end')
            self.cadet_email.insert(0,values[2])
            
            self.cadet_grad_label.pack(side="top", padx=10, pady=(10,0), fill="x")
            self.cadet_grad.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.cadet_grad.delete(0,'end')
            self.cadet_grad.insert(0,values[3])
        
            self.cadet_company_label.pack(side="top", padx=10, pady=(10,0), fill="x")
            self.cadet_company.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.cadet_company.delete(0,'end')
            self.cadet_company.insert(0,values[4])

            # Keep at end
        

    def save_edits(self):
        if self.edit_frame.winfo_ismapped():
            if self.edit_cadet.winfo_ismapped():
                selected_items=self.cadet_tree.selection()
                selected_item=selected_items[0]
                values=self.cadet_tree.item(selected_item, "values")
                name=values[0]
                box=values[1]
                email=values[2]
                grad=values[3]
                company=values[4]
                new_name=self.cadet_name.get()
                new_box=self.cadet_box.get()
                new_email=self.cadet_email.get()
                new_grad=self.cadet_grad.get()
                new_company=self.cadet_company.get()

                query=f'''
                       UPDATE cadets
                       SET
                       name='{new_name}',
                       box_number={new_box},
                       email='{new_email}',
                       graduation_date={new_grad},
                       company='{new_company}'
                       WHERE
                       name='{name}' AND
                       box_number={box} AND
                       email='{email}' AND
                       graduation_date={grad} AND
                       company='{company}';
                       '''
                self.parent.database.cursor.execute(query)
                self.close_edits()
            if self.edit_package.winfo_ismapped():
                selected_items=self.package_tree.selection()
                selected_item=selected_items[0]
                values=self.package_tree.item(selected_item, "values")
                track=values[0]
                addr=values[1]
                received=values[2]
                picked=values[3]
                new_track=self.pack_track.get()
                new_addr=self.pack_addr.get()
                new_received=self.pack_rec.get()
                new_picked=self.pack_pick.get()
                new_fragile=self.pack_fragile.get()
                query=f'''
                       UPDATE packages
                       SET
                       tracking_number={new_track},
                       adressee='{new_addr}',
                       received='{new_received}',
                       picked_up='{new_picked}',
                       fragile={new_fragile}
                       WHERE
                       tracking_number={track} AND
                       adressee='{addr}' AND
                       received='{received}';
                       '''
                print(query)
                self.parent.database.cursor.execute(query)
                self.close_edits()
        else:
            print("Not editing")

    def close_edits(self):
        if self.edit_package.winfo_ismapped():
            self.package_tree.pack(padx=(0,10), pady=10, fill="both", expand=True)
            self.search_packages()
        if self.edit_cadet.winfo_ismapped():
            self.cadet_tree.pack(padx=(0,10), pady=10, fill="both", expand=True)
            self.search_cadets()
        if self.edit_frame.winfo_ismapped():
            self.edit_frame.pack_forget()
            self.save_button.pack_forget()
            self.close_edit_button.pack_forget()
            self.edit_button.pack(padx=10, pady=10)
 

    def switch_tree(self):
        if self.package_tree.winfo_ismapped():

            # Clear old
            self.package_tree.pack_forget()
            self.name_search_input.pack_forget()
            self.box_search_input.pack_forget()
            self.track_search_input.pack_forget()
            self.search_packages_button.pack_forget()

            

            # Pack new
            self.cadet_tree.pack(padx=(0,10), pady=10, fill="both", expand=True)
            self.c_name_search_input.pack(side="top", padx=10, pady=10)
            self.c_box_search_input.pack(side="top", padx=10, pady=10)
            self.c_email_search_input.pack(side="top", padx=10, pady=10)
            self.c_grad_search_input.pack(side="top", padx=10, pady=10)
            self.c_company_search_input.pack(side="top", padx=10, pady=10)
            self.search_cadets_button.pack(padx=10, pady=10)

        if self.cadet_tree.winfo_ismapped():

            # Clear old
            self.cadet_tree.pack_forget()
            self.c_name_search_input.pack_forget()
            self.c_box_search_input.pack_forget()
            self.c_email_search_input.pack_forget()
            self.c_grad_search_input.pack_forget()
            self.c_company_search_input.pack_forget()
            self.search_cadets_button.pack_forget()

            # Pack New
            self.package_tree.pack(padx=(0,10), pady=10, fill="both", expand=True)
            self.name_search_input.pack(side="top", padx=10, pady=10)
            self.box_search_input.pack(side="top", padx=10, pady=10)
            self.track_search_input.pack(side="top", padx=10, pady=10)
            self.search_packages_button.pack(padx=10, pady=10)


class Reports(NavGUI):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame

        self.options_frame=ctk.CTkFrame(self.main_frame, width=300, height=400, fg_color=("#d3d3d3", "#191919"))
        self.options_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        self.choose_report_frame=ctk.CTkFrame(self.options_frame)
        self.choose_report_frame.pack(side="top", padx=10, pady=10, fill="both", expand=True)
        
        self.report_options_frame=ctk.CTkFrame(self.options_frame)
        self.report_options_frame.pack(side="top", padx=10, pady=(0,10), fill="both", expand=True)

        # Choose Report Frame
        self.report_choice=ctk.CTkOptionMenu(self.choose_report_frame)
        self.report_choice.pack(side="top", padx=10, pady=10)


        # Average number of packages per day
        # # Sort by company, class

        # Average number of packages by hour
        # # Sort by company, class

        # Average number of packages by company
        # # Sort by class

        # Average number of packages by class
        # # Sort by company

        # For all of these, can limit time range. 



class Settings(NavGUI):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame
        self.config=self.parent.config

        self.left_frame=ctk.CTkFrame(self.main_frame, width=200, height=400, fg_color=("#d3d3d3", "#000000"))
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        

        self.middle_frame=ctk.CTkFrame(self.main_frame, width=300, height=200, fg_color=("#d3d3d3", "#000000"))
        self.middle_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame=ctk.CTkFrame(self.main_frame, width=300, height=200, fg_color=("#d3d3d3", "#000000"))
        self.right_frame.pack(side="left", fill="y", padx=10, pady=10)

    def ChangeColorMode(self, choice):
        ...
        
