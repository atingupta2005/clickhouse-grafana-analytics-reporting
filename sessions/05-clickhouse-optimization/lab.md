# Lab — ClickHouse Query Optimization

## Lab Objective

In this lab, you will investigate query performance, identify bottlenecks, apply practical improvements, and compare the results before and after optimization.

Use the existing `training` database and the manufacturing sales dataset (`training.v_lab_orders`).

**Live sort key** (you will confirm with `SHOW CREATE`):

```text
ORDER BY (order_date, plant_id, order_id)
```

**Region tip:** Prefer `region_id = 3` for demos. Region 2 has non-Completed data; for Completed use 1 / 3 / 5. Always add `LIMIT` on `SELECT *` detail queries.

---

## 1. Establish a Baseline

Start with a regional sales query:

```sql
SELECT
    region_id,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
GROUP BY region_id
ORDER BY region_id;
```

Record:

```text
Execution time:
Rows read:
Bytes read:
Memory usage:
```

The exact values will depend on the size of the training dataset and the environment.

---

## 2. Compare Required Columns vs SELECT *

Run:

```sql
SELECT *
FROM training.v_lab_orders
WHERE region_id = 3
LIMIT 100;
```

Now run:

```sql
SELECT
    order_id,
    order_date,
    region_id,
    sales_amount
FROM training.v_lab_orders
WHERE region_id = 3
LIMIT 100;
```

### Tasks

Compare the two queries.

Record:

* Execution time
* Rows read
* Bytes read
* Memory usage

Discuss why selecting only required columns can reduce unnecessary data processing.

**Tip:** Region 2 is fine for any-status checks; for Completed use region 1 / 3 / 5.

---

## 3. Investigate Filtering

Run a query without a date restriction:

```sql
SELECT
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE region_id = 3;
```

Now restrict the reporting period:

```sql
SELECT
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE region_id = 3
  AND order_date >= '2023-01-01'
  AND order_date < '2023-04-01';
```

### Tasks

Compare the query statistics.

Identify:

* Rows read
* Bytes read
* Execution time

Explain why restricting the required reporting period can reduce work. Because `order_date` leads the sorting key, date filters are especially useful on this table.

---

## 4. Review the Sorting Key

Inspect the table definition:

```sql
SHOW CREATE TABLE training.orders;
```

**Expected result:** you should see something like:

```text
PARTITION BY toYYYYMM(order_date)
ORDER BY (order_date, plant_id, order_id)
```

Now run a query aligned with the sort key:

```sql
SELECT
    sum(sales_amount)
FROM training.v_lab_orders
WHERE order_date >= '2023-01-01'
  AND order_date < '2023-04-01'
  AND plant_id = 1;
```

Also try a region + date filter (region is useful for reporting, but is **not** a leading sort-key column):

```sql
SELECT
    sum(sales_amount)
FROM training.v_lab_orders
WHERE region_id = 3
  AND order_date >= '2023-01-01'
  AND order_date < '2023-04-01';
```

### Tasks

Explain:

1. Which columns are in the sorting key? (`order_date`, `plant_id`, `order_id`)
2. Why does the sorting key begin with `order_date`?
3. How does `plant_id` in the sorting key support plant-level reporting?
4. Why is a `region_id`-only filter less aligned with this key than a date/plant filter?

---

## 5. Review Partitioning

Inspect the table parts:

```sql
SELECT
    partition,
    count() AS parts,
    sum(rows) AS rows
FROM system.parts
WHERE database = 'training'
  AND table = 'orders'
  AND active
GROUP BY partition
ORDER BY partition;
```

Run a query restricted to one month:

```sql
SELECT
    count() AS order_count,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE order_date >= '2023-02-01'
  AND order_date < '2023-03-01';
```

### Task

Identify which partition or partitions are relevant to the query.

Explain the difference between:

* Partitioning
* Sorting key

---

## 6. Use EXPLAIN

Run:

```sql
EXPLAIN
SELECT
    region_id,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE region_id = 3
GROUP BY region_id;
```

### Tasks

Review the plan and identify the major stages involved in executing the query.

Then try:

```sql
EXPLAIN indexes = 1
SELECT
    region_id,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE region_id = 3
  AND order_date >= '2023-01-01'
  AND order_date < '2023-04-01'
GROUP BY region_id;
```

Discuss what information the index-related output provides about data selection.

**Note:** Region 2 has non-Completed data; for Completed use 1 / 3 / 5. Prefer region **3** in EXPLAIN demos here.

---

## 7. Inspect Query History

Run a few analytical queries from the previous exercises.

Then inspect completed queries:

```sql
SELECT
    event_time,
    query_duration_ms,
    read_rows,
    read_bytes,
    result_rows,
    memory_usage,
    query
FROM system.query_log
WHERE type = 'QueryFinish'
ORDER BY event_time DESC
LIMIT 10;
```

### Task

Identify:

* The slowest query
* The query reading the most rows
* The query reading the most bytes
* The query using the most memory

Do not assume that the slowest query is necessarily the one reading the most data.

