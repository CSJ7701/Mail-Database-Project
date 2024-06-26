import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
from datetime import datetime


def send_email(send_to, name, box, fragile=0):
    """
    Send an email notification to a recipient.

    Args:
        send_to (str): Email address for recipient.
        name (str): Name of the recipient.
        box (int): Box Number.
        fragile (int): Flag indicating if the package is fragile or not.
    """
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
  position: relative;
}}
.stripe {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ff8c00 10%, transparent 30%);
}}
.reversestripe {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, transparent 70%, #ff8c00 85%);
}}
.content {{
  padding: 20px;
}}
</style>
</head>
<body>
    <div class="header">
        <div class="stripe"></div>
        <h1>USCGA Mailroom</h1>
        <div class="reversestripe"></div>
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
    # Authenticates the sender using a stored username and password
    server.login(sender_email, sender_password)
    server.send_message(message)
          
