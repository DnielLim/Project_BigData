// OmniData Big Data Studio Client Controller v2.0
let charts = {};

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  initSeedProfiler();
  initSynthesizer();
  initCleansing();
  initBenchmark();
  initAnalytics();
  initGovernance();
  initCleanDataExplorer();
  loadOverview();
  initOverviewCharts();
});

// Toast notification helper
function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = "toast";
  let icon = "ℹ️";
  if (type === "success") icon = "✅";
  if (type === "error") icon = "❌";
  if (type === "warning") icon = "⚠️";
  
  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Download chart as PNG image
window.downloadChart = function(canvasId, filename = "chart.png") {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const link = document.createElement("a");
  link.download = filename;
  link.href = canvas.toDataURL("image/png");
  link.click();
  showToast(`Chart disimpan sebagai ${filename}`, "success");
};

// 1. Navigation
function initNavigation() {
  const navItems = document.querySelectorAll(".nav-item");
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      navItems.forEach(n => n.classList.remove("active"));
      item.classList.add("active");
      
      const tabId = item.getAttribute("data-tab");
      document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
      const activePane = document.getElementById(tabId);
      if (activePane) activePane.classList.add("active");

      // Auto load clean data when opening cleansing tab
      if (tabId === "tab-cleansing") {
        document.getElementById("cleansing-empty-notice").style.display = "none";
        document.getElementById("cleansing-dashboard").style.display = "block";
        if (typeof window.loadCleanData === "function") {
          window.loadCleanData();
        }
      }

      // Update Topbar Title
      const titles = {
        "tab-overview": "Big Data Planning Canvas & Architecture",
        "tab-seed": "Seed Data Profiler (/Data)",
        "tab-synthesizer": "Synthetic Data Generator & Veracity Injector",
        "tab-cleansing": "Data Cleansing & Veracity Audit",
        "tab-benchmark": "Storage Footprint & Query Latency Benchmark",
        "tab-analytics": "Advanced Analytics & Distributed PySpark",
        "tab-governance": "Data Governance, Ethics & PII Anonymization",
        "tab-deliverables": "Deliverables Hub & File Exports"
      };
      if (titles[tabId]) {
        document.getElementById("page-title").innerText = titles[tabId];
      }
    });
  });
}

// 2. Overview Loader & Visual Charts
async function loadOverview() {
  try {
    const res = await fetch("/api/overview");
    const data = await res.json();
    if (data.seed_info && data.seed_info.online_retail && data.seed_info.online_retail.rows) {
      document.getElementById("kpi-fact-val").innerText = Number(data.seed_info.online_retail.rows).toLocaleString() + "+";
    }
  } catch (err) {
    console.error("Failed to load overview:", err);
  }
}

