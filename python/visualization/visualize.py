"""
visualize.py
Generates publication-quality charts saved to reports/
Run after etl_pipeline.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

PROCESSED = Path(__file__).parent.parent / "data" / "processed"
RAW       = Path(__file__).parent.parent / "data" / "raw"
REPORTS   = Path(__file__).parent.parent / "reports"
REPORTS.mkdir(exist_ok=True)

sns.set_theme(style="darkgrid", palette="deep")
plt.rcParams.update({
    "figure.facecolor": "#0f0f1a",
    "axes.facecolor":   "#161625",
    "axes.labelcolor":  "#c8c8e0",
    "xtick.color":      "#888899",
    "ytick.color":      "#888899",
    "text.color":       "#e0e0f0",
    "grid.color":       "#2a2a3d",
    "grid.linewidth":   0.6,
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.titlepad":    12,
})
PALETTE = ["#6c63ff","#ff6584","#43e97b","#f7971e","#38b2f7","#f093fb","#4facfe","#fa709a"]

sales    = pd.read_csv(RAW / "sales_raw.csv", parse_dates=["order_date"])
monthly  = pd.read_csv(PROCESSED / "monthly_summary.csv")
category = pd.read_csv(PROCESSED / "category_summary.csv")
region   = pd.read_csv(PROCESSED / "region_summary.csv")
products = pd.read_csv(PROCESSED / "product_performance.csv")
reps     = pd.read_csv(PROCESSED / "rep_performance.csv")
segment  = pd.read_csv(PROCESSED / "segment_summary.csv")

fmt = mticker.FuncFormatter(lambda x, _: f"₹{x/1e5:.0f}L" if x >= 1e5 else f"₹{x:.0f}")

def save(name):
    plt.tight_layout()
    p = REPORTS / name
    plt.savefig(p, dpi=150, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
    plt.close()
    print(f"  ✅ {name}")

# ── Chart 1: Monthly Revenue & Profit Trend ─────────────────
fig, ax = plt.subplots(figsize=(12, 5))
for yr, grp in monthly.groupby("year"):
    grp = grp.sort_values("month")
    ax.plot(grp["month_name"], grp["revenue"]/1e5,  marker="o", label=f"{yr} Revenue", linewidth=2)
    ax.plot(grp["month_name"], grp["profit"]/1e5,   marker="s", linestyle="--", label=f"{yr} Profit", linewidth=1.5)
ax.set_title("Monthly Revenue & Profit Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Amount (₹ Lakhs)")
ax.legend(facecolor="#1c1c27", labelcolor="#e0e0f0", fontsize=9)
save("01_monthly_trend.png")

# ── Chart 2: Revenue by Category (Horizontal Bar) ───────────
fig, ax = plt.subplots(figsize=(9, 5))
cat_sorted = category.sort_values("revenue")
bars = ax.barh(cat_sorted["category"], cat_sorted["revenue"]/1e5, color=PALETTE[:len(cat_sorted)])
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
for bar, val in zip(bars, cat_sorted["revenue"]/1e5):
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, f"₹{val:.0f}L", va="center", fontsize=9)
ax.set_title("Revenue by Product Category")
ax.set_xlabel("Revenue (₹ Lakhs)")
save("02_revenue_by_category.png")

# ── Chart 3: Regional Revenue (Donut) ───────────────────────
fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    region["revenue"], labels=region["region_name"],
    autopct="%1.1f%%", colors=PALETTE,
    wedgeprops={"width": 0.55, "edgecolor": "#0f0f1a", "linewidth": 2},
    startangle=90, pctdistance=0.75,
)
for at in autotexts: at.set_fontsize(10)
ax.set_title("Revenue Distribution by Region")
save("03_region_donut.png")

# ── Chart 4: Top 10 Products by Revenue ─────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
top10 = products.head(10).sort_values("revenue")
colors = [PALETTE[0] if c == "Electronics" else PALETTE[1] if c == "Furniture" else PALETTE[2]
          for c in top10["category"]]
bars = ax.barh(top10["product_name"], top10["revenue"]/1e5, color=colors)
for bar, val in zip(bars, top10["revenue"]/1e5):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2, f"₹{val:.0f}L", va="center", fontsize=9)
ax.set_title("Top 10 Products by Revenue")
ax.set_xlabel("Revenue (₹ Lakhs)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=PALETTE[0],label="Electronics"),
                   Patch(color=PALETTE[1],label="Furniture"),
                   Patch(color=PALETTE[2],label="Stationery")],
          facecolor="#1c1c27", labelcolor="#e0e0f0")
save("04_top_products.png")

# ── Chart 5: Sales Rep Performance (Grouped Bar) ────────────
fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(reps))
bars = ax.bar(x, reps["revenue"]/1e5, color=PALETTE[:len(reps)], width=0.5)
ax.set_xticks(list(x))
ax.set_xticklabels(reps["rep_name"], rotation=15, ha="right")
ax.set_title("Sales Rep Revenue Performance")
ax.set_ylabel("Revenue (₹ Lakhs)")
for bar, val in zip(bars, reps["revenue"]/1e5):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"₹{val:.0f}L", ha="center", fontsize=9)
save("05_rep_performance.png")

# ── Chart 6: Customer Segment Breakdown ─────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].pie(segment["revenue"], labels=segment["segment"],
            autopct="%1.1f%%", colors=PALETTE[:3],
            wedgeprops={"edgecolor": "#0f0f1a", "linewidth": 2})
axes[0].set_title("Revenue by Segment")
axes[1].bar(segment["segment"], segment["avg_order_value"]/1e3, color=PALETTE[:3])
axes[1].set_title("Avg Order Value by Segment (₹K)")
axes[1].set_ylabel("₹ Thousands")
save("06_segment_analysis.png")

# ── Chart 7: Discount vs Margin Scatter ─────────────────────
delivered = sales[sales["status"] == "Delivered"]
fig, ax = plt.subplots(figsize=(8, 5))
scatter = ax.scatter(delivered["discount"]*100, delivered["margin_pct"],
                     c=delivered["revenue"], cmap="plasma", alpha=0.5, s=20)
plt.colorbar(scatter, ax=ax, label="Order Revenue (₹)")
ax.set_title("Discount vs Profit Margin")
ax.set_xlabel("Discount (%)")
ax.set_ylabel("Profit Margin (%)")
save("07_discount_vs_margin.png")

# ── Chart 8: Order Status Heatmap by Month ──────────────────
pivot = (sales.groupby(["month_name","status"])
         .size().unstack(fill_value=0))
month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
pivot = pivot.reindex([m for m in month_order if m in pivot.index])
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot, ax=ax, cmap="YlOrRd", annot=True, fmt="d",
            linewidths=0.5, linecolor="#0f0f1a",
            cbar_kws={"shrink": 0.8})
ax.set_title("Order Status Distribution by Month")
ax.set_xlabel("Status")
ax.set_ylabel("Month")
save("08_status_heatmap.png")

print(f"\n🎉 All 8 charts saved to reports/")
