const API_URL = "http://127.0.0.1:8000/kpis";

let hourChart = null;
let dayChart = null;

// Load KPI Data

async function loadDashboard() {
  const team = document.getElementById("team").value;
  const shift = document.getElementById("shift").value;
  const startDate = document.getElementById("startDate").value;
  const endDate = document.getElementById("endDate").value;

  const params = new URLSearchParams();

  if (team) {
    params.append("team", team);
  }

  if (shift) {
    params.append("shift", shift);
  }

  if (startDate) {
    params.append("start_date", startDate);
  }

  if (endDate) {
    params.append("end_date", endDate);
  }

  try {
    const response = await fetch(`${API_URL}?${params.toString()}`);

    if (!response.ok) {
      const errorData = await response.json();

      throw new Error(errorData.detail || "Failed to load data");
    }

    const data = await response.json();

    updateKPIs(data);

    updateCharts(data);
  } catch (error) {
    console.error(error);

    alert("Could not load dashboard data. Make sure FastAPI is running.");
  }
}

// Update KPI Cards

function updateKPIs(data) {
  document.getElementById("answerRate").textContent = `${data.answer_rate}%`;

  document.getElementById("abandonRate").textContent = `${data.abandon_rate}%`;

  document.getElementById("aht").textContent = data.aht_seconds;

  document.getElementById("awt").textContent = data.awt_seconds;

  document.getElementById("csat").textContent = data.csat;

  document.getElementById("fcr").textContent = `${data.fcr}%`;

  document.getElementById(
    "transferRate"
  ).textContent = `${data.transfer_rate}%`;

  document.getElementById("contactVolume").textContent = data.contact_volume;

  document.getElementById(
    "peakHour"
  ).textContent = `Peak: ${data.peak_hour}:00 (${data.peak_hour_volume} calls)`;

  document.getElementById(
    "peakDay"
  ).textContent = `Peak: ${data.peak_day} (${data.peak_day_volume} calls)`;
}

// Update Charts

function updateCharts(data) {
  updateHourChart(data.contact_volume_by_hour);

  updateDayChart(data.contact_volume_by_day);
}

// Hour Chart

function updateHourChart(hourData) {
  const labels = Object.keys(hourData);

  const values = Object.values(hourData);

  const ctx = document.getElementById("hourChart").getContext("2d");

  if (hourChart) {
    hourChart.destroy();
  }

  hourChart = new Chart(ctx, {
    type: "bar",

    data: {
      labels: labels,

      datasets: [
        {
          label: "Number of Calls",
          data: values,
          borderWidth: 1,
        },
      ],
    },

    options: {
      responsive: true,

      maintainAspectRatio: false,

      plugins: {
        legend: {
          display: false,
        },
      },

      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0,
          },
        },
      },
    },
  });
}

// Day Chart

function updateDayChart(dayData) {
  const labels = Object.keys(dayData);

  const values = Object.values(dayData);

  const ctx = document.getElementById("dayChart").getContext("2d");

  if (dayChart) {
    dayChart.destroy();
  }

  dayChart = new Chart(ctx, {
    type: "line",

    data: {
      labels: labels,

      datasets: [
        {
          label: "Number of Calls",

          data: values,

          tension: 0.3,

          fill: false,

          borderWidth: 2,
        },
      ],
    },

    options: {
      responsive: true,

      maintainAspectRatio: false,

      plugins: {
        legend: {
          display: false,
        },
      },

      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0,
          },
        },
      },
    },
  });
}

// Filter Button

document
  .getElementById("applyFilters")
  .addEventListener("click", loadDashboard);

// Initial Load

loadDashboard();
