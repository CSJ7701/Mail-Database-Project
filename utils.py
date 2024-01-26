import sqlite3
import smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
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

class ToolTip(object):
    def __init__(self,widget):
        self.widget=widget
        self.tipwindow=None
        self.id=None
        self.x=self.y=0
    def showtip(self,text):
        "Display text in tooltip window"
        self.text=text
        if self.tipwindow or not self.text:
            return
        x,y,cx,cy=self.widget.bbox("insert")
        x=x+self.widget.winfo_rootx()+57
        y=y+cy+self.widget.winfo_rooty()+27
        self.tipwindow=tw=Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x,y))
        label=ttk.Label(tw,text=self.text,justify='left',relief='solid',borderwidth=1)
        label.pack(ipadx=1)
    def hidetip(self):
        tw=self.tipwindow
        self.tipwindow=None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    tooltip=ToolTip(widget)
    def enter(event):
        tooltip.showtip(text)
    def leave(event):
        tooltip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def find_in_db(var):
    cursor.execute("SELECT * FROM packages WHERE adressee LIKE (?)", ('%'+var+'%',))

def send_mail(subject, body, sender, to, password):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=','.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")


