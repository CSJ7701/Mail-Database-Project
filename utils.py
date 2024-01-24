import sqlite3
import smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import ttk
from datetime import datetime

connection=sqlite3.connect("MailDB.db")
cursor=connection.cursor()

def get_cadet_info(box):
    name=cursor.execute("select name from cadets where box_number = ?", (box,))
    names=cursor.fetchall()
    email=cursor.execute("select email from cadets where box_number = ?", (box,))
    emails=cursor.fetchall()
    return names, emails

def add_package(box, track):
    name, email=get_cadet_info(box)
    date=datetime.today().strftime('%Y%b%d')
    # cursor.execute("insert into packages")
    

def send_mail(subject, body, sender, to, password):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=','.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")


