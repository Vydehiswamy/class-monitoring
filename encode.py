import os, pickle
import face_recognition

DATASET_DIR = "datasets"
ENCODINGS_FILE = "models/face_encodings.pkl"

known_encodings = []
known_names = []

for student in os.listdir(DATASET_DIR):
    folder = os.path.join(DATASET_DIR, student)
    for img in os.listdir(folder):
        path = os.path.join(folder, img)
        image = face_recognition.load_image_file(path)
        encs = face_recognition.face_encodings(image)
        if encs:
            known_encodings.append(encs[0])
            known_names.append(student)

with open(ENCODINGS_FILE, "wb") as f:
    pickle.dump((known_encodings, known_names), f)

print("Encodings updated successfully")
