# Session 13 — End-to-End Reporting Dashboard Workshop

## Core Lab — Build the Reporting Dashboard

### Dashboard

Create:

```text
Session 13 - Reporting Workshop
```

### Core outcome

Build a compact interactive dashboard containing:

- Completed Orders
- Completed Revenue
- High-Value Lines
- Revenue by Region
- Revenue by Plant
- Region filter
- Plant filter
- Status filter
- Absolute time range

Use the provisioned **ClickHouse** datasource.

---

## 1. Open Grafana

Open:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/
```

Sign in with:

```text
Username: student
Password: StudentLab!2026
```

Open **Dashboards** and create a new dashboard.

Save it as:

```text
Session 13 - Reporting Workshop
```

### Expected Result

A new empty dashboard is available for building the workshop report.

### Trainer Tip

Students should use the existing **ClickHouse** datasource. Do not create another ClickHouse datasource.

---

## 2. Set the Dashboard Time Range

Set the dashboard time picker to:

```text
From: 2023-01-01
To:   2025-06-18
```

Use the absolute time range for the Core dashboard.

### Expected Result

The dashboard is working against the complete available seed period.

### Trainer Tip

Do not use **Last 30 days**. The seed ends on `2025-06-18`, so a current relative range can produce empty results.

---

## 3. Create the Region Variable

Open:

**Dashboard settings → Variables → Add variable**

Configure:

```text
Name: region
Label: Region
Type: Query
```

Select the existing **ClickHouse** datasource.

Use:

```sql
SELECT DISTINCT region_id
FROM training.v_lab_orders
ORDER BY region_id
```

Enable:

```text
Multi-value
Include All option
```

Set the default selection to:

```text
All
```

### Expected Result

The Region variable contains the available region IDs.

The Completed lab data includes regions:

```text
1
3
5
```

Region `2` may be available as a selectable region and is useful for validation.

### Trainer Tip

Do not assume Region 2 should show Completed data. The seed intentionally has no Completed data for Region 2.

---

## 4. Create the Plant Variable

Create another variable:

```text
Name: plant
Label: Plant
Type: Query
```

Use the **ClickHouse** datasource.

Query (cascade plants to selected regions — Session 10 pattern):

```sql
SELECT DISTINCT plant_id
FROM training.v_lab_orders
WHERE region_id IN (${region})
ORDER BY plant_id
```

Enable:

```text
Multi-value
Include All option
```

Set the default selection to:

```text
All
```

### Expected Result

The Plant variable lists plant IDs for the selected region(s). Changing Region refreshes Plant.

### Trainer Tip

Use the values returned by the lab data. Do not manually invent plant names. If Plant is empty, check that Region has a selection (or All).

---

## 5. Create the Status Variable

Create:

```text
Name: status
Label: Status
Type: Custom
```

Set the value to:

```text
Completed
```

Set the default value to:

```text
Completed
```

### Expected Result

The dashboard displays a Status filter with `Completed` selected.

### Trainer Tip

The workshop reporting status is `Completed`. Do not substitute the stored source status.

---

## 6. Add the Completed Orders KPI

Add a new panel.

Select the **ClickHouse** datasource.

Use:

```sql
SELECT
    uniqExact(order_id) AS completed_orders
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
  AND region_id IN (${region})
  AND plant_id IN (${plant})
```

Set the visualization to a **Stat** panel.

Panel title:

```text
Completed Orders
```

### Expected Result

The Stat panel displays approximately:

```text
125000
```

with the default full-seed filters.

### Trainer Tip

The expected value is approximate because the seed validation target is approximately 125,000 distinct Completed orders.

Do not use `count()` for this KPI. The reporting view contains line-level rows, so one order can appear more than once.

---

## 7. Add the Completed Revenue KPI

Add another panel using the **ClickHouse** datasource.

Query:

```sql
SELECT
    sum(sales_amount) AS completed_revenue
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
  AND region_id IN (${region})
  AND plant_id IN (${plant})
```

Visualization:

```text
Stat
```

Panel title:

```text
Completed Revenue
```

### Expected Result

The panel displays the Completed revenue for the selected filters and dashboard time range.

### Trainer Tip

Do not hard-code a revenue value into the dashboard. The value must respond to the Region, Plant, Status, and dashboard time filters.

---

## 8. Add the High-Value Lines KPI

Add another **Stat** panel.

Use:

```sql
SELECT
    countIf(sales_amount >= 2000) AS high_value_lines
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
  AND region_id IN (${region})
  AND plant_id IN (${plant})
```

Panel title:

```text
High-Value Lines
```

### Expected Result

The panel displays the number of reporting lines where:

```text
sales_amount >= 2000
```

The value changes when dashboard filters change.

### Trainer Tip

This is a **line-level** metric. Do not describe it as the number of high-value orders.

---

## 9. Add Revenue by Region

Add a new panel.

Use the **ClickHouse** datasource.

Query:

```sql
SELECT
    region_id,
    sum(sales_amount) AS revenue
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
  AND region_id IN (${region})
  AND plant_id IN (${plant})
GROUP BY region_id
ORDER BY region_id
```

Use a suitable categorical visualization such as a **Bar chart**.

Panel title:

```text
Revenue by Region
```

### Expected Result

The panel displays revenue grouped by Region.

With the default Completed selection, the meaningful Completed regions are:

```text
1
3
5
```

### Trainer Tip

If the Region filter is set to Region 2 with Status `Completed`, the panel should contain no Completed data.

That is an expected seed result, not necessarily a dashboard error.

---

## 10. Add Revenue by Plant

Add one final Core analytical panel.

Use:

```sql
SELECT
    plant_id,
    sum(sales_amount) AS revenue
FROM training.v_lab_orders
WHERE status IN (${status:sqlstring})
  AND region_id IN (${region})
  AND plant_id IN (${plant})
