import sqlite3
import smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import ttk

MailDB = sqlite3.connect("MailDB")
Mail = MailDB.cursor()

#test=Mail.execute("SELECT * FROM Cadets")
#print(test.fetchall())

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

# Example content for each tab
#ttk.Label(tab1, text="This is a test").grid(column=0, row=0, padx=30, pady=30)
#ttk.Label(tab2, text="This is a TEST").grid(column=0, row=0, padx=30, pady=30)

# Setting up labels and buttons
package_number = ttk.Entry(tab1).grid(column=0, row=0, padx=30, pady=30)












window.mainloop()

def send_mail(subject, body, sender, to, password):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=','.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

#if __name__ == '__main__':
#    main()


    
