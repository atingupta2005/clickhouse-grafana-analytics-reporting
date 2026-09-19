# Session 12 — Advanced Grafana Dashboards

## 1. Dashboard Organization

A dashboard should answer a reporting question quickly. Organize panels so that users can move from summary to detail:

1. KPI/stat panels
2. Trend panels
3. Comparison panels
4. Detail tables
5. Navigation or drill-down panels

Keep related panels together. Avoid placing many panels with different purposes in the same row.

### Trainer tip

Start with the question the dashboard should answer, then decide which panel type supports that question. Do not start by adding panels simply because Grafana provides them.

---

## 2. Choosing Panel Types

### Stat

Use a Stat panel for a single important value.

Typical examples:

- Completed orders
- Total sales
- Total quantity
- Number of regions

For example:

```sql
SELECT uniqExact(order_id) AS completed_orders
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date < '2025-06-19'
```

### Time series

Use a Time series panel when the important question is how a measure changes over time.

A monthly sales trend can be produced with:

```sql
SELECT
    toStartOfMonth(order_date) AS month,
    sum(sales_amount) AS sales
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date < '2025-06-19'
GROUP BY month
ORDER BY month
```

The time field should be recognized as the timestamp/date field by Grafana.

### Bar chart

Use a bar chart for comparisons between categories.

For regional sales:

```sql
SELECT
    region_id,
    sum(sales_amount) AS sales
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date < '2025-06-19'
GROUP BY region_id
ORDER BY sales DESC
```

### Table

Tables are useful when users need individual values rather than a visual summary.

For detail panels, select only the fields required by the report and use a reasonable `LIMIT`.

```sql
SELECT
    order_id,
    order_date,
    region_id,
    sales_amount,
    status
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date < '2025-06-19'
ORDER BY order_date DESC
LIMIT 100
```

### Trainer tip

Do not use a table to display thousands of rows when a summary or chart answers the same question.

---

## 3. Thresholds

Thresholds help users identify values that need attention without reading every number.

A threshold should have a clear reporting meaning.

Examples:

- Low/normal/high KPI ranges
- Sales target indicators
- Exception counts

Do not select arbitrary thresholds simply to demonstrate the feature. When the business target is not defined, explain the threshold as a dashboard-formatting example rather than a business rule.

### Trainer tip

Threshold colors and ranges are presentation rules. They do not change the underlying query result.

---

## 4. Units and Number Formatting

Formatting should make values easier to read.

Examples:

- Currency for sales
- Integer formatting for order counts
- Quantity formatting for quantities
- Appropriate decimal precision for calculated values

Avoid excessive decimal places in business dashboards.

For example, a value such as:

```text
125000.000000
```

is usually less useful to a reporting user than:

```text
125,000
```

### Trainer tip

Formatting should be applied at the Grafana field/panel level when the underlying numeric value is still needed for calculations.

---

## 5. Legends

Legends help users identify series in charts.

For a single sales series, a simple legend is sufficient.

For multiple regional series, the legend should clearly identify the region.

Avoid displaying unnecessary statistical information in the legend when it does not help the dashboard user.

---

## 6. Field Configuration

Field configuration controls how Grafana displays returned data.

Common settings include:

- Unit
- Decimals
- Display name
- Thresholds
- Min/max
- Value mappings
- Field-specific overrides

Use overrides when different fields require different formatting.

### Example

A table may contain:

| Field | Display |
|---|---|
| `order_id` | Integer |
| `sales_amount` | Currency/number |
| `order_date` | Date |
| `region_id` | Integer |

The database values remain unchanged. Grafana controls their presentation.

---

## 7. Transformations

Transformations modify the data returned to a panel before visualization.

They are useful when the query already returns the required information but the dashboard needs additional shaping.

Common examples include:

- Organizing fields
- Rename fields
- Reduce
- Join
- Calculate fields
- Filter fields

### Why use a transformation?

Suppose a query returns:

```text
region_id
sales
quantity
```

A transformation can organize or rename these fields for presentation without changing the underlying ClickHouse query.

### Trainer tip

Use SQL for database-level filtering, aggregation, and calculations when practical. Use Grafana transformations for presentation-level shaping.

This keeps the query easier to understand and usually reduces unnecessary dashboard processing.

---

## 8. Calculated Values

A calculated value can derive a new metric from fields already returned to Grafana.

For example, when both sales and quantity are available:

```text
average value = sales / quantity
```

The calculation can be performed using a Grafana transformation when appropriate.

### Trainer tip

Make sure the source fields are numeric and that division-by-zero cases are considered.

If the calculation is expensive or needs database-level filtering, prefer doing it in ClickHouse.