function initOverviewCharts() {
  // Chart 1: Big Data 5V Radar
  const ctxRadar = document.getElementById("chart-5v-radar");
  if (ctxRadar) {
    charts.radar5v = new Chart(ctxRadar.getContext("2d"), {
      type: "radar",
      data: {
        labels: ["Volume (1M+ rows)", "Velocity (Clickstream)", "Variety (Relational + JSON)", "Veracity (Cleansing)", "Value (RFM & Cohort)"],
        datasets: [{
          label: "Big Data Maturity Score (%)",
          data: [98, 92, 96, 91, 95],
          backgroundColor: "rgba(99, 102, 241, 0.25)",
          borderColor: "#6366f1",
          pointBackgroundColor: "#06b6d4",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "#06b6d4"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          r: {
            angleLines: { color: "rgba(255, 255, 255, 0.1)" },
            grid: { color: "rgba(255, 255, 255, 0.08)" },
            pointLabels: { color: "#94a3b8", font: { size: 11, weight: "600" } },
            ticks: { display: false, min: 50, max: 100 }
          }
        }
      }
    });
  }

  // Chart 2: Entity Volume Breakdown
  const ctxVolume = document.getElementById("chart-entity-volume");
  if (ctxVolume) {
    charts.entityVolume = new Chart(ctxVolume.getContext("2d"), {
      type: "doughnut",
      data: {
        labels: ["Fact Transactions (1M)", "Clickstream Events (200k)", "Dim Customers (50k)"],
        datasets: [{
          data: [1000000, 200000, 50000],
          backgroundColor: ["#6366f1", "#06b6d4", "#10b981"],
          borderWidth: 0,
          hoverOffset: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: { color: "#cbd5e1", font: { size: 12 }, padding: 16 }
          }
        },
        cutout: "65%"
      }
    });
  }
}

// 3. Seed Profiler
function initSeedProfiler() {
  const btnRefresh = document.getElementById("btn-refresh-seed");
  const btnRetail = document.getElementById("btn-show-retail");
  const btnEshop = document.getElementById("btn-show-eshop");

  async function loadSeedMeta() {
    try {
      const res = await fetch("/api/overview");
      const d = await res.json();
      const ret = d.seed_info.online_retail;
      const esh = d.seed_info.eshop_clothing;

      const retStats = document.getElementById("seed-retail-stats");
      if (ret.rows) {
        retStats.innerHTML = `<strong>Rows:</strong> ${Number(ret.rows).toLocaleString()} | <strong>Columns (${ret.cols.length}):</strong> ${ret.cols.slice(0, 5).join(", ")}...`;
      } else {
        retStats.innerText = "Status: " + ret.status;
      }

      const eshStats = document.getElementById("seed-eshop-stats");
      if (esh.rows) {
        eshStats.innerHTML = `<strong>Rows:</strong> ${Number(esh.rows).toLocaleString()} | <strong>Columns (${esh.cols.length}):</strong> ${esh.cols.slice(0, 5).join(", ")}...`;
      } else {
        eshStats.innerText = "Status: " + esh.status;
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function loadSample(dataset) {
    try {
      const res = await fetch(`/api/seed-data?dataset=${dataset}&limit=6`);
      const d = await res.json();
      renderTable("seed-table-head", "seed-table-body", d.data);
    } catch (e) {
      showToast("Gagal memuat sample data: " + e.message, "error");
    }
  }

  btnRefresh.addEventListener("click", () => {
    loadSeedMeta();
    loadSample("online_retail");
    showToast("Seed data metadata refreshed!", "success");
  });

  btnRetail.addEventListener("click", () => loadSample("online_retail"));
  btnEshop.addEventListener("click", () => loadSample("eshop_clothing"));

  // Initial load
  loadSeedMeta();
  loadSample("online_retail");
}

// Generic table renderer
function renderTable(headId, bodyId, records) {
  const head = document.getElementById(headId);
  const body = document.getElementById(bodyId);
  head.innerHTML = "";
  body.innerHTML = "";

  if (!records || records.length === 0) {
    body.innerHTML = "<tr><td colspan='100%'>Tidak ada data.</td></tr>";
    return;
  }

  const columns = Object.keys(records[0]);
  let headHtml = "<tr>";
  columns.forEach(col => {
    headHtml += `<th>${col}</th>`;
  });
  headHtml += "</tr>";
  head.innerHTML = headHtml;

  let bodyHtml = "";
  records.forEach(row => {
    bodyHtml += "<tr>";
    columns.forEach(col => {
      let val = row[col];
      if (val === null || val === undefined) val = "<span style='color: var(--accent-rose); font-weight: 600;'>NULL</span>";
      bodyHtml += `<td>${val}</td>`;
    });
    bodyHtml += "</tr>";
  });
  body.innerHTML = bodyHtml;
}

// 4. Synthesizer
function initSynthesizer() {
  const dirtySlider = document.getElementById("synth-dirty-rate");
  const dirtyVal = document.getElementById("dirty-rate-val");
  const btnGenerate = document.getElementById("btn-generate-data");
  const synthStatus = document.getElementById("synth-status");
  const synthResults = document.getElementById("synth-results");

  dirtySlider.addEventListener("input", () => {
    dirtyVal.innerText = Math.round(dirtySlider.value * 100) + "%";
  });

  btnGenerate.addEventListener("click", async () => {
    const factRows = parseInt(document.getElementById("synth-fact-rows").value);
    const custRows = parseInt(document.getElementById("synth-cust-rows").value);
    const clickEvents = parseInt(document.getElementById("synth-click-events").value);
    const dirtyRate = parseFloat(dirtySlider.value);

    btnGenerate.disabled = true;
    synthStatus.innerText = "⏳ Sedang mensintesis dataset (ini membutuhkan beberapa detik)...";
    showToast("Memulai Data Synthesizer...", "info");

    try {
      const res = await fetch("/api/generate-synthetic", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fact_rows: factRows,
          customer_rows: custRows,
          clickstream_events: clickEvents,
          dirty_rate: dirtyRate
        })
      });
      const data = await res.json();
      if (data.status === "success") {
        synthStatus.innerText = "✅ Selesai!";
        synthResults.style.display = "block";
        showToast("Dataset sintetis 1M+ berhasil dibuat!", "success");
      } else {
        throw new Error(data.detail || "Gagal membuat dataset");
      }
    } catch (e) {
      synthStatus.innerText = "❌ Terjadi error: " + e.message;
      showToast(e.message, "error");
    } finally {
      btnGenerate.disabled = false;
    }
  });
}

// 5. Cleansing
function initCleansing() {
  const btnClean = document.getElementById("btn-run-cleansing");
  btnClean.addEventListener("click", async () => {
    btnClean.disabled = true;
    btnClean.innerText = "⏳ Memproses Cleansing Pipeline...";
    showToast("Menjalankan pipeline data cleansing & veracity check...", "info");

    try {
      const res = await fetch("/api/run-cleansing", { method: "POST" });
      const d = await res.json();
      if (d.status === "success") {
        const audit = d.audit;
        document.getElementById("cleansing-empty-notice").style.display = "none";
        document.getElementById("cleansing-dashboard").style.display = "block";

        document.getElementById("audit-raw-rows").innerText = Number(audit.total_raw_rows).toLocaleString() + " baris";
        document.getElementById("audit-anomalies").innerText = Number(audit.anomalies_removed).toLocaleString() + " baris";
        document.getElementById("audit-score").innerText = audit.veracity_score + "%";

        // Animate circular gauge
        const gaugeCircle = document.getElementById("gauge-circle");
        if (gaugeCircle) {
          const circumference = 2 * Math.PI * 50; // 314
          const offset = circumference - (circumference * (audit.veracity_score / 100));
          gaugeCircle.style.strokeDashoffset = offset;
        }

        // Render anomaly breakdown
        const b = audit.dirty_breakdown;
        const breakdownHtml = `
          <tr>
            <td>Missing Customer ID (Null)</td>
            <td><code>customer_id: null</code></td>
            <td style="color: var(--accent-rose); font-weight: 700;">${Number(b.missing_customer_ids).toLocaleString()}</td>
            <td><span class="badge badge-emerald">Filtered Out</span></td>
          </tr>
          <tr>
            <td>Missing Timestamp / Category</td>
            <td><code>timestamp: null, category: null</code></td>
            <td style="color: var(--accent-rose); font-weight: 700;">${Number(b.missing_timestamps + b.missing_categories).toLocaleString()}</td>
            <td><span class="badge badge-emerald">Filtered Out</span></td>
          </tr>
          <tr>
            <td>Outlier Negatif (Price & Qty)</td>
            <td><code>price: -150000, quantity: -2</code></td>
            <td style="color: var(--accent-rose); font-weight: 700;">${Number(b.negative_prices + b.negative_quantities).toLocaleString()}</td>
            <td><span class="badge badge-emerald">Filtered Out</span></td>
          </tr>
          <tr>
            <td>Duplikasi Transaction ID</td>
            <td><code>duplicate transaction_id</code></td>
            <td style="color: var(--accent-rose); font-weight: 700;">${Number(b.duplicate_transactions).toLocaleString()}</td>
            <td><span class="badge badge-emerald">Deduplicated (Window Qualify)</span></td>
          </tr>
          <tr>
            <td>Inconsistent String Kota</td>
            <td><code>JKT, dki jakarta, SBY, BDG</code></td>
            <td style="color: var(--accent-amber); font-weight: 700;">${Number(b.city_inconsistencies_fixed).toLocaleString()}</td>
            <td><span class="badge badge-primary">Normalized to Canonical Name</span></td>
          </tr>
        `;
        document.getElementById("cleansing-breakdown-body").innerHTML = breakdownHtml;

        // Refresh full clean data explorer
        if (typeof window.loadCleanData === "function") {
          window.loadCleanData();
        }
        showToast("Data Cleansing berhasil diselesaikan!", "success");
      }
    } catch (e) {
      showToast("Error saat cleansing: " + e.message, "error");
    } finally {
      btnClean.disabled = false;
      btnClean.innerText = "⚡ Jalankan Cleansing Pipeline";
    }
  });
}

// 6. Benchmark
function initBenchmark() {
  const btnBench = document.getElementById("btn-run-benchmark");
  btnBench.addEventListener("click", async () => {
    btnBench.disabled = true;
    btnBench.innerText = "⏳ Sedang mengukur storage & query speed...";
    showToast("Menjalankan benchmark CSV vs JSONL vs Parquet...", "info");

    try {
      const res = await fetch("/api/benchmark");
      const d = await res.json();
      if (d.status === "success") {
        const b = d.benchmark;
        document.getElementById("benchmark-empty-notice").style.display = "none";
        document.getElementById("benchmark-results").style.display = "block";
        document.getElementById("benchmark-verdict-text").innerText = b.verdict;

        // Render Table
        const tbHtml = `
          <tr>
            <td><strong>CSV (Row-oriented Text)</strong></td>
            <td>${b.file_size_mb.CSV} MB</td>
            <td>${b.query_time_ms.CSV} ms</td>
            <td>1.0x (Baseline)</td>
            <td>Format standar umum, ukuran besar, parsing baris lambat pada analitis besar.</td>
          </tr>
          <tr>
            <td><strong>JSONL (Semi-structured)</strong></td>
            <td>${b.file_size_mb.JSONL} MB</td>
            <td>${b.query_time_ms.JSONL} ms</td>
            <td>0.7x - 0.9x</td>
            <td>Fleksibel untuk schema-less telemetri, tetapi payload string sangat boros memori.</td>
          </tr>
          <tr style="background: rgba(16, 185, 129, 0.08);">
            <td><strong style="color: var(--accent-emerald);">Apache Parquet (Snappy Columnar)</strong></td>
            <td style="color: var(--accent-emerald); font-weight: 700;">${b.file_size_mb["Parquet (Snappy)"]} MB</td>
            <td style="color: var(--accent-emerald); font-weight: 700;">${b.query_time_ms["Parquet (Snappy)"]} ms</td>
            <td style="color: var(--accent-emerald); font-weight: 700;">Hemat ${b.storage_saved_percent}%</td>
            <td><strong>Pilihan Utama Big Data:</strong> Columnar scanning, dictionary encoding, kompresi tinggi, pushdown predicate.</td>
          </tr>
        `;
        document.getElementById("benchmark-table-body").innerHTML = tbHtml;

        // Render Charts
        renderBenchmarkCharts(b.file_size_mb, b.query_time_ms);
        showToast("Benchmark selesai diuji!", "success");
      }
    } catch (e) {
      showToast("Error saat benchmark: " + e.message, "error");
    } finally {
      btnBench.disabled = false;
      btnBench.innerText = "⏱️ Eksekusi Benchmark Sekarang";
    }
  });
}

function renderBenchmarkCharts(sizeData, queryData) {
  // 1. File Size Chart
  const ctxSize = document.getElementById("chart-file-size").getContext("2d");
  if (charts.sizeChart) charts.sizeChart.destroy();
  charts.sizeChart = new Chart(ctxSize, {
    type: "bar",
    data: {
      labels: Object.keys(sizeData),
      datasets: [{
        label: "Ukuran File di Storage (MB)",
        data: Object.values(sizeData),
        backgroundColor: ["#f43f5e", "#f59e0b", "#10b981"],
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: { color: "rgba(255,255,255,0.06)" }, ticks: { color: "#9ca3af" } },
        x: { ticks: { color: "#9ca3af" } }
      }
    }
  });

  // 2. Query Latency Chart
  const ctxQuery = document.getElementById("chart-query-time").getContext("2d");
  if (charts.queryChart) charts.queryChart.destroy();
  charts.queryChart = new Chart(ctxQuery, {
    type: "bar",
    data: {
      labels: Object.keys(queryData),
      datasets: [{
        label: "Query Execution Time (ms)",
        data: Object.values(queryData),
        backgroundColor: ["#f43f5e", "#f59e0b", "#06b6d4"],
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: { color: "rgba(255,255,255,0.06)" }, ticks: { color: "#9ca3af" } },
        x: { ticks: { color: "#9ca3af" } }
      }
    }
  });
}

// 7. Advanced Analytics
function initAnalytics() {
  const btnRefresh = document.getElementById("btn-refresh-analytics");
  btnRefresh.addEventListener("click", () => loadAnalyticsData(true));
  document.querySelector('[data-tab="tab-analytics"]').addEventListener("click", () => {
    if (!charts.rfmDonut) loadAnalyticsData();
  });
}

async function loadAnalyticsData(force = false) {
  try {
    showToast("Menghitung model analitis RFM & Cohort...", "info");
    const res = await fetch("/api/analytics");
    const d = await res.json();
    if (d.status === "success") {
      const a = d.analytics;

      // 1. RFM Donut Chart & Table
      renderRFM(a.rfm_segments);

      // 2. Cohort Heatmap
      renderCohortHeatmap(a.cohort);

      // 3. Funnel & Devices
      renderFunnel(a.funnel);
      renderDevices(a.devices);

      // 4. Categories & Cities
      renderCategoryChart(a.categories);
      renderCityChart(a.cities);

      showToast("Analisis Milestone 2 berhasil dimuat!", "success");
    }
  } catch (e) {
    showToast("Error analitis: " + e.message, "error");
  }
}

function renderRFM(segments) {
  const tbody = document.getElementById("rfm-table-body");
  let html = "";
  segments.forEach(s => {
    html += `
      <tr class="clickable-row" onclick="openDrilldown('rfm', '${s.rfm_segment}')" title="Klik untuk Drill-down transaksi">
        <td><strong style="color: var(--accent-cyan);">${s.rfm_segment}</strong></td>
        <td>${Number(s.customer_count).toLocaleString()}</td>
        <td>${s.avg_recency_days} hari</td>
        <td>Rp ${Number(s.avg_monetary_idr).toLocaleString('id-ID')}</td>
      </tr>
    `;
  });
  tbody.innerHTML = html;

  const ctx = document.getElementById("chart-rfm-donut").getContext("2d");
  if (charts.rfmDonut) charts.rfmDonut.destroy();
  charts.rfmDonut = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: segments.map(s => s.rfm_segment),
      datasets: [{
        data: segments.map(s => s.customer_count),
        backgroundColor: ["#10b981", "#3b82f6", "#06b6d4", "#f59e0b", "#f43f5e", "#8b5cf6"],
        borderWidth: 0,
        hoverOffset: 10
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { color: "#d1d5db", font: { size: 11.5 }, padding: 12 } }
      },
      onClick: (evt, elements) => {
        if (elements.length > 0) {
          const index = elements[0].index;
          const segmentName = segments[index].rfm_segment;
          openDrilldown('rfm', segmentName);
        }
      }
    }
  });
}

