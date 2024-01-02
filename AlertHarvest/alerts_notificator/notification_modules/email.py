import configparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def read_email_config(file_path='notification_config/email.conf'):
    config = configparser.ConfigParser()
    try:
        with open(file_path, 'r') as config_file:
            config.read_file(config_file)
            email_config = config['EmailConfig']
    except FileNotFoundError:
        print(f"Config file not found: {file_path}")
        return None
    except KeyError:
        print(f"Error reading 'EmailConfig' section from {file_path}")
        return None
    email_config = config['EmailConfig']
    
    smtp_server = email_config.get('smtp_server')
    smtp_port = email_config.getint('smtp_port')
    smtp_username = email_config.get('smtp_username')
    smtp_password = email_config.get('smtp_password')
    to_email = email_config.get('to_email')
    
    return smtp_server, smtp_port, smtp_username, smtp_password, to_email

def send_notification(alert):
    smtp_server, smtp_port, smtp_username, smtp_password, to_email = read_email_config()

    # Create the email message
    subject = 'Alert Notification'
    body = f"Received alert notification: {alert.source}, {alert.location}, {alert.message}, {alert.last_occurrence}"
    sender_email = smtp_username

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, to_email, message.as_string())
