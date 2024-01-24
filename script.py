import sqlite3
import smtplib
from email.mime.text import MIMEText

MailDB = sqlite3.connect("MailDB")
Mail = MailDB.cursor()

test=Mail.execute("SELECT * FROM Cadets")
print(test.fetchall())

def send_mail(subject, body, sender, to, password):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=','.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")


    
