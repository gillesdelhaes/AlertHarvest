import configparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path  # Import Path for handling file paths

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

    return {
        'smtp_server': email_config.get('smtp_server'),
        'smtp_port': email_config.getint('smtp_port'),
        'smtp_username': email_config.get('smtp_username'),
        'smtp_password': email_config.get('smtp_password')
    }

def send_notification(alert, **kwargs):
    email_config = read_email_config()

    # with open('notification_log.txt', 'a') as file:
    #     file.write(str(kwargs) + '\n')

    # Read HTML template
    template_path = Path('notification_config/notification_template.html')
    with template_path.open('r') as template_file:
        html_template = template_file.read()

    # Create the email message
    subject = 'Alert Notification'
    body = html_template.format_map({
        'source': alert.source,
        'location': alert.location,
        'severity': alert.severity,
        'message': alert.message,
        'last_occurrence': alert.last_occurrence
    })
    sender_email = email_config['smtp_username']

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = kwargs.get('to_email')
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))  # Set the content type to HTML

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
        server.starttls()
        server.login(email_config['smtp_username'], email_config['smtp_password'])
        server.sendmail(sender_email, kwargs.get('to_email'), message.as_string())

