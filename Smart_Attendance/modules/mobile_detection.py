import cv2
from ultralytics import YOLO
from datetime import datetime
from utils.camera import open_camera, close_camera
from utils.csv_helper import write_csv
from modules.email_service import send_mail

MODEL_PATH = "models/yolov8n.pt"
CSV_FILE = "csv_files/mobile_logs.csv"

def start_mobile_detection():
    model = YOLO(MODEL_PATH)
    cap = open_camera()

    while True:
        ret, frame = cap.read()
        results = model(frame, verbose=False)

        for r in results:
            for cls in r.boxes.cls:
                if int(cls) == 67:  # mobile phone
                    write_csv(
                        CSV_FILE,
                        ["Date", "Time", "Event"],
                        [datetime.now().date(), datetime.now().time(), "Mobile Detected"]
                    )
                    send_mail(
                        "teacher@gmail.com",
                        "Mobile Alert",
                        "A student is using a mobile phone in class"
                    )

        cv2.imshow("Mobile Detection", frame)
        if cv2.waitKey(1) == 27:
            break

    close_camera(cap)
