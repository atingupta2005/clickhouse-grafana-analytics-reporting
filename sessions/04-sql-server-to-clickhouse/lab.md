# Lab — SQL Server to ClickHouse Query Migration

## Lab Objective

Migrate representative SQL Server reporting queries to ClickHouse and validate that the ClickHouse results match the intended business logic.

Use the existing:

* SQL Server database: `TrainingDB`
* ClickHouse database: `training`

### Connect

| Item | Value |
|------|--------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| SQL Server connection | **Session 04 — SQL Server TrainingDB** |
| ClickHouse connection | **Session 01–05 — ClickHouse training (LAN RO)** |
| ClickHouse user | `training_ro` / `TrainingReadOnly!2026` |
| Alternate host (if LAN fails) | `100.86.105.24` (same ports: SQL `1433`, CH `8123`) |

**Important:** SQL Server is a **compact sample**; ClickHouse has the **full seed**. Expect SQL Server counts to be **much smaller**. Compare query **shape and logic** (columns, filters, aggregates), not identical row counts.

Statuses in ClickHouse: `Open`, `Shipped`, `Completed`, `Cancelled` — there is no `Pending`.

The tables represent the same manufacturing and sales **model** (not the same row volume).

---

## 1. Review the Source Data

Start by reviewing the available tables in both systems.

SQL Server:

```sql
USE TrainingDB;

SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';
```

ClickHouse:

```sql
SHOW TABLES FROM training;
```

Review the structure of the main tables:

```sql
SELECT *
FROM training.v_lab_orders
LIMIT 5;
```

---

## 2. Migrate TOP to LIMIT

### SQL Server

```sql
SELECT TOP 5
 order_id,
 order_date,
 sales_amount
FROM orders
ORDER BY sales_amount DESC;
```

### Task

Rewrite the query for ClickHouse.

Expected pattern:

```sql
SELECT
 order_id,
 order_date,
 sales_amount
FROM training.v_lab_orders
ORDER BY sales_amount DESC
LIMIT 5;
```

### Validate

Compare:

* Number of rows returned by this TOP/LIMIT query (both should return 5)
* Order of rows by `sales_amount`
* Column shape (`order_id`, `order_date`, `sales_amount`)

**Tip:** Do not expect the top-5 `order_id` values to match across engines — the datasets differ in size. Check that both return five rows sorted by sales descending.

---

## 3. Migrate ISNULL

### SQL Server

```sql
SELECT
 customer_id,
 customer_name,
 ISNULL(email, 'Not Available') AS email
FROM customers;
```

### Task

Rewrite the query using ClickHouse `ifNull()`.

```sql
SELECT
 customer_id,
 customer_name,
 ifNull(email, 'Not Available') AS email
FROM training.customers;
```

Run both queries and verify the customer with a missing email.

---

## 4. Migrate COALESCE

### SQL Server

```sql
SELECT
 customer_id,
 COALESCE(email, 'Not Available') AS email
FROM customers;
```

### Task

Run the equivalent ClickHouse query.

```sql
SELECT
 customer_id,
 coalesce(email, 'Not Available') AS email
FROM training.customers;
```

Compare the result with the SQL Server query.

---

## 5. Migrate CAST and CONVERT

### SQL Server

```sql
SELECT
 order_id,
 CAST(sales_amount AS decimal(12,2)) AS sales_amount
FROM orders;
```

### Task

Rewrite it for ClickHouse.

```sql
SELECT
 order_id,
 CAST(sales_amount, 'Decimal(12,2)') AS sales_amount
FROM training.v_lab_orders;
```

Now review a date conversion.

SQL Server:

```sql
SELECT
 order_id,
 CAST(order_date AS datetime) AS order_datetime
FROM orders;
```

ClickHouse:

```sql
SELECT
 order_id,
 toDateTime(order_date) AS order_datetime
FROM training.v_lab_orders;
```

