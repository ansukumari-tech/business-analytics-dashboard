-- ============================================================
-- Business Analytics Dashboard — Core Analytical Queries
-- ============================================================
USE business_analytics;

-- ─────────────────────────────────────────
-- Q1: Total Revenue, Cost, Profit Overview
-- ─────────────────────────────────────────
SELECT
    COUNT(DISTINCT o.order_id)                                              AS total_orders,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount))                    AS total_revenue,
    SUM(oi.quantity * p.unit_cost)                                          AS total_cost,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount))
        - SUM(oi.quantity * p.unit_cost)                                    AS gross_profit,
    ROUND(
        (SUM(oi.quantity * oi.unit_price * (1 - oi.discount))
         - SUM(oi.quantity * p.unit_cost))
        / SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) * 100, 2)   AS profit_margin_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p     ON oi.product_id = p.product_id
WHERE o.status = 'Delivered';

-- ─────────────────────────────────────────
-- Q2: Monthly Revenue Trend (2023 & 2024)
-- ─────────────────────────────────────────
SELECT
    YEAR(o.order_date)                                                      AS year,
    MONTH(o.order_date)                                                     AS month,
    DATE_FORMAT(o.order_date, '%b %Y')                                      AS period,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2)          AS revenue,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount))
          - SUM(oi.quantity * p.unit_cost), 2)                              AS profit
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p     ON oi.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY YEAR(o.order_date), MONTH(o.order_date)
ORDER BY year, month;

-- ─────────────────────────────────────────
-- Q3: Revenue by Product Category
-- ─────────────────────────────────────────
SELECT
    p.category,
    COUNT(DISTINCT o.order_id)                                              AS orders,
    SUM(oi.quantity)                                                        AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2)          AS revenue,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount))
          - SUM(oi.quantity * p.unit_cost), 2)                              AS profit,
    ROUND(AVG(oi.discount) * 100, 2)                                        AS avg_discount_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p     ON oi.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category
ORDER BY revenue DESC;

-- ─────────────────────────────────────────
-- Q4: Top 10 Products by Revenue
-- ─────────────────────────────────────────
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity)                                                        AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2)          AS revenue,
    ROUND((SUM(oi.quantity * oi.unit_price * (1 - oi.discount))
           - SUM(oi.quantity * p.unit_cost))
          / SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) * 100, 2) AS margin_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p     ON oi.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;

-- ─────────────────────────────────────────
-- Q5: Customer Segment Analysis
-- ─────────────────────────────────────────
SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id)                                           AS customers,
    COUNT(DISTINCT o.order_id)                                              AS orders,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2)          AS revenue,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount))
          / COUNT(DISTINCT o.order_id), 2)                                  AS avg_order_value
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Delivered'
GROUP BY c.segment
ORDER BY revenue DESC;

-- ─────────────────────────────────────────
-- Q6: Regional Sales Performance vs Target
-- ─────────────────────────────────────────
SELECT
    r.region_name,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2)          AS actual_revenue,
    COALESCE(SUM(mt.target_revenue), 0)                                     AS target_revenue,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount))
          / NULLIF(SUM(mt.target_revenue), 0) * 100, 2)                    AS achievement_pct
FROM regions r
JOIN customers c    ON r.region_id = c.region_id
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN monthly_targets mt ON r.region_id = mt.region_id
    AND mt.year = YEAR(o.order_date) AND mt.month = MONTH(o.order_date)
WHERE o.status = 'Delivered'
GROUP BY r.region_id, r.region_name
ORDER BY actual_revenue DESC;

-- ─────────────────────────────────────────
-- Q7: Sales Rep Leaderboard
-- ─────────────────────────────────────────
SELECT
    sr.rep_name,
    r.region_name,
    COUNT(DISTINCT o.order_id)                                              AS orders_closed,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2)          AS revenue_generated,
    sr.target_amount,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount))
          / sr.target_amount * 100, 2)                                     AS target_achievement_pct,
    RANK() OVER (ORDER BY SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) DESC) AS `rank`
FROM sales_reps sr
JOIN regions r      ON sr.region_id = r.region_id
JOIN orders o       ON sr.rep_id = o.rep_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Delivered'
GROUP BY sr.rep_id, sr.rep_name, r.region_name, sr.target_amount
ORDER BY revenue_generated DESC;

-- ─────────────────────────────────────────
-- Q8: Order Status Distribution
-- ─────────────────────────────────────────
SELECT
    status,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- ─────────────────────────────────────────
-- Q9: Top 5 Customers by Lifetime Value
-- ─────────────────────────────────────────
SELECT
    c.customer_name,
    c.segment,
    r.region_name,
    COUNT(DISTINCT o.order_id)                                              AS total_orders,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2)          AS lifetime_value,
    MIN(o.order_date)                                                       AS first_order,
    MAX(o.order_date)                                                       AS last_order
FROM customers c
JOIN regions r      ON c.region_id = r.region_id
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Delivered'
GROUP BY c.customer_id, c.customer_name, c.segment, r.region_name
ORDER BY lifetime_value DESC
LIMIT 5;

-- ─────────────────────────────────────────
-- Q10: YoY Revenue Growth
-- ─────────────────────────────────────────
WITH yearly AS (
    SELECT
        YEAR(o.order_date) AS yr,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'Delivered'
    GROUP BY YEAR(o.order_date)
)
SELECT
    yr,
    revenue,
    LAG(revenue) OVER (ORDER BY yr)                                        AS prev_year_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY yr))
          / LAG(revenue) OVER (ORDER BY yr) * 100, 2)                     AS yoy_growth_pct
FROM yearly;
