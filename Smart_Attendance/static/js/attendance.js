let stream = null;
let regStream = null;
let selectedStudent = "";

/* ---------------- REGISTER ---------------- */

function startRegCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(s => {
            regStream = s;
            document.getElementById("regVideo").srcObject = s;
        });
}

function captureRegister() {
    const student = document.getElementById("regStudent").value;
    if (!student) {
        alert("Enter student ID like student24");
        return;
    }

    const video = document.getElementById("regVideo");
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    fetch("/register-face", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            student: student,
            image: canvas.toDataURL("image/jpeg")
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("regResult").innerText = data.message;
        regStream.getTracks().forEach(t => t.stop());
    });
}

/* ---------------- ATTENDANCE ---------------- */

document.getElementById("startBtn").onclick = async () => {
    selectedStudent = document.getElementById("student").value;
    if (!selectedStudent) {
        alert("Select a student");
        return;
    }

    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    document.getElementById("video").srcObject = stream;
    document.getElementById("cameraSection").style.display = "block";
};

document.getElementById("captureBtn").onclick = () => {
    const canvas = document.getElementById("canvas");
    const video = document.getElementById("video");
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);

    fetch("/process-attendance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            student: selectedStudent,
            image: canvas.toDataURL("image/jpeg")
        })
    })
    .then(res => res.json())
    .then(data => {
        const result = document.getElementById("result");
        result.innerText = "Attendance: " + data.status;
        result.style.color = data.status === "Present" ? "green" : "red";

        stream.getTracks().forEach(t => t.stop());
        document.getElementById("newBtn").style.display = "block";
    });
};

document.getElementById("newBtn").onclick = () => {
    location.reload();
};
