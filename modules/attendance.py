import cv2
import pickle
import face_recognition
import csv
import os
from datetime import datetime
from utils.email_alert import send_absent_email

ENCODINGS_FILE = "models/face_encodings.pkl"
ATTENDANCE_CSV = "csv_files/attendance.csv"
MAIL_LOG = "csv_files/absent_mail_log.csv"


def mark_attendance_from_image(student, frame):
    with open(ENCODINGS_FILE, "rb") as f:
        known_encodings, known_names = pickle.load(f)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ✅ MUST detect locations first
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    status = "Absent"

    for enc in face_encodings:
        matches = face_recognition.compare_faces(
            known_encodings, enc, tolerance=0.45
        )
        if True in matches:
            idx = matches.index(True)
            if known_names[idx] == student:
                status = "Present"
                break

    save_attendance(student, status)
    return status


def save_attendance(student, status):
    os.makedirs("csv_files", exist_ok=True)

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")

    file_exists = os.path.exists(ATTENDANCE_CSV)

    with open(ATTENDANCE_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["student_id", "date", "time", "status"])
        writer.writerow([student, today, time_now, status])

    # ✅ Email only once per day
    if status == "Absent" and not email_sent_today(student, today):
        send_absent_email(student, today, time_now)
        log_email_sent(student, today)


def email_sent_today(student, date):
    if not os.path.exists(MAIL_LOG):
        return False

    with open(MAIL_LOG, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row == [student, date]:
                return True
    return False


def log_email_sent(student, date):
    file_exists = os.path.exists(MAIL_LOG)
    with open(MAIL_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["student_id", "date"])
        writer.writerow([student, date])
