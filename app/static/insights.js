
async function fetchJSON(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${url}`);
    return res.json();
  } catch (err) {
    console.error(`❌ Fetch failed for ${url}:`, err);
    return [];
  }
}


async function loadSummary() {
  try {
    const data = await fetchJSON("/api/insights/summary");

    document.getElementById("total_jobs").textContent = data.total_jobs ?? "–";
    document.getElementById("companies").textContent = data.unique_companies ?? "–";
    document.getElementById("skills").textContent = data.unique_skills ?? "–";
    document.getElementById("last_update").textContent = data.last_update
      ? new Date(data.last_update).toLocaleString()
      : "N/A";
  } catch (err) {
    console.error("❌ Failed to update summary:", err);
  }
}

// ========== Charts Section ==========

async function renderCharts() {
  const loadingEl = document.getElementById("loading");
  loadingEl.style.display = "block"; // Show loading spinner

  const days = document.getElementById("dateRange").value;
  const skillFilter = document.getElementById("skillFilter").value.trim().toLowerCase();

  try {
    document.querySelectorAll("canvas").forEach(c => c.remove());
    const containers = document.querySelectorAll(".chart-container");
    containers.forEach(container => {
      const canvas = document.createElement("canvas");
      container.appendChild(canvas);
    });

    const [skills, titles, salary, sources, freq] = await Promise.all([
      fetchJSON("/api/insights/top-skills"),
      fetchJSON("/api/insights/top-titles"),
      fetchJSON("/api/insights/salary-ranges"),
      fetchJSON("/api/insights/job-sources"),
      fetchJSON("/api/insights/post-frequency"),
    ]);

    const filteredSkills = skillFilter
      ? skills.filter(s => s.skill.toLowerCase().includes(skillFilter))
      : skills;

    const colors = ["#22d3ee", "#a78bfa", "#f472b6", "#38bdf8", "#c084fc"];
    const safe = (data, msg) => (data.length ? data : [{ label: msg, count: 0 }]);

    new Chart(document.querySelectorAll("canvas")[0], {
      type: "bar",
      data: {
        labels: safe(filteredSkills, "No skills found").map(s => s.skill || s.label),
        datasets: [{
          label: "Count",
          data: safe(filteredSkills, "No skills found").map(s => s.count),
          backgroundColor: colors[0]
        }]
      },
      options: { animation: { duration: 1000 }, plugins: { legend: { display: false } } }
    });

    // Top Job Titles
    new Chart(document.querySelectorAll("canvas")[1], {
      type: "bar",
      data: {
        labels: safe(titles, "No titles found").map(t => t.title || t.label),
        datasets: [{
          label: "Jobs",
          data: safe(titles, "No titles found").map(t => t.count),
          backgroundColor: colors[1]
        }]
      },
      options: { indexAxis: "y", animation: { duration: 1000 }, plugins: { legend: { display: false } } }
    });

    // Salary Range Breakdown
    new Chart(document.querySelectorAll("canvas")[2], {
      type: "bar",
      data: {
        labels: safe(salary, "No salary data").map(r => r.range || r.label),
        datasets: [{
          label: "Count",
          data: safe(salary, "No salary data").map(r => r.count),
          backgroundColor: colors[2]
        }]
      },
      options: { animation: { duration: 1000 }, plugins: { legend: { display: false } } }
    });

    //Job Sources Pie Chart
    new Chart(document.querySelectorAll("canvas")[3], {
      type: "pie",
      data: {
        labels: safe(sources, "No sources found").map(s => s.source || s.label),
        datasets: [{
          data: safe(sources, "No sources found").map(s => s.count),
          backgroundColor: colors
        }]
      },
      options: { animation: { duration: 1500 } }
    });

    // Posting Frequency (Line Chart)
    const cutoffData = freq.slice(-Number(days));
    new Chart(document.querySelectorAll("canvas")[4], {
      type: "line",
      data: {
        labels: safe(cutoffData, "No data").map(d => d.date),
        datasets: [{
          label: "Jobs Posted",
          data: safe(cutoffData, "No data").map(d => d.count),
          borderColor: colors[0],
          tension: 0.3,
          fill: false
        }]
      },
      options: {
        animation: { duration: 1000 },
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      }
    });

  } catch (err) {
    console.error("❌ Failed to render charts:", err);
  } finally {
    loadingEl.style.display = "none";
  }
}

document.getElementById("dateRange").addEventListener("change", renderCharts);

document.getElementById("skillFilter").addEventListener("input", () => {
  clearTimeout(window.filterTimeout);
  window.filterTimeout = setTimeout(renderCharts, 500);
});

document.getElementById("refreshBtn").addEventListener("click", () => {
  loadSummary();
  renderCharts();
});

(async () => {
  const loadingEl = document.getElementById("loading");
  loadingEl.style.display = "block";
  await loadSummary();
  await renderCharts();
  loadingEl.style.display = "none";

  // Auto-refresh every 90s
  setInterval(() => {
    loadSummary();
    renderCharts();
  }, 90000);
})();
