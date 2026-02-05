import pandas as pd
import matplotlib.pyplot as plt

ATTENDANCE_CSV = "csv_files/attendance.csv"

def attendance_pie_chart():
    df = pd.read_csv(ATTENDANCE_CSV)
    counts = df["status"].value_counts()

    plt.figure()
    counts.plot.pie(autopct="%1.1f%%")
    plt.title("Attendance Distribution")
    plt.ylabel("")
    plt.savefig("static/charts/attendance_pie.png")
    plt.close()
