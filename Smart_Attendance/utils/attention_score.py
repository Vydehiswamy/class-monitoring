import pandas as pd

CSV_FILE = "csv_files/classroom_log.csv"

BAD_EMOTIONS = ["Angry", "Sad", "Fear", "Disgust"]

def student_attention_score(student_id):
    df = pd.read_csv(CSV_FILE)
    df = df[df["person"] == student_id]

    if len(df) == 0:
        return 100

    mobile_penalty = len(df[df["mobile"] == "Yes"]) / len(df) * 40
    emotion_penalty = len(df[df["emotion"].isin(BAD_EMOTIONS)]) / len(df) * 60

    score = 100 - (mobile_penalty + emotion_penalty)
    return max(0, round(score, 2))
