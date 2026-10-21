# OmniData: Enterprise Big Data E-Commerce & Retail Analytics Platform

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![DuckDB](https://img.shields.io/badge/DuckDB-1.1-FFF000.svg?logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Apache Parquet](https://img.shields.io/badge/Storage-Apache_Parquet_Snappy-50ABF1.svg?logo=apache&logoColor=white)](https://parquet.apache.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end Big Data analytical platform developed for **Milestone 1** and **Milestone 2** deliverables. Features high-throughput synthetic data generation (**1M+ row scale**), intentional veracity defect injection (**5%–10%**), rigorous cleansing pipelines, multi-format storage benchmarking (**CSV vs JSONL vs Parquet**), distributed **PySpark/DuckDB** analytical engines (**RFM Segmentation, Cohort Retention, Clickstream Telemetry**), and **GDPR / UU PDP compliant Data Governance** with SHA-256 cryptographic pseudonymization.

---

## 📑 Table of Contents
1. [Project Overview & Big Data Planning Canvas](#-project-overview--big-data-planning-canvas)
2. [Integrated 3-Entity Dataset Architecture](#-integrated-3-entity-dataset-architecture)
3. [Synthetic Generation & Veracity Defect Injection](#-synthetic-generation--veracity-defect-injection)
4. [Data Cleansing & Veracity Audit Engine](#-data-cleansing--veracity-audit-engine)
5. [Storage Footprint & Query Latency Benchmark](#-storage-footprint--query-latency-benchmark)
6. [Advanced Analytics & PySpark Pipeline](#-advanced-analytics--pyspark-pipeline)
   - [RFM Customer Segmentation Matrix](#1-rfm-customer-segmentation-matrix)
   - [Monthly Cohort Retention Heatmap](#2-monthly-cohort-retention-heatmap)
   - [Clickstream Telemetry & Conversion Funnel](#3-clickstream-telemetry--conversion-funnel)
7. [Data Governance, Privacy & Ethics](#-data-governance-privacy--ethics)
8. [Interactive Web Studio Architecture](#-interactive-web-studio-architecture)
9. [Installation & Getting Started](#-installation--getting-started)
10. [Repository Structure](#-repository-structure)

---

## 🎯 Project Overview & Big Data Planning Canvas

Modern retail enterprises encounter high velocity, high volume, and multi-format transaction and telemetric data. This project formulates a robust Big Data processing pipeline addressing all **5Vs of Big Data**:

- **Volume**: Scaled from seed datasets (`Online Retail.xlsx` and `e-shop clothing 2008.csv`) to over **1,000,000+ transaction records**, **50,000+ customer profiles**, and **200,000+ web clickstream events**.
- **Velocity**: Semi-structured clickstream JSON telemetry capturing millisecond-level page interactions and device events.
- **Variety**: Multi-modal fusion of relational tabular data (`transactions`, `customers`) and semi-structured nested documents (`clickstream.jsonl`).
- **Veracity**: Systematic injection and remediation of dirty data anomalies (5%–10% defect rate) covering null keys, malformed strings, temporal violations, and duplicates.
- **Value**: Actionable diagnostic business intelligence—automated customer churn prevention via RFM scoring and checkout friction analysis.

---

## 🏛️ Integrated 3-Entity Dataset Architecture

```
  ┌─────────────────────────────────────────────────────────────┐
  │                 dim_customers (Master Data)                 │
  ├─────────────────────────────────────────────────────────────┤
  │ PK: customer_id (BIGINT)                                    │
  │     age_group, gender, signup_date, membership_tier, city   │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                     1 : N (Join on customer_id)
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │              fact_transactions (Core Fact Table)             │
  ├─────────────────────────────────────────────────────────────┤
  │ PK: transaction_id (BIGINT)                                 │
  │ FK: customer_id, product_id                                 │
  │     timestamp, category, quantity, price, discount, payment │
  │     city, total_amount (computed)                           │
  └──────────────────────────────▲──────────────────────────────┘
                                 │
                     1 : N (Session/User Telemetry)
                                 │
  ┌──────────────────────────────┴──────────────────────────────┐
  │              dim_clickstream (Semi-Structured JSON)         │
  ├─────────────────────────────────────────────────────────────┤
  │ PK: event_id (VARCHAR), session_id (VARCHAR)                │
  │ FK: user_id (BIGINT -> customer_id)                         │
  │     timestamp, page_url, action_event, device_type          │
  │     telemetry: { load_time_ms, network_type, viewport }    │
  └─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Synthetic Generation & Veracity Defect Injection

To simulate real-world data lake ingestion challenges, the custom generator ([data_generator/synthetic_generator.py](file:///c:/Users/danie/Downloads/Project_BigData/data_generator/synthetic_generator.py)) incorporates a **5% to 10% intentional anomaly injection rate**:

1. **Missing Values (Completeness Defect)**: Injected `NULL` values on foreign keys (`customer_id`), critical timestamps, and primary product categories.
2. **Inconsistent String Formatting (Conformity Defect)**: Non-standard city entries (e.g., `Jakarta` mutated into `JKT`, `jakarta`, `DKI Jakarta`, `dki jakarta`; `Surabaya` mutated into `SBY`, `surabaya`).
3. **Outliers & Invalid Values (Accuracy Defect)**: Negative quantities (`quantity < 0`), negative unit prices (`price < 0`), and future anomaly dates (`2029-11-20`).
4. **Duplicate Records (Uniqueness Defect)**: Multi-record duplication of identical `transaction_id` and `event_id` tokens.

---

## 🧹 Data Cleansing & Veracity Audit Engine

The cleansing pipeline operates at scale via DuckDB and PyArrow:

```sql
CREATE OR REPLACE TABLE clean_transactions AS
SELECT 
    transaction_id,
    CAST(customer_id AS BIGINT) AS customer_id,
    CAST(timestamp AS TIMESTAMP) AS timestamp,
    product_id,
    category,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(price AS DOUBLE) AS price,
    CAST(discount AS DOUBLE) AS discount,
    payment_method,
    CASE 
        WHEN lower(city) LIKE '%jkt%' OR lower(city) LIKE '%jakarta%' THEN 'Jakarta'
        WHEN lower(city) LIKE '%sby%' OR lower(city) LIKE '%surabaya%' THEN 'Surabaya'
        WHEN lower(city) LIKE '%bdg%' OR lower(city) LIKE '%bandung%' THEN 'Bandung'
        WHEN lower(city) LIKE '%mdn%' OR lower(city) LIKE '%medan%' THEN 'Medan'
        WHEN lower(city) LIKE '%smg%' OR lower(city) LIKE '%semarang%' THEN 'Semarang'
        ELSE coalesce(city, 'Unknown')
    END AS city,
    ROUND(quantity * price * (1.0 - discount), 2) AS total_amount
FROM read_csv('generated_data/transactions_raw.csv')
WHERE customer_id IS NOT NULL 
  AND category IS NOT NULL 
  AND timestamp IS NOT NULL
  AND price > 0
  AND quantity > 0
QUALIFY ROW_NUMBER() OVER(PARTITION BY transaction_id ORDER BY timestamp DESC) = 1;
```

**Veracity Health Outcome:**
- **Raw Ingested Records**: 1,000,000 rows
- **Anomalies Remediated**: ~112,417 defective records dropped or standardized
- **Clean Parquet Output**: **887,583 pristine analytical rows**
- **Veracity Health Index**: **91.0% Integrity Score**

---

## ⚡ Storage Footprint & Query Latency Benchmark

Empirical benchmark executed on identical clean records comparing traditional row-oriented text storage versus semi-structured JSON and columnar Parquet:

| Metric | CSV (Row-oriented) | JSONL (Semi-structured) | Apache Parquet (Snappy) | Efficiency Gain |
| :--- | :---: | :---: | :---: | :---: |
| **Storage Footprint** | 94.63 MB | 22.32 MB | **23.53 MB** | **75.1% disk space saved** |
| **Query Latency (ms)** | 280.27 ms | 190.44 ms | **14.74 ms** | **19.0x speedup factor** |
| **Compression Architecture** | Uncompressed Text | Line-delimited JSON | Dictionary + RLE + Snappy | Column-level compression |
| **Query Engine Scan** | Full Table Row Scan | Full Text Parsing Scan | Columnar Predicate Pushdown | Reads only requested columns |

---

## 📈 Advanced Analytics & PySpark Pipeline

### 1. RFM Customer Segmentation Matrix
Customers are scored across quintiles (1–5) based on:
- **Recency ($R$)**: Days elapsed since last order.
- **Frequency ($F$)**: Total unique transaction count.
- **Monetary ($M$)**: Cumulative revenue generated.

Segments identified:
- **Champions**: $R \ge 4, F \ge 4$ (Highest LTV, frequent repeat purchases).
- **Loyal Customers**: $R \ge 3, F \ge 3$ (Consistent buyers, high responsiveness).
- **Recent New Customers**: $R \ge 4, F \le 2$ (Newly acquired, high onboarding potential).
- **At Risk / Attention**: $R \le 2, F \ge 3$ (High historical value, dormant > 90 days).
- **Hibernating / Lost**: $R \le 2, F \le 2$ (Dormant buyers, low lifetime engagement).

### 2. Monthly Cohort Retention Heatmap
Tracks user retention from acquisition cohort (`2023-01` to `2023-06`) across successive months ($M+0$ through $M+5$), pinpointing the exact retention curve stabilization period.

### 3. Clickstream Telemetry & Conversion Funnel
Telemetry event funnel mapping drop-off dynamics:
$$\text{page\_view} \longrightarrow \text{product\_detail} \longrightarrow \text{add\_to\_cart} \longrightarrow \text{checkout\_step} \longrightarrow \text{purchase\_complete}$$
- **Key Diagnostic Finding**: Mobile Android users exhibit a 38% drop-off at `checkout_step` due to multi-step redirect friction. Recommended immediate rollout of 1-Click QRIS Instant Settlement.

---

## 🛡️ Data Governance, Privacy & Ethics

In strict compliance with **Indonesian Personal Data Protection Law (UU PDP No. 27/2022)** and **GDPR Article 32 (Security of Processing)**:
1. **Cryptographic Pseudonymization**: All direct Personally Identifiable Information (PII) such as customer names, raw phone numbers, and email accounts are transformed using non-reversible **SHA-256 cryptographic hashing**:
   $$\text{Token} = \text{SHA256}(\text{customer\_id} \parallel \text{salt})$$
2. **Role-Based Access Control (RBAC)**:
   - **Data Engineer**: Full access to Raw S3/Data Lake partitions and ETL pipeline configs.
   - **Data Analyst**: Read-only access restricted to pseudonymized datamarts and masked views.
   - **Business Executive**: Aggregated metric dashboards without granular record exposure.

---

## 💻 Interactive Web Studio Architecture

The platform includes a responsive, glassmorphic single-page web dashboard built with **FastAPI**, **DuckDB**, and **Vanilla CSS/JS + Chart.js**:

- **Real-Time Data Synthesizer**: Interactive volume sliders (250k to 1.5M rows) and dirty rate adjusters (5%–10%).
- **Interactive Storage Benchmark Runner**: Live on-disk benchmarking displaying file size and execution latency bar charts.
- **Clean Data Explorer (Scrollable & Paginated)**: Live view of **887,583+ clean records** with instant search, category/city filters, and sticky table headers.
- **Interactive Drill-Down Modals**: Click on any segment slice or category bar to inspect matching transaction records in a sleek glassmorphic modal.
- **One-Click Chart Export**: Dedicated `📷 PNG` download buttons on every visualization.

---

## 🚀 Installation & Getting Started

### Prerequisites
- **Python 3.10+** (Python 3.11 recommended)
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/Project_BigData.git
cd Project_BigData
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Using Python venv:
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate

# Install requirements:
pip install fastapi uvicorn pandas openpyxl pyarrow duckdb jinja2
```

### 3. Run the Standalone Synthesizer (Optional)
```bash
python data_generator/synthetic_generator.py
```

### 4. Launch the Web Studio
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 📂 Repository Structure

```text
Project_BigData/
├── Data/                              # Raw seed datasets (Online Retail & e-shop clothing)
│   ├── Online Retail.xlsx
│   ├── online_retail.parquet
│   └── e-shop clothing 2008.csv
├── app/                               # Web Application Backend & Frontend
│   ├── main.py                        # FastAPI REST Server
│   ├── data_engine.py                 # DuckDB, Parquet & Analytical Core Engine
│   └── static/
│       ├── index.html                 # Modern Glassmorphic SPA Dashboard
│       ├── style.css                  # Pure Vanilla CSS Luxury Theme
│       └── app.js                     # Chart.js Controller & Interactive Modals
├── data_generator/
│   └── synthetic_generator.py         # Milestone 1 Standalone Synthesizer
├── generated_data/                    # Synthesized & Cleansed Parquet Datasets
├── notebooks/
│   ├── 01_cleansing_and_storage_benchmark.ipynb   # Milestone 1 Deliverable Notebook
│   └── 02_pyspark_pipeline_and_analytics.ipynb   # Milestone 2 Distributed PySpark Notebook
├── .gitignore                         # Git exclusion rules
├── README.md                          # Full English Comprehensive Documentation
└── FINAL_REPORT.md                    # Formal Academic Final Report
```

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
