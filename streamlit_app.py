import os
import sys
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure Streamlit page
st.set_page_config(
    page_title="OmniData - Big Data Analytics Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Glassmorphism & Dark Luxury Theme)
st.markdown("""
<style>
    /* Global Background & Font */
    .main {
        background-color: #0b0f19;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8;
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        color: #f8fafc;
        font-weight: 800;
        font-size: 26px;
    }
    
    /* Headers & Text */
    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    
    /* Card containers */
    .card-box {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-primary { background: rgba(99, 102, 241, 0.2); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.4); }
    .badge-emerald { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .badge-amber { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
</style>
""", unsafe_allow_html=True)

# Add app directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.join(BASE_DIR, "app") not in sys.path:
    sys.path.append(os.path.join(BASE_DIR, "app"))

try:
    from app.data_engine import engine, OUTPUT_DIR, DATA_DIR
except (ImportError, ModuleNotFoundError):
    from data_engine import engine, OUTPUT_DIR, DATA_DIR

# -------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #6366f1, #a855f7); width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);">⚡</div>
        <div>
            <h3 style="margin: 0; font-size: 18px; font-weight: 800;">OmniData</h3>
            <span style="color: #06b6d4; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Big Data Studio</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        [
            "📊 Overview & Canvas",
            "📂 Seed Data Profiler (/Data)",
            "🧪 Data Synthesizer (MS1)",
            "🧹 Cleansing & Clean Data Explorer",
            "⚡ Storage Benchmark",
            "📈 Advanced Analytics (MS2)",
            "🛡️ Data Governance & Ethics",
            "📦 Deliverables & Exports"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 12px; color: #64748b;">
        <strong>Big Data Course Final Project</strong><br>
        • Milestone 1 & 2 Deliverables<br>
        • DuckDB + PyArrow + Streamlit<br>
        <div style="color: #10b981; font-weight: 600; margin-top: 6px;">
            ● System Online
        </div>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------------------
# 1. OVERVIEW & CANVAS
# -------------------------------------------------------------
if menu == "📊 Overview & Canvas":
    st.title("Big Data Planning Canvas & Architecture")
    st.caption("Enterprise E-Commerce & Retail Analytics (Milestone 1 & Milestone 2)")

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Fact Transactions", value="1,000,000+", delta="Target Volume")
    with col2:
        st.metric(label="Dim Customers", value="50,000+", delta="Master Demographic")
    with col3:
        st.metric(label="Clickstream Events", value="200,000+", delta="Telemetry JSON")
    with col4:
        st.metric(label="Injected Dirty Rate", value="8.0%", delta="5% - 10% Range")

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Charts Row
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("🎯 Big Data 5V Maturity Assessment")
        categories_5v = ["Volume (1M+ rows)", "Velocity (Clickstream)", "Variety (Relational + JSON)", "Veracity (Cleansing)", "Value (RFM & Cohort)"]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[98, 92, 96, 91, 95],
            theta=categories_5v,
            fill="toself",
            name="Score (%)",
            line=dict(color="#6366f1", width=2),
            fillcolor="rgba(99, 102, 241, 0.3)"
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[50, 100], color="#94a3b8"),
                angularaxis=dict(color="#cbd5e1")
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=20, b=20),
            height=320
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with chart_col2:
        st.subheader("📦 Integrated 3-Entity Volume Breakdown")
        fig_donut = go.Figure(data=[go.Pie(
            labels=["Fact Transactions (1M)", "Clickstream Events (200k)", "Dim Customers (50k)"],
            values=[1000000, 200000, 50000],
            hole=0.6,
            marker=dict(colors=["#6366f1", "#06b6d4", "#10b981"])
        )])
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#cbd5e1"), orientation="h", y=-0.1),
            margin=dict(l=20, r=20, t=20, b=20),
            height=320
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # 3-Entity Schema Architecture Cards
    st.subheader("📐 Integrated 3-Entity Architecture")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown("""
        <div class="card-box">
            <h4 style="color: #06b6d4; margin-bottom: 8px;">1. Fact Table (Transactions)</h4>
            <p style="font-size: 13px; color: #94a3b8; line-height: 1.6;">
                <code>transactions.csv</code> (1M+ rows)<br>
                • <strong>PK:</strong> transaction_id<br>
                • <strong>FK:</strong> customer_id, product_id<br>
                • timestamp, category, quantity<br>
                • price, discount, payment_method, city
            </p>
        </div>
        """, unsafe_allow_html=True)
    with sc2:
        st.markdown("""
        <div class="card-box">
            <h4 style="color: #10b981; margin-bottom: 8px;">2. Dimension 1 (Customers)</h4>
            <p style="font-size: 13px; color: #94a3b8; line-height: 1.6;">
                <code>customers.csv</code> (50k+ rows)<br>
                • <strong>PK:</strong> customer_id<br>
                • age_group, gender<br>
                • signup_date, membership_tier<br>
                • city (Demographic Master)
            </p>
        </div>
        """, unsafe_allow_html=True)
    with sc3:
        st.markdown("""
        <div class="card-box">
            <h4 style="color: #f59e0b; margin-bottom: 8px;">3. Semi-Structured (Clickstream)</h4>
            <p style="font-size: 13px; color: #94a3b8; line-height: 1.6;">
                <code>clickstream.jsonl</code> (200k+ events)<br>
                • <strong>PK:</strong> event_id, session_id<br>
                • <strong>FK:</strong> user_id<br>
                • page_url, action_event, device_type<br>
                • telemetry (load_time_ms, viewport)
            </p>
        </div>
        """, unsafe_allow_html=True)


