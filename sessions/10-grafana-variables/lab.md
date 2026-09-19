# Session 10 — Grafana Variables Lab

## Lab Objective

Build an interactive dashboard **Session 10 - Variables Lab** with Grafana variables and 2–3 panels that respond to Region, Plant, Status, and time.

**Core vs Stretch:** Core steps are marked. Stretch items are optional / homework.

---

## 0. Access Grafana (Core)

Open:

**https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/**

Sign in:

* User: `student`
* Password: `StudentLab!2026`

Use provisioned data sources only:

* **ClickHouse** (uid `clickhouse`)
* **Infinity** (uid `infinity`) — Stretch panels

Do **not** create new data sources.

---

## 1. Create the Dashboard (Core)

1. **Dashboards** → **New** → **New dashboard**.
2. Open **Dashboard settings** (gear).
3. Name: **Session 10 - Variables Lab**.
4. Save (folder: Training if available).

Set time range to **absolute**:

* From: **2023-01-01**
* To: **2025-06-18**

> Do not leave **Last 30 days**. Seed data ends mid-2025; relative “last month” in 2026 is empty.

> **Tip:** Confirm the time picker shows absolute dates before you build SQL panels.

---

## 2. Variable — Region (Query) (Core)

**Dashboard settings → Variables → Add variable**

| Field | Value |
| ----- | ----- |
| Name | `region` |
| Label | Region |
| Type | Query |
| Data source | ClickHouse |
| Multi-value | **On** |
| Include All option | **On** |

Query:

```sql
SELECT
    region_id,
    region_name
FROM training.regions
ORDER BY region_id
```

Set display so the dropdown shows **region_name** and the value is **region_id** (variable UI: Value / Text fields, or equivalent for this Grafana version).

**Default:** select region **3** (or All / 1+3+5). Prefer a Completed region for first demo.

**Expected result:** Dropdown lists North America, Europe, Asia Pacific, … (ids 1–6).

Save the dashboard.

---

## 3. Variable — Status (Custom) (Core)

| Field | Value |
| ----- | ----- |
| Name | `status` |
| Label | Status |
| Type | Custom |
| Values | `Open,Shipped,Completed,Cancelled` |
| Multi-value | On |
| Include All | optional |
| Default | **Completed** |

**Expected result:** Status defaults to Completed on dashboard load.

---

## 4. Variable — Plant (Cascading Query) (Core)

| Field | Value |
| ----- | ----- |
| Name | `plant` |
| Label | Plant |
| Type | Query |
| Data source | ClickHouse |
| Multi-value | On |
| Include All | On |

Query:

```sql
SELECT
    plant_id,
    plant_name
FROM training.plants
WHERE region_id IN (${region})
ORDER BY plant_id
```

1. Save.
2. On the dashboard, change **Region** (e.g. 3 only, then 1 only).
3. Confirm the **Plant** list changes.

> **Tip:** If Plant stays empty, Region has no selection, or the plant query is missing `WHERE region_id IN (${region})`.

**Expected result:** Plant options follow the selected region(s). Seed has 40 plants across 6 regions.

---

## 5. Optional Variables — Category, Product, Customer (Stretch)

Add if time allows. Keep Core panels working without them first.

**Category:**

```sql
SELECT category_id, category_name
FROM training.categories
ORDER BY category_id
```

**Product (cascade from category):**

```sql
SELECT product_id, product_name
FROM training.products
WHERE category_id IN (${category})
ORDER BY product_id
LIMIT 500
```

**Customer (limited list):**

```sql
SELECT customer_id, customer_name
FROM training.customers
WHERE region_id IN (${region})
ORDER BY customer_id
LIMIT 200
```

---

## 6. Panel 1 — Stat KPI (Core)

Add visualization → **Stat** → data source **ClickHouse**.

```sql
SELECT
    sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE region_id IN (${region})
  AND plant_id IN (${plant})
  AND status IN (${status:sqlstring})
```

Title: **Filtered Sales**.

1. Select Region **3**, Status **Completed**, All plants for that region (or All).
2. Run query.

**Expected result:** Non-zero sales for region 3 + Completed.

3. Switch Region to **2**, keep Status **Completed**.

**Expected result:** **Empty / zero** — Completed seed exists only for regions **1, 3, 5**.

> Explain empty Completed + region 2 so students do not “fix” working filters.

---

## 7. Panel 2 — Table (Core)

Add **Table** panel → ClickHouse.

```sql
SELECT
    order_date,
    region_id,
    plant_id,
    order_id,
    product_id,
    customer_id,
    quantity,
    sales_amount,
    status
FROM training.v_lab_orders
WHERE region_id IN (${region})
  AND plant_id IN (${plant})
  AND status IN (${status:sqlstring})
ORDER BY order_date DESC
LIMIT 100
```

Title: **Filtered Orders**.

**Expected result:** Up to 100 rows; columns match the SELECT; changing Region/Plant/Status refreshes the table.

---

## 8. Panel 3 — Time Series (Core optional / Stretch if slow)

Add **Time series** → ClickHouse.

```sql
SELECT
    order_date AS time,
    sum(sales_amount) AS sales
FROM training.v_lab_orders
WHERE region_id IN (${region})
  AND status IN (${status:sqlstring})
GROUP BY order_date
ORDER BY time
```

Map `time` as the time field. Keep absolute dashboard range **2023-01-01 → 2025-06-18**.

**Expected result:** A trend across the seed window for Completed regions; empty for region 2 + Completed.

---

## 9. Formatting Check (Core)

With multi-value Region **1** and **3**, Status **Completed**:

Confirm the Stat / Table still work with:

```sql
WHERE region_id IN (${region})
  AND status IN (${status:sqlstring})
```

If Status errors, verify the `:sqlstring` (or equivalent quoted) format — bare `${status}` is wrong for strings in `IN`.

---

## 10. Infinity REST Panel with Variables (Stretch)

Add panel → **Infinity**.

| Setting | Value |
| ------- | ----- |
| Parser | JSON |
| Root selector | **`data`** |
| Method | GET |

URL (single-value Region/Status recommended for REST):

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/api/sales?region_id=${region}&status=${status}&page=1&page_size=50&date_from=${__from:date:YYYY-MM-DD}&date_to=${__to:date:YYYY-MM-DD}
```

Reminders:

* REST pagination is **`page` / `page_size`** — not `top`/`skip`
* Multi-value `region_id=${region}` is awkward; turn Multi off for this panel or pick one region

**Expected result:** Rows under `data` when region ∈ {1,3,5} and status Completed.

---

## 11. Infinity OData Panel with Variables (Stretch)

Infinity → root selector **`value`**.

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$filter=Status eq '${status}' and RegionId eq ${region}&$top=20
```

**Unsupported on lab API:** `$expand` — do not require it. Mention only as “not available here / Session 11 topic.”

**Expected result:** Up to 20 orders in the `value` array for Completed + region 3.

---

## 12. Defaults and Save (Core)

1. Set Status default = **Completed**.
2. Set Region default to **3** (or 1+3+5).
3. Reload the dashboard — variables and panels should show Completed data without re-picking.
4. Save **Session 10 - Variables Lab**.

---

## 13. Validate

```text
[ ] Grafana login (student / StudentLab!2026)
[ ] Absolute time 2023-01-01 → 2025-06-18
[ ] Variable region (query from training.regions)
[ ] Variable status (custom, default Completed)
[ ] Variable plant (cascade WHERE region_id IN (${region}))
[ ] Multi-value + All used on region/plant
[ ] Stat panel uses IN (${region}) and IN (${status:sqlstring})
[ ] Table panel filters with same variables
[ ] Region 2 + Completed understood as empty seed
[ ] Dashboard saved as Session 10 - Variables Lab
[ ] (Stretch) Category / Product / Customer variables
[ ] (Stretch) Infinity REST root data + page/page_size
[ ] (Stretch) Infinity OData root value; no $expand
```

## Completion Checklist

```text
[ ] Dashboard created and named
[ ] Query + custom + cascading variables work
[ ] ClickHouse panels update when filters change
[ ] Formatting for multi-value strings verified
[ ] Empty Completed+Region2 demonstrated
[ ] Dashboard saved with sensible defaults
```
