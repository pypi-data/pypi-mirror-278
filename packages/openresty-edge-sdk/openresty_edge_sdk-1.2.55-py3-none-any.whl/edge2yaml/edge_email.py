import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from .utils import error, warn, info
from .read_config import read_yaml_file

def read_email_configs(config_file):
    if not os.path.exists(config_file):
        return None

    configs = read_yaml_file(config_file)
    if configs is None:
        return None

    if 'sender' not in configs:
        error(f"sender not found in email config file: {config_file}")

    if 'password' not in configs:
        error(f"sender password not found in email config file: {config_file}")

    if 'new_user_email_template' not in configs:
        error(f"email template not found in email config file: {config_file}")

    email_template = configs.get('new_user_email_template', None)
    if 'subject' not in email_template:
        error(f"email template subject not found in email config file: {config_file}")

    if 'content' not in email_template:
        error(f"email template content not found in email config file: {config_file}")

    if 'smtp_server' not in configs:
        error(f"smtp server not found in email config file: {config_file}")

    if 'smtp_port' not in configs:
        warn(f"smtp port not found in email config file: {config_file}, using default port: 587")

    return configs

def send_email(configs, receiver, subject, content):
    sender = configs['sender']
    password = configs['password']
    smtp_server = configs['smtp_server']
    smtp_port = configs.get('smtp_port', 587)

    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    res = False
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()

        smtp.login(sender, password)

        smtp.sendmail(sender, receiver, message.as_string())
        info("send email to " + receiver + " success")
        res = True
    except smtplib.SMTPException as e:
        warn("send email to " + receiver + " failed: " + str(e))
    finally:
        smtp.quit()

    return res
