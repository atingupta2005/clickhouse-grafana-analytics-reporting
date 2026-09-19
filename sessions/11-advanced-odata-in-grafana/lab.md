# Session 11 Lab — Advanced OData Querying in Grafana

## Objective

Build an interactive Grafana panel that uses dashboard variables to construct OData queries dynamically.

The lab focuses on:

- Grafana variables in `$filter`
- Multiple filter conditions
- AND / OR conditions
- Date/time filtering
- Multi-value filtering
- `$select`
- `$orderby`
- `$top`
- `$skip`
- JSON response handling
- Empty-result handling
- Query troubleshooting
- Reducing unnecessary data retrieval

The lab uses the provisioned Grafana Infinity datasource and the lab OData service.

**Core:** Steps 1–14. **Stretch** (Part 2) is optional / homework.

---

# Lab Environment

## Grafana

Open:

`https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/`

Sign in:

* User: `student`
* Password: `StudentLab!2026`

## OData Endpoint

Base URL:

`https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/`

Orders entity set:

`https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders`

## Grafana Datasource

Use the provisioned:

- Datasource: `Infinity`
- UID: `infinity`
- Query type: JSON
- Parser: JSON
- OData root selector: `value`

Do not create or modify the datasource.

## Dashboard

Create:

`Session 11 - Advanced OData Lab`

## Shared Data

Use the following known values:

- Entity set: `Orders`
- Status: `Completed`
- Completed regions: `1`, `3`, `5`
- Region `2` + `Completed`: no matching records
- Date range: `2023-01-01` through `2025-06-18`

Use the absolute dashboard time range:

`2023-01-01 → 2025-06-18`

---

# Part 1 — Core Lab

## Step 1 — Create the Session Dashboard

1. Open Grafana.
2. Create a new dashboard.
3. Name it:

 `Session 11 - Advanced OData Lab`

4. Add a new panel.
5. Select the provisioned `Infinity` datasource.

### Expected Result

A new panel is available with the Infinity datasource selected.

### Tip

Do not create another datasource. The lab environment already contains the required Infinity datasource.

---

## Step 2 — Query the Orders Entity Set

In the Infinity query editor:

1. Select `GET`.
2. Use the following URL:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders
```

3. Select the JSON parser.
4. Set the root selector to:

```text
value
```

5. Run the query.

### Expected Result

The panel receives the OData response and displays order records.

The records are contained in the OData `value` collection.

### Tip

If no rows appear, check the following before changing anything else:

1. URL
2. Datasource
3. Parser
4. Root selector

For this OData endpoint, the root selector is `value`.

---

## Step 3 — Create the Region Variable

Create a dashboard variable named:

```text
region
```

Type: **Custom**. Multi-value: **Off** for Core.

Use these controlled values (include **2** only so the empty-result demo in Step 7 works):

```text
1,2,3,5
```

Default: **1** (or **3**). Prefer a Completed region for the first demo.

Now replace the fixed OData query with a variable-driven query:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$filter=RegionId%20eq%20${region}
```

Run the query.

### Test

Select:

```text
Region = 1
```

Then select:

```text
Region = 3
```

Then:

```text
Region = 5
```

### Expected Result

The panel changes when the selected region changes.

The OData query is constructed from the Grafana variable rather than requiring the region value to be changed manually in the URL.

### Tip

The important pattern is:

```text
Grafana variable
 ↓
URL substitution
 ↓
OData $filter
 ↓
JSON response
 ↓
Grafana panel
```

---

## Step 4 — Add the Status Variable

Create another controlled dashboard variable:

```text
status
```

Use:

```text
Completed
```

