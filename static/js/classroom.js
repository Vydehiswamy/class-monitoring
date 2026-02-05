const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const statusText = document.getElementById("status");

let monitoring = false;

document.getElementById("startBtn").onclick = async () => {
    monitoring = true;
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    captureFrame();
};

function captureFrame() {
    if (!monitoring) return;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    fetch("/process-classroom-frame", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            image: canvas.toDataURL("image/jpeg")
        })
    })
    .then(res => res.json())
    .then(data => {
        statusText.innerText = JSON.stringify(data.result, null, 2);
    });

    setTimeout(captureFrame, 2000);
}
