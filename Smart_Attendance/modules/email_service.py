import smtplib
from email.mime.text import MIMEText
from config import EMAIL, EMAIL_PASSWORD

def send_mail(to, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
