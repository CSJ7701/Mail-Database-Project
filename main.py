import utils
from utils import *


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




root=tk.Tk()
root.geomtry=("400x450")
root.title("Mail Database")

# Define tab system and create tabs
tabControl=ttk.Notebook(root)
tab1=ttk.Frame(tabControl)
tab2=ttk.Frame(tabControl)
tabControl.add(tab1, text='  Add Package  ')
tabControl.add(tab2, text='  Search Packages and Retrieve  ')
tabControl.pack(expand=1, fill='both')

# Tab 1 - Package Entry
package_number = ttk.Entry(tab1)
package_number.grid(column=1, row=0, padx=30, pady=30)
package_number_label=tk.Label(tab1, text='Tracking Number').grid(row=0, column=0, padx=10, pady=10)

package_box = ttk.Entry(tab1)
package_box.grid(column=1, row=1, padx=30, pady=10)
package_box_label=ttk.Label(tab1, text='Box Number').grid(row=1, column=0, padx=10, pady=10)

package_button = ttk.Button(tab1, text="Enter Package", command=lambda: add_package(package_box.get(), package_number.get())).grid(row=2, column=1, pady=5)


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
CreateToolTip(search_button, text='Fill out fields to search for a package.\n'
                                  'The system will narrow results to match all fields;\n'
                                  'leave fields blank to exclude them from the search')

table=ttk.Treeview(tab2, columns=('track', 'name', 'received', 'picked'), show = 'headings')
table.heading('track', text='Tracking Number')
table.heading('name', text='Cadet Name')
table.heading('received', text='Received')
table.heading('picked', text='Picked Up')
table.grid(column=3, row=1, padx=20, pady=10, columnspan=1, rowspan=4)

# Events and Items.
def item_select(_):
    #print(table.selection())
    for i in table.selection():
        print(table.item(i)['values'])

table.bind('<<TreeviewSelect>>', item_select)

# Display Window
root.mainloop()


