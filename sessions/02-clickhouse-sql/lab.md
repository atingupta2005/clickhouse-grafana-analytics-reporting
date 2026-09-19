# Lab — ClickHouse SQL for Analytics and Reporting

## Business Scenario

The reporting team now has sales data in ClickHouse.

Management needs basic reports for:

* Order volume
* Sales
* Quantity
* Regional performance
* Daily trends
* Monthly trends
* High-value orders
* Completed orders

In this lab, you will build these reports using ClickHouse SQL.

Use the `training` database.

### Connect

| Item | Value |
|------|--------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| Connection | **ClickHouse training** |
| User | `training_ro` |

Open CloudBeaver → pick **ClickHouse training** → run `SELECT version();`.

For reporting queries in this session, use the lab view **`training.v_lab_orders`**. 
It joins orders + line items + plants and exposes:

* `sales_amount`, `quantity`, `region_id`
* `status = 'Completed'` (maps stored `Closed`)

Seed date range: **2023-01-01** through **2025-06-18**. 
Completed rows exist for **region_id 1, 3, and 5** (not 2 / 4 / 6).

**Statuses in the seed:** `Open`, `Shipped`, `Completed`, `Cancelled` — there is no `Pending`.

**Tip:** Prefer aggregates or `LIMIT` on detail queries. The view is large; unbounded `SELECT` can hit result-row limits.

---

## 1. Review the Orders Data

Start by checking the available orders:

```sql
SELECT *
FROM training.v_lab_orders
LIMIT 10;
```

Check the number of orders:

```sql
SELECT count()
FROM training.v_lab_orders;
```

---

## 2. Select Required Columns

Instead of selecting all columns, select only the fields needed for a report.

```sql
SELECT
 order_id,
 order_date,
 region_id,
 quantity,
 sales_amount,
 status
FROM training.v_lab_orders
LIMIT 100;
```

### Exercise

Modify the query to display only:

* `order_id`
* `order_date`
* `sales_amount`

Keep `LIMIT 100` (or similar) on detail lists.

---

## 3. Filter Orders Using WHERE

Find orders from region 1:

```sql
SELECT
 order_id,
 order_date,
 sales_amount
FROM training.v_lab_orders
WHERE region_id = 1
LIMIT 100;
```

Find completed orders:

```sql
SELECT
 order_id,
 order_date,
 sales_amount
FROM training.v_lab_orders
WHERE status = 'Completed'
LIMIT 100;
```

Combine conditions:

```sql
SELECT
 order_id,
 order_date,
 sales_amount
FROM training.v_lab_orders
WHERE region_id = 1
 AND status = 'Completed'
LIMIT 100;
```

### Exercise

Find completed orders from region 3 (add `LIMIT 100`).

---

## 4. Filter by Sales Amount

Find orders greater than 2,000:

```sql
SELECT
 order_id,
 sales_amount
FROM training.v_lab_orders
WHERE sales_amount > 2000
ORDER BY sales_amount DESC
LIMIT 100;
```

Find orders between 1,000 and 2,000:

```sql
SELECT
 order_id,
 sales_amount
FROM training.v_lab_orders
WHERE sales_amount >= 1000
 AND sales_amount <= 2000
ORDER BY sales_amount DESC
LIMIT 100;
```

### Exercise

Find all orders with a sales amount greater than 1,500 (use `LIMIT 100`).

---

## 5. Use ORDER BY and LIMIT

Find the five highest-value orders:

```sql
SELECT
 order_id,
 order_date,
 sales_amount
FROM training.v_lab_orders
ORDER BY sales_amount DESC
LIMIT 5;
```

Find the five lowest-value orders:

```sql
SELECT
 order_id,
 order_date,
 sales_amount
FROM training.v_lab_orders
ORDER BY sales_amount ASC
LIMIT 5;
```

### Exercise

Return the three most recent orders.

---

## 6. Find Unique Values

Find all regions represented in the orders:

