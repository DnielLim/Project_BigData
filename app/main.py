import os
import sys
from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

# Ensure app directory is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from data_engine import engine, OUTPUT_DIR, DATA_DIR

app = FastAPI(
    title="Big Data E-Commerce & Retail Analytics Platform",
    description="Big Data Project Platform (Milestone 1 & Milestone 2) with 3 integrated entities, data synthesis, veracity checks, storage benchmarks, and distributed analytics.",
    version="1.0.0"
)

# Mount static files
STATIC_DIR = os.path.join(CURRENT_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Big Data Analytics Platform API is running. UI is initializing..."}

@app.get("/api/overview")
def get_overview():
    seed_info = engine.get_seed_data_info()
    
    # Check generated files
    clean_parquet = os.path.join(OUTPUT_DIR, "transactions_clean.parquet")
    raw_csv = os.path.join(OUTPUT_DIR, "transactions_raw.csv")
    customers_csv = os.path.join(OUTPUT_DIR, "customers.csv")
    clickstream_jsonl = os.path.join(OUTPUT_DIR, "clickstream.jsonl")

    status_data = {
        "has_raw_fact": os.path.exists(raw_csv),
        "has_clean_fact": os.path.exists(clean_parquet),
        "has_dim_customers": os.path.exists(customers_csv),
        "has_clickstream": os.path.exists(clickstream_jsonl),
        "seed_info": seed_info,
        "kpis": {
            "target_fact_volume": "1.000.000+ baris",
            "target_dim_cust": "50.000+ baris",
            "target_clickstream": "200.000+ event JSON",
            "dirty_injection_range": "5% - 10%",
            "supported_storage": ["CSV", "JSONL", "Parquet (Snappy)"],
            "analytical_models": ["RFM Segmentation", "Cohort Retention", "Funnel Analytics", "Distributed PySpark"]
        }
    }
    return status_data

@app.get("/api/seed-data")
def get_seed_data(dataset: str = Query("online_retail"), limit: int = 8):
    sample = engine.get_seed_preview(dataset=dataset, limit=limit)
    return {"dataset": dataset, "limit": limit, "data": sample}

class GenerateRequest(BaseModel):
    fact_rows: Optional[int] = 1000000
    customer_rows: Optional[int] = 50000
    clickstream_events: Optional[int] = 200000
    dirty_rate: Optional[float] = 0.08

@app.post("/api/generate-synthetic")
def generate_synthetic(req: GenerateRequest = Body(...)):
    try:
        # Constrain minimums or fast test options
        res = engine.generate_datasets(
            fact_rows=req.fact_rows,
            customer_rows=req.customer_rows,
            clickstream_events=req.clickstream_events,
            dirty_rate=req.dirty_rate
        )
        return {"status": "success", "result": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/run-cleansing")
def run_cleansing():
    try:
        res = engine.run_cleansing_audit()
        return {"status": "success", "audit": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clean-data")
def get_clean_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=10, le=500),
    category: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    try:
        data = engine.get_clean_data_paginated(
            page=page,
            page_size=page_size,
            category=category,
            city=city,
            search=search
        )
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/benchmark")
def run_benchmark():
    try:
        res = engine.run_storage_benchmark()
        return {"status": "success", "benchmark": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics")
def get_analytics():
    try:
        res = engine.get_rfm_and_analytics()
        return {"status": "success", "analytics": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/drilldown")
def get_drilldown(filter_type: str = Query("rfm"), filter_value: str = Query("Champions"), limit: int = 12):
    try:
        records = engine.get_drilldown_records(filter_type=filter_type, filter_value=filter_value, limit=limit)
        return {"status": "success", "filter_type": filter_type, "filter_value": filter_value, "records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/governance")
def get_governance(limit: int = 8):
    try:
        hashing_samples = engine.simulate_governance_hashing(limit=limit)
        return {
            "hashing_algorithm": "SHA-256",
            "gdpr_compliance": "Pseudonymization & Anonymization Article 32 GDPR / UU PDP No. 27/2022",
            "samples": hashing_samples,
            "roles": [
                {"role": "Data Engineer", "access": "Full Access to Raw & Clean Parquet Pipeline", "permissions": "Read/Write/Partition"},
                {"role": "Data Analyst", "access": "Clean Analytical Datamart & Masked Views", "permissions": "Read-Only (No raw PII)"},
                {"role": "Business User", "access": "Aggregated Dashboards & RFM Insights", "permissions": "Metrics & Visuals"}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