GROUP BY plant_id
ORDER BY plant_id
```

Use a **Bar chart** or another suitable categorical visualization.

Panel title:

```text
Revenue by Plant
```

### Expected Result

The panel displays revenue grouped by plant and responds to the dashboard filters.

### Trainer Tip

Do not manually type plant names. The reporting view supplies the plant identifiers.

---

## 11. Check Variable Filtering

Return to the dashboard and test the filters.

### Test 1 — Default

Use:

```text
Status: Completed
Region: All
Plant: All
```

Expected:

- KPI panels contain data
- Revenue by Region contains Completed data
- Revenue by Plant contains Completed data

---

### Test 2 — Region 2

Set:

```text
Status: Completed
Region: 2
```

Expected:

- Completed panels return no data or zero, depending on panel behavior
- Revenue by Region contains no Completed result

This is expected because:

```text
Region 2 + Completed = empty
```

### Trainer Tip

This test is useful for distinguishing a valid empty result from an incorrect query.

---

### Test 3 — Region 1

Set:

```text
Status: Completed
Region: 1
```

Expected:

- Completed Orders contains data
- Completed Revenue contains data
- High-Value Lines contains data where applicable
- Revenue by Region shows Region 1
- Revenue by Plant is restricted by Region 1

---

## 12. Validate the Q1 2023 Requirement

The workshop brief includes Q1 2023.

Set the dashboard time range to:

```text
From: 2023-01-01
To:   2023-04-01
```

Keep:

```text
Status: Completed
Region: All
Plant: All
```

### Expected Result

The dashboard now represents the Q1 2023 reporting period rather than the complete seed range.

The KPI values should change because the time range has changed.

### Trainer Tip

Do not expect the Q1 2023 values to match the full-seed values.

The upper date boundary should be handled consistently with the dashboard time range.

---

## 13. Validate the Underlying Query

Before considering the dashboard complete, run this validation query in the ClickHouse panel query editor or CloudBeaver:

```sql
SELECT
    count() AS completed_rows,
    uniqExact(order_id) AS completed_orders
FROM training.v_lab_orders
WHERE status = 'Completed'
```

### Expected Result

The seed validation targets are approximately:

```text
completed_rows:   300000
completed_orders: 125000
```

These numbers represent the full Completed seed, not the Q1 2023 filtered dashboard.

---

## 14. Validate Completed Regions

Run:

```sql
SELECT
    region_id,
    count() AS rows,
    uniqExact(order_id) AS orders,
    sum(sales_amount) AS revenue
FROM training.v_lab_orders
WHERE status = 'Completed'
GROUP BY region_id
ORDER BY region_id
```

### Expected Result

Completed data is present for:

```text
1
3
5
```

Region `2` should not appear in this Completed result.

### Trainer Tip

This query is a useful troubleshooting query when students believe the Region variable is not working.

---

## 15. Review Dashboard Usability

Arrange the panels so that the report can be understood from top to bottom.

A practical layout is:

```text
Completed Orders | Completed Revenue | High-Value Lines

Revenue by Region

Revenue by Plant
```

Place the variables prominently so users can see the active filters.

Check:

- Panel titles are meaningful
- KPI values are easy to read
- Filters are visible
- No unnecessary panels are present
- Charts are not overloaded
- Empty Region 2 results are understood
- Dashboard time range is visible and correct

---

## 16. Core Validation Checklist

Before finishing the Core lab, confirm:

- [ ] Dashboard name is `Session 13 - Reporting Workshop`
- [ ] Existing ClickHouse datasource is used
- [ ] Absolute time range is `2023-01-01` → `2025-06-18`
- [ ] Region variable exists
- [ ] Plant variable exists
- [ ] Status variable exists
- [ ] Status defaults to `Completed`
- [ ] Completed Orders KPI exists
- [ ] Completed Revenue KPI exists
- [ ] High-Value Lines KPI exists
- [ ] Revenue by Region panel exists
- [ ] Revenue by Plant panel exists
- [ ] Region filtering works
- [ ] Plant filtering works
- [ ] Status filtering works
- [ ] Region 2 + Completed behavior has been tested
- [ ] Q1 2023 time-range behavior has been tested
- [ ] Full-seed validation is approximately 300,000 Completed rows
- [ ] Full-seed validation is approximately 125,000 distinct Completed orders

---

# Stretch — Optional API/OData Panel

Complete this section only after the Core dashboard is working.

## 17. Add an OData Panel

Use the provisioned **Infinity** datasource.

OData base URL:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/
```

Use the `Orders` entity set.

A simple OData URL for Completed orders can use:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$filter=Status%20eq%20%27Completed%27&$select=OrderId,OrderDate,RegionId,PlantId,SalesAmount&$top=100
```

Configure the Infinity parser as:

```text
Parser: JSON
Root selector: value
```

### Expected Result

The panel receives OData records from the `Orders` entity set.

### Trainer Tip

This is Stretch because the Core dashboard is already complete using ClickHouse.

Do not use `$expand`.

---

## 18. OData Region Filtering — Stretch

OData does not use ClickHouse syntax such as:

```text
IN (${region})
```

For multiple regions, the OData filter must use expressions such as:

```text
RegionId eq 1 or RegionId eq 3
```

For status:

```text
Status eq 'Completed'
```

For a date range:

```text
OrderDate ge 2023-01-01 and OrderDate lt 2023-04-01
```

A combined filter can therefore look like:

```text
Status eq 'Completed' and (RegionId eq 1 or RegionId eq 3)
```

### Trainer Tip

Do not make multi-value OData variable construction a Core requirement. The purpose of this Stretch is to demonstrate the difference between ClickHouse SQL filtering and OData `$filter`.
