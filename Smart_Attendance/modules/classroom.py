import cv2
import csv
import os
import base64
import numpy as np
from datetime import datetime
from ultralytics import YOLO
import face_recognition
import pickle

print("🔥 Classroom module loaded")

# ================= PATHS =================
ENCODINGS_FILE = "models/face_encodings.pkl"
YOLO_MODEL = "models/yolov8n.pt"
CSV_FILE = "csv_files/classroom_log.csv"

# ================= LOAD MODELS =================
known_encodings, known_names = [], []
if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "rb") as f:
        known_encodings, known_names = pickle.load(f)

yolo = YOLO(YOLO_MODEL)
os.makedirs("csv_files", exist_ok=True)

# ================= MAIN FUNCTION =================
def process_classroom_image(image_data):

    encoded = image_data.split(",")[1]
    frame = cv2.imdecode(
        np.frombuffer(base64.b64decode(encoded), np.uint8),
        cv2.IMREAD_COLOR
    )

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ---------- FACE DETECTION ----------
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    # ---------- MOBILE DETECTION ----------
    phone_boxes = []
    results = yolo(frame, conf=0.35, verbose=False)[0]

    for box in results.boxes:
        label = yolo.names[int(box.cls[0])]
        if label == "cell phone":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            phone_boxes.append((x1, y1, x2, y2))

    response = []

    for (top, right, bottom, left), enc in zip(face_locations, face_encodings):

        # ---------- FACE MATCH ----------
        matches = face_recognition.compare_faces(
            known_encodings, enc, tolerance=0.5
        )
        if True in matches:
            person = known_names[matches.index(True)]
        else:
            person = "Unknown"

        # ---------- MOBILE NEAR FACE ----------
        mobile_detected = False
        face_box = (left, top, right, bottom)

        for (px1, py1, px2, py2) in phone_boxes:
            # If phone overlaps face region → student using phone
            if px2 > face_box[0] and px1 < face_box[2] and py2 > face_box[1] and py1 < face_box[3]:
                mobile_detected = True
                break

        # ---------- LISTENING LOGIC ----------
        # Listening = face detected + NOT using phone
        listening = "Yes" if not mobile_detected else "No"

        save_log(person, mobile_detected, listening)

        response.append({
            "person": person,
            "mobile": "Yes" if mobile_detected else "No",
            "listening": listening
        })

    return response

# ================= CSV LOG =================
def save_log(person, mobile, listening):
    exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow([
                "person", "mobile", "listening", "date", "time"
            ])

        now = datetime.now()
        writer.writerow([
            person,
            "Yes" if mobile else "No",
            listening,
            now.date(),
            now.strftime("%H:%M:%S")
        ])
