from datetime import datetime
import customtkinter as ctk
# from gui import NavGUI
from tkinter import ttk
from Screen import Screen


class HomeScreen(Screen):
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