---

## 8. Optimize an Unnecessary SELECT *

Start with:

```sql
SELECT *
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date < '2023-04-01'
LIMIT 100;
```

Assume the report only needs:

* `order_id`
* `order_date`
* `region_id`
* `sales_amount`

Rewrite the query:

```sql
SELECT
    order_id,
    order_date,
    region_id,
    sales_amount
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date < '2023-04-01'
LIMIT 100;
```

### Task

Compare the two versions and document the difference in data read.

---

## 9. Optimize a JOIN Query

Run:

```sql
SELECT
    c.customer_name,
    sum(o.sales_amount) AS total_sales
FROM training.v_lab_orders AS o
INNER JOIN training.customers AS c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_sales DESC;
```

Now apply a business filter:

```sql
SELECT
    c.customer_name,
    sum(o.sales_amount) AS total_sales
FROM training.v_lab_orders AS o
INNER JOIN training.customers AS c
    ON o.customer_id = c.customer_id
WHERE o.status = 'Completed'
  AND o.order_date >= '2023-01-01'
  AND o.order_date < '2023-04-01'
GROUP BY c.customer_name
ORDER BY total_sales DESC;
```

### Tasks

Compare both queries.

Determine whether the second query processes less data.

Confirm that the filter is part of the intended reporting requirement before treating it as an optimization.

---

## 10. Review Aggregation

Run:

```sql
SELECT
    region_id,
    plant_id,
    customer_id,
    product_id,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
GROUP BY
    region_id,
    plant_id,
    customer_id,
    product_id;
```

This may produce a large number of groups when using the full training dataset.

Now run:

```sql
SELECT
    region_id,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
GROUP BY region_id;
```

### Tasks

Compare:

* Number of result groups
* Rows read
* Execution time
* Memory usage

Explain why grouping by more dimensions can require more intermediate state.

---

## 11. Query Rewrite Exercise

Start with:

```sql
SELECT
    *
FROM training.v_lab_orders
WHERE order_date >= '2023-01-01'
  AND order_date < '2023-04-01'
  AND status = 'Completed'
LIMIT 100;
```

Rewrite it for a management report that only needs:

* Region
* Order date
* Sales amount

Your query should avoid reading unnecessary columns.

Then compare the result with the original query.

---

## 12. Table Design Review

Inspect:

```sql
SHOW CREATE TABLE training.orders;
```

Answer:

1. What is the engine?
2. What is the partitioning expression?
3. What is the sorting key? (**Expected:** `(order_date, plant_id, order_id)`)
4. Why does the sorting key begin with `order_date`?
5. How does `plant_id` in the sorting key support reporting?
6. Which reporting queries benefit from this design? Which may not (for example, filter only by `customer_id` or only by `region_id`)?

Now consider this query:

```sql
SELECT
    customer_id,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE customer_id = 10002
GROUP BY customer_id;
```

Discuss whether the current sorting key is directly aligned with this filter.

Do not change the table yet.

---

## 13. Before-and-After Optimization

Select one query from this lab that can be improved without changing its business result.

Record the baseline:

```text
Query:
________________________________

Execution time:
________________________________

Rows read:
________________________________

Bytes read:
________________________________

Memory usage:
________________________________
```

Apply one change.

Examples:

* Remove unnecessary columns
* Add a required reporting filter
* Rewrite the query
* Review the join input
* Reduce unnecessary grouping dimensions

Run the query again.

Record:

```text
Change made:
________________________________

Execution time:
________________________________

Rows read:
________________________________

Bytes read:
________________________________

Memory usage:
________________________________
```

---

## 14. Validate Correctness

For the optimized query, compare the result with the original query.

Check:

```sql
SELECT
    count() AS row_count,
    sum(sales_amount) AS total_sales,
    sum(quantity) AS total_quantity,
    min(order_date) AS min_date,
    max(order_date) AS max_date
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date < '2023-04-01';
```

The optimized query must preserve the required business result.

---

## 15. Final Optimization Challenge

Consider this reporting query:

```sql
SELECT
    *
FROM training.v_lab_orders
WHERE order_date >= '2023-01-01'
  AND order_date < '2023-04-01';
```

The reporting requirement is:

> Show total completed sales by region for the first quarter of 2023.

### Tasks

1. Identify unnecessary columns.
2. Add the required business filter.
3. Aggregate only at the required level.
4. Run the original and rewritten queries.
5. Compare query statistics.
6. Validate the total sales.
7. Explain why the rewritten query is more appropriate for the report.

Create your final query.

---

## Lab Completion Checklist

```text
[ ] Established a performance baseline
[ ] Compared SELECT * with required columns
[ ] Reviewed filtering
[ ] Inspected partitioning
[ ] Reviewed sorting key
[ ] Used EXPLAIN
[ ] Inspected system.query_log
[ ] Investigated a JOIN
[ ] Investigated aggregation
[ ] Rewrote a query
[ ] Compared before and after measurements
[ ] Validated result correctness
[ ] Completed final optimization challenge
```
