import sqlite3
import smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import ttk, Toplevel
from idlelib.tooltip import Hovertip
from datetime import datetime


# ===== Function Definitions =====

def get_cadet_info(box):
    name=cursor.execute("select name from cadets where box_number = ?", (box,))
    names=cursor.fetchone()
    names=''.join(item for item in names if item.isalnum())
    email=cursor.execute("select email from cadets where box_number = ?", (box,))
    emails=cursor.fetchall()
    #print("Box for", (names))
    return names, emails

def add_package(box, track):
    name, email=get_cadet_info(box)
    date=datetime.today().strftime('%Y%b%d')
    cursor.execute("insert into packages(tracking_number,adressee,received) values ({track},'{name}','{date}')".format(track=track, name=name, date=date))
    connection.commit()

def find_in_db(var):
    cursor.execute("SELECT * FROM packages WHERE adressee LIKE (?)", ('%'+var+'%',))
    
def populate_table(name=None, box=None, track=None):
    table.delete(*table.get_children())
    query="SELECT * FROM packages WHERE 1=1"
    if name:
        query+=f" AND adressee LIKE '%{name}%'"
    if track:
        query+=f" AND tracking_number LIKE '%{track}%'"
    if box:
        query+=f" AND box_number LIKE '%{box}%'"
    results=cursor.execute(query)
    results=cursor.fetchall()
    for data in results:
        table.insert('', 'end', values=(data[1], data[2], data[3], data[4]))

def send_mail(subject, body, sender, to, password):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=','.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

# ===== Defining the GUI =====

connection=sqlite3.connect("MailDB.db") # Connects to the database
cursor=connection.cursor() # Cursor is what actually allows you to interact with the database. 

root=tk.Tk() # Establishes a "root window" that all other elements are placed in
root.geometry=("500x450") # Sets dimensions for the root window
root.title("Mail Database") # Sets the Title

# Define tab system and create tabs
tabControl=ttk.Notebook(root) # Defines a tab system within the root window
tab1=ttk.Frame(tabControl) # Creates a tab named 'tab1'
tab2=ttk.Frame(tabControl) # Creates a tab names 'tab2'
tabControl.add(tab1, text='  Add Package  ') # Defines the label for 'tab1'
tabControl.add(tab2, text='  Search Packages and Retrieve  ') # Label for 'tab2'
tabControl.pack(expand=1, fill='both') # Places the tabs into the root window

# Tab 1 - Package Entry
package_number = ttk.Entry(tab1) # Creates an entry field in tab1
package_number.grid(column=1, row=0, padx=30, pady=30) # Places the entry field
package_number_label=ttk.Label(tab1, text='Tracking Number').grid(row=0, column=0, padx=10, pady=10) # Creates and places a label next to the entry field

package_box = ttk.Entry(tab1) # Repeat above steps
package_box.grid(column=1, row=1, padx=30, pady=10)
package_box_label=ttk.Label(tab1, text='Box Number').grid(row=1, column=0, padx=10, pady=10)

package_button = ttk.Button(tab1, text="Enter Package", command=lambda: add_package(package_box.get(), package_number.get())).grid(row=2, column=1, pady=5) # Creates and places a button in tab1


# Tab 2 - Package Retrieval

search_name=ttk.Entry(tab2)
search_name.grid(column=1, row=1, padx=10, pady=10)
search_name_label=ttk.Label(tab2, text='Cadet Name').grid(row=1, column=0, padx=10, pady=10)
search_box=ttk.Entry(tab2)
search_box.grid(column=1, row=2, padx=10, pady=10)
search_box_label=ttk.Label(tab2, text='Box Number').grid(column=0, row=2, padx=10, pady=10)
search_track=ttk.Entry(tab2)
search_track.grid(column=1, row=3, padx=10, pady=10)
search_track_label=ttk.Label(tab2, text='Tracking Number').grid(column=0, row=3, padx=10, pady=10)

search_button=ttk.Button(tab2, text="Search", command=lambda: populate_table(name=search_name.get(), box=search_box.get(), track=search_track.get()))
search_button.grid(row=4, column=0, columnspan=2)
tooltip=Hovertip(search_button, 'Fill out fields to search.\nResults will narrow to match all fields.\nLeave fields blank to exclude them from search.')

table=ttk.Treeview(tab2, columns=('track', 'name', 'received', 'picked'), show = 'headings') # Creates a table in tab2
table.heading('track', text='Tracking Number')
table.heading('name', text='Cadet Name')
table.heading('received', text='Received')
table.heading('picked', text='Picked Up') # Names 4 columns in the table
table.column('track', width=100)
table.column('name', width=150)
table.column('received', width=80)
table.column('picked', width=80) # Sets column widths
table.grid(column=3, row=1, padx=20, pady=10, columnspan=1, rowspan=4) # Sets table dimensions

# Events and Items.
## Not finished yet. Currently prints selection to terminal.
## Goal is for this to let select, then use button to accomplish an action on the selected items.
def item_select(_):
    #print(table.selection())
    for i in table.selection():
        print(table.item(i)['values'])

table.bind('<<TreeviewSelect>>', item_select)



# Appearance
style=ttk.Style()
style.theme_use("clam")

## Treeview
style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25, fieldbackground="#d3d3d3")

# Display Window
root.mainloop()


