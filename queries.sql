-- ============================================
-- RETAIL SALES ANALYSIS PROJECT
-- SQL QUERIES
-- ============================================

-- Create Table

CREATE TABLE retail_sales (
transaction_id INT PRIMARY KEY,
sale_date DATE,
customer_id INT,
gender VARCHAR(10),
age INT,
product_category VARCHAR(50),
quantity INT,
price_per_unit FLOAT,
total_amount FLOAT
);

-- ============================================
-- DATA EXPLORATION
-- ============================================

-- Total Records
SELECT COUNT(*) AS total_records
FROM retail_sales;

-- View First Records
SELECT *
FROM retail_sales
LIMIT 10;

-- Unique Product Categories
SELECT DISTINCT product_category
FROM retail_sales;

-- Total Customers
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM retail_sales;

-- ============================================
-- SALES ANALYSIS
-- ============================================

-- Total Revenue
SELECT SUM(total_amount) AS total_revenue
FROM retail_sales;

-- Average Revenue Per Transaction
SELECT AVG(total_amount) AS avg_transaction_value
FROM retail_sales;

-- Highest Transaction Value
SELECT MAX(total_amount) AS highest_transaction
FROM retail_sales;

-- Lowest Transaction Value
SELECT MIN(total_amount) AS lowest_transaction
FROM retail_sales;

-- ============================================
-- PRODUCT CATEGORY ANALYSIS
-- ============================================

-- Revenue by Product Category
SELECT product_category,
SUM(total_amount) AS revenue
FROM retail_sales
GROUP BY product_category
ORDER BY revenue DESC;

-- Quantity Sold by Category
SELECT product_category,
SUM(quantity) AS total_quantity_sold
FROM retail_sales
GROUP BY product_category
ORDER BY total_quantity_sold DESC;

-- Average Revenue by Category
SELECT product_category,
AVG(total_amount) AS avg_revenue
FROM retail_sales
GROUP BY product_category
ORDER BY avg_revenue DESC;

-- ============================================
-- CUSTOMER ANALYSIS
-- ============================================

-- Revenue by Gender
SELECT gender,
SUM(total_amount) AS revenue
FROM retail_sales
GROUP BY gender;

-- Number of Customers by Gender
SELECT gender,
COUNT(customer_id) AS customer_count
FROM retail_sales
GROUP BY gender;

-- Average Age by Gender
SELECT gender,
AVG(age) AS avg_age
FROM retail_sales
GROUP BY gender;

-- ============================================
-- AGE GROUP ANALYSIS
-- ============================================

SELECT
CASE
WHEN age BETWEEN 18 AND 25 THEN '18-25'
WHEN age BETWEEN 26 AND 35 THEN '26-35'
WHEN age BETWEEN 36 AND 45 THEN '36-45'
WHEN age BETWEEN 46 AND 60 THEN '46-60'
ELSE '60+'
END AS age_group,
SUM(total_amount) AS revenue
FROM retail_sales
GROUP BY age_group
ORDER BY revenue DESC;

-- ============================================
-- MONTHLY SALES ANALYSIS
-- ============================================

SELECT MONTH(sale_date) AS month,
SUM(total_amount) AS monthly_revenue
FROM retail_sales
GROUP BY MONTH(sale_date)
ORDER BY month;

-- Monthly Quantity Sold
SELECT MONTH(sale_date) AS month,
SUM(quantity) AS total_quantity
FROM retail_sales
GROUP BY MONTH(sale_date)
ORDER BY month;

-- ============================================
-- TOP CUSTOMERS
-- ============================================

SELECT customer_id,
SUM(total_amount) AS total_spent
FROM retail_sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- ============================================
-- TOP TRANSACTIONS
-- ============================================

SELECT transaction_id,
customer_id,
total_amount
FROM retail_sales
ORDER BY total_amount DESC
LIMIT 10;

-- ============================================
-- BUSINESS INSIGHTS QUERIES
-- ============================================

-- Best Selling Product Category
SELECT product_category,
SUM(quantity) AS quantity_sold
FROM retail_sales
GROUP BY product_category
ORDER BY quantity_sold DESC
LIMIT 1;

-- Most Profitable Product Category
SELECT product_category,
SUM(total_amount) AS revenue
FROM retail_sales
GROUP BY product_category
ORDER BY revenue DESC
LIMIT 1;

-- Overall Sales Summary
SELECT
COUNT(*) AS total_transactions,
COUNT(DISTINCT customer_id) AS unique_customers,
SUM(total_amount) AS total_revenue,
AVG(total_amount) AS average_transaction_value
FROM retail_sales;
