# Lab — Advanced ClickHouse SQL

## Business Scenario

The reporting team now needs reports that cannot be produced easily from a single table.

They need to:

* Display customer and product details with orders
* Analyze sales by product and customer
* Find customers with Cancelled-only activity (or plants with few orders)
* Rank customers and products
* Calculate running sales
* Compare monthly sales
* Build multiple KPIs in a single query

Use the existing `training` database.

**Reporting view:** use **`training.v_lab_orders`** for order sales/quantity/region. Statuses in the seed: `Open`, `Shipped`, `Completed`, `Cancelled` (no `Pending`).

**Tip:** On large JOINs, add `LIMIT 100` (or filter by date/status) so CloudBeaver stays responsive.

---

## 1. Review the Tables

Check the available tables:

```sql
SHOW TABLES FROM training;
```

Review the main tables:

```sql
DESCRIBE TABLE training.orders;
```

```sql
DESCRIBE TABLE training.customers;
```

```sql
DESCRIBE TABLE training.products;
```

---

## 2. INNER JOIN — Orders and Customers

Display the order and customer name together:

```sql
SELECT
 o.order_id,
 o.order_date,
 c.customer_name,
 o.sales_amount
FROM training.v_lab_orders AS o
INNER JOIN training.customers AS c
 ON o.customer_id = c.customer_id
ORDER BY o.order_date
LIMIT 100;
```

Observe that the `customer_id` is used to connect the two tables.

### Exercise

Modify the query to also display:

* `region_id`
* `status`

---

## 3. Orders and Products

Display product names instead of only product IDs:

```sql
SELECT
 o.order_id,
 o.order_date,
 p.product_name,
 o.quantity,
 o.sales_amount
FROM training.v_lab_orders AS o
INNER JOIN training.products AS p
 ON o.product_id = p.product_id
ORDER BY o.order_date
LIMIT 100;
```

### Exercise

Create a product sales report containing:

```text
product_name
order_count
total_quantity
total_sales
```

Sort by total sales descending.

---

## 4. Orders, Customers and Products

Combine three tables:

```sql
SELECT
 o.order_id,
 o.order_date,
 c.customer_name,
 p.product_name,
 o.quantity,
 o.sales_amount
FROM training.v_lab_orders AS o
INNER JOIN training.customers AS c
 ON o.customer_id = c.customer_id
INNER JOIN training.products AS p
 ON o.product_id = p.product_id
ORDER BY o.order_date
LIMIT 100;
```

This is a common reporting pattern where transaction data is enriched with descriptive information.

---

## 5. LEFT JOIN — Customers With Cancelled Only

In this seed, every customer has at least one order, so “customers without any orders” always returns **0 rows**. Use a workable LEFT JOIN pattern instead.

**Pattern A — customers with Cancelled orders only (no Completed):**

```sql
SELECT
 c.customer_id,
 c.customer_name,
 countIf(o.status = 'Cancelled') AS cancelled_orders,
 countIf(o.status = 'Completed') AS completed_orders
FROM training.customers AS c
LEFT JOIN training.v_lab_orders AS o
 ON c.customer_id = o.customer_id
GROUP BY
 c.customer_id,
 c.customer_name
HAVING cancelled_orders > 0
 AND completed_orders = 0
ORDER BY c.customer_id
LIMIT 100;
```

**Pattern B — plants with few orders (same LEFT JOIN idea on a smaller grain):**

```sql
SELECT
 p.plant_id,
 p.plant_name,
 count(o.order_id) AS order_rows
FROM training.plants AS p
LEFT JOIN training.v_lab_orders AS o
 ON p.plant_id = o.plant_id
GROUP BY
 p.plant_id,
 p.plant_name
HAVING order_rows < 1000
ORDER BY order_rows;
```

**Tip:** If you only need to try `LEFT JOIN` + `IS NULL`, create a tiny inline list of fictional IDs and left-join to `customers` — do not expect empty customers on the lab data.

### Discussion

Why would `INNER JOIN` remove customers that only appear on the left side of a LEFT JOIN pattern?

---

## 6. Customer Sales Report

Create a customer-level report:

