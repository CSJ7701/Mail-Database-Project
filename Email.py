import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
from datetime import datetime


def send_email(send_to, name, box, fragile=0):
    config=Config('config.ini')
    sender_email=config.system('SENDER_EMAIL')
    sender_password=config.system('SENDER_PASSWORD')
    message=MIMEMultipart()
    message["From"]=sender_email
    message["To"]=send_to
    message["Subject"]='You have a package'

    if fragile == 1:
        fragile_string="\nThis package is fragile."
    else:
        fragile_string=""
    
    NOW=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body=f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>USCGA Mailroom</title>
<style>
  body {{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
    }}
    .header {{
        background-color: #005fae;
        color: #ffffff;
        padding: 20px;
        text-align: center;
    }}
    .content {{
        padding: 20px;
    }}
</style>
</head>
<body>
    <div class="header">
        <h1>USCGA Mailroom</h1>
    </div>
    <div class="content">
        <p>Hello {name},</p>
        <p>A package has arrived for you at box {box}.</p>
        <p>Please come to the mailroom to collect it at your earliest convenience.{fragile_string}</p>
        <p>Regards,</p>
        <p>Mailroom Staff</p>
    </div>
</body>
</html>
"""

    message.attach(MIMEText(body, "html"))

    server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(message)
          