function renderCohortHeatmap(cohort) {
  const head = document.getElementById("cohort-head");
  const body = document.getElementById("cohort-body");
  head.innerHTML = "";
  body.innerHTML = "";

  if (!cohort || !cohort.labels || cohort.labels.length === 0) {
    body.innerHTML = "<tr><td>Data cohort belum tersedia. Jalankan synthesizer & cleansing terlebih dahulu.</td></tr>";
    return;
  }

  let headHtml = "<tr><th>Cohort Bulan</th>";
  cohort.months.forEach(m => {
    headHtml += `<th>${m}</th>`;
  });
  headHtml += "</tr>";
  head.innerHTML = headHtml;

  let bodyHtml = "";
  cohort.labels.forEach((lbl, rIdx) => {
    bodyHtml += `<tr><td><strong>${lbl}</strong></td>`;
    const rowValues = cohort.matrix[rIdx];
    rowValues.forEach((val, cIdx) => {
      const alpha = Math.min(1, Math.max(0.15, val / 100));
      const color = `rgba(99, 102, 241, ${alpha})`;
      bodyHtml += `<td class="heatmap-cell" style="background: ${color};" title="Bulan: ${lbl}, ${cohort.months[cIdx]}: ${val}%">${val > 0 ? val + '%' : '-'}</td>`;
    });
    bodyHtml += "</tr>";
  });
  body.innerHTML = bodyHtml;
}