Compare the resulting data types and values.

---

## 6. Migrate CASE Expressions

### SQL Server

```sql
SELECT
 order_id,
 sales_amount,
 CASE
 WHEN sales_amount >= 2000 THEN 'High'
 WHEN sales_amount >= 1000 THEN 'Medium'
 ELSE 'Low'
 END AS sales_class
FROM orders;
```

### Task

Run the equivalent query in ClickHouse.

```sql
SELECT
 order_id,
 sales_amount,
 CASE
 WHEN sales_amount >= 2000 THEN 'High'
 WHEN sales_amount >= 1000 THEN 'Medium'
 ELSE 'Low'
 END AS sales_class
FROM training.v_lab_orders;
```

Validate the classification for several orders.

---

## 7. Migrate Date Functions

### SQL Server

```sql
SELECT
 YEAR(order_date) AS order_year,
 MONTH(order_date) AS order_month,
 SUM(sales_amount) AS total_sales
FROM orders
GROUP BY
 YEAR(order_date),
 MONTH(order_date)
ORDER BY
 order_year,
 order_month;
```

### Task

Rewrite the query using ClickHouse date functions.

```sql
SELECT
 toYear(order_date) AS order_year,
 toMonth(order_date) AS order_month,
 sum(sales_amount) AS total_sales
FROM training.v_lab_orders
GROUP BY
 order_year,
 order_month
ORDER BY
 order_year,
 order_month;
```

Compare the monthly totals.

---

## 8. Migrate String Functions

### SQL Server

```sql
SELECT
 customer_name,
 UPPER(customer_name) AS customer_name_upper,
 LOWER(customer_name) AS customer_name_lower
FROM customers;
```

### Task

Rewrite the query for ClickHouse.

```sql
SELECT
 customer_name,
 upper(customer_name) AS customer_name_upper,
 lower(customer_name) AS customer_name_lower
FROM training.customers;
```

Now test string length:

SQL Server:

```sql
SELECT
 customer_name,
 LEN(customer_name) AS name_length
FROM customers;
```

ClickHouse:

```sql
SELECT
 customer_name,
 length(customer_name) AS name_length
FROM training.customers;
```

---

## 9. Migrate a JOIN Query

### SQL Server

```sql
SELECT
 o.order_id,
 c.customer_name,
 o.order_date,
 o.sales_amount
FROM orders o
INNER JOIN customers c
 ON o.customer_id = c.customer_id
WHERE o.status = 'Completed';
```

### Task

Rewrite the query for ClickHouse.

```sql
SELECT
 o.order_id,
 c.customer_name,
 o.order_date,
 o.sales_amount
FROM training.v_lab_orders AS o
INNER JOIN training.customers AS c
 ON o.customer_id = c.customer_id
WHERE o.status = 'Completed';
```

Compare:

* Row count
* Customer names
* Sales amounts
* Order dates

---

## 10. Migrate a CTE

### SQL Server

```sql
WITH regional_sales AS
(
 SELECT
 region_id,
 SUM(sales_amount) AS total_sales
 FROM orders
 WHERE status = 'Completed'
 GROUP BY region_id
)
SELECT
 region_id,
 total_sales
FROM regional_sales
WHERE total_sales > 300000
ORDER BY total_sales DESC;
```

### Task

Rewrite the query for ClickHouse.

```sql
WITH regional_sales AS
(
 SELECT
 region_id,
 sum(sales_amount) AS total_sales
 FROM training.v_lab_orders
 WHERE status = 'Completed'
 GROUP BY region_id
)
SELECT
 region_id,
 total_sales
FROM regional_sales
WHERE total_sales > 300000
ORDER BY total_sales DESC;
```

Validate the result against SQL Server.

---

## 11. Migrate a Subquery

### SQL Server

```sql
SELECT
 order_id,
 sales_amount
FROM orders
WHERE sales_amount >
(
 SELECT AVG(sales_amount)
 FROM orders
)
ORDER BY sales_amount DESC;
```

