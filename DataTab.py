import sqlite3
import customtkinter as ctk
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from Screen import Screen
from Email import send_email

class DataScreen(Screen):
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
        try:
            query="INSERT INTO packages(tracking_number, adressee, received, fragile) VALUES (?,?,?,?)"
            self.parent.database.cursor.execute(query, (track, name, date, fragile))
            # self.parent.database.cursor.execute("INSERT INTO packages(tracking_number,adressee,received) VALUES ({track}, '{name}','{date}')".format(track=track, name=name, date=date))
            self.parent.database.conn.commit()
        except sqlite3.IntegrityError as e:
            self.show_error(e)
            return
        self.search()
        send_email(email, name, box, fragile)

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
            time=datetime.now().strftime('%H:%M:%S')
            query='''
                  UPDATE packages
                  SET picked_up = ?, picked_up_time=?
                  WHERE tracking_number = ?
                  '''
            self.parent.database.cursor.execute(query, (date, time, track_num))
        self.parent.database.conn.commit()
        self.search()
