import sqlite3
import smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import ttk

def DB_Connect(db):
    connection=sqlite3.connect(db)
    cursor=connection.cursor()


def get_cadet_info():
    box=package_box.get()
    name=cursor.execute("select name from cadets where box_number = %s" % box)
    email=cursor.execute("select email from cadets where box_number = %s" % box)
    print("Name: %s, Email: %s, Box: %s" % name, email, box)


def send_mail(subject, body, sender, to, password):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=','.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")


