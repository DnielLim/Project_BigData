"""
synthetic_generator.py
Standalone Data Synthesizer for Big Data Final Project (Milestone 1)
Category: E-Commerce & Retail Analytics

Generates 3 Integrated Datasets:
1. transactions.csv (Fact - >= 1,000,000 rows)
2. customers.csv (Dimension 1 - >= 50,000 rows)
3. clickstream.jsonl (Semi-Structured JSON - >= 200,000 events)

Injects 5% - 10% intentional dirty data for veracity checking:
- Missing values (null customer_id, timestamp, category)
- Inconsistent string formatting (Jakarta, JKT, jakarta, DKI Jakarta)
- Outliers & invalid values (negative price, future dates)
- Duplicate records (duplicate transaction_id, event_id)
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def generate_all(
    fact_rows=1000000,
    customer_rows=50000,
    clickstream_events=200000,
    dirty_rate=0.08,
    output_dir="generated_data",
    seed=42
):
    np.random.seed(seed)
    random.seed(seed)
    os.makedirs(output_dir, exist_ok=True)

    print(f"[*] Starting Data Synthesizer with Seed={seed}")
    print(f"[*] Target Scale: Fact={fact_rows:,}, Customers={customer_rows:,}, Clickstream={clickstream_events:,}")
    print(f"[*] Dirty Data Injection Rate: {dirty_rate*100:.1f}%\n")

    canonical_cities = ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Yogyakarta", "Makassar", "Denpasar", "Palembang", "Balikpapan"]
    city_variations = {
        "Jakarta": ["Jakarta", "JKT", "jakarta", "DKI Jakarta", "dki jakarta", "JAKARTA"],
        "Surabaya": ["Surabaya", "SBY", "surabaya", "Kota Surabaya", "SURABAYA"],
        "Bandung": ["Bandung", "BDG", "bandung", "Kota Bandung", "BANDUNG"],
        "Medan": ["Medan", "MDN", "medan", "MEDAN"],
        "Semarang": ["Semarang", "SMG", "semarang", "SEMARANG"]
    }
    categories = ["Electronics", "Apparel", "Home & Living", "Health & Beauty", "Books & Stationery", "Sports & Outdoors", "Automotive", "Groceries"]
    payment_methods = ["Credit Card", "E-Wallet (GoPay/OVO)", "Bank Transfer (BCA/Mandiri)", "Virtual Account", "QRIS", "COD (Cash On Delivery)"]
    age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
    membership_tiers = ["Bronze", "Silver", "Gold", "Platinum"]
    action_events = ["page_view", "product_detail", "add_to_cart", "remove_from_cart", "checkout_step", "payment_attempt", "purchase_complete"]
    device_types = ["Mobile Android", "Mobile iOS", "Desktop Chrome", "Desktop Safari", "Tablet iPad"]

    # 1. GENERATE DIM_CUSTOMERS (>= 50,000 rows)
    print("[-] Generating Dimension Table: customers.csv...")
    cust_ids = np.arange(100001, 100001 + customer_rows)
    cust_cities = np.random.choice(canonical_cities, size=customer_rows, p=[0.35, 0.15, 0.12, 0.08, 0.08, 0.06, 0.06, 0.04, 0.03, 0.03])
    
    # Inconsistent city format injection
    dirty_city_indices = np.random.choice(customer_rows, size=int(customer_rows * dirty_rate), replace=False)
    cust_cities_dirty = list(cust_cities)
    for idx in dirty_city_indices:
        orig = cust_cities_dirty[idx]
        if orig in city_variations:
            cust_cities_dirty[idx] = random.choice(city_variations[orig])

    start_date = datetime(2022, 1, 1)
    signup_deltas = [start_date + timedelta(days=int(d)) for d in np.random.randint(0, 1000, size=customer_rows)]
    signup_str = [d.strftime("%Y-%m-%d") for d in signup_deltas]

    # Future date outlier injection
    for idx in np.random.choice(customer_rows, size=int(customer_rows * (dirty_rate * 0.3)), replace=False):
        signup_str[idx] = "2029-11-20"

    df_customers = pd.DataFrame({
        "customer_id": cust_ids,
        "age_group": np.random.choice(age_groups, size=customer_rows, p=[0.25, 0.40, 0.20, 0.10, 0.05]),
        "gender": np.random.choice(["Male", "Female"], size=customer_rows, p=[0.48, 0.52]),
        "signup_date": signup_str,
        "membership_tier": np.random.choice(membership_tiers, size=customer_rows, p=[0.50, 0.30, 0.15, 0.05]),
        "city": cust_cities_dirty
    })
    cust_path = os.path.join(output_dir, "customers.csv")
    df_customers.to_csv(cust_path, index=False)
    print(f"    Saved: {cust_path} ({len(df_customers):,} rows)")

    # 2. GENERATE FACT_TRANSACTIONS (>= 1,000,000 rows)
    print("[-] Generating Main Fact Table: transactions.csv...")
    txn_ids = np.arange(10000001, 10000001 + fact_rows)
    txn_cust_ids = np.random.choice(cust_ids, size=fact_rows)
    txn_prod_ids = [f"PRD-{i:05d}" for i in np.random.randint(1, 5001, size=fact_rows)]
    txn_categories = np.random.choice(categories, size=fact_rows, p=[0.22, 0.20, 0.15, 0.14, 0.09, 0.08, 0.06, 0.06])
    quantities = np.random.geometric(p=0.4, size=fact_rows)
    base_prices = np.round(np.random.exponential(scale=150000, size=fact_rows) + 15000, -2)
    discounts = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50], size=fact_rows, p=[0.40, 0.20, 0.15, 0.10, 0.08, 0.05, 0.02])
    txn_payments = np.random.choice(payment_methods, size=fact_rows, p=[0.20, 0.35, 0.15, 0.15, 0.10, 0.05])
    txn_cities = np.random.choice(canonical_cities, size=fact_rows, p=[0.35, 0.15, 0.12, 0.08, 0.08, 0.06, 0.06, 0.04, 0.03, 0.03])

    txn_start_ts = int(datetime(2023, 1, 1).timestamp())
    txn_end_ts = int(datetime(2024, 12, 31).timestamp())
    random_timestamps = np.random.randint(txn_start_ts, txn_end_ts, size=fact_rows)
    txn_ts_strings = [datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") for ts in random_timestamps]

    # Injections
    # Null values
    txn_cust_ids_obj = txn_cust_ids.astype(object)
    txn_cust_ids_obj[np.random.rand(fact_rows) < (dirty_rate * 0.35)] = None

    txn_categories_obj = txn_categories.astype(object)
    txn_categories_obj[np.random.rand(fact_rows) < (dirty_rate * 0.25)] = None

    txn_ts_obj = np.array(txn_ts_strings, dtype=object)
    txn_ts_obj[np.random.rand(fact_rows) < (dirty_rate * 0.15)] = None

    # Negatives / Outliers
    invalid_mask = np.random.rand(fact_rows) < (dirty_rate * 0.25)
    base_prices[invalid_mask] = -1 * np.abs(base_prices[invalid_mask])
    quantities[invalid_mask] = -1 * np.abs(quantities[invalid_mask])

    # City typos
    dirty_city_mask = np.random.rand(fact_rows) < (dirty_rate * 0.40)
    txn_cities_obj = txn_cities.astype(object)
    for i in np.where(dirty_city_mask)[0]:
        c = txn_cities_obj[i]
        if c in city_variations:
            txn_cities_obj[i] = random.choice(city_variations[c])

    # Duplicates
    num_duplicates = int(fact_rows * (dirty_rate * 0.20))
    dup_indices = np.random.choice(fact_rows, size=num_duplicates, replace=False)
    source_indices = np.random.choice(fact_rows, size=num_duplicates, replace=False)
    txn_ids[dup_indices] = txn_ids[source_indices]

    df_transactions = pd.DataFrame({
        "transaction_id": txn_ids,
        "customer_id": txn_cust_ids_obj,
        "timestamp": txn_ts_obj,
        "product_id": txn_prod_ids,
        "category": txn_categories_obj,
        "quantity": quantities,
        "price": base_prices,
        "discount": discounts,
        "payment_method": txn_payments,
        "city": txn_cities_obj
    })
    txn_path = os.path.join(output_dir, "transactions_raw.csv")
    df_transactions.to_csv(txn_path, index=False)
    print(f"    Saved: {txn_path} ({len(df_transactions):,} rows)")

    # 3. GENERATE CLICKSTREAM JSON (>= 200,000 events)
    print("[-] Generating Semi-structured Telemetry: clickstream.jsonl...")
    session_pool_size = max(10000, int(clickstream_events / 4))
    session_ids = [f"sess_{np.random.randint(100000, 999999)}_{i}" for i in range(session_pool_size)]
    assigned_sessions = np.random.choice(session_ids, size=clickstream_events)
    assigned_users = np.random.choice(cust_ids, size=clickstream_events)
    assigned_events = np.random.choice(action_events, size=clickstream_events, p=[0.45, 0.25, 0.12, 0.04, 0.06, 0.05, 0.03])
    assigned_devices = np.random.choice(device_types, size=clickstream_events, p=[0.40, 0.25, 0.20, 0.10, 0.05])
    pages = ["/home", "/catalog/electronics", "/catalog/apparel", "/product/detail", "/cart", "/checkout/shipping", "/checkout/payment", "/order/success"]
    assigned_pages = np.random.choice(pages, size=clickstream_events)
    click_timestamps = [datetime.fromtimestamp(ts).isoformat() for ts in np.random.randint(txn_start_ts, txn_end_ts, size=clickstream_events)]

    dirty_click_idx = set(np.random.choice(clickstream_events, size=int(clickstream_events * dirty_rate), replace=False))
    click_path = os.path.join(output_dir, "clickstream.jsonl")

    with open(click_path, "w", encoding="utf-8") as f:
        for idx in range(clickstream_events):
            event_uid = f"evt_{1000000 + idx}"
            u_id = int(assigned_users[idx])
            if idx in dirty_click_idx:
                if idx % 2 == 0:
                    u_id = None
                else:
                    event_uid = f"evt_{1000000 + (idx - 1)}"

            record = {
                "event_id": event_uid,
                "session_id": assigned_sessions[idx],
                "user_id": u_id,
                "timestamp": click_timestamps[idx],
                "page_url": assigned_pages[idx],
                "action_event": assigned_events[idx],
                "device_type": assigned_devices[idx],
                "telemetry": {
                    "load_time_ms": int(np.random.normal(350, 80)),
                    "network_type": random.choice(["4G", "5G", "WiFi"]),
                    "viewport": random.choice(["390x844", "1920x1080"])
                }
            }
            f.write(json.dumps(record) + "\n")
    print(f"    Saved: {click_path} ({clickstream_events:,} events)")
    print("\n[+] Data Synthesis complete! All 3 datasets created successfully.")

if __name__ == "__main__":
    generate_all()