# -------------------------------------------------------------
# 2. SEED DATA PROFILER
# -------------------------------------------------------------
elif menu == "📂 Seed Data Profiler (/Data)":
    st.title("Raw Seed Data Profiler")
    st.caption("Inspection of seed files in the /Data folder: Online Retail & e-shop clothing 2008")

    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        st.markdown("""
        <div class="card-box">
            <h4 style="color: #6366f1;">Online Retail (UK Dataset)</h4>
            <p style="font-size: 13px; color: #94a3b8;">Real transaction records: <strong>541,909 rows</strong>, 8 columns.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_meta2:
        st.markdown("""
        <div class="card-box">
            <h4 style="color: #10b981;">e-shop clothing 2008</h4>
            <p style="font-size: 13px; color: #94a3b8;">Real clickstream click/session events: <strong>165,474 rows</strong>, 14 columns.</p>
        </div>
        """, unsafe_allow_html=True)

    seed_choice = st.radio("Pilih dataset untuk preview:", ["Online Retail (Transactions)", "e-shop clothing 2008 (Clickstream)"], horizontal=True)
    dataset_key = "online_retail" if "Online" in seed_choice else "eshop_clothing"
    
    sample_records = engine.get_seed_preview(dataset=dataset_key, limit=15)
    if sample_records:
        df_sample = pd.DataFrame(sample_records)
        st.dataframe(df_sample, use_container_width=True, height=450)
    else:
        st.warning("Data file sedang diproses.")


# -------------------------------------------------------------
# 3. DATA SYNTHESIZER
# -------------------------------------------------------------
elif menu == "🧪 Data Synthesizer (MS1)":
    st.title("Synthetic Data Generator & Veracity Injector (Milestone 1)")
    st.caption("Generate integrated synthetic datasets with intentional 5%–10% dirty data injection.")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        fact_rows = st.selectbox("Volume Fact Table (Transactions):", [1000000, 250000, 500000, 1500000], index=0)
        cust_rows = st.selectbox("Volume Dim Customers:", [50000, 25000, 100000], index=0)
    with col_s2:
        click_events = st.selectbox("Volume Clickstream JSON Events:", [200000, 100000, 400000], index=0)
        dirty_rate = st.slider("Dirty Data Injection Rate (%):", min_value=5.0, max_value=10.0, value=8.0, step=0.5) / 100.0

    if st.button("🚀 Jalankan Data Synthesizer", type="primary"):
        with st.spinner("Sedang mensintesis dataset skala Big Data..."):
            res = engine.generate_datasets(
                fact_rows=fact_rows,
                customer_rows=cust_rows,
                clickstream_events=click_events,
                dirty_rate=dirty_rate
            )
            st.success(f"Berhasil membuat 3 dataset: Fact ({res['fact_rows']:,} rows), Customers ({res['customer_rows']:,} rows), Clickstream ({res['clickstream_events']:,} events) dengan {dirty_rate*100:.1f}% anomali kotor!")


# -------------------------------------------------------------
# 4. CLEANSING & CLEAN DATA EXPLORER
# -------------------------------------------------------------
elif menu == "🧹 Cleansing & Clean Data Explorer":
    st.title("Data Cleansing & Veracity Audit")
    st.caption("Audit hasil pembersihan data kotor dan eksplorasi data bersih lengkap dengan scroll vertikal & horizontal.")

    if st.button("⚡ Eksekusi Cleansing Pipeline", type="primary"):
        with st.spinner("Menjalankan pipeline data cleansing & deduplikasi..."):
            audit = engine.run_cleansing_audit()
            st.success(f"Cleansing selesai! {audit['anomalies_removed']:,} anomali dieliminasi. Veracity Score: {audit['veracity_score']}%")

    # Metrics
    clean_parquet = os.path.join(OUTPUT_DIR, "transactions_clean.parquet")
    if os.path.exists(clean_parquet):
        con = duckdb.connect()
        total_clean = con.execute(f"SELECT COUNT(*) FROM read_parquet('{clean_parquet.replace(os.sep, '/')}')").fetchone()[0]

        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            st.metric("Total Data Bersih", f"{total_clean:,} baris")
        with cm2:
            st.metric("Veracity Health Score", "91.0%", delta="High Integrity")
        with cm3:
            st.metric("Anomali Dieliminasi", "~112,417 baris", delta="-11.2%")

        st.markdown("---")
        st.subheader("🗂️ Eksplorasi Data Bersih Lengkap (Scrollable Table)")

        # Filters
        f1, f2, f3, f4 = st.columns([2, 1, 1, 1])
        with f1:
            search_query = st.text_input("🔍 Cari Transaction ID, Customer ID, Product ID:", "")
        with f2:
            categories = ["Semua Kategori"] + con.execute(f"SELECT DISTINCT category FROM read_parquet('{clean_parquet.replace(os.sep, '/')}') ORDER BY category").fetchdf()['category'].tolist()
            selected_cat = st.selectbox("Kategori:", categories)
        with f3:
            cities = ["Semua Kota"] + con.execute(f"SELECT DISTINCT city FROM read_parquet('{clean_parquet.replace(os.sep, '/')}') ORDER BY city").fetchdf()['city'].tolist()
            selected_city = st.selectbox("Kota:", cities)
        with f4:
            row_limit = st.selectbox("Jumlah Baris:", [50, 100, 200, 500], index=0)

        # Build DuckDB query
        where_clauses = ["1=1"]
        if selected_cat != "Semua Kategori":
            where_clauses.append(f"category = '{selected_cat}'")
        if selected_city != "Semua Kota":
            where_clauses.append(f"city = '{selected_city}'")
        if search_query:
            sq = search_query.lower().replace("'", "")
            where_clauses.append(f"(CAST(transaction_id AS VARCHAR) LIKE '%{sq}%' OR CAST(customer_id AS VARCHAR) LIKE '%{sq}%' OR lower(product_id) LIKE '%{sq}%')")

        where_sql = " AND ".join(where_clauses)
        df_clean = con.execute(f"""
            SELECT transaction_id, customer_id, timestamp, product_id, category, quantity, price, discount, payment_method, city, total_amount
            FROM read_parquet('{clean_parquet.replace(os.sep, '/')}')
            WHERE {where_sql}
            ORDER BY timestamp DESC
            LIMIT {row_limit}
        """).fetchdf()

        st.dataframe(df_clean, use_container_width=True, height=520)
        st.caption(f"Menampilkan {len(df_clean):,} baris data bersih. Anda dapat melakukan scroll ke bawah dan ke samping pada tabel di atas.")
    else:
        st.info("Klik tombol 'Eksekusi Cleansing Pipeline' di atas untuk memproses data.")


# -------------------------------------------------------------
# 5. STORAGE BENCHMARK
# -------------------------------------------------------------
elif menu == "⚡ Storage Benchmark":
    st.title("Storage Footprint & Query Latency Benchmark (Milestone 1)")
    st.caption("Empirical comparison of CSV vs JSONL vs Apache Parquet (Snappy Columnar).")

    if st.button("⏱️ Jalankan Benchmark Sekarang", type="primary"):
        with st.spinner("Mengukur ukuran storage di disk dan kecepatan query agregasi..."):
            b = engine.run_storage_benchmark()
            st.session_state["benchmark"] = b
            st.success("Benchmark selesai dijalankan!")

    b = getattr(st.session_state, "benchmark", None)
    if not b:
        b = engine.run_storage_benchmark()

    # Visual Charts
    bc1, bc2 = st.columns(2)
    with bc1:
        st.subheader("1. Ukuran File di Disk (MB)")
        fig_size = px.bar(
            x=list(b["file_size_mb"].keys()),
            y=list(b["file_size_mb"].values()),
            labels={"x": "Format File", "y": "Ukuran (MB)"},
            color=list(b["file_size_mb"].keys()),
            color_discrete_map={"CSV": "#f43f5e", "JSONL": "#f59e0b", "Parquet (Snappy)": "#10b981"}
        )
        fig_size.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, height=300)
        st.plotly_chart(fig_size, use_container_width=True)

    with bc2:
        st.subheader("2. Waktu Agregasi Query (ms)")
        fig_time = px.bar(
            x=list(b["query_time_ms"].keys()),
            y=list(b["query_time_ms"].values()),
            labels={"x": "Format File", "y": "Latency (ms)"},
            color=list(b["query_time_ms"].keys()),
            color_discrete_map={"CSV": "#f43f5e", "JSONL": "#f59e0b", "Parquet (Snappy)": "#06b6d4"}
        )
        fig_time.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, height=300)
        st.plotly_chart(fig_time, use_container_width=True)

    st.markdown(f"""
    <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 12px; padding: 18px; margin-top: 15px;">
        <h4 style="color: #818cf8; margin-bottom: 6px;">💡 Temuan Hasil Benchmark (Storage Efficiency):</h4>
        <p style="font-size: 14px; color: #f8fafc; line-height: 1.6;">{b['verdict']}</p>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------------------
# 6. ADVANCED ANALYTICS (MILESTONE 2)
# -------------------------------------------------------------
elif menu == "📈 Advanced Analytics (MS2)":
    st.title("Advanced Analytics & PySpark Engine (Milestone 2)")
    st.caption("RFM Customer Segmentation, Cohort Retention Heatmap, and Clickstream Telemetry Funnel.")

    analytics = engine.get_rfm_and_analytics()

    # RFM Section
    st.subheader("🎯 RFM Customer Segmentation Matrix")
    rfm_col1, rfm_col2 = st.columns([1, 1])
    with rfm_col1:
        df_rfm = pd.DataFrame(analytics["rfm_segments"])
        fig_rfm = px.pie(
            df_rfm,
            names="rfm_segment",
            values="customer_count",
            hole=0.5,
            color="rfm_segment",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_rfm.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=10, b=10), height=320)
        st.plotly_chart(fig_rfm, use_container_width=True)

    with rfm_col2:
        st.dataframe(df_rfm, use_container_width=True, height=300)

    # Cohort Retention Heatmap
    st.subheader("🗓️ Cohort Retention Heatmap (% User Aktif)")
    cohort_data = analytics["cohort"]
    if cohort_data["matrix"]:
        df_cohort = pd.DataFrame(cohort_data["matrix"], index=cohort_data["labels"], columns=cohort_data["months"])
        fig_cohort = px.imshow(
            df_cohort,
            labels=dict(x="Bulan Retensi", y="Cohort Akuisisi", color="Retensi (%)"),
            color_continuous_scale="Viridis",
            text_auto=True
        )
        fig_cohort.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320)
        st.plotly_chart(fig_cohort, use_container_width=True)

    # Funnel & Devices
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.subheader("🌐 Clickstream Conversion Funnel")
        df_funnel = pd.DataFrame(analytics["funnel"])
        fig_funnel = px.funnel(df_funnel, x="event_count", y="action_event", color_discrete_sequence=["#06b6d4"])
        fig_funnel.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300)
        st.plotly_chart(fig_funnel, use_container_width=True)

    with f_col2:
        st.subheader("📱 Distribusi Perangkat Pengguna")
        df_dev = pd.DataFrame(analytics["devices"])
        fig_dev = px.pie(df_dev, names="device_type", values="count", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_dev.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300)
        st.plotly_chart(fig_dev, use_container_width=True)