function renderFunnel(funnel) {
  const ctx = document.getElementById("chart-funnel").getContext("2d");
  if (charts.funnelChart) charts.funnelChart.destroy();
  charts.funnelChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: funnel.map(f => f.action_event),
      datasets: [{
        label: "Jumlah Event",
        data: funnel.map(f => f.event_count),
        backgroundColor: "rgba(6, 182, 212, 0.85)",
        borderColor: "#06b6d4",
        borderWidth: 1,
        borderRadius: 8
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: "rgba(255,255,255,0.06)" }, ticks: { color: "#9ca3af" } },
        y: { ticks: { color: "#cbd5e1", font: { weight: "600" } } }
      }
    }
  });
}

function renderDevices(devices) {
  const ctx = document.getElementById("chart-devices").getContext("2d");
  if (charts.deviceChart) charts.deviceChart.destroy();
  charts.deviceChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: devices.map(d => d.device_type),
      datasets: [{
        data: devices.map(d => d.count),
        backgroundColor: ["#6366f1", "#a855f7", "#3b82f6", "#10b981", "#f59e0b"],
        borderWidth: 0,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { color: "#d1d5db", font: { size: 11.5 }, padding: 10 } }
      },
      cutout: "60%"
    }
  });
}

function renderCategoryChart(categories) {
  const ctx = document.getElementById("chart-categories");
  if (!ctx) return;
  if (charts.catChart) charts.catChart.destroy();
  charts.catChart = new Chart(ctx.getContext("2d"), {
    type: "bar",
    data: {
      labels: categories.map(c => c.category),
      datasets: [{
        label: "Total Pendapatan (IDR)",
        data: categories.map(c => c.revenue),
        backgroundColor: "rgba(99, 102, 241, 0.8)",
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#9ca3af", font: { size: 10.5 } } },
        y: { grid: { color: "rgba(255,255,255,0.06)" }, ticks: { color: "#9ca3af" } }
      },
      onClick: (evt, elements) => {
        if (elements.length > 0) {
          const index = elements[0].index;
          openDrilldown('category', categories[index].category);
        }
      }
    }
  });
}

function renderCityChart(cities) {
  const ctx = document.getElementById("chart-cities");
  if (!ctx) return;
  if (charts.cityChart) charts.cityChart.destroy();
  charts.cityChart = new Chart(ctx.getContext("2d"), {
    type: "bar",
    data: {
      labels: cities.map(c => c.city),
      datasets: [{
        label: "Total Transaksi",
        data: cities.map(c => c.orders),
        backgroundColor: "rgba(6, 182, 212, 0.8)",
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#9ca3af" } },
        y: { grid: { color: "rgba(255,255,255,0.06)" }, ticks: { color: "#9ca3af" } }
      },
      onClick: (evt, elements) => {
        if (elements.length > 0) {
          const index = elements[0].index;
          openDrilldown('city', cities[index].city);
        }
      }
    }
  });
}

// 8. Interactive Drilldown Modal
window.openDrilldown = async function(filterType, filterValue) {
  const modal = document.getElementById("modal-drilldown");
  const title = document.getElementById("drilldown-title");
  title.innerText = `🔍 Drill-Down Records: ${filterValue} (${filterType.toUpperCase()})`;
  modal.classList.add("active");

  try {
    const res = await fetch(`/api/drilldown?filter_type=${filterType}&filter_value=${encodeURIComponent(filterValue)}&limit=12`);
    const d = await res.json();
    renderTable("drilldown-head", "drilldown-body", d.records);
  } catch (e) {
    showToast("Gagal memuat drilldown: " + e.message, "error");
  }
};

window.closeDrilldown = function() {
  document.getElementById("modal-drilldown").classList.remove("active");
};

// 9. Governance & Ethics
async function initGovernance() {
  document.querySelector('[data-tab="tab-governance"]').addEventListener("click", async () => {
    try {
      const res = await fetch("/api/governance");
      const d = await res.json();
      const tbody = document.getElementById("governance-table-body");
      let html = "";
      d.samples.forEach(s => {
        html += `
          <tr>
            <td><code>${s.raw_id}</code></td>
            <td style="color: var(--accent-cyan); font-family: monospace;"><code>${s.hashed_id}</code></td>
            <td><span style="filter: blur(4px); user-select: none;">${s.pseudo_email}</span></td>
            <td style="color: var(--accent-emerald); font-family: monospace;"><code>${s.hashed_email}</code></td>
            <td>${s.city}</td>
            <td><span class="badge badge-emerald">Anonymized</span></td>
          </tr>
        `;
      });
      tbody.innerHTML = html;
    } catch (e) {
      console.error(e);
    }
  });
}

// 10. Clean Data Explorer (Scrollable Live Records)
let cleanPage = 1;
let cleanPageSize = 50;
let cleanSearch = "";
let cleanCategory = "all";
let cleanCity = "all";
let cleanTotalPages = 1;
let filterOptionsLoaded = false;

window.loadCleanData = async function() {
  const countInfo = document.getElementById("clean-data-count-info");
  const tableHead = document.getElementById("clean-full-head");
  const tableBody = document.getElementById("clean-full-body");
  const pageInfo = document.getElementById("pagination-page-info");
  const btnPrev = document.getElementById("btn-prev-page");
  const btnNext = document.getElementById("btn-next-page");
  const btnFirst = document.getElementById("btn-first-page");
  const btnLast = document.getElementById("btn-last-page");

  if (!tableBody) return;

  countInfo.innerHTML = "⏳ <em>Memuat data bersih dari storage Parquet...</em>";

  try {
    const params = new URLSearchParams({
      page: cleanPage,
      page_size: cleanPageSize,
      category: cleanCategory,
      city: cleanCity,
      search: cleanSearch
    });

    const res = await fetch(`/api/clean-data?${params.toString()}`);
    const d = await res.json();

    if (d.status === "success") {
      const data = d.data;
      cleanTotalPages = data.total_pages;

      // Populate filter dropdowns once
      if (!filterOptionsLoaded && data.categories && data.cities) {
        const catSelect = document.getElementById("clean-filter-cat");
        const citySelect = document.getElementById("clean-filter-city");
        
        data.categories.forEach(cat => {
          const opt = document.createElement("option");
          opt.value = cat;
          opt.textContent = cat;
          catSelect.appendChild(opt);
        });

        data.cities.forEach(city => {
          const opt = document.createElement("option");
          opt.value = city;
          opt.textContent = city;
          citySelect.appendChild(opt);
        });
        filterOptionsLoaded = true;
      }

      // Render Table Headers
      tableHead.innerHTML = `
        <tr>
          <th>Transaction ID</th>
          <th>Customer ID</th>
          <th>Timestamp</th>
          <th>Product ID</th>
          <th>Category</th>
          <th>Qty</th>
          <th>Price (IDR)</th>
          <th>Discount</th>
          <th>Payment</th>
          <th>City</th>
          <th>Total Amount (IDR)</th>
        </tr>
      `;

      // Render Rows
      if (!data.records || data.records.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="11" style="text-align: center; padding: 30px; color: var(--text-dim);">Tidak ada data yang cocok dengan kriteria pencarian.</td></tr>`;
      } else {
        let rowsHtml = "";
        data.records.forEach(r => {
          rowsHtml += `
            <tr>
              <td><code style="color: var(--accent-cyan);">${r.transaction_id}</code></td>
              <td><code>${r.customer_id}</code></td>
              <td style="color: var(--text-muted); font-size: 12px;">${r.timestamp}</td>
              <td><span class="badge badge-primary" style="font-size: 10px;">${r.product_id}</span></td>
              <td><strong>${r.category}</strong></td>
              <td style="text-align: center;">${r.quantity}</td>
              <td>Rp ${Number(r.price).toLocaleString('id-ID')}</td>
              <td style="color: var(--accent-amber);">${Math.round(r.discount * 100)}%</td>
              <td><span style="font-size: 12px; color: var(--text-muted);">${r.payment_method}</span></td>
              <td><span class="badge badge-cyan" style="font-size: 11px;">${r.city}</span></td>
              <td style="color: var(--accent-emerald); font-weight: 700;">Rp ${Number(r.total_amount).toLocaleString('id-ID')}</td>
            </tr>
          `;
        });
        tableBody.innerHTML = rowsHtml;
      }

      // Update Info & Pagination
      const startIdx = data.total_records === 0 ? 0 : ((cleanPage - 1) * cleanPageSize) + 1;
      const endIdx = Math.min(cleanPage * cleanPageSize, data.total_records);
      countInfo.innerHTML = `Menampilkan <strong>${startIdx.toLocaleString()} - ${endIdx.toLocaleString()}</strong> dari <strong>${Number(data.total_records).toLocaleString()}</strong> baris data bersih`;
      pageInfo.innerText = `Halaman ${cleanPage} dari ${cleanTotalPages.toLocaleString()} (${Number(data.total_records).toLocaleString()} total)`;

      // Enable/Disable buttons
      btnFirst.disabled = cleanPage <= 1;
      btnPrev.disabled = cleanPage <= 1;
      btnNext.disabled = cleanPage >= cleanTotalPages;
      btnLast.disabled = cleanPage >= cleanTotalPages;
    }
  } catch (err) {
    countInfo.innerHTML = `<span style="color: var(--accent-rose);">Gagal memuat data bersih: ${err.message}</span>`;
  }
};

function initCleanDataExplorer() {
  const searchInput = document.getElementById("clean-search-input");
  const catFilter = document.getElementById("clean-filter-cat");
  const cityFilter = document.getElementById("clean-filter-city");
  const pageSizeSelect = document.getElementById("clean-page-size");
  const btnFirst = document.getElementById("btn-first-page");
  const btnPrev = document.getElementById("btn-prev-page");
  const btnNext = document.getElementById("btn-next-page");
  const btnLast = document.getElementById("btn-last-page");
  const btnRefresh = document.getElementById("btn-refresh-clean-table");

  if (!searchInput) return;

  // Search debounce
  let searchTimer;
  searchInput.addEventListener("input", (e) => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      cleanSearch = e.target.value.trim();
      cleanPage = 1;
      window.loadCleanData();
    }, 350);
  });

  // Filter change
  catFilter.addEventListener("change", (e) => {
    cleanCategory = e.target.value;
    cleanPage = 1;
    window.loadCleanData();
  });

  cityFilter.addEventListener("change", (e) => {
    cleanCity = e.target.value;
    cleanPage = 1;
    window.loadCleanData();
  });

  pageSizeSelect.addEventListener("change", (e) => {
    cleanPageSize = parseInt(e.target.value);
    cleanPage = 1;
    window.loadCleanData();
  });

  // Pagination buttons
  btnFirst.addEventListener("click", () => {
    if (cleanPage > 1) {
      cleanPage = 1;
      window.loadCleanData();
    }
  });

  btnPrev.addEventListener("click", () => {
    if (cleanPage > 1) {
      cleanPage--;
      window.loadCleanData();
    }
  });

  btnNext.addEventListener("click", () => {
    if (cleanPage < cleanTotalPages) {
      cleanPage++;
      window.loadCleanData();
    }
  });

  btnLast.addEventListener("click", () => {
    if (cleanPage < cleanTotalPages) {
      cleanPage = cleanTotalPages;
      window.loadCleanData();
    }
  });

  btnRefresh.addEventListener("click", () => {
    window.loadCleanData();
    showToast("Data bersih dimuat ulang!", "success");
  });

  // Initial fetch
  window.loadCleanData();
}