---

## 9. Field Organization

A table should expose the information in an order that matches how users read it.

For example:

```text
Order ID → Order Date → Region → Status → Sales Amount
```

Remove fields that are not required by the user.

Renaming fields can also make technical database names easier to understand.

For example:

```text
sales_amount
```

can be displayed as:

```text
Sales Amount
```

without changing the database column.

---

## 10. Variables and Interactive Filtering

Session 12 reuses the variable approach introduced in earlier sessions.

The dashboard should use existing variables rather than creating a different filtering mechanism for each panel.

The important variables are:

- Region
- Status
- Dashboard time range

### ClickHouse variable syntax

For a multi-value region variable:

```sql
IN (${region})
```

For a multi-value status variable (Session 10 pattern):

```sql
status IN (${status:sqlstring})
```

Do **not** write `status = ${status:sqlstring}` when Multi-value is on — that breaks when more than one status is selected.

The exact variable configuration should match the existing Session 10 dashboard pattern (ClickHouse panels only).

### Trainer tip

Do not copy ClickHouse variable syntax into Infinity OData queries.

OData uses OData expressions, for example:

```text
RegionId eq 1 or RegionId eq 3
```

and string values are quoted.

---

## 11. Panel Links and Dashboard Links

Links allow users to move from a summary panel to a more detailed view.

A useful pattern is:

```text
Summary dashboard
       ↓
Regional analysis
       ↓
Order detail
```

The link should pass useful context when possible.

For example, a regional dashboard can receive a selected region through a dashboard variable.

### Trainer tip

Keep drill-down paths short. The user should always understand where the link will take them.

Do not invent links to external systems that are not part of the lab.

---

## 12. Drill-Down Design

A drill-down should answer the next natural question.

Example:

**Question 1:** How many completed orders are there?

→ Stat panel

**Question 2:** How are they distributed by region?

→ Bar chart

**Question 3:** Which orders contribute to a selected region?

→ Detail table

This creates a useful reporting flow without requiring additional applications.

---

## 13. Annotations

Annotations add event information to visualizations.

They can be useful for marking events such as:

- Deployment
- Incident
- Maintenance
- Reporting milestone

For this course lab, annotations are Stretch because they depend on additional event data and are not required to demonstrate the core dashboard concepts.

### Trainer tip

Do not create artificial operational events simply to populate an annotation timeline.

---

## 14. Query Performance

Grafana can make it easy to issue expensive queries repeatedly.

Use these basic rules:

### Select only required columns

Prefer:

```sql
SELECT
    region_id,
    sum(sales_amount) AS sales
```

instead of:

```sql
SELECT *
```

### Filter early

Use the status and date filters before aggregation:

```sql
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date < '2025-06-19'
```

### Aggregate before displaying

A chart normally does not need hundreds of thousands of detail rows.

For example:

```sql
GROUP BY region_id
```

is preferable to returning every order when the dashboard only needs regional totals.

### Limit detail queries

For a detail table:

```sql
LIMIT 100
```

prevents the dashboard from attempting to display an unnecessarily large result.

### Use the actual seed range

The training data ends on `2025-06-18`.

Use:

```text
2023-01-01 → 2025-06-18
```

rather than relative ranges such as **Last 30 days**.

---

## 15. Grafana Footguns

### Region 2 + Completed

The seed contains Completed data for regions:

```text
1, 3, 5
```

Region `2` with `Completed` is intentionally empty.

An empty panel does not necessarily mean the query is broken.

### Wrong datasource

REST and OData panels should use the provisioned **Infinity** datasource.

ClickHouse SQL panels should use the provisioned **ClickHouse** datasource.

### Wrong Infinity root selector

Use:

- REST → `data`
- OData → `value`

### Incorrect OData syntax

OData filters are not ClickHouse SQL.

Correct OData-style multi-value filtering:

```text
RegionId eq 1 or RegionId eq 3
```

Do not use:

```text
IN (${region})
```

inside an OData `$filter`.

### Student permissions

Students use the provisioned environment and should not be expected to create datasources or change server configuration.

### Large tables

A detail table without filtering or `LIMIT` can create unnecessary load and poor dashboard responsiveness.

---

## 16. Live Teaching Flow

Use the following progression during the session:

```text
Existing dashboard
      ↓
Organize layout
      ↓
Add KPI/stat panels
      ↓
Add trend and comparison charts
      ↓
Format fields and thresholds
      ↓
Apply transformation/calculated value
      ↓
Add navigation/drill-down
      ↓
Review query performance
```

Keep the dashboard focused on the reporting task rather than demonstrating every Grafana option.