```sql
SELECT DISTINCT region_id
FROM training.v_lab_orders
ORDER BY region_id;
```

Find unique order statuses:

```sql
SELECT DISTINCT status
FROM training.v_lab_orders
ORDER BY status;
```

Find unique region and plant combinations:

```sql
SELECT DISTINCT
 region_id,
 plant_id
FROM training.v_lab_orders
ORDER BY
 region_id,
 plant_id;
```

---

## 7. Calculate Basic KPIs

Create a simple overall sales KPI report:

```sql
SELECT
 count() AS total_orders,
 sum(quantity) AS total_quantity,
 sum(sales_amount) AS total_sales,
 avg(sales_amount) AS average_order_value,
 min(sales_amount) AS minimum_order_value,
 max(sales_amount) AS maximum_order_value
FROM training.v_lab_orders;
```

Review each value and identify what business question it answers.

---

## 8. Sales by Region

Management wants sales for each region.

```sql
SELECT
 region_id,
 count() AS order_count,
 sum(quantity) AS total_quantity,
 sum(sales_amount) AS total_sales
FROM training.v_lab_orders
GROUP BY region_id
ORDER BY total_sales DESC;
```

The result provides one row per region.

### Exercise

Modify the query so that it returns only:

```text
region_id
total_sales
```

---

## 9. Sales by Plant

Create a plant-level report:

```sql
SELECT
 plant_id,
 count() AS order_count,
 sum(quantity) AS total_quantity,
 sum(sales_amount) AS total_sales
FROM training.v_lab_orders
GROUP BY plant_id
ORDER BY total_sales DESC;
```

### Exercise

Find the plant with the highest total sales.

Use `ORDER BY` and `LIMIT`.

---

## 10. Filter Groups Using HAVING

Management wants to see only regions whose total sales are greater than 300,000.

```sql
SELECT
 region_id,
 sum(sales_amount) AS total_sales
FROM training.v_lab_orders
GROUP BY region_id
HAVING total_sales > 300000
ORDER BY total_sales DESC;
```

Notice that the condition is applied to the aggregated value.

Compare:

```text
WHERE
 -> filters individual rows

HAVING
 -> filters grouped results
```

### Exercise

Find plants with total sales greater than 200,000.

---

## 11. Daily Sales Report

Create a daily sales report:

```sql
SELECT
 order_date,
 count() AS order_count,
 sum(quantity) AS total_quantity,
 sum(sales_amount) AS total_sales
FROM training.v_lab_orders
GROUP BY order_date
ORDER BY order_date;
```

This gives the reporting team a daily view of business activity.

### Exercise

Modify the query to show only dates where total sales were greater than 100,000.

---

## 12. Monthly Sales Report

Create a monthly report:

```sql
SELECT
 toYYYYMM(order_date) AS month,
 count() AS order_count,
 sum(quantity) AS total_quantity,
 sum(sales_amount) AS total_sales
FROM training.v_lab_orders
GROUP BY month
ORDER BY month;
```

This is a common input for a monthly management report.

### Exercise

Return only:

```text
month
total_sales
```

---

## 13. Date Range Reporting

Management wants the sales report for January 2023.

```sql
SELECT
 count() AS order_count,
 sum(quantity) AS total_quantity,
 sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE order_date >= '2023-01-01'
 AND order_date < '2023-02-01';
```

The same pattern can be used for other months.

For example, February:

```sql
SELECT
 count() AS order_count,
 sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE order_date >= '2023-02-01'
 AND order_date < '2023-03-01';
```

---

## 14. String Functions

Use the `customers` table for this exercise.

Display customer names in uppercase:

```sql
SELECT
 customer_id,
 upper(customer_name) AS customer_name
FROM training.customers;
```

Find customers whose name contains `Industrial`:

```sql
SELECT
 customer_id,
 customer_name
FROM training.customers
WHERE customer_name LIKE '%Industrial%';
```

### Exercise

Find customers whose name contains `Customer` (seed names look like `Customer-N` / `Industrial-N`).

