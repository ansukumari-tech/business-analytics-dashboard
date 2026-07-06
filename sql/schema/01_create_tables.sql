-- ============================================================
-- Business Analytics Dashboard — Schema
-- Database: business_analytics
-- Author: Ansu Verma
-- ============================================================

CREATE DATABASE IF NOT EXISTS business_analytics;
USE business_analytics;

-- Regions
CREATE TABLE IF NOT EXISTS regions (
    region_id   INT PRIMARY KEY AUTO_INCREMENT,
    region_name VARCHAR(50) NOT NULL,
    country     VARCHAR(50) NOT NULL DEFAULT 'India'
);

-- Products
CREATE TABLE IF NOT EXISTS products (
    product_id    INT PRIMARY KEY AUTO_INCREMENT,
    product_name  VARCHAR(100) NOT NULL,
    category      VARCHAR(50)  NOT NULL,
    sub_category  VARCHAR(50),
    unit_cost     DECIMAL(10,2) NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL
);

-- Customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id   INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    segment       ENUM('Consumer','Corporate','Small Business') NOT NULL,
    region_id     INT,
    city          VARCHAR(50),
    email         VARCHAR(100),
    joined_date   DATE,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

-- Sales Reps
CREATE TABLE IF NOT EXISTS sales_reps (
    rep_id          INT PRIMARY KEY AUTO_INCREMENT,
    rep_name        VARCHAR(100) NOT NULL,
    region_id       INT,
    hire_date       DATE,
    target_amount   DECIMAL(12,2),
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

-- Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id    INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    rep_id      INT,
    order_date  DATE NOT NULL,
    ship_date   DATE,
    status      ENUM('Delivered','Pending','Cancelled','Returned') DEFAULT 'Delivered',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
);

-- Order Line Items
CREATE TABLE IF NOT EXISTS order_items (
    item_id    INT PRIMARY KEY AUTO_INCREMENT,
    order_id   INT NOT NULL,
    product_id INT NOT NULL,
    quantity   INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    discount   DECIMAL(4,2) DEFAULT 0.00,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Monthly Targets
CREATE TABLE IF NOT EXISTS monthly_targets (
    target_id      INT PRIMARY KEY AUTO_INCREMENT,
    region_id      INT NOT NULL,
    year           INT NOT NULL,
    month          INT NOT NULL,
    target_revenue DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);
