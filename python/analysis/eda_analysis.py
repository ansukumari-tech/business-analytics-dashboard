"""
eda_analysis.py
Exploratory Data Analysis — prints stats and insights.
Run after etl_pipeline.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

PROCESSED = Path(__file__).parent.parent / "data" / "processed"
RAW = Path(__file__).parent.parent / "data" / "raw"

sales     = pd.read_csv(RAW / "sales_raw.csv", parse_dates=["order_date"])
monthly   = pd.read_csv(PROCESSED / "monthly_summary.csv")
category  = pd.read_csv(PROCESSED / "category_summary.csv")
region    = pd.read_csv(PROCESSED / "region_summary.csv")
products  = pd.read_csv(PROCESSED / "product_performance.csv")
reps      = pd.read_csv(PROCESSED / "rep_performance.csv")
segment   = pd.read_csv(PROCESSED / "segment_summary.csv")

delivered = sales[sales["status"] == "Delivered"]

separator = "─" * 55

def section(title):
    print(f"\n{separator}\n  {title}\n{separator}")

section("1. OVERALL KPIs")
print(f"  Total Orders       : {len(delivered):,}")
print(f"  Total Revenue      : ₹{delivered['revenue'].sum():,.0f}")
print(f"  Total Profit       : ₹{delivered['profit'].sum():,.0f}")
print(f"  Avg Profit Margin  : {delivered['profit'].sum()/delivered['revenue'].sum()*100:.1f}%")
print(f"  Avg Order Value    : ₹{delivered.groupby('order_id')['revenue'].sum().mean():,.0f}")

section("2. ORDER STATUS BREAKDOWN")
print(sales["status"].value_counts().to_string())

section("3. REVENUE BY CATEGORY")
print(category[["category","revenue","profit","margin_pct"]]
      .sort_values("revenue", ascending=False).to_string(index=False))

section("4. MONTHLY REVENUE (DELIVERED ONLY)")
for yr in sorted(monthly["year"].unique()):
    print(f"\n  ── {yr} ──")
    sub = monthly[monthly["year"] == yr][["month_name","revenue","profit","margin_pct"]]
    print(sub.to_string(index=False))

section("5. REGIONAL PERFORMANCE")
print(region.sort_values("revenue", ascending=False).to_string(index=False))

section("6. TOP 5 PRODUCTS BY REVENUE")
print(products.head(5)[["product_name","category","revenue","profit","units"]].to_string(index=False))

section("7. SALES REP LEADERBOARD")
print(reps.to_string(index=False))

section("8. CUSTOMER SEGMENT ANALYSIS")
print(segment.to_string(index=False))

section("9. CORRELATION — DISCOUNT vs PROFIT MARGIN")
corr = delivered[["discount","margin_pct"]].corr().iloc[0,1]
print(f"  Pearson r = {corr:.3f}")
print(f"  Interpretation: {'Negative — higher discounts reduce margins' if corr < 0 else 'Positive'}")

section("10. YoY GROWTH")
yearly = delivered.groupby("year")["revenue"].sum()
years = list(yearly.index)
for i, yr in enumerate(years):
    rev = yearly[yr]
    if i == 0:
        print(f"  {yr}: ₹{rev:,.0f} (base year)")
    else:
        prev_rev = yearly[years[i-1]]
        growth = (rev - prev_rev) / prev_rev * 100
        print(f"  {yr}: ₹{rev:,.0f}  → YoY growth: {growth:+.1f}%")

print(f"\n{'─'*55}")
print("  EDA complete. Run visualize.py to generate charts.")
print(f"{'─'*55}\n")
