import cv2
import numpy as np
from datetime import datetime
from modules.emotion_model import build_emotion_model

MODEL_PATH = "models/emotion_model.h5"

EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

def start_emotion_detection():
    model = build_emotion_model()
    model.load_weights(MODEL_PATH)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (48, 48))
        gray = gray / 255.0
        gray = gray.reshape(1, 48, 48, 1)

        emotion = EMOTIONS[np.argmax(model.predict(gray, verbose=0))]

        cv2.putText(frame, emotion, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Emotion Detection", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
