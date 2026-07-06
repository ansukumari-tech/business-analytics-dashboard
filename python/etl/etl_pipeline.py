"""
etl_pipeline.py
Generates clean CSV datasets from raw source using Pandas.
Run this first before any analysis scripts.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import random
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ── Dimension tables ─────────────────────────────────────────
regions = pd.DataFrame({
    "region_id":   [1, 2, 3, 4, 5],
    "region_name": ["North", "South", "East", "West", "Central"],
    "country":     ["India"] * 5,
})

products = pd.DataFrame({
    "product_id":   range(1, 16),
    "product_name": [
        "Laptop Pro 15","Wireless Mouse","USB-C Hub 7-in-1","Office Chair Ergo",
        "Standing Desk","Whiteboard 4x3","Sticky Notes Pack","Ballpoint Pens 12pk",
        "A4 Paper Ream 500","Webcam HD 1080p","Monitor 24-inch","Mechanical Keyboard",
        "Desk Lamp LED","File Cabinet 4-draw","Planner 2024",
    ],
    "category": [
        "Electronics","Electronics","Electronics","Furniture","Furniture",
        "Office","Stationery","Stationery","Stationery","Electronics",
        "Electronics","Electronics","Furniture","Furniture","Stationery",
    ],
    "unit_cost":  [45000,350,900,8000,15000,3500,80,60,250,2200,12000,3500,900,7500,200],
    "unit_price": [72000,799,1999,14500,28000,6500,199,149,499,4299,19999,6999,1799,13500,449],
})
products["margin_pct"] = ((products["unit_price"] - products["unit_cost"]) / products["unit_price"] * 100).round(1)

customers = pd.DataFrame({
    "customer_id":   range(1, 16),
    "customer_name": [
        "Reliance Industries","TechStart Solutions","Rahul Sharma","Infosys Ltd",
        "Priya Nair","Growfast Ventures","Wipro Technologies","Sneha Joshi",
        "NextGen Retail","Amit Kumar","Zomato Pvt Ltd","Meera Singh",
        "CloudNine Tech","HCL Technologies","Divya Reddy",
    ],
    "segment":    ["Corporate","Small Business","Consumer","Corporate","Consumer",
                   "Small Business","Corporate","Consumer","Small Business","Consumer",
                   "Corporate","Consumer","Small Business","Corporate","Consumer"],
    "region_id":  [1,2,1,2,2,4,2,4,5,3,1,5,1,1,2],
    "city":       ["Mumbai","Bangalore","Delhi","Bangalore","Chennai","Pune",
                   "Hyderabad","Pune","Nagpur","Kolkata","Gurgaon","Bhopal",
                   "Noida","Noida","Hyderabad"],
    "joined_year":[2022,2022,2022,2022,2022,2022,2022,2023,2023,2023,2023,2023,2023,2023,2023],
})

sales_reps = pd.DataFrame({
    "rep_id":       range(1, 6),
    "rep_name":     ["Arjun Mehta","Kavya Iyer","Rohit Das","Simran Kaur","Nikhil Tiwari"],
    "region_id":    [1, 2, 3, 4, 5],
    "target_amount":[2500000, 2800000, 2000000, 2200000, 1800000],
})

# ── Fact table (denormalised sales) ─────────────────────────
np.random.seed(42)
n = 300
order_ids = range(1, n + 1)
order_dates = [date(2023, 1, 1) + timedelta(days=int(x)) for x in np.random.randint(0, 730, n)]
cust_ids = np.random.choice(customers["customer_id"].tolist(), n)
rep_ids  = np.random.choice(sales_reps["rep_id"].tolist(), n)
prod_ids = np.random.choice(products["product_id"].tolist(), n)
quantities = np.random.randint(1, 8, n)
discounts  = np.random.choice([0.0, 0.0, 0.0, 0.05, 0.08, 0.10, 0.15, 0.20], n)
statuses   = np.random.choice(["Delivered","Delivered","Delivered","Pending","Cancelled","Returned"], n)

sales = pd.DataFrame({
    "order_id":   order_ids,
    "order_date": order_dates,
    "customer_id":cust_ids,
    "rep_id":     rep_ids,
    "product_id": prod_ids,
    "quantity":   quantities,
    "discount":   discounts,
    "status":     statuses,
})

# Merge in dimension info
sales = sales.merge(customers[["customer_id","customer_name","segment","region_id","city"]], on="customer_id")
sales = sales.merge(regions[["region_id","region_name"]], on="region_id")
sales = sales.merge(sales_reps[["rep_id","rep_name"]], on="rep_id")
sales = sales.merge(products[["product_id","product_name","category","unit_cost","unit_price"]], on="product_id")

sales["revenue"] = (sales["quantity"] * sales["unit_price"] * (1 - sales["discount"])).round(2)
sales["cost"]    = (sales["quantity"] * sales["unit_cost"]).round(2)
sales["profit"]  = (sales["revenue"] - sales["cost"]).round(2)
sales["year"]    = pd.to_datetime(sales["order_date"]).dt.year
sales["month"]   = pd.to_datetime(sales["order_date"]).dt.month
sales["month_name"] = pd.to_datetime(sales["order_date"]).dt.strftime("%b")
sales["quarter"] = pd.to_datetime(sales["order_date"]).dt.quarter
sales["margin_pct"] = (sales["profit"] / sales["revenue"] * 100).round(2)

# ── Save raw CSVs ────────────────────────────────────────────
sales.to_csv(RAW_DIR / "sales_raw.csv", index=False)
products.to_csv(RAW_DIR / "products.csv", index=False)
customers.to_csv(RAW_DIR / "customers.csv", index=False)
regions.to_csv(RAW_DIR / "regions.csv", index=False)
sales_reps.to_csv(RAW_DIR / "sales_reps.csv", index=False)
print("✅ Raw CSVs saved to data/raw/")

# ── Processed aggregates ─────────────────────────────────────
delivered = sales[sales["status"] == "Delivered"]

# Monthly summary
monthly = (delivered.groupby(["year","month","month_name"])
           .agg(orders=("order_id","nunique"), revenue=("revenue","sum"),
                cost=("cost","sum"), profit=("profit","sum"))
           .reset_index())
monthly["margin_pct"] = (monthly["profit"] / monthly["revenue"] * 100).round(2)
monthly.to_csv(PROCESSED_DIR / "monthly_summary.csv", index=False)

# Category summary
category = (delivered.groupby("category")
            .agg(revenue=("revenue","sum"), profit=("profit","sum"),
                 units=("quantity","sum"))
            .reset_index())
category["margin_pct"] = (category["profit"] / category["revenue"] * 100).round(2)
category.to_csv(PROCESSED_DIR / "category_summary.csv", index=False)

# Region summary
region = (delivered.groupby("region_name")
          .agg(revenue=("revenue","sum"), profit=("profit","sum"),
               orders=("order_id","nunique"))
          .reset_index())
region.to_csv(PROCESSED_DIR / "region_summary.csv", index=False)

# Product performance
product_perf = (delivered.groupby(["product_name","category"])
                .agg(revenue=("revenue","sum"), profit=("profit","sum"),
                     units=("quantity","sum"))
                .reset_index()
                .sort_values("revenue", ascending=False))
product_perf.to_csv(PROCESSED_DIR / "product_performance.csv", index=False)

# Rep leaderboard
rep_perf = (delivered.groupby(["rep_name","region_name"])
            .agg(orders=("order_id","nunique"), revenue=("revenue","sum"))
            .reset_index()
            .sort_values("revenue", ascending=False))
rep_perf.to_csv(PROCESSED_DIR / "rep_performance.csv", index=False)

# Segment analysis
segment = (delivered.groupby("segment")
           .agg(customers=("customer_id","nunique"), revenue=("revenue","sum"),
                orders=("order_id","nunique"))
           .reset_index())
segment["avg_order_value"] = (segment["revenue"] / segment["orders"]).round(2)
segment.to_csv(PROCESSED_DIR / "segment_summary.csv", index=False)

print("✅ Processed CSVs saved to data/processed/")
print(f"\n📊 Dataset summary:")
print(f"   Total orders  : {len(sales)}")
print(f"   Delivered     : {len(delivered)}")
print(f"   Total revenue : ₹{delivered['revenue'].sum():,.0f}")
print(f"   Gross profit  : ₹{delivered['profit'].sum():,.0f}")
print(f"   Profit margin : {(delivered['profit'].sum()/delivered['revenue'].sum()*100):.1f}%")
