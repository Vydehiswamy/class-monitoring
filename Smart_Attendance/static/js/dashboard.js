fetch("/dashboard-data")
  .then(res => res.json())
  .then(data => {

    // ================= ATTENDANCE =================
    new Chart(document.getElementById("attendanceChart"), {
      type: "bar",
      data: {
        labels: ["Present", "Absent"],
        datasets: [{
          label: "Attendance Count",
          data: [data.attendance.present, data.attendance.absent],
          backgroundColor: ["green", "red"]
        }]
      }
    });

    // ================= PHONE USAGE =================
    document.getElementById("phoneUsageText").innerText =
      data.phone_usage + "%";

    new Chart(document.getElementById("phoneChart"), {
      type: "pie",
      data: {
        labels: ["Using Phone", "Not Using Phone"],
        datasets: [{
          data: [data.phone_usage, 100 - data.phone_usage],
          backgroundColor: ["orange", "lightgreen"]
        }]
      }
    });

    // ================= ATTENTION =================
    new Chart(document.getElementById("attentionChart"), {
      type: "bar",
      data: {
        labels: Object.keys(data.attention_scores),
        datasets: [{
          label: "Attention %",
          data: Object.values(data.attention_scores),
          backgroundColor: "blue"
        }]
      },
      options: {
        indexAxis: "y"
      }
    });

  });