Update the OData query so that both variables are used:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$filter=RegionId%20eq%20${region}%20and%20Status%20eq%20%27${status}%27
```

### Expected Result

The query applies both conditions:

```text
RegionId eq <selected region>
and
Status eq 'Completed'
```

The panel displays only matching records.

### Tip

`RegionId` is numeric, while `Status` is a string.

The generated filter therefore needs to distinguish between:

```text
RegionId eq 1
```

and:

```text
Status eq 'Completed'
```

---

## Step 5 — Test AND Conditions

Keep:

```text
status = Completed
```

Test the following regions:

```text
1
3
5
```

The effective filter should follow this pattern:

```text
RegionId eq <region> and Status eq 'Completed'
```

### Expected Result

Each valid region returns matching `Completed` records.

### Tip

Use the query preview or inspector to verify the actual URL generated after Grafana substitutes the variables.

This is an important troubleshooting technique for dynamic queries.

---

## Step 6 — Demonstrate OR Conditions

Create a second query that demonstrates a fixed OData OR expression.

Use:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$filter=(RegionId%20eq%201%20or%20RegionId%20eq%203)%20and%20Status%20eq%20%27Completed%27
```

### Expected Result

The query returns `Completed` records from Region 1 or Region 3.

### Tip

Parentheses make the intended logic clear:

```text
(Region 1 OR Region 3)
AND
Completed
```

Explain why parentheses matter when combining `and` and `or`.

---

## Step 7 — Demonstrate an Empty Result

Set:

```text
region = 2
```

Keep:

```text
status = Completed
```

Run the variable-driven query.

### Expected Result

The panel returns no matching records.

This is an expected business-data result because Region 2 has no `Completed` records in the lab data.

### Tip

An empty result does not necessarily mean that the query failed.

Check:

1. Was the query valid?
2. Did Grafana substitute the variables?
3. Does the selected combination contain data?

Restore:

```text
region = 1
```

The panel should return data again.

---

## Step 8 — Add Date Filtering

Keep the Grafana dashboard time range absolute:

```text
2023-01-01 → 2025-06-18
```

Do not use `Last 30 days`.

For the **OData** `$filter`, use a concrete Q1 2023 window (same pattern as Session 07):

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$filter=RegionId%20eq%20${region}%20and%20Status%20eq%20%27${status}%27%20and%20OrderDate%20ge%202023-01-01%20and%20OrderDate%20lt%202023-04-01&$top=20
```

Decoded filter:

```text
RegionId eq ${region}
and Status eq '${status}'
and OrderDate ge 2023-01-01
and OrderDate lt 2023-04-01
```

### Expected Result

With `region = 1` (or 3/5) and `status = Completed`, the panel returns Completed orders in **Q1 2023** for that region.

### Tip

First prove this URL works with a fixed region (for example `RegionId eq 3`) in the browser or Infinity. Then restore `${region}` / `${status}`.

Do not invent other date literal formats — this lab service accepts `YYYY-MM-DD` as in Session 07.

---

## Step 9 — Reduce Returned Fields with `$select`

Modify the query to return only fields needed by the panel.

Use:

```text
$select=OrderId,RegionId,Status,OrderDate,SalesAmount
```

For example:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$select=OrderId,RegionId,Status,OrderDate,SalesAmount
```

Combine `$select` with the existing filter when required.

### Expected Result

The response contains only the requested fields.

### Tip

`$select` is useful when the panel does not need every field returned by the entity set.

This is one way to reduce unnecessary API data retrieval.

---

## Step 10 — Sort the Result with `$orderby`

Add:

```text
$orderby=OrderDate desc
```

For example:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$select=OrderId,RegionId,Status,OrderDate,SalesAmount&$orderby=OrderDate%20desc
```

### Expected Result

The records are returned with the newest order dates first.

### Tip

Do not introduce arbitrary sort fields.

Use fields known to exist in the Orders response.

---

## Step 11 — Limit Results with `$top`

Add:

```text
$top=20
```

For example:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$select=OrderId,RegionId,Status,OrderDate,SalesAmount&$orderby=OrderDate%20desc&$top=20
```

### Expected Result

The query returns no more than 20 records.

### Tip

`$top` is useful when a panel needs only a limited number of records.

It also prevents unnecessarily large responses during exploration.

---

## Step 12 — Use `$skip` for Pagination

Keep:

```text
$top=20
```

and add:

```text
$skip=20
```

Example:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$select=OrderId,RegionId,Status,OrderDate,SalesAmount&$orderby=OrderDate%20desc&$top=20&$skip=20
```

### Expected Result

The query returns a different page of records.

Explain the pagination pattern:

```text
Page 1
$top=20
$skip=0

