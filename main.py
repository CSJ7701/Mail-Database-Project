import utils
from utils import *

window=tk.Tk()
window.geomtry=("400x450")
window.title("Mail Database")

# Define tab system and create tabs
tabControl=ttk.Notebook(window)
tab1=ttk.Frame(tabControl)
tab2=ttk.Frame(tabControl)
tabControl.add(tab1, text='  Add Package  ')
tabControl.add(tab2, text='  Search Packages and Retrieve  ')
tabControl.pack(expand=1, fill='both')

# Setting up labels and buttons
package_number = ttk.Entry(tab1).grid(column=1, row=0, padx=30, pady=30)
package_number_label=ttk.Label(tab1, text='Tracking Number').grid(row=0, column=0, padx=10, pady=10)
package_box = tk.Entry(tab1)
package_box.grid(column=1, row=1, padx=30, pady=10)
package_box_label=ttk.Label(tab1, text='Box Number').grid(row=1, column=0, padx=10, pady=10)
package_button = ttk.Button(tab1, text="Get Info", command=lambda: get_cadet_info(package_box.get())).grid(row=2, column=1, pady=5)

get_cadet_info(101)

window.mainloop()
