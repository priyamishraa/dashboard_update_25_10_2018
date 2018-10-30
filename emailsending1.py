import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from base64 import b64decode


def send_email(userid,passcode,toaddress,sub,body):
    fromaddr = userid
    toaddrs  = str(toaddress)
    msg = MIMEMultipart()
    passcode = b64decode(passcode).decode('ASCII')
    text = MIMEText(body)
    msg['Subject'] = sub
    msg.attach(text)
    
    username = userid
    password = passcode
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()
    #print('e-Mail Sent')
    
    
    