```sql
SELECT
 c.customer_id,
 c.customer_name,
 count(o.order_id) AS order_count,
 sum(o.sales_amount) AS total_sales
FROM training.customers AS c
LEFT JOIN training.v_lab_orders AS o
 ON c.customer_id = o.customer_id
GROUP BY
 c.customer_id,
 c.customer_name
ORDER BY total_sales DESC
LIMIT 100;
```

This report retains customers even if they have no orders (on this seed, every customer has orders, so order_count will be > 0).

---

## 7. Use a CTE

Create a regional sales result first:

```sql
WITH regional_sales AS
(
 SELECT
 region_id,
 sum(sales_amount) AS total_sales
 FROM training.v_lab_orders
 GROUP BY region_id
)
SELECT
 region_id,
 total_sales
FROM regional_sales
ORDER BY total_sales DESC;
```

The CTE is:

```text
regional_sales
 |
 v
Main SELECT
```

### Exercise

Modify the CTE to also calculate:

```text
order_count
total_quantity
```

---

## 8. CTE with Filtering

Create a CTE containing completed regional sales:

```sql
WITH regional_sales AS
(
 SELECT
 region_id,
 count() AS completed_orders,
 sum(sales_amount) AS completed_sales
 FROM training.v_lab_orders
 WHERE status = 'Completed'
 GROUP BY region_id
)
SELECT *
FROM regional_sales
WHERE completed_sales > 300000
ORDER BY completed_sales DESC;
```

---

## 9. Subquery — Orders Above Average

Find orders whose value is greater than the average order value:

```sql
SELECT
 order_id,
 order_date,
 sales_amount
FROM training.v_lab_orders
WHERE sales_amount >
(
 SELECT avg(sales_amount)
 FROM training.v_lab_orders
)
ORDER BY sales_amount DESC
LIMIT 100;
```

### Exercise

Modify the query to return the average order value along with each result.

---

## 10. Ranking Orders

Rank all orders by sales amount:

```sql
SELECT
 order_id,
 region_id,
 sales_amount,
 row_number() OVER (
 ORDER BY sales_amount DESC
 ) AS sales_rank
FROM training.v_lab_orders
ORDER BY sales_rank
LIMIT 100;
```

The highest-value order receives rank 1.

---

## 11. Ranking Within Each Region

Now rank orders separately within each region:

```sql
SELECT
 order_id,
 region_id,
 sales_amount,
 row_number() OVER (
 PARTITION BY region_id
 ORDER BY sales_amount DESC
 ) AS region_rank
FROM training.v_lab_orders
ORDER BY
 region_id,
 region_rank
LIMIT 100;
```

Notice the use of:

```sql
PARTITION BY region_id
```

inside the window function.

This is different from table-level partitioning.

Here, `PARTITION BY` defines the group of rows over which the window function operates.

---

## 12. Top Orders Per Region

Use the previous ranking query as a CTE:

```sql
WITH ranked_orders AS
(
 SELECT
 order_id,
 region_id,
 sales_amount,
 row_number() OVER (
 PARTITION BY region_id
 ORDER BY sales_amount DESC
 ) AS region_rank
 FROM training.v_lab_orders
)
SELECT
 order_id,
 region_id,
 sales_amount,
 region_rank
FROM ranked_orders
WHERE region_rank <= 2
ORDER BY
 region_id,
 region_rank;
```

This returns the top two orders from each region.

---

## 13. Running Sales Total

Create a daily sales dataset first:

```sql
WITH daily_sales AS
(
 SELECT
 order_date,
 sum(sales_amount) AS daily_sales
 FROM training.v_lab_orders
 GROUP BY order_date
)
SELECT
 order_date,
 daily_sales,
 sum(daily_sales) OVER (
 ORDER BY order_date
 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
 ) AS running_sales
FROM daily_sales
ORDER BY order_date;
```

The result shows:

```text
Date Daily Sales Running Sales
---------- ----------- -------------
Day 1 100 100
Day 2 200 300
Day 3 150 450
```

The values above are only an illustration of the calculation.

---

## 14. Monthly Sales Comparison

Create monthly sales:

```sql
WITH monthly_sales AS
(
 SELECT
 toStartOfMonth(order_date) AS month,
 sum(sales_amount) AS total_sales
 FROM training.v_lab_orders
 GROUP BY month
)
SELECT
 month,
 total_sales,
 lagInFrame(total_sales) OVER (
 ORDER BY month
 ) AS previous_month_sales
FROM monthly_sales
ORDER BY month;
```

