# Session 8 — Grafana Fundamentals and ClickHouse Integration

## Lab Objective

In this lab, you will connect Grafana to the training ClickHouse database and build a basic manufacturing sales dashboard.

You will work with:

* Grafana interface
* ClickHouse data source
* ClickHouse SQL
* Explore
* Time ranges
* Panels
* Dashboard creation
* Dashboard refresh

---

## 1. Access Grafana

Open:

**https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/**

Sign in with the student credentials provided by the instructor:

* User: `student`
* Password: `StudentLab!2026`

Do not use infrastructure administrator credentials.

The **ClickHouse** data source is already provisioned. Prefer that data source for all panels in this lab.

> Instructor demo only: “Add data source” is optional for trainers. Students should **not** create a second ClickHouse data source.

> Tip: For queries that need `sales_amount`, `quantity`, and `region_id` together, use the lab view `training.v_lab_orders` (it joins orders + items + plants and maps `Closed` → `Completed`).

> Seed: order dates **2023-01-01** … **2025-06-18**. Completed orders exist for regions **1, 3, 5** only.

**Verify dashboard (optional reference):**  
https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/d/lab-s08-clickhouse-kpis/session-08-clickhouse-kpis-lab-verify  

Set the dashboard time range to absolute **2023-01-01** → **2025-06-18** if panels look empty.

---

## 2. Explore the Grafana Interface

Identify the following areas:

* Dashboards
* Explore
* Connections / Data Sources
* Search
* User/profile menu

Open the dashboard area and Explore once to understand the navigation.

---

## 3. Open Explore

Open **Explore**.

Select the ClickHouse data source configured for the training environment.

Run a simple query:

```sql
SELECT
    count() AS total_orders
FROM training.v_lab_orders;
```

Verify that a result is returned.

---

## 4. Inspect the Orders Data

Run:

```sql
SELECT
    *
FROM training.v_lab_orders
LIMIT 10;
```

Identify:

* `order_id`
* `order_date`
* `region_id`
* `plant_id`
* `customer_id`
* `product_id`
* `quantity`
* `sales_amount`
* `status`

---

## 5. Create a New Dashboard

Create a new dashboard and add a panel.

Select the ClickHouse data source.

Use the following query:

```sql
SELECT
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE status = 'Completed';
```

Run the query and verify the result.

---

## 6. Create the Total Sales KPI

Select a **Stat** visualization.

Configure the panel so that the completed sales amount is displayed as the main KPI.

Give the panel a meaningful title such as:

**Total Sales**

Save the panel.

---

## 7. Create the Total Orders KPI

Add another panel.

Use:

```sql
SELECT
    count() AS total_orders
FROM training.v_lab_orders
WHERE status = 'Completed';
```

Use a **Stat** visualization.

Set the title to:

**Total Orders**

---

## 8. Create a Regional Sales Panel

Add another panel.

Use:

```sql
SELECT
    region_id,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE status = 'Completed'
GROUP BY region_id
ORDER BY region_id;
```

Select a **Bar chart** or **Table** visualization.

Set the title to:

**Sales by Region**

Verify that **Completed** regions **1, 3, and 5** each have a corresponding sales value. Regions without Completed seed data (for example 2) may be missing or zero for Completed-only queries — that is expected.

---

## 9. Create a Daily Sales Panel

Add another panel.

Use:

```sql
SELECT
    order_date,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE status = 'Completed'
GROUP BY order_date
ORDER BY order_date;
```

Select a **Time series** visualization.

Set the title to:

**Daily Sales**

Verify that the horizontal axis represents the order date.

---

## 10. Work with the Dashboard Time Range

**Primary time range for this lab (required):** set an **absolute** range:

**From:** `2023-01-01`  
**To:** `2025-06-18`

Do **not** use “Last 30 days” as the main setting. Class dates in 2026 sit after the seed ends (2025-06-18), so relative ranges often return **empty panels**.

Optionally, after panels work, try a shorter absolute window (for example Q1 2023) to see how the time picker filters results.

---

## 11. Create a Time-Filtered Query

Modify the daily sales query to use an explicit reporting period:

```sql
SELECT
    order_date,
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date < '2023-04-01'
GROUP BY order_date
ORDER BY order_date;
```

Run the query and verify the returned dates.

---

## 12. Inspect the Query in Explore

Return to **Explore**.

Run the same query there.

Compare the result with the dashboard panel.

The purpose is to confirm that the query itself produces the expected data before troubleshooting the visualization.

---

## 13. Add a Detailed Orders Table

Create another panel.

Use:

```sql
SELECT
    order_id,
    order_date,
    region_id,
    plant_id,
    quantity,
    sales_amount,
    status
FROM training.v_lab_orders
ORDER BY order_date DESC
LIMIT 20;
```

Select the **Table** visualization.

Set the title to:

**Recent Orders**

---

## 14. Arrange the Dashboard

Arrange the panels into a simple reporting layout:

```text
+----------------+----------------+
| Total Sales    | Total Orders   |
+----------------+----------------+
| Sales by Region| Daily Sales    |
+----------------+----------------+
|         Recent Orders          |
+--------------------------------+
```

Keep related information together and avoid unnecessary panels.

---

## 15. Configure Dashboard Refresh

Open the dashboard refresh options.

Select a reasonable refresh interval, such as:

**5 minutes**

Observe the refresh behavior.

For a static training dataset, the refresh interval is mainly for understanding the feature.

---

## 16. Validate the Dashboard

Check each panel.

### Total Sales

* Query executes successfully
* Completed orders are included
* Value is numeric

### Total Orders

* Query executes successfully
* Completed orders are counted

### Sales by Region

* Region is displayed correctly
* Sales are aggregated correctly

### Daily Sales

* Date is displayed correctly
* Sales values are plotted correctly

### Recent Orders

* Expected columns are displayed
* Latest records appear first

---

## 17. Basic Troubleshooting Exercise

Intentionally introduce a problem into one panel.

For example, change:

```sql
training.v_lab_orders
```

to:

```sql
training.order
```

Run the query and observe the error.

Restore the correct table name.

Next, remove the date range from the time-series query and inspect the result.

Discuss with the instructor why query validation is important before changing visualization settings.

---

## 18. Final Dashboard Challenge

Build a basic **Manufacturing Sales Dashboard** containing:

1. Total Sales
2. Total Orders
3. Sales by Region
4. Daily Sales
5. Recent Orders

**Requirements**

* Use ClickHouse as the data source.
* Use ClickHouse SQL for every panel.
* Use at least one Stat panel.
* Use at least one Table panel.
* Use at least one Time series panel.
* Use at least one Bar chart panel.
* Use an absolute dashboard time range: **2023-01-01** → **2025-06-18**.
* Configure dashboard refresh.
* Validate every panel before saving.
* Optional check against: `/grafana/d/lab-s08-clickhouse-kpis/session-08-clickhouse-kpis-lab-verify`

### Expected Dashboard Flow

```text
ClickHouse
    |
    v
Grafana ClickHouse Data Source
    |
    v
ClickHouse SQL
    |
    +----> Total Sales
    |
    +----> Total Orders
    |
    +----> Sales by Region
    |
    +----> Daily Sales
    |
    +----> Recent Orders
    |
    v
Manufacturing Sales Dashboard
```

## Completion Checklist

```text
[ ] Accessed Grafana (student / StudentLab!2026)
[ ] Explored Grafana interface
[ ] Used Explore with provisioned ClickHouse DS
[ ] Set absolute time range 2023-01-01 → 2025-06-18
[ ] Executed ClickHouse SQL on v_lab_orders
[ ] Created KPI panels
[ ] Created regional sales panel (Completed regions 1/3/5)
[ ] Created time-series panel
[ ] Created table panel
[ ] Configured refresh
[ ] Validated all panels
[ ] (Optional) Opened lab-s08-clickhouse-kpis verify dashboard
[ ] Completed the manufacturing sales dashboard
```
