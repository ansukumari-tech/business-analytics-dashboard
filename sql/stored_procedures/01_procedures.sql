-- ============================================================
-- Business Analytics Dashboard — Stored Procedures
-- ============================================================
USE business_analytics;

DELIMITER $$

-- SP 1: Get revenue summary for a given year
CREATE PROCEDURE IF NOT EXISTS sp_revenue_summary(IN p_year INT)
BEGIN
    SELECT
        month_name,
        SUM(revenue)  AS revenue,
        SUM(profit)   AS profit,
        ROUND(SUM(profit)/SUM(revenue)*100, 2) AS margin_pct
    FROM vw_monthly_kpi
    WHERE year = p_year
    GROUP BY month, month_name
    ORDER BY month;
END$$

-- SP 2: Get rep performance for a given year
CREATE PROCEDURE IF NOT EXISTS sp_rep_performance(IN p_year INT)
BEGIN
    SELECT
        rep_name,
        region_name,
        COUNT(DISTINCT order_id) AS orders,
        ROUND(SUM(revenue), 2)   AS revenue
    FROM vw_sales_fact
    WHERE status = 'Delivered' AND year = p_year
    GROUP BY rep_name, region_name
    ORDER BY revenue DESC;
END$$

-- SP 3: Add a new order (transaction-safe)
CREATE PROCEDURE IF NOT EXISTS sp_create_order(
    IN p_customer_id INT,
    IN p_rep_id      INT,
    IN p_order_date  DATE,
    IN p_product_id  INT,
    IN p_quantity    INT,
    IN p_discount    DECIMAL(4,2)
)
BEGIN
    DECLARE v_order_id INT;
    DECLARE v_unit_price DECIMAL(10,2);

    START TRANSACTION;
        SELECT unit_price INTO v_unit_price FROM products WHERE product_id = p_product_id;

        INSERT INTO orders (customer_id, rep_id, order_date, status)
        VALUES (p_customer_id, p_rep_id, p_order_date, 'Pending');

        SET v_order_id = LAST_INSERT_ID();

        INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount)
        VALUES (v_order_id, p_product_id, p_quantity, v_unit_price, p_discount);

        SELECT v_order_id AS new_order_id;
    COMMIT;
END$$

DELIMITER ;