**Expected result:** You should see matching rows. Searching for `Global` returns empty — that name is not in the seed.

---

## 15. NULL Handling

Some customers do not have an email address.

Find them:

```sql
SELECT
 customer_id,
 customer_name,
 email
FROM training.customers
WHERE email IS NULL;
```

Display a replacement value instead of `NULL`:

```sql
SELECT
 customer_id,
 customer_name,
 coalesce(email, 'Not Available') AS email
FROM training.customers;
```

### Exercise

Write a query that returns only customers who have an email address.

---

## 16. Conditional Classification

Classify orders according to sales amount:

```sql
SELECT
 order_id,
 sales_amount,
 CASE
 WHEN sales_amount >= 2000 THEN 'High'
 WHEN sales_amount >= 1000 THEN 'Medium'
 ELSE 'Low'
 END AS order_category
FROM training.v_lab_orders
ORDER BY sales_amount DESC
LIMIT 100;
```

This type of classification is commonly used in reports.

### Exercise

Create your own classification:

```text
Very High
High
Normal
```

Choose suitable sales thresholds.

---

## 17. Conditional Aggregation

Calculate completed sales:

```sql
SELECT
 sumIf(sales_amount, status = 'Completed') AS completed_sales
FROM training.v_lab_orders;
```

Calculate completed orders:

```sql
SELECT
 countIf(status = 'Completed') AS completed_orders
FROM training.v_lab_orders;
```

Calculate both:

```sql
SELECT
 countIf(status = 'Completed') AS completed_orders,
 sumIf(sales_amount, status = 'Completed') AS completed_sales
FROM training.v_lab_orders;
```

---

## 18. Regional Completed Sales

Combine filtering, grouping and conditional aggregation.

```sql
SELECT
 region_id,
 countIf(status = 'Completed') AS completed_orders,
 sumIf(sales_amount, status = 'Completed') AS completed_sales
FROM training.v_lab_orders
GROUP BY region_id
ORDER BY completed_sales DESC;
```

This produces a useful management report without needing to remove non-completed rows first.

---

## 19. Build a Management KPI Report

Create one query that returns:

```text
total_orders
completed_orders
total_quantity
total_sales
completed_sales
average_order_value
```

One possible solution is:

```sql
SELECT
 count() AS total_orders,
 countIf(status = 'Completed') AS completed_orders,
 sum(quantity) AS total_quantity,
 sum(sales_amount) AS total_sales,
 sumIf(sales_amount, status = 'Completed') AS completed_sales,
 avg(sales_amount) AS average_order_value
FROM training.v_lab_orders;
```

Review each KPI and explain what it means to a business user.

---

## 20. Final Reporting Query

Create a regional management report containing:

```text
region_id
order_count
completed_orders
total_quantity
total_sales
completed_sales
```

Use:

* `GROUP BY`
* `count()`
* `countIf()`
* `sum()`
* `sumIf()`
* `ORDER BY`

A possible solution:

```sql
SELECT
 region_id,
 count() AS order_count,
 countIf(status = 'Completed') AS completed_orders,
 sum(quantity) AS total_quantity,
 sum(sales_amount) AS total_sales,
 sumIf(sales_amount, status = 'Completed') AS completed_sales
FROM training.v_lab_orders
GROUP BY region_id
ORDER BY total_sales DESC;
```

This query is similar to the type of dataset that will later be displayed in a dashboard.

---

## Lab Check

Before finishing, make sure you can independently:

* Select required columns.
* Filter rows with `WHERE`.
* Sort results with `ORDER BY`.
* Limit results.
* Find unique values with `DISTINCT`.
* Use aggregate functions.
* Group data with `GROUP BY`.
* Filter aggregated results with `HAVING`.
* Use date functions for daily and monthly reports.
* Use basic string functions.
* Handle `NULL` values.
* Use `CASE` for classification.
* Use `sumIf()` and `countIf()` for KPI calculations.
* Build a simple management report from raw order data.
