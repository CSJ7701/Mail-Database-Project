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
    

def send_mail(subject, body, sender, to, password):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=','.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")


