from os.path import expanduser
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
            self.root.destroy()
            root=ctk.CTk()
            NavGUI(root, self.database, self.user)
             

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
        self.logout_button.pack(side="bottom", pady=(60,20))

        self.main_frame=ctk.CTkFrame(self.root, width=400, height=300, fg_color=("#d3d3d3","#191919"))
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=(20))

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
        print("SHOW REPORTS HERE")

    def show_settings(self):
        self.clear_main_frame()
        Settings(self.main_frame, self)

    def logout(self):
        print("Logout")
        # DAN implement function here.
        # To give you someplace to start, what this should do is destroy the current open window (saved under variable "self.root")
        # Then you will need to open a new instance of the "loginscreen" class.

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

        self.input_frame=ctk.CTkFrame(self.main_frame, width=300, height=400, fg_color=("#d3d3d3", "#191919"))
        self.input_frame.pack(side="left", fill="y")

        self.input_add_frame=ctk.CTkFrame(self.input_frame, height=200)
        self.input_add_frame.pack(fill="y", expand=True, padx=10, pady=10)
        self.input_search_frame=ctk.CTkFrame(self.input_frame, height=200)
        self.input_search_frame.pack(fill="y", expand=True, padx=10, pady=10)

        self.tree_frame=ctk.CTkFrame(self.main_frame, width=600, height=400, fg_color=("#d3d3d3", "#191919"))
        self.tree_frame.pack(side="right", fill="both", expand=True)
        self.tree=ttk.Treeview(self.tree_frame, columns=('track', 'name', 'received', 'picked'), show='headings', height=15)
        self.tree.heading("#1", text="Tracking Number")
        self.tree.heading("#2", text="Name")
        self.tree.heading("#3", text="Date Received")
        self.tree.heading("#4", text="Date Picked Up")
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

        self.track_search_input.get()
        self.search()

        
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
            self.tree.insert('', 'end', values=(data[1], data[2], data[3], data[4]))