This allows the report to show the previous month's value next to the current month.

---

## 15. Calculate the Difference

Extend the previous query:

```sql
WITH monthly_sales AS
(
 SELECT
 toStartOfMonth(order_date) AS month,
 sum(sales_amount) AS total_sales
 FROM training.v_lab_orders
 GROUP BY month
),
monthly_comparison AS
(
 SELECT
 month,
 total_sales,
 lagInFrame(total_sales) OVER (
 ORDER BY month
 ) AS previous_month_sales
 FROM monthly_sales
)
SELECT
 month,
 total_sales,
 previous_month_sales,
 total_sales - previous_month_sales AS sales_difference
FROM monthly_comparison
ORDER BY month;
```

The first month will not have a previous-month value.

---

## 16. Conditional Aggregation

Create a regional KPI report:

```sql
SELECT
 region_id,
 count() AS total_orders,
 countIf(status = 'Completed') AS completed_orders,
 countIf(status = 'Open') AS open_orders,
 countIf(status = 'Cancelled') AS cancelled_orders,
 sum(sales_amount) AS total_sales,
 sumIf(sales_amount, status = 'Completed') AS completed_sales
FROM training.v_lab_orders
GROUP BY region_id
ORDER BY total_sales DESC;
```

This produces several KPIs in a single query.

**Expected result:** `open_orders` and `cancelled_orders` are non-zero for some regions. There is no `Pending` status in the seed.

---

## 17. Product Ranking

Calculate total sales by product and rank the products:

```sql
WITH product_sales AS
(
 SELECT
 product_id,
 sum(sales_amount) AS total_sales
 FROM training.v_lab_orders
 GROUP BY product_id
)
SELECT
 p.product_name,
 ps.total_sales,
 row_number() OVER (
 ORDER BY ps.total_sales DESC
 ) AS sales_rank
FROM product_sales AS ps
INNER JOIN training.products AS p
 ON ps.product_id = p.product_id
ORDER BY sales_rank;
```

---

## 18. Customer Ranking

Create a customer sales ranking:

```sql
WITH customer_sales AS
(
 SELECT
 customer_id,
 sum(sales_amount) AS total_sales
 FROM training.v_lab_orders
 GROUP BY customer_id
)
SELECT
 c.customer_name,
 cs.total_sales,
 row_number() OVER (
 ORDER BY cs.total_sales DESC
 ) AS sales_rank
FROM customer_sales AS cs
INNER JOIN training.customers AS c
 ON cs.customer_id = c.customer_id
ORDER BY sales_rank;
```

---

## 19. Basic Array Exercise

Create a simple array:

```sql
SELECT
 [10, 20, 30, 40] AS values;
```

Expand the values into separate rows:

```sql
SELECT
 arrayJoin([10, 20, 30, 40]) AS value;
```

Try changing the values in the array.

For example:

```sql
SELECT
 arrayJoin(['North', 'South', 'East', 'West']) AS region;
```

The objective is only to understand the basic array concept.

---

## 20. Final Challenge — Regional Sales Analysis

Create a report that contains:

```text
region_name
order_count
completed_orders
total_quantity
total_sales
completed_sales
sales_rank
```

**Requirements**

* Use `training.v_lab_orders`
* Use `training.regions`
* Calculate the KPIs by region
* Rank regions by total sales
* Sort by rank

Use a CTE and a window function.

A possible approach is:

```text
Orders
 |
 v
Regional KPI CTE
 |
 +-- total orders
 +-- completed orders
 +-- quantity
 +-- total sales
 +-- completed sales
 |
 v
Join with Regions
 |
 v
Rank by Sales
 |
 v
Final Report
```

---

## Lab Check

Before finishing, make sure you can:

* Use `INNER JOIN`.
* Use `LEFT JOIN`.
* Explain when each join is appropriate.
* Use CTEs to break a query into logical steps.
* Use subqueries.
* Use window functions.
* Rank rows globally.
* Rank rows within a group.
* Calculate running totals.
* Compare values across periods.
* Use conditional aggregation.
* Work with basic arrays.
* Combin