### Task

Rewrite and execute the equivalent ClickHouse query.

```sql
SELECT
 order_id,
 sales_amount
FROM training.v_lab_orders
WHERE sales_amount >
(
 SELECT avg(sales_amount)
 FROM training.v_lab_orders
)
ORDER BY sales_amount DESC;
```

Check that the same business condition is being applied.

---

## 12. Migrate a Window Function

### SQL Server

```sql
SELECT
 order_id,
 order_date,
 sales_amount,
 SUM(sales_amount) OVER (
 ORDER BY order_date, order_id
 ) AS running_sales
FROM orders;
```

### Task

Rewrite it for ClickHouse.

```sql
SELECT
 order_id,
 order_date,
 sales_amount,
 sum(sales_amount) OVER (
 ORDER BY order_date, order_id
 ) AS running_sales
FROM training.v_lab_orders;
```

Compare several rows from both systems.

---

## 13. End-to-End Migration

Migrate the following SQL Server reporting query.

```sql
SELECT TOP 5
 c.customer_name,
 COUNT(*) AS order_count,
 SUM(o.quantity) AS total_quantity,
 SUM(o.sales_amount) AS total_sales
FROM orders o
INNER JOIN customers c
 ON o.customer_id = c.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_name
HAVING SUM(o.sales_amount) > 100000
ORDER BY SUM(o.sales_amount) DESC;
```

### Task

Create the ClickHouse version using:

* ClickHouse table names
* ClickHouse aggregate functions
* `LIMIT`
* Appropriate aliases
* ClickHouse-compatible syntax

A possible structure is:

```sql
SELECT
 c.customer_name,
 count() AS order_count,
 sum(o.quantity) AS total_quantity,
 sum(o.sales_amount) AS total_sales
FROM training.v_lab_orders AS o
INNER JOIN training.customers AS c
 ON o.customer_id = c.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_name
HAVING total_sales > 100000
ORDER BY total_sales DESC
LIMIT 5;
```

Validate the result against SQL Server.

---

## 14. Migration Validation

For the final validation, compare the source and migrated queries using a simple checklist.

| Check | SQL Server | ClickHouse | Notes |
| -------------- | ---------: | ---------: | ----- |
| Row count | | | Expect CH ≫ SQL Server |
| Total sales | | | Shape/logic, not equal totals |
| Total quantity | | | Same |
| Minimum date | | | May differ by dataset |
| Maximum date | | | May differ by dataset |
| NULL count | | | On matching dimension tables |

**Expected result:** SQL Server row counts are much smaller. That does **not** mean the migration failed. Confirm filters, joins, and expressions behave the same way.

For example (ClickHouse — full seed):

```sql
SELECT
 count() AS row_count,
 sum(sales_amount) AS total_sales,
 sum(quantity) AS total_quantity,
 min(order_date) AS min_date,
 max(order_date) AS max_date
FROM training.v_lab_orders;
```

Run a similar aggregate on SQL Server `dbo.orders` and record both sides. Discuss why the numbers differ.

The goal is not simply to make the query execute. Confirm that the migrated query preserves the intended reporting **logic**.

---

## 15. Migration Checklist

For each SQL Server query:

```text
[ ] Understand the business requirement
[ ] Identify SQL Server-specific syntax
[ ] Check data types
[ ] Map functions
[ ] Review NULL handling
[ ] Review date/time expressions
[ ] Review string expressions
[ ] Review joins
[ ] Review CTEs/subqueries
[ ] Review window functions
[ ] Execute the ClickHouse query
[ ] Compare results
[ ] Validate important KPIs
```

## Lab Completion

By the end of the lab, you should have migrated and validated multiple reporting queries covering common SQL Server patterns.

The final migrated queries should produce results that are consistent with the intended SQL Server business logic.
