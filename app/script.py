import sqlite3
import smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import ttk

connection=sqlite3.connect("Test.db")
cursor=connection.cursor()
# cursor.execute("create table cadets (name TEXT, email TEXT, graduation_date DATE, box_number INTEGER)")
# cursor.execute("create table packages (tracking_number INTEGER, adressee TEXT, received DATE, picked_up DATE)")
# connection.commit()
# connection.close()

# Define root window
window=tk.Tk()
window.geometry("400x450")
window.title("Mail Database")

# Define tab system and create tabs
tabControl=ttk.Notebook(window)
tab1=ttk.Frame(tabControl)
tab2=ttk.Frame(tabControl)
tabControl.add(tab1, text='  Add Package  ')
tabControl.add(tab2, text='  Search Packages and Retrieve  ')
tabControl.pack(expand=1, fill='both')



def get_cadet_info():
    box=package_box.get()
    name=cursor.execute("select name from cadets where box_number = %s" % box)
    email=cursor.execute("select email from cadets where box_number = %s" % box)
    print("Name: %s, Email: %s, Box: %s" % name, email, box)


# Example content for each tab
#ttk.Label(tab1, text="This is a test").grid(column=0, row=0, padx=30, pady=30)
#ttk.Label(tab2, text="This is a TEST").grid(column=0, row=0, padx=30, pady=30)

# Setting up labels and buttons
package_number = ttk.Entry(tab1).grid(column=1, row=0, padx=30, pady=30)
package_number_label=ttk.Label(tab1, text='Tracking Number').grid(row=0, column=0, padx=10, pady=10)
package_box = tk.Entry(tab1)
package_box.grid(column=1, row=1, padx=30, pady=10)
package_box_label=ttk.Label(tab1, text='Box Number').grid(row=1, column=0, padx=10, pady=10)
package_button = ttk.Button(tab1, text="Get Info", command=get_cadet_info).grid(row=2, column=1, pady=5)









def send_mail(subject, body, sender, to, password):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=','.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

window.mainloop()

#if __name__ == '__main__':
#    main()


    