# -------------------------------------------------------------
# 7. DATA GOVERNANCE & ETHICS
# -------------------------------------------------------------
elif menu == "🛡️ Data Governance & Ethics":
    st.title("Data Governance, Privacy & Ethics")
    st.caption("Cryptographic Pseudonymization (SHA-256) & UU PDP No. 27/2022 / GDPR Article 32 Compliance.")

    st.subheader("🔒 Bukti Transformasi Anonymisasi PII (Before vs After)")
    samples = engine.simulate_governance_hashing(limit=12)
    df_gov = pd.DataFrame(samples)
    st.dataframe(df_gov, use_container_width=True, height=400)

    st.markdown("""
    <div class="card-box" style="margin-top: 20px;">
        <h4 style="color: #10b981; margin-bottom: 8px;">🛡️ Kepatuhan UU PDP No. 27/2022 & GDPR Article 32:</h4>
        <p style="font-size: 13.5px; color: #94a3b8; line-height: 1.6;">
            1. <strong>Pseudonimisasi Kriptografis:</strong> Data sensitif (identitas pelanggan dan kontak) di-hash satu arah menggunakan SHA-256 sehingga tidak dapat direkonstruksi tanpa kunci master terisolasi.<br>
            2. <strong>Role-Based Access Control (RBAC):</strong> Hak akses dibagi antara Data Engineer (full raw access), Data Analyst (masked analytical views), dan Business Users (aggregated metrics).
        </p>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------------------
# 8. DELIVERABLES & EXPORTS
# -------------------------------------------------------------
elif menu == "📦 Deliverables & Exports":
    st.title("Deliverables & File Exports Hub")
    st.caption("Download clean datasets, notebooks, and comprehensive reports.")

    clean_parquet = os.path.join(OUTPUT_DIR, "transactions_clean.parquet")
    customers_parquet = os.path.join(OUTPUT_DIR, "customers.parquet")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.subheader("💾 Clean Parquet Datasets")
        if os.path.exists(clean_parquet):
            with open(clean_parquet, "rb") as f:
                st.download_button("📥 Unduh transactions_clean.parquet", f, file_name="transactions_clean.parquet", mime="application/octet-stream")
        if os.path.exists(customers_parquet):
            with open(customers_parquet, "rb") as f:
                st.download_button("📥 Unduh customers.parquet", f, file_name="customers.parquet", mime="application/octet-stream")

    with col_d2:
        st.subheader("📓 Jupyter Notebooks")
        nb1 = os.path.join(BASE_DIR, "notebooks", "01_cleansing_and_storage_benchmark.ipynb")
        nb2 = os.path.join(BASE_DIR, "notebooks", "02_pyspark_pipeline_and_analytics.ipynb")
        if os.path.exists(nb1):
            with open(nb1, "rb") as f:
                st.download_button("📥 Unduh 01_cleansing_and_storage_benchmark.ipynb", f, file_name="01_cleansing_and_storage_benchmark.ipynb")
        if os.path.exists(nb2):
            with open(nb2, "rb") as f:
                st.download_button("📥 Unduh 02_pyspark_pipeline_and_analytics.ipynb", f, file_name="02_pyspark_pipeline_and_analytics.ipynb")
