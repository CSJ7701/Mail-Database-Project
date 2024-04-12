import customtkinter as ctk
from tkinter import ttk
from Screen import Screen

class Manage(Screen):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame

        self.parent.database.cursor.execute(f"SELECT admin FROM accounts WHERE username IS '{self.parent.user.username}'")
        self.user_priviledge=self.parent.database.cursor.fetchone()[0]
        print(self.user_priviledge)

        self.input_frame=ctk.CTkFrame(self.main_frame, width=300, height=400, fg_color=("#d3d3d3", "#191919"))
        self.input_frame.pack(side="left", fill="y")

        self.input_search_frame=ctk.CTkFrame(self.input_frame, height=200)
        self.input_search_frame.pack(fill="y", expand=True, padx=10, pady=10)
        self.input_action_frame=ctk.CTkFrame(self.input_frame, height=200)
        self.input_action_frame.pack(fill="y", expand=True, padx=10, pady=10)

        self.tree_frame=ctk.CTkFrame(self.main_frame, width=600, height=400, fg_color=("#d3d3d3", "#191919"))
        self.tree_frame.pack(side="right", fill="both", expand=True)

        # Package Tree 
        self.package_tree=ttk.Treeview(self.tree_frame, columns=('track', 'name', 'received', 'picked', 'picked_time', 'fragile'), show='headings', height=15)
        self.package_tree.heading("#1", text="Tracking Number")
        self.package_tree.heading("#2", text="Name")
        self.package_tree.heading("#3", text="Date Received")
        self.package_tree.heading("#4", text="Date Picked Up")
        self.package_tree.heading("#5", text="Time Picked Up")
        self.package_tree.heading("#6", text="Fragile")
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
        self.add_cadet_button=ctk.CTkButton(self.input_search_frame, text="Add", command=self.add_cadet)

        

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
        self.pack_addr_label=ctk.CTkLabel(self.edit_package, text="Addressee")
        self.pack_addr=ctk.CTkEntry(self.edit_package)
        self.pack_rec_label=ctk.CTkLabel(self.edit_package, text="Received Date")
        self.pack_rec=ctk.CTkEntry(self.edit_package)
        self.pack_pick_label=ctk.CTkLabel(self.edit_package, text="Retrieved Date")
        self.pack_pick=ctk.CTkEntry(self.edit_package)
        self.pack_pick_time_label=ctk.CTkLabel(self.edit_package, text="Retrieved Time")
        self.pack_pick_time=ctk.CTkEntry(self.edit_package)
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
            self.package_tree.insert('', 'end', values=(data[1], data[2], data[3], data[4], data[5], data[6]))

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

    def add_cadet(self):
        name=self.c_name_search_input.get()
        box=self.c_box_search_input.get()
        email=self.c_email_search_input.get()
        grad=self.c_grad_search_input.get()
        company=self.c_company_search_input.get()
        if not name:
            self.show_error("Name not specified")
            return None
        if not box:
            self.show_error("Box not specified")
            return None
        if not email:
            self.show_error("Email not specified")
            return None
        if not grad:
            self.show_error("Graduation Date not specified")
        if not company:
            self.show_error("Company not specified")
        query=f"INSERT INTO cadets (name, box_number, email, graduation_date, company) VALUES ('{name}', {box}, '{email}', {grad}, '{company}');"
        self.parent.database.cursor.execute(query)
        self.parent.database.conn.commit()
        self.c_name_search_input.delete(0,'end')
        self.c_box_search_input.delete(0,'end')
        self.c_email_search_input.delete(0,'end')
        self.c_grad_search_input.delete(0,'end')
        self.c_company_search_input.delete(0,'end')
        self.search_cadets()

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

            self.pack_pick_time_label.pack(side="top", padx=10, pady=(10,0), fill="x")
            self.pack_pick_time.pack(side="top", padx=10, pady=(0,10), fill="x")
            self.pack_pick_time.delete(0,'end')
            self.pack_pick_time.insert(0,values[4])

            self.pack_fragile.pack(side="top", padx=10, pady=(20,0), fill="x")
            if values[5] == '0':
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
                print(query)
                self.parent.database.cursor.execute(query)
                self.parent.database.conn.commit()
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
                new_picked_time=self.pack_pick_time.get()
                new_fragile=self.pack_fragile.get()
                query=f'''
                       UPDATE packages
                       SET
                       tracking_number={new_track},
                       adressee='{new_addr}',
                       received='{new_received}',
                       picked_up='{new_picked}',
                       picked_up_time='{new_picked_time}',
                       fragile={new_fragile}
                       WHERE
                       tracking_number={track} AND
                       adressee='{addr}' AND
                       received='{received}';
                       '''
                print(query)
                self.parent.database.cursor.execute(query)
                self.parent.database.conn.commit()
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
            self.add_cadet_button.pack(padx=10, pady=10)

        if self.cadet_tree.winfo_ismapped():

            # Clear old
            self.cadet_tree.pack_forget()
            self.c_name_search_input.pack_forget()
            self.c_box_search_input.pack_forget()
            self.c_email_search_input.pack_forget()
            self.c_grad_search_input.pack_forget()
            self.c_company_search_input.pack_forget()
            self.search_cadets_button.pack_forget()
            self.add_cadet_button.pack_forget()

            # Pack New
            self.package_tree.pack(padx=(0,10), pady=10, fill="both", expand=True)
            self.name_search_input.pack(side="top", padx=10, pady=10)
            self.box_search_input.pack(side="top", padx=10, pady=10)
            self.track_search_input.pack(side="top", padx=10, pady=10)
            self.search_packages_button.pack(padx=10, pady=10)
