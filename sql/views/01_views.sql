-- ============================================================
-- Business Analytics Dashboard — Views
-- ============================================================
USE business_analytics;

-- View 1: Flat sales fact table (used by Power BI & Excel)
CREATE OR REPLACE VIEW vw_sales_fact AS
SELECT
    o.order_id,
    o.order_date,
    YEAR(o.order_date)                                          AS year,
    MONTH(o.order_date)                                         AS month,
    DATE_FORMAT(o.order_date, '%b')                             AS month_name,
    QUARTER(o.order_date)                                       AS quarter,
    o.status,
    c.customer_name,
    c.segment,
    c.city,
    r.region_name,
    sr.rep_name,
    p.product_name,
    p.category,
    p.sub_category,
    oi.quantity,
    oi.unit_price,
    oi.discount,
    ROUND(oi.quantity * oi.unit_price * (1 - oi.discount), 2)  AS revenue,
    ROUND(oi.quantity * p.unit_cost, 2)                         AS cost,
    ROUND(oi.quantity * oi.unit_price * (1 - oi.discount)
          - oi.quantity * p.unit_cost, 2)                       AS profit,
    ROUND((oi.quantity * oi.unit_price * (1 - oi.discount)
           - oi.quantity * p.unit_cost)
          / NULLIF(oi.quantity * oi.unit_price * (1 - oi.discount), 0) * 100, 2) AS margin_pct
FROM orders o
JOIN customers  c  ON o.customer_id = c.customer_id
JOIN regions    r  ON c.region_id   = r.region_id
JOIN sales_reps sr ON o.rep_id      = sr.rep_id
JOIN order_items oi ON o.order_id   = oi.order_id
JOIN products   p  ON oi.product_id = p.product_id;

-- View 2: Monthly KPI summary
CREATE OR REPLACE VIEW vw_monthly_kpi AS
SELECT
    year,
    month,
    month_name,
    region_name,
    COUNT(DISTINCT order_id)    AS orders,
    SUM(revenue)                AS revenue,
    SUM(cost)                   AS cost,
    SUM(profit)                 AS profit,
    ROUND(SUM(profit)/SUM(revenue)*100, 2) AS margin_pct
FROM vw_sales_fact
WHERE status = 'Delivered'
GROUP BY year, month, month_name, region_name;

-- View 3: Product performance
CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    product_name,
    category,
    sub_category,
    SUM(quantity)   AS units_sold,
    SUM(revenue)    AS revenue,
    SUM(profit)     AS profit,
    ROUND(AVG(margin_pct), 2) AS avg_margin_pct,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM vw_sales_fact
WHERE status = 'Delivered'
GROUP BY product_name, category, sub_category;

-- View 4: Customer RFM (Recency, Frequency, Monetary)
CREATE OR REPLACE VIEW vw_customer_rfm AS
SELECT
    customer_name,
    segment,
    region_name,
    DATEDIFF(CURDATE(), MAX(order_date))    AS recency_days,
    COUNT(DISTINCT order_id)               AS frequency,
    ROUND(SUM(revenue), 2)                 AS monetary
FROM vw_sales_fact
WHERE status = 'Delivered'
GROUP BY customer_name, segment, region_name;
