# 📊 Business Analytics Dashboard

> End-to-end business intelligence project using **SQL · Python · Excel · Power BI** — covering sales analytics, regional performance, customer segmentation, and YoY growth for a simulated Indian B2B company.

![SQL](https://img.shields.io/badge/SQL-MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-Advanced-217346?style=flat-square&logo=microsoft-excel&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-6C63FF?style=flat-square)

---

## 🎯 Project Overview

A complete business analytics system for a B2B product company selling across 5 regions in India. The project demonstrates the full analytics pipeline — from raw data modelling in SQL to automated ETL in Python, visual reporting in Excel, and an interactive dashboard in Power BI.

**Dataset:** 300 orders, 15 products, 15 customers, 5 sales reps, 2 years (2023–2024)

---

## 📁 Project Structure

```
business-analytics-dashboard/
│
├── assets/
│   ├── Executive_Summary.png          # Power BI Page 1 screenshot
│   ├── Product_Analysis.png           # Power BI Page 2 screenshot
│   ├── Excel_Preview.png              # Excel workbook screenshot
│   ├── sql_tables.png                 # MySQL SHOW TABLES screenshot
│   └── sql_kpi_counts.png             # MySQL KPI counts screenshot
│
├── excel/
│   └── Business_Analytics_Dashboard.xlsx  # 7-sheet formatted workbook
│
├── powerbi/
│   ├── Business_Analytics_Dashboard.pbix  # Power BI dashboard file
│   └── dax_measures.dax                   # All DAX measures reference
│
├── python/
│   ├── analysis/
│   │   └── eda_analysis.py            # EDA with 10 analytical sections
│   ├── data/
│   │   ├── raw/                       # Generated CSVs by etl_pipeline.py
│   │   └── processed/                 # Aggregated summary CSVs
│   ├── etl/
│   │   ├── etl_pipeline.py            # Data generation + CSV export
│   │   └── generate_excel.py          # Excel workbook builder (7 sheets)
│   ├── reports/                       # 8 PNG charts from visualize.py
│   └── visualization/
│       └── visualize.py               # 8 publication charts
│
├── sql/
│   ├── schema/
│   │   ├── 01_create_tables.sql       # Database schema (6 tables)
│   │   └── 02_seed_data.sql           # Full seed data
│   ├── queries/
│   │   └── 01_core_analytics.sql      # 10 analytical queries
│   ├── views/
│   │   └── 01_views.sql               # 4 reusable SQL views
│   └── stored_procedures/
│       └── 01_procedures.sql          # 3 stored procedures
│
├── .gitignore
├── README.md
└── requirements.txt

```

---

## 🛠️ Tech Stack & Skills Demonstrated

| Tool | What You'll Learn |
|------|-------------------|
| **MySQL** | Schema design, JOINs, GROUP BY, Window Functions (RANK, LAG), CTEs, Views, Stored Procedures |
| **Python (Pandas)** | ETL pipeline, data cleaning, aggregations, merge/groupby |
| **Python (Matplotlib/Seaborn)** | 8 chart types: line, bar, donut, scatter, heatmap |
| **Python (openpyxl)** | Excel automation — formatting, formulas, charts |
| **Excel** | 7-sheet workbook with conditional formatting, charts, RFM analysis |
| **Power BI** | Star schema, DAX measures, time intelligence, interactive dashboards |

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- MySQL 8.0+ (optional — for SQL section)
- Power BI Desktop (optional — for dashboard)

### Step 1: Clone & install dependencies

```bash
git clone https://github.com/YOUR_USERNAME/business-analytics-dashboard.git
cd business-analytics-dashboard

pip install -r requirements.txt
```

### Step 2: Run the ETL pipeline (generates all data)

```bash
python python/etl/etl_pipeline.py
```

Output:
```
✅ Raw CSVs saved to data/raw/
✅ Processed CSVs saved to data/processed/

📊 Dataset summary:
   Total orders  : 300
   Delivered     : 150
   Total revenue : ₹6,616,820
   Gross profit  : ₹2,517,120
   Profit margin : 38.0%
```

### Step 3: Run EDA

```bash
python python/analysis/eda_analysis.py
```

Prints 10 analytical sections: KPIs, monthly trends, categories, regions, reps, segments, correlation, YoY growth.

### Step 4: Generate Charts

```bash
python python/visualization/visualize.py
```

Saves 8 PNG charts to `reports/`

### Step 5: Build Excel Workbook

```bash
python python/etl/generate_excel.py
```

Generates `excel/Business_Analytics_Dashboard.xlsx` with 7 sheets.

---

## 🗄️ SQL Setup (MySQL)

```bash
# Connect to MySQL
mysql -u root -p

# Run schema
source sql/schema/01_create_tables.sql
source sql/schema/02_seed_data.sql

# Create views
source sql/views/01_views.sql

# Create stored procedures
source sql/stored_procedures/01_procedures.sql

# Run analytics queries
source sql/queries/01_core_analytics.sql
```

**Key SQL features used:**
- Window functions: `RANK()`, `LAG()`, `SUM() OVER()`
- CTEs: `WITH yearly AS (...)`
- Multi-table JOINs (5-way joins)
- Aggregations: `GROUP BY`, `HAVING`
- `COALESCE`, `NULLIF`, `DATE_FORMAT`

---

## 📊 Excel Workbook — 7 Sheets

| Sheet | Contents |
|-------|---------|
| **Sales Data** | Full 300-row fact table with filters enabled |
| **Monthly KPI** | KPI summary cards + monthly table + line chart |
| **Category Analysis** | Revenue/profit/margin by category + bar chart |
| **Regional Performance** | Region breakdown + pie chart |
| **Rep Leaderboard** | Gold/Silver/Bronze colour coding |
| **Product Performance** | Top 15 products ranked |
| **Customer RFM** | Recency-Frequency-Monetary tier analysis |

---

## 📈 Power BI Dashboard

Follow `powerbi/POWERBI_SETUP_GUIDE.md` to build a 4-page interactive dashboard:

- **Page 1:** Executive Summary (Revenue, Profit, Orders, Trends)
- **Page 2:** Product Analysis (Matrix, Scatter, Category drill-down)
- **Page 3:** Sales Rep Performance (Leaderboard, Gauge, Map)
- **Page 4:** Customer Intelligence (RFM Table, Segment breakdown)

All DAX measures are in `powerbi/dax_measures.dax` — copy-paste ready.

---

## 📸 Generated Charts

| Chart | Type | Insight |
|-------|------|---------|
| `01_monthly_trend.png` | Line | Revenue & profit trend 2023–2024 |
| `02_revenue_by_category.png` | Horizontal Bar | Category comparison |
| `03_region_donut.png` | Donut | Regional revenue split |
| `04_top_products.png` | Bar | Top 10 products |
| `05_rep_performance.png` | Bar | Sales rep leaderboard |
| `06_segment_analysis.png` | Pie + Bar | Segment revenue + AOV |
| `07_discount_vs_margin.png` | Scatter | Discount impact on margin |
| `08_status_heatmap.png` | Heatmap | Order status by month |

---

## 💡 Key Business Insights

- **Electronics** drives 63% of revenue but has the **lowest margin (36%)**
- **Stationery** has the **highest margin (52%)** despite lowest revenue — pricing opportunity
- **North & South regions** account for 63% of total revenue
- **Discounts above 15% strongly reduce margins** (Pearson r = -0.45)
- **2024 revenue grew +114.5% YoY** — driven by Corporate segment expansion
- **Corporate segment** has the highest Average Order Value (₹52K)
- **Laptop Pro 15** alone contributes 43% of total Electronics revenue

---

## 🔍 SQL Queries Summary

| Query | Technique |
|-------|-----------|
| Revenue / Cost / Profit Overview | Multi-table JOIN + aggregate |
| Monthly Revenue Trend | DATE_FORMAT + GROUP BY |
| Top 10 Products | ORDER BY + LIMIT |
| Regional vs Target | LEFT JOIN + NULLIF |
| Sales Rep Leaderboard | RANK() Window Function |
| YoY Growth | CTE + LAG() Window Function |
| Customer Lifetime Value | GROUP BY + MIN/MAX |
| Order Status % | SUM() OVER() |

---
