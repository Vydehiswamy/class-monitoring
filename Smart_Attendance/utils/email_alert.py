import smtplib
from email.message import EmailMessage
import csv
import os

EMAIL_ADDRESS = "Vydehiswamy2@gmail.com"
EMAIL_PASSWORD = "svhc emod eadp qgzt"   # app password (no spaces)

STUDENT_EMAILS = "csv_files/student_emails.csv"


def get_student_email(student_id):
    if not os.path.exists(STUDENT_EMAILS):
        print("❌ student_emails.csv not found")
        return None

    with open(STUDENT_EMAILS, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["student_id"] == student_id:
                return row["email"]
    return None


def send_absent_email(student, date, time):
    receiver = get_student_email(student)
    if not receiver:
        print(f"❌ No email found for {student}")
        return

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver
    msg["Subject"] = "⚠️ Attendance Alert – Absent"

    msg.set_content(f"""
Dear Student,

You were marked ABSENT.

Student ID : {student}
Date       : {date}
Time       : {time}

Regards,
Smart Attendance System
""")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {receiver}")

    except Exception as e:
        print("❌ Email sending failed:", e)
    print("📤 Preparing email...")

    receiver = get_student_email(student)
    if not receiver:
        print(f"❌ No email found for {student}")
        return

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver
    msg["Subject"] = "⚠️ Attendance Alert – Absent"

    msg.set_content(f"""
Dear Student,

You were marked ABSENT.

Student ID : {student}
Date       : {date}
Time       : {time}

Regards,
Smart Attendance System
""")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent to {receiver}")

    except Exception as e:
        print("❌ Email sending failed:", e)

    print("📤 Preparing email...")

    receiver = get_student_email(student)
    if not receiver:
        print(f"❌ No email found for {student}")
        return

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver
    msg["Subject"] = "⚠️ Attendance Alert – Absent"

    msg.set_content(
        f"""
Dear Student,

You were marked ABSENT.

Student ID : {student}
Date       : {date}
Time       : {time}

Please contact your faculty if this is incorrect.

Regards,
Smart Attendance System
"""
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {receiver}")

    except Exception as e:
        print("❌ Email sending failed:", e)
