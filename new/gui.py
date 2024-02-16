import tkinter as tk
from tkinter import ttk, Toplevel
from idlelib.tooltip import Hovertip
from database import Database

class GUI:
    def __init__(self, root, database):
        self.root=root
        self.database=database

        # Tabs
        self.tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='  Add Package  ')
        self.tabControl.add(self.tab2, text='  Search Packages and Retrieve  ')
        self.tabControl.pack(expand=1, fill='both')

        # Tab 1 - Package Entry
        self.package_number = ttk.Entry(self.tab1)
        self.package_number.grid(column=1, row=0, padx=30, pady=30)
        self.package_number_label = ttk.Label(self.tab1, text='Tracking Number').grid(row=0, column=0, padx=10, pady=10)

        self.package_box = ttk.Entry(self.tab1)
        self.package_box.grid(column=1, row=1, padx=30, pady=10)
        self.package_box_label = ttk.Label(self.tab1, text='Box Number').grid(row=1, column=0, padx=10, pady=10)

        self.package_button = ttk.Button(self.tab1, text="Enter Package", command=self.add_package).grid(row=2, column=1, pady=5)

        # Tab 2 - Package Retrieval
        self.search_name = ttk.Entry(self.tab2)
        self.search_name.grid(column=1, row=1, padx=10, pady=10)
        self.search_name_label = ttk.Label(self.tab2, text='Cadet Name').grid(row=1, column=0, padx=10, pady=10)

        self.search_box = ttk.Entry(self.tab2)
        self.search_box.grid(column=1, row=2, padx=10, pady=10)
        self.search_box_label = ttk.Label(self.tab2, text='Box Number').grid(column=0, row=2, padx=10, pady=10)

        self.search_track = ttk.Entry(self.tab2)
        self.search_track.grid(column=1, row=3, padx=10, pady=10)
        self.search_track_label = ttk.Label(self.tab2, text='Tracking Number').grid(column=0, row=3, padx=10, pady=10)

        self.search_button = ttk.Button(self.tab2, text="Search", command=self.populate_table)
        self.search_button.grid(row=4, column=0, columnspan=2)
        self.tooltip = Hovertip(self.search_button, 'Fill out fields to search.\nResults will narrow to match all fields.\nLeave fields blank to exclude them from search.')

        self.table = ttk.Treeview(self.tab2, columns=('track', 'name', 'received', 'picked'), show='headings')
        self.table.heading('track', text='Tracking Number')
        self.table.heading('name', text='Cadet Name')
        self.table.heading('received', text='Received')
        self.table.heading('picked', text='Picked Up')
        self.table.column('track', width=100)
        self.table.column('name', width=150)
        self.table.column('received', width=80)
        self.table.column('picked', width=80)
        self.table.grid(column=3, row=1, padx=20, pady=10, columnspan=1, rowspan=4)

        self.table.bind('<<TreeviewSelect>>', self.item_select)

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
            self.table.insert('', 'end', values(data[1], data[2], data[3], data[4]))

    def item_select(self, _):
        for i in self.table.selection():
            print(self.table.item(i)['values'])

    
