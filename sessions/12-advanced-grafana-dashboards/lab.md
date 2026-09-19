# Session 12 — Advanced Grafana Dashboard Lab

## Lab Goal

Build and enhance:

**`Session 12 - Advanced Dashboard Lab`**

The dashboard combines KPI cards, a trend chart, regional comparison, a detail table, formatting, a transformation, and dashboard navigation.

Use the existing **ClickHouse** datasource. Prefer copying variables from **Session 10 - Variables Lab** (Session 11 is OData-focused).

### Lab data

- View: `training.v_lab_orders`
- Status: `Completed`
- Completed regions: `1`, `3`, `5`
- Time range: `2023-01-01` → `2025-06-18`
- ClickHouse datasource UID: `clickhouse`

### Grafana login

- Username: `student`
- Password: `StudentLab!2026`

---

# Core Lab

## 1. Open Grafana and Set the Time Range

1. Open:

 `https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/`

2. Log in with:

 ```text
 Username: student
 Password: StudentLab!2026
 ```

3. Prefer copying **Session 10 - Variables Lab** (it already has `region` / `status`). If that dashboard is missing, create a new dashboard and add the same variables as Session 10 (region query from `training.regions`, status custom default **Completed**).

 Session 11 is OData-focused — do not rely on it as the only source of ClickHouse variables.

4. Set the dashboard time range to:

 ```text
 2023-01-01 00:00:00
 →
 2025-06-18 23:59:59
 ```

5. Save a working copy as:

 **`Session 12 - Advanced Dashboard Lab`**

### Expected result

The dashboard opens with the existing variables available and the time range covering the complete training dataset.

### Tip

Do not use **Last 30 days**. The seed data ends in June 2025.

---

## 2. Organize the Dashboard

Arrange the dashboard into these logical sections:

| Section | Panels |
|---|---|
| Summary | Completed Orders, Total Sales |
| Trends | Monthly Sales |
| Regional Analysis | Sales by Region |
| Details | Recent/filtered completed orders |
| Navigation | Drill-down/dashboard link |

Keep KPI panels at the top and detail information lower on the dashboard.

### Expected result

The dashboard can be read from summary → trend → comparison → detail.

---

## 3. Add a Completed Orders Stat Panel

Create a new **Stat** panel.

Use the existing ClickHouse datasource.

Query:

```sql
SELECT
 uniqExact(order_id) AS completed_orders
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
 AND order_date >= '2023-01-01'
 AND order_date < '2025-06-19'
 AND region_id IN (${region})
```

Configure:

- Visualization: **Stat**
- Unit: `none`
- Decimals: `0`
- Display name: `Completed Orders`

### Expected result

The Stat panel displays the number of completed orders for the selected region and status values.

### Tip

If the status variable is configured for `Completed`, keep it selected. If multiple status values are available, the query uses the existing multi-value variable syntax.

---

## 4. Add a Total Sales Stat Panel

Create another **Stat** panel.

Use:

```sql
SELECT
 sum(sales_amount) AS total_sales
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
 AND order_date >= '2023-01-01'
 AND order_date < '2025-06-19'
 AND region_id IN (${region})
```

Configure:

- Visualization: **Stat**
- Unit: appropriate currency/number format
- Decimals: `0`
- Display name: `Total Sales`

### Expected result

The panel displays total sales for the selected region, status, and dashboard time range.

### Tip

The dashboard time range is fixed for this lab, but the query also demonstrates explicit seed-date filtering. 

---

## 5. Add a Monthly Sales Time Series

Create a new panel using the ClickHouse datasource.

Use:

```sql
SELECT
 toStartOfMonth(order_date) AS month,
 sum(sales_amount) AS sales
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
 AND order_date >= '2023-01-01'
 AND order_date < '2025-06-19'
 AND region_id IN (${region})
GROUP BY month
ORDER BY month
```

Configure:

- Visualization: **Time series**
- Time field: `month`
- Value: `sales`
- Unit: appropriate number/currency format
- Legend: visible

Panel title:

**Monthly Sales Trend**

### Expected result

A monthly sales trend appears across the training data period.