# Fix the search func
    def add(self):
        box=self.box_add_input.get()
        track=self.track_add_input.get()
        name, email=self.get_cadet_info(box)
        print(f"Name:{name}")
        print(f"Email:{email}")
        date=datetime.today().strftime('%Y%b%d')
        query="INSERT INTO packages(tracking_number, adressee, received) VALUES (?,?,?)"
        self.parent.database.cursor.execute(query, (track, name, date))
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
            date=datetime.now().strftime('%Y%b%d').upper()
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
        self.package_tree=ttk.Treeview(self.tree_frame, columns=('track', 'name', 'received', 'picked'), show='headings', height=15)
        self.package_tree.heading("#1", text="Tracking Number")
        self.package_tree.heading("#2", text="Name")
        self.package_tree.heading("#3", text="Date Received")
        self.package_tree.heading("#4", text="Date Picked Up")
        self.package_tree.pack(padx=(0,10), pady=10, fill="both", expand=True)

        self.name_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Cadet Name")
        self.name_search_input.pack(side="top", padx=10, pady=10)
        self.box_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Box Number")
        self.box_search_input.pack(side="top", padx=10, pady=10)
        self.track_search_input=ctk.CTkEntry(self.input_search_frame, placeholder_text="Tracking Number")
        self.track_search_input.pack(side="top", padx=10, pady=10)
        self.search_button=ctk.CTkButton(self.input_search_frame, text="Search", command=self.search)
        self.search_button.pack(padx=10, pady=(10,10))

        self.edit_button=ctk.CTkButton(self.input_action_frame, text="Edit Item", command=self.edit_item)
        self.delete_button=ctk.CTkButton(self.input_action_frame, text="Delete Item", command=self.delete_item)
        self.save_button=ctk.CTkButton(self.input_action_frame, text="Save Edits", command=self.save_edits)
        self.close_edit_button=ctk.CTkButton(self.input_action_frame, text="Close Edits", command=self.close_edits)
        self.delete_button.pack(padx=10, pady=10)
        self.edit_button.pack(padx=10, pady=10)
        self.search()

        # Edit Frame
        self.edit_frame=ctk.CTkFrame(self.tree_frame, fg_color=("#d3d3d3", "#191919"))
        self.edit_left=ctk.CTkFrame(self.edit_frame)
        self.edit_right=ctk.CTkFrame(self.edit_frame)
        self.package_label=ctk.CTkLabel(self.edit_left, text="Package Info")
        self.pack_track_label=ctk.CTkLabel(self.edit_left, text="Tracking Number")
        self.pack_track=ctk.CTkEntry(self.edit_left)
        self.pack_pick_label=ctk.CTkLabel(self.edit_left, text="Retrieved Date")
        self.pack_addr_label=ctk.CTkLabel(self.edit_left, text="Addressee")
        self.pack_addr=ctk.CTkEntry(self.edit_left)
        self.pack_rec_label=ctk.CTkLabel(self.edit_left, text="Received Date")
        self.pack_rec=ctk.CTkEntry(self.edit_left)
        self.pack_pick=ctk.CTkEntry(self.edit_left)
        self.cadet_label=ctk.CTkLabel(self.edit_right, text="Cadet Info")
        self.cadet_name_label=ctk.CTkLabel(self.edit_right, text="Name")
        self.cadet_name=ctk.CTkEntry(self.edit_right)
        self.cadet_box_label=ctk.CTkLabel(self.edit_right, text="Box Number")
        self.cadet_box=ctk.CTkEntry(self.edit_right)
        self.cadet_email_label=ctk.CTkLabel(self.edit_right, text="Email")
        self.cadet_email=ctk.CTkEntry(self.edit_right)
        self.cadet_grad_label=ctk.CTkLabel(self.edit_right, text="Graduation Date")
        self.cadet_grad=ctk.CTkEntry(self.edit_right)
        self.cadet_company_label=ctk.CTkLabel(self.edit_right, text="Company")
        self.cadet_company=ctk.CTkEntry(self.edit_right)

    def search(self):
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
            self.package_tree.insert('', 'end', values=(data[1], data[2], data[3], data[4]))

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
            self.edit_frame.pack_forget()
            self.package_tree.pack(padx=(0,10), pady=10, fill="both", expand=True)
        
        self.search()

    def edit_item(self):
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
        query="SELECT * FROM cadets WHERE name IS ?"
        name_search=self.parent.database.cursor.execute(query, (values[1],))
        cvalues=name_search.fetchall()[0]
        print(cvalues)
        self.package_tree.pack_forget()
        self.edit_frame.pack(fill="both", expand=True)
        self.edit_left.pack(side="left", fill="both", expand=True, padx=(10,5), pady=10)
        self.edit_right.pack(side="right", fill="both", expand=True, padx=(5,10), pady=10)
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

        # Cadet Info
       
        self.cadet_label.pack(side="top", padx=10, pady=10)

        self.cadet_name_label.pack(side="top", padx=10, pady=(10,0), fill="x")
        self.cadet_name.pack(side="top", padx=10, pady=(0,10), fill="x")
        self.cadet_name.delete(0,'end')
        self.cadet_name.insert(0, cvalues[1])
        
        self.cadet_box_label.pack(side="top", padx=10, pady=(10,0), fill="x")
        self.cadet_box.pack(side="top", padx=10, pady=(0,10), fill="x")
        self.cadet_box.delete(0,'end')
        self.cadet_box.insert(0,cvalues[2])

        self.cadet_email_label.pack(side="top", padx=10, pady=(10,0), fill="x")
        self.cadet_email.pack(side="top", padx=10, pady=(0,10), fill="x")
        self.cadet_email.delete(0,'end')
        self.cadet_email.insert(0,cvalues[3])
        
        self.cadet_grad_label.pack(side="top", padx=10, pady=(10,0), fill="x")
        self.cadet_grad.pack(side="top", padx=10, pady=(0,10), fill="x")
        self.cadet_grad.delete(0,'end')
        self.cadet_grad.insert(0,cvalues[4])
       
        self.cadet_company_label.pack(side="top", padx=10, pady=(10,0), fill="x")
        self.cadet_company.pack(side="top", padx=10, pady=(0,10), fill="x")
        self.cadet_company.delete(0,'end')
        self.cadet_company.insert(0,cvalues[5])
        

    def save_edits(self):
        if self.edit_frame.winfo_ismapped():
            print("save")
        else:
            print("Not editing")

    def close_edits(self):
        if self.edit_frame.winfo_ismapped():
            self.edit_frame.pack_forget()
            self.tree.pack(padx=(0,10), pady=10, fill="both", expand=True)
            self.save_button.pack_forget()
            self.close_edit_button.pack_forget()
            self.edit_button.pack(padx=10, pady=10)



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
        
