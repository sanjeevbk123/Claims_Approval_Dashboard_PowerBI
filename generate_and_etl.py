"""
generate_and_etl.py
Creates a realistic synthetic insurance claims dataset, performs cleaning/ETL,
and stores the results as CSV and SQLite for easy BI dashboarding.
"""

from pathlib import Path
import random
import sqlite3
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

# ---------- Paths ----------
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROC_DIR = ROOT / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

RAW_CSV = RAW_DIR / "insurance_claims.csv"
CLEAN_CSV = PROC_DIR / "clean_claims.csv"
DB_PATH = PROC_DIR / "insurance.db"
EXCEL_SUMMARY = ROOT / "reports" / "summary.xlsx"

# ---------- Parameters ----------
N_RECORDS = 600  # ~500-800 is good for a portfolio demo
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker("en_IN")

CLAIM_TYPES = ["Motor", "Health", "Property"]
STATUSES = ["Approved", "Rejected", "Pending"]
REGIONS = [
    "Karnataka", "Maharashtra", "Delhi", "Tamil Nadu", "Gujarat",
    "Telangana", "West Bengal", "Rajasthan", "Uttar Pradesh", "Kerala"
]
AGENTS = [f"A{str(i).zfill(3)}" for i in range(1, 51)]  # A001..A050

# ---------- Helpers ----------
def rand_date_within_months(months_back=18):
    days_back = random.randint(0, months_back * 30)
    return datetime.today() - timedelta(days=days_back)

def generate_record(idx: int) -> dict:
    claim_type = random.choices(CLAIM_TYPES, weights=[0.5, 0.3, 0.2], k=1)[0]
    status = random.choices(STATUSES, weights=[0.7, 0.2, 0.1], k=1)[0]
    region = random.choice(REGIONS)
    agent = random.choice(AGENTS)

    # Amount ranges by type (in INR)
    if claim_type == "Motor":
        amount = random.randint(10000, 250000)
        base_days = random.randint(5, 25)
    elif claim_type == "Health":
        amount = random.randint(20000, 500000)
        base_days = random.randint(7, 35)
    else:  # Property
        amount = random.randint(30000, 500000)
        base_days = random.randint(10, 45)

    # Fraud flags slightly more frequent for higher amounts
    fraud_flag = 1 if random.random() < min(0.05 + amount/1_000_000, 0.15) else 0

    # Pending claims usually more recent and with fewer settlement days recorded
    claim_date = rand_date_within_months(18)
    if status == "Pending":
        settlement_days = random.randint(1, 10)
    else:
        jitter = int(np.random.normal(loc=0, scale=5))
        settlement_days = max(1, base_days + jitter)

    return {
        "ClaimID": f"C{100000 + idx}",
        "PolicyID": f"P{200000 + random.randint(1, 99999)}",
        "CustomerID": f"CU{300000 + random.randint(1, 99999)}",
        "ClaimType": claim_type,
        "ClaimAmount": amount,
        "ClaimStatus": status,
        "SettlementDays": settlement_days,
        "FraudFlag": fraud_flag,
        "ClaimDate": claim_date.date().isoformat(),
        "Region": region,
        "AgentID": agent,
    }

def generate_raw(n=N_RECORDS) -> pd.DataFrame:
    rows = [generate_record(i) for i in range(n)]
    df = pd.DataFrame(rows)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Remove obviously bad rows
    df = df[df["ClaimAmount"] > 0].copy()

    # Clamp settlement days to reasonable range
    df["SettlementDays"] = df["SettlementDays"].clip(1, 90)

    # Ensure statuses are valid
    df["ClaimStatus"] = df["ClaimStatus"].where(df["ClaimStatus"].isin(STATUSES), "Pending")

    # Derive year-month for trend charts
    df["ClaimDate"] = pd.to_datetime(df["ClaimDate"])
    df["YearMonth"] = df["ClaimDate"].dt.to_period("M").astype(str)

    return df

def write_sqlite(df: pd.DataFrame, db_path: Path, table_name="Claims"):
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

def build_excel_summary(df: pd.DataFrame, path: Path):
    # Simple pivot-style summaries
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        # KPI sheet
        kpi = pd.DataFrame({
            "TotalClaims": [len(df)],
            "ApprovalRate": [(df["ClaimStatus"]=="Approved").mean()],
            "AvgSettlementDays": [df.loc[df["ClaimStatus"]=="Approved","SettlementDays"].mean()]
        })
        kpi.to_excel(writer, sheet_name="KPI", index=False)

        # By Type
        by_type = df.groupby("ClaimType").agg(
            Total=("ClaimID","count"),
            AvgSettlementDays=("SettlementDays","mean"),
            FraudRate=("FraudFlag","mean")
        ).reset_index()
        by_type.to_excel(writer, sheet_name="ByType", index=False)

        # By Region
        by_region = df.groupby("Region").agg(
            Total=("ClaimID","count"),
            FraudCases=("FraudFlag","sum")
        ).reset_index()
        by_region.to_excel(writer, sheet_name="ByRegion", index=False)

        # Trend
        trend = df.groupby("YearMonth").size().reset_index(name="ClaimVolume")
        trend.to_excel(writer, sheet_name="Trend", index=False)

def main():
    print("Generating raw dataset...")
    raw_df = generate_raw(N_RECORDS)
    raw_df.to_csv(RAW_CSV, index=False)
    print(f"Wrote raw CSV: {RAW_CSV}")

    print("Cleaning & transforming...")
    clean_df = clean_data(raw_df)
    clean_df.to_csv(CLEAN_CSV, index=False)
    print(f"Wrote clean CSV: {CLEAN_CSV}")

    print("Writing SQLite database...")
    write_sqlite(clean_df, DB_PATH)
    print(f"Wrote SQLite DB: {DB_PATH}")

    print("Building Excel summary...")
    build_excel_summary(clean_df, EXCEL_SUMMARY)
    print(f"Wrote Excel: {EXCEL_SUMMARY}")

    print("Done. You can now connect Tableau/Power BI to the clean CSV or SQLite DB.")

if __name__ == "__main__":
    main()