Changing the existing region variable changes the displayed trend.

### Tip

Do not return order-level rows for a time-series panel. Aggregate at the required reporting grain first.

---

## 6. Add Sales by Region

Create a **Bar chart** panel.

Use:

```sql
SELECT
 region_id,
 sum(sales_amount) AS sales
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
 AND order_date >= '2023-01-01'
 AND order_date < '2025-06-19'
 AND region_id IN (${region})
GROUP BY region_id
ORDER BY sales DESC
```

Configure:

- Visualization: **Bar chart**
- Category: `region_id`
- Value: `sales`
- Legend: visible if useful
- Unit: appropriate number/currency format

Panel title:

**Sales by Region**

### Expected result

The chart displays sales totals for the selected regions.

### Tip

With the normal Completed seed, regions `1`, `3`, and `5` contain data. Region `2` with Completed is intentionally empty.

---

## 7. Configure Thresholds

Open the **Completed Orders** Stat panel.

Configure a threshold appropriate for demonstrating dashboard formatting.

Use the threshold as a visual demonstration rather than a business target because no business target is defined in the training seed.

Configure the panel so that different value ranges are visually distinguishable.

### Expected result

The Stat panel changes its visual state according to the configured thresholds.

### Tip

Note: thresholds affect presentation. They do not modify the ClickHouse result.

---

## 8. Format the Sales Field

Open the **Total Sales** Stat panel.

Configure the field so that:

- The value is displayed as a readable number.
- Unnecessary decimal places are removed.
- The unit clearly communicates that the value represents sales.

Repeat appropriate formatting for the `sales` field in the regional bar chart.

### Expected result

Sales values are easier to read and compare.

### Tip

Use Grafana field configuration for presentation. Do not convert numeric database values to formatted strings in SQL when Grafana still needs the numeric value.

---

## 9. Add a Detail Table

Create a **Table** panel using ClickHouse.

Use:

```sql
SELECT
 order_id,
 order_date,
 region_id,
 status,
 sales_amount
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
 AND order_date >= '2023-01-01'
 AND order_date < '2025-06-19'
 AND region_id IN (${region})
ORDER BY order_date DESC
LIMIT 100
```

Panel title:

**Completed Order Details**

Organize the fields in this order:

```text
Order ID
Order Date
Region
Status
Sales Amount
```

### Expected result

The table displays no more than 100 matching rows and responds to the existing region/status selections.

### Tip

The `LIMIT 100` is intentional. Do not remove it from the Core dashboard.

---

## 10. Apply a Transformation

Open the **Completed Order Details** panel.

Use a field-organization transformation to:

- Keep the five reporting fields.
- Arrange them in the required order.
- Rename technical field labels where useful.

For example:

```text
order_id → Order ID
order_date → Order Date
region_id → Region
sales_amount → Sales Amount
```

Keep `status` available when it helps explain the selected filter.

### Expected result

The table is easier for a reporting user to read without changing the underlying ClickHouse query.

### Tip

This is a presentation transformation. Do not use it as a replacement for database filtering.

---

## 11. Add a Calculated Value

Create or use a panel where both sales and quantity are available.

Use this ClickHouse query:

```sql
SELECT
 region_id,
 sum(sales_amount) AS sales,
 sum(quantity) AS quantity
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
 AND order_date >= '2023-01-01'
 AND order_date < '2025-06-19'
 AND region_id IN (${region})
GROUP BY region_id
ORDER BY region_id
```

Use a Grafana transformation to calculate:

```text
Average Value = Sales / Quantity
```

Display the calculated value with a suitable number format.

### Expected result

The panel contains the original sales and quantity values plus a calculated average value.

### Tip

The calculation should remain numeric. Avoid converting sales or quantity into display strings before the calculation.

---

## 12. Add Dashboard Navigation

Create a second dashboard for drill-down:

**`Session 12 - Regional Detail`**

The dashboard should contain a table using the existing variables and the same training view.

Use this query:

```sql
SELECT
 order_id,
 order_date,
 region_id,
 status,
 sales_amount
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
 AND order_date >= '2023-01-01'
 AND order_date < '2025-06-19'
 AND region_id IN (${region})
ORDER BY order_date DESC
LIMIT 100
```

