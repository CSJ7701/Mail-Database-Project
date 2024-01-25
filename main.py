import utils
from utils import *

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
search_box=ttk.Entry(tab2)
search_box.grid(column=1, row=0, padx=10, pady=10)
search_box_label=ttk.Label(tab2, text='Enter Cadet Name').grid(row=0, column=0, padx=10, pady=10)

# Display Window
root.mainloop()


