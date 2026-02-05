import pandas as pd

CSV_FILE = "csv_files/classroom_log.csv"

def phone_usage_percentage():
    df = pd.read_csv(CSV_FILE)
    total = len(df)
    phone_yes = len(df[df["mobile"] == "Yes"])

    if total == 0:
        return 0

    return round((phone_yes / total) * 100, 2)
