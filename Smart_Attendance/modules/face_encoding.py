import os
import pickle
import face_recognition

DATASET_DIR = "datasets"
ENCODINGS_FILE = "models/face_encodings.pkl"


def encode_faces():
    known_encodings = []
    known_names = []

    print("[INFO] Starting face encoding process...")

    for student_name in os.listdir(DATASET_DIR):
        student_path = os.path.join(DATASET_DIR, student_name)

        if not os.path.isdir(student_path):
            continue

        print(f"[INFO] Encoding student: {student_name}")

        for image_name in os.listdir(student_path):
            if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            image_path = os.path.join(student_path, image_name)

            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if not encodings:
                print(f"[WARNING] No face found in {image_path}")
                continue

            known_encodings.append(encodings[0])
            known_names.append(student_name)

    os.makedirs("models", exist_ok=True)
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump((known_encodings, known_names), f)

    print("[SUCCESS] Face encodings saved successfully!")
    print(f"[INFO] Total students encoded : {len(set(known_names))}")
    print(f"[INFO] Total images encoded   : {len(known_encodings)}")


# 🔒 CRITICAL LINE — DO NOT REMOVE
if __name__ == "__main__":
    encode_faces()