### Expected result

The second dashboard provides a detail view using the same training data.

---

## 13. Add a Link from the Main Dashboard

Return to:

**`Session 12 - Advanced Dashboard Lab`**

Add a dashboard link from the regional analysis area to:

**`Session 12 - Regional Detail`**

Configure the link so that the current region and status variable selections are passed to the destination dashboard.

The navigation should follow:

```text
Session 12 - Advanced Dashboard Lab
 ↓
 Regional Detail
```

### Expected result

Selecting a region/status context and opening the dashboard link takes the user to the regional detail dashboard with the relevant variable context.

### Tip

Use Grafana dashboard navigation rather than inventing an external URL.

---

## 14. Test the Interactive Filters

Test the dashboard with the existing region variable.

Verify:

1. Select region `1`.
2. Confirm the Stat panels change.
3. Confirm the time-series panel changes.
4. Confirm the regional chart changes.
5. Confirm the detail table changes.
6. Select region `3`.
7. Repeat the checks.
8. Select regions `1` and `3` together if the existing variable supports multi-selection.

### Expected result

All Core panels respond consistently to the same dashboard filters.

### Tip

If a panel does not change, first check whether its query actually references the variable.

---

## 15. Test an Empty Result

Select:

```text
Region = 2
Status = Completed
```

If region `2` is missing from the dropdown, add it (Session 10’s query variable from `training.regions` already includes it).

### Expected result

The affected panels can show no data because Region `2` has no Completed rows in the training seed.

### Tip

This is an intentional seed condition. Do not change the query simply to manufacture a result.

---

## 16. Review Query Performance

Review each Core query.

Check that:

- The query selects only required columns.
- `status` is filtered.
- `order_date` is bounded.
- `region_id` is filtered where appropriate.
- Aggregation is performed before charting.
- Detail queries have `LIMIT`.
- No query uses `SELECT *`.

### Expected result

The dashboard uses focused queries rather than repeatedly requesting the complete reporting view.

---

# Core Lab Checklist

Before finishing, verify:

- [ ] Dashboard is named `Session 12 - Advanced Dashboard Lab`
- [ ] Absolute time range is `2023-01-01` → `2025-06-18`
- [ ] Existing `region` variable is reused
- [ ] Existing `status` variable is reused
- [ ] Completed Orders Stat panel works
- [ ] Total Sales Stat panel works
- [ ] Monthly Sales Time Series works
- [ ] Sales by Region Bar chart works
- [ ] Detail Table works
- [ ] Thresholds are configured
- [ ] Sales fields are formatted
- [ ] Table fields are organized
- [ ] A calculated value is demonstrated
- [ ] Dashboard navigation works
- [ ] Detail query uses `LIMIT 100`
- [ ] No unsupported plugin is required

---

# Stretch

## 17. Add an Annotation

If time permits, demonstrate Grafana annotations using an available Grafana-supported annotation mechanism.

Skip or observe if your account cannot create or save the required annotation configuration.

### Expected result

You should understand how event markers can be displayed against a time-series visualization.

### Tip


---

## 18. Add an Infinity Panel

Use the **Infinity** datasource. 

Example OData table (root selector **`value`**):

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$filter=RegionId%20eq%203%20and%20Status%20eq%20%27Completed%27&$select=OrderId,RegionId,Status,SalesAmount,OrderDate&$top=20
```

For OData multi-region filters, use OData syntax — **not** ClickHouse `IN (${region})`:

```text
RegionId eq 1 or RegionId eq 3
```

For REST, use root selector **`data`** and `page` / `page_size` (Session 09).

### Expected result

You see how an Infinity panel can complement ClickHouse-based panels.

### Tip

Keep this as Stretch. Do not make the dashboard dependent on the Infinity panel for Core completion.

---

## 19. Add an Additional Drill-Down

Add another navigation path from the main dashboard to the regional detail dashboard.

Pass the relevant dashboard variables through the link.

### Expected result

Users can move from a summary visualization to a filtered detail view without manually re-entering the filter context.