Page 2
$top=20
$skip=20

Page 3
$top=20
$skip=40
```

### Tip

`$skip` is an OData query option.

It does not automatically create a pagination control in Grafana.

A Grafana variable can be used later to make the offset dynamic.

---

## Step 13 — Validate the JSON Response

Open the query response or query inspector.

Verify:

- HTTP request completed successfully.
- Response is JSON.
- Records are under `value`.
- Requested fields are present.
- Filters affect the returned records.
- `$top` limits the number of records.
- `$skip` changes the returned page.

### Expected Result

You can identify the difference between:

```text
Valid response + records
```

and:

```text
Valid response + zero records
```

and:

```text
Invalid query / response
```

### Tip

When a Grafana panel is empty, do not immediately change the panel visualization.

First inspect the query and response.

---

## Step 14 — Final Core Panel

Return to the variable-driven query.

The final Core panel should use:

- `region`
- `status`
- `$filter`
- `$select`
- `$orderby`
- `$top`

Use the known valid test:

```text
region = 1
status = Completed
```

Use:

```text
$top=20
```

and a useful `$select` list.

### Expected Result

The final table panel dynamically responds to the selected region while retaining the status filter.

---

# Part 2 — Stretch Lab

Complete these exercises after the Core workflow is working.

## Stretch 1 — Multi-Value Region Variable

Enable **Multi-value** on `region`. Use Completed regions only for this stretch:

```text
1,3,5
```

**Important:** Session 10’s ClickHouse `${region}` / `${status:sqlstring}` patterns are **not** valid OData. OData needs an `or` chain (or an equivalent custom format).

Working example with two regions selected (1 and 3) — use a **custom** variable format or a fixed demo URL first:

```text
$filter=(RegionId eq 1 or RegionId eq 3) and Status eq 'Completed'
```

In Grafana, a practical approach is:

1. Prove the fixed `or` URL works.
2. Then use a custom multi-value format that expands to `RegionId eq 1 or RegionId eq 3` (for example a regex/custom format that prefixes each value), **or** keep multi-region as a fixed OR demo if formatting is too fiddly in the time available.

Do **not** leave:

```text
RegionId eq ${region}
```

when `${region}` expands to `1,3` — that is invalid OData.

### Expected Result

Selecting more than one Completed region returns records for all selected regions (or the fixed OR demo clearly shows the pattern).

---

## Stretch 2 — Dynamic `$select`

Create a controlled Grafana variable for a small set of approved field combinations.

For example:

```text
OrderId,RegionId,Status
```

and:

```text
OrderId,OrderDate,SalesAmount
```

Use the variable in `$select`.

### Expected Result

Changing the variable changes the fields returned by the OData request.

### Tip

Use controlled values.

Do not allow arbitrary user-entered URL expressions.

---

## Stretch 3 — Dynamic `$orderby`

Create a controlled variable containing supported sort expressions.

For example:

```text
OrderDate asc
OrderDate desc
SalesAmount asc
SalesAmount desc
```

Use the selected value in `$orderby`.

### Expected Result

Changing the variable changes the ordering of the returned records.

---

## Stretch 4 — Dynamic Pagination

Create a controlled variable for the page offset:

```text
0
20
40
60
```

Use the selected value for `$skip`.

Keep:

```text
$top=20
```

### Expected Result

Changing the page variable retrieves a different page.

---

## Stretch 5 — Dynamic Date Filtering

After validating a fixed date filter, make the date values dynamic.

Use the date range already established for the course:

```text
2023-01-01 → 2025-06-18
```

Build the final OData URL from controlled Grafana values.

### Expected Result

Changing the selected date values changes the OData result.

### Tip

Validate the generated URL before troubleshooting the panel.

---

## Stretch 6 — Query Reduction

Compare two requests:

### Query A

Returns the default Orders response.

### Query B

Uses:

```text
$select
$filter
$orderby
$top
```

Discuss:

- response size,
- number of fields,
- amount of data transferred,
- amount of data Grafana needs to process.

### Expected Result

You should understand why API queries should retrieve only the data required by the panel.

---

# Part 3 — Related Entities

## `$expand` — Theory Only

OData supports the concept of related entities through `$expand`.

A conceptual query may look like:

```text
Orders?$expand=Customer
```

However, `$expand` is **not supported in the Core student OData workflow for this lab**.

Do not make `$expand` a required hands-on task.

Discuss:

- why `$expand` is useful,
- how it can return related data,
- why expanded responses can become more complex,
- why unsupported `$expand` should not be treated as a Grafana configuration problem.

### Expected Result

You should understand the purpose and limitation of `$expand`.

---

# Part 4 — Query Troubleshooting

## Troubleshooting Exercise

Intentionally test a few controlled changes.

### Test A — Valid Filter

```text
RegionId eq 1
```

Expected: data.

### Test B — Valid Empty Filter

```text
RegionId eq 2 and Status eq 'Completed'
```

Expected: no matching records.

### Test C — Incorrect Field Name

Temporarily use an incorrect field name.

Expected: query/API error rather than a valid empty business result.

Restore the correct field.

### Test D — Incorrect Variable Substitution

Inspect the generated URL when changing a variable.

Verify that the actual value appears in the request.

### Expected Result

You can distinguish:

```text
Query error
```

from:

```text
Valid query with zero rows
```

and:

```text
Valid query with unexpected filter values
```

---

## Final Integration Exercise

Build the final interactive OData table using:

```text
Session 11 - Advanced OData Lab
```

The panel should use:

1. `region` variable
2. `status` variable
3. Dynamic `$filter`
4. `$select`
5. `$orderby`
6. `$top`
7. OData JSON response
8. Root selector `value`

Use this test sequence:

### Test 1

```text
Region = 1
Status = Completed
```

Expected: records.

### Test 2

```text
Region = 3
Status = Completed
```

Expected: records.

### Test 3

```text
Region = 5
Status = Completed
```

Expected: records.

### Test 4

```text
Region = 2
Status = Completed
```

Expected: empty result.

### Test 5

Return to:

```text
Region = 1
Status = Completed
```

Expected: records return.

---

# Troubleshooting guide
## Problem: Panel is completely empty

Check:

1. Infinity datasource.
2. HTTPS URL.
3. JSON parser.
4. Root selector `value`.
5. Query response.
6. Variable substitution.

## Problem: Variable changes but data does not change

Check the generated URL.

The selected variable value must actually appear in `$filter`.

## Problem: Region 2 shows no records

This is expected for:

```text
Region 2 + Completed
```

Use Region 1, 3, or 5 to verify that the query is working.

## Problem: Multi-value filter fails

Check the Session 10 variable formatting pattern.

Do not assume that the raw multi-value substitution is automatically valid OData.

## Problem: Query returns too much data

Use:

```text
$select
```

and:

```text
$top
```

Also apply an appropriate `$filter`.

## Problem: `$expand` fails

This is expected for the student Core workflow.

Do not recreate the datasource or change the lab infrastructure.

---

# Core Completion Checklist

The Core lab is complete when the student can:

- [ ] Create `Session 11 - Advanced OData Lab`
- [ ] Use the provisioned Infinity datasource
- [ ] Query the OData `Orders` entity set
- [ ] Configure the OData JSON root selector as `value`
- [ ] Create a Region variable
- [ ] Create a Status variable
- [ ] Use variables in `$filter`
- [ ] Combine conditions with `and`
- [ ] Demonstrate `or`
- [ ] Demonstrate an intentional empty result
- [ ] Apply date filtering
- [ ] Use `$select`
- [ ] Use `$orderby`
- [ ] Use `$top`
- [ ] Use `$skip`
- [ ] Validate the JSON response
- [ ] Troubleshoot variable substitution
- [ ] Distinguish an empty result from a query error
- [ ] Explain why `$expand` is not a Core lab feature
- [ ] Reduce unnecessary API data retrieval

## Final Known-Good State

Return the dashboard to:

```text
Region = 1
Status = Completed
```

Use the absolute dashboard range:

```text
2023-01-01 → 2025-06-18
```

The final panel should display OData order records successfully.
