import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from .settings import settings


def send_mail_smtp(sender: str, to: str, msg: MIMEMultipart):
    print(f"send mail from {sender} to {to} over {settings.mail_host}")
    with smtplib.SMTP(host=settings.mail_host, port=settings.mail_port) as server:
        
        if settings.mail_starttls:
            server.starttls()

        try:
            if settings.mail_user:
                server.login(settings.mail_user, settings.mail_password)
            server.sendmail(sender, to, msg.as_string())
        except Exception as e:
            print('Error sending email')
            print(str(e))
        finally:
            server.quit()


def send_mail(to: str, subject: str, html: str, sender: str = None):

    sender = sender or settings.mail_from

    msg = MIMEMultipart('alternative')
    msg['From']    = sender
    msg['Subject'] = subject
    msg['To']      = to

    print("Transport:", settings.mail_transport)
    if settings.mail_transport == "stdout":
        print(html)
    elif settings.mail_transport == "SMTP": 
        msg.attach(MIMEText(html, 'html'))
        send_mail_smtp(sender=sender, to=to, msg=msg)
