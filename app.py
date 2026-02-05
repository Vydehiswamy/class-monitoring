from flask import Flask, render_template, jsonify, session, redirect, url_for, request
from datetime import datetime
import csv
import os
import base64
import numpy as np
import cv2

from modules.attendance import mark_attendance_from_image
from modules.classroom import process_classroom_image

app = Flask(__name__)
app.secret_key = "your-secret-key-here"

ADMIN_CSV = "csv_files/admin_users.csv"


# ================== INIT ADMIN CSV ==================
def init_admin_csv():
    os.makedirs("csv_files", exist_ok=True)
    if not os.path.exists(ADMIN_CSV):
        with open(ADMIN_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "email", "password"])


# ================== AUTH HELPERS ==================
def get_admin_by_email(email):
    init_admin_csv()
    with open(ADMIN_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"] == email:
                return row
    return None


# ================== ROUTES ==================

@app.route("/")
def index():
    if session.get("admin"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    init_admin_csv()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        admin = get_admin_by_email(email)

        if admin and admin["password"] == password:
            session.clear()
            session["admin"] = email
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    init_admin_csv()

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # prevent duplicate email
        if get_admin_by_email(email):
            return render_template(
                "register.html",
                error="Email already registered"
            )

        with open(ADMIN_CSV, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([username, email, password])

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))

    current_time = datetime.now()
    return render_template("dashboard.html", current_time=current_time)


# ---------------- ATTENDANCE ----------------
@app.route("/attendance")
def attendance():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("attendance.html")


@app.route("/process-attendance", methods=["POST"])
def process_attendance():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    student = data["student"]
    image_data = data["image"]

    encoded = image_data.split(",")[1]
    img_bytes = base64.b64decode(encoded)
    frame = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    status = mark_attendance_from_image(student, frame)
    return jsonify({"status": status})


# ---------------- CLASSROOM ----------------
@app.route("/classroom")
def classroom():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("classroom.html")


@app.route("/process-classroom-frame", methods=["POST"])
def process_classroom_frame():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    image = data.get("image")
    result = process_classroom_image(image)
    return jsonify({"result": result})


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
