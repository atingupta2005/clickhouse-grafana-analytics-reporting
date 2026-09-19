# Lab — JSON and REST API Data

## Lab Objective

In this lab, you will work with JSON data and REST APIs used by the reporting environment.

You will:

* Inspect JSON responses
* Extract fields (inline ClickHouse — no CREATE)
* Understand nested JSON as theory (live API is flat)
* Handle missing values
* Call REST endpoints
* Use query parameters (`page` / `page_size`, `date_from` / `date_to`)
* Handle pagination
* Troubleshoot API responses
* Prepare API data for reporting

Use the training REST API provided in the lab environment.

**Base URL:** `https://vmclickhouse.canadacentral.cloudapp.azure.com`

Examples:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/api
https://vmclickhouse.canadacentral.cloudapp.azure.com/api/regions
https://vmclickhouse.canadacentral.cloudapp.azure.com/api/orders?page=1&page_size=10
```

List endpoints return JSON shaped like `{ "data": [ ... ], "count": N }`.

`status=Completed` is accepted as an alias for stored status `Closed`.

**Core vs Stretch:** Core steps are marked below. Stretch items are optional / homework.

> Students connect to ClickHouse as **`training_ro`** (read-only). Do **not** `CREATE` or `INSERT` tables on the `training` database.

---

## 1. Discover the API (Core)

Start by opening the API documentation or checking the available endpoints.

```text
/api/regions
/api/plants
/api/products
/api/customers
/api/orders
/api/transactions
/api/sales
/api/sales/by-region
/api/kpis
```

### Task

Identify:

* Available endpoints
* HTTP method supported (`GET`)
* Optional parameters (`region_id`, `status`, `from_date`/`to_date` or `date_from`/`date_to`, `page`, `page_size`)
* Response format `{ data, count }`
* Pagination: **`page` / `page_size`** (not `limit` / `top` / `skip`)

---

## 2. Call a Basic REST Endpoint (Core)

Call:

```text
GET /api/regions
```

Inspect the response.

Identify:

* HTTP status code
* Response headers
* JSON body
* Number of records (`count`)
* Field names

A response looks similar to:

```json
{
 "data": [
 {
 "region_id": 1,
 "region_name": "North"
 },
 {
 "region_id": 2,
 "region_name": "South"
 }
 ],
 "count": 2
}
```

### Task

Identify where the actual records are located (`data`).

---

## 3. Inspect JSON Objects (Core)

Call:

```text
GET /api/customers?page=1&page_size=10
```

Inspect one customer record.

Seed-style names look like `Customer-N` or `Industrial-N` (not invented company brands).

Identify fields such as:

```text
customer_id
customer_name
region_id
email
```

### Task

Determine whether any fields contain `null` or are missing.

---

## 4. Live Orders JSON Is Flat (Core)

Call:

```text
GET /api/orders?page=1&page_size=5
```

A representative **live** row looks like:

```json
{
 "order_id": 100001,
 "customer_id": 1,
 "plant_id": 1,
 "region_id": 1,
 "order_date": "2023-01-05",
 "status": "Completed",
 "currency": "USD",
 "quantity": 12,
 "sales_amount": 1250.50
}
```

There is **no** nested `customer` / `plant` object and **no** `product_id` on `/api/orders`.

### Task

Map the flat fields you need for reporting:

```text
order_id
order_date
customer_id
region_id
plant_id
quantity
sales_amount
status
```

### Stretch — nested JSON theory only

Some production APIs nest related objects. Practice reading a nested sample (do **not** expect this from the live training `/api/orders`):

```json
{
 "order_id": 100001,
 "customer": { "customer_id": 1, "customer_name": "Customer-1" },
 "plant": { "plant_id": 1, "plant_name": "Plant-1" }
}
```

---

## 5. Extract JSON Fields in ClickHouse (Core) — no CREATE

Use an **inline** JSON string. Do not create `training.json_demo`.

```sql
SELECT
 JSONExtractUInt(j, 'customer_id') AS customer_id,
 JSONExtractString(j, 'customer_name') AS customer_name,
 JSONExtractFloat(j, 'sales_amount') AS sales_amount
FROM
(
 SELECT '{"customer_id":1,"customer_name":"Customer-1","sales_amount":1250.50}' AS j
);
```

### Task

Verify the extracted values have the expected types and values.

---

## 6. Handle NULL Values (Core)

```sql
SELECT
 JSONExtractString(j, 'customer_name') AS customer_name,
 JSONExtractString(j, 'email') AS email_raw,
 if(
 JSONHas(j, 'email') = 0 OR JSONExtractString(j, 'email') = '',
 'Not Available',
 JSONExtractString(j, 'email')
 ) AS email_display
FROM
(
 SELECT '{"customer_id":3,"customer_name":"Customer-3","email":null}' AS j
);
```

### Task

Determine how extraction treats `null`, then show `Not Available` when email is missing.

---

## 7. Nested JSON Extraction (Stretch)

Inline nested practice (theory — not the live orders envelope):

```sql
SELECT
 JSONExtractUInt(j, 'order_id') AS order_id,
 JSONExtractUInt(j, 'customer', 'id') AS customer_id,
 JSONExtractString(j, 'customer', 'name') AS customer_name,
 JSONExtractFloat(j, 'sales_amount') AS sales_amount
FROM
(
 SELECT '{"order_id":100001,"customer":{"id":1,"name":"Customer-1"},"sales_amount":1250.50}' AS j
);
```

### Task

Verify the extracted values.

---

## 8. Work with JSON Arrays (Stretch)

Consider a theoretical line-item array (not returned by `/api/orders`):

```json
{
 "order_id": 100001,
 "products": [
 { "product_id": 1001, "quantity": 5 },
 { "product_id": 1003, "quantity": 2 }
 ]
}
```

Discuss how you would flatten to:

```text
order_id | product_id | quantity
```

For live product lists, call `/api/products` instead.

---

## 9. Call the Orders API (Core)

Call:

```text
GET /api/orders?page=1&page_size=10
```

Identify:

* Order ID
* Order date
* Region (`region_id`)
* Customer (`customer_id` — name is not on this endpoint)
* Plant (`plant_id`)
* Quantity
* Sales amount
* Status

### Task

Field mapping:

```text
API Field Reporting Field
----------------------------------------
order_id order_id
order_date order_date
region_id region_id
customer_id customer_id
quantity quantity
sales_amount sales_amount
status status
```

---

## 10. Use Query Parameters (Core)

```text
GET /api/orders?region_id=3&page=1&page_size=10
```

Compare with:

```text
GET /api/orders?page=1&page_size=10
```

### Tasks

1. Confirm that the parameter changes the result.
2. Note `count` and page size.
3. Verify returned records belong to region 3.

---

## 11. Filter by Status (Core)

```text
GET /api/orders?status=Completed&page=1&page_size=10
```

Then combine:

```text
GET /api/orders?region_id=3&status=Completed&page=1&page_size=10
```

>

---

## 12. Date Parameters (Core)

Both parameter name pairs work:

```text
GET /api/orders?from_date=2023-01-01&to_date=2023-03-31&page=1&page_size=10
GET /api/orders?date_from=2023-01-01&date_to=2023-03-31&page=1&page_size=10
```

### Task

Verify earliest/latest dates fall inside Q1 2023. Use `YYYY-MM-DD`. Seed range is **2023-01-01** … **2025-06-18**.

---

## 13. Inspect API Headers (Core)

Make a request and inspect response headers (`Content-Type`, cache headers if present). Confirm JSON.

---

## 14. Test HTTP Status Codes (Core)

```text
GET /api/does-not-exist
```

Record status and body. Explain what the status code tells you.

---

## 15. Authentication — not applicable

The **training REST API has no authentication**. Do not expect `401` when calling `/api`.

```text
[ ] N/A — training API has no auth (skip credential drills)
```

Optional stretch (theory only): list auth types you might see in production (API key, Basic, Bearer). Do not invent lab credentials.

---

## 16. Pagination (Core)

```text
GET /api/orders?page=1&page_size=10
GET /api/orders?page=2&page_size=10
```

### Tasks

1. Record records per page (`count`).
2. Identify how the next page is requested (`page=N+1`).
3. Check that records are not duplicated between pages.
4. Determine end of result set (`count` < `page_size` or empty `data`).

---

## 17. Handle a Paginated Dataset (Core)

```text
Page | Records | First Order | Last Order
-----|---------|-------------|------------
1 | | |
2 | | |
3 | | |
```

---

## 18. Prepare API Data for Reporting (Core)

Prefer `/api/orders` (has `customer_id`) or `/api/sales` (leaner grain).

```text
GET /api/orders?page=1&page_size=50
```

Prepare:

```text
order_id
order_date
region_id
customer_id
quantity
sales_amount
```

Do **not** require `product_id` from `/api/orders` — it is not returned. Optional: call `/api/products` separately for product catalogs.

---

## 19. API Troubleshooting Scenario (Core)

Request with a bad date:

```text
GET /api/orders?from_date=01-01-2026
```

Then try:

```text
GET /api/orders?date_from=2023-01-01&date_to=2023-01-31&page=1&page_size=10
```

### Tasks

1. What is wrong with the first date format?
2. Confirm `YYYY-MM-DD`.
3. Confirm the aliases `date_from` / `date_to` work.

---

## 20. Final API-to-Reporting Challenge (Stretch / homework)

Build:

```text
REST API → GET /api/orders → JSON {data,count} → Extract fields → Filters → Pagination → Reporting dataset
```

### Requirement

**Completed orders for Region 3 during Q1 2023.**

Final columns (match live `/api/orders`):

```text
order_id
order_date
customer_id
region_id
quantity
sales_amount
```

Example request shape:

```text
GET /api/orders?region_id=3&status=Completed&date_from=2023-01-01&date_to=2023-03-31&page=1&page_size=50
```

### Tasks

1. Identify endpoint and parameters.
2. Call the API; inspect `{ data, count }`.
3. Extract the flat fields above (no nested flatten needed).
4. Process pages.
5. Validate region, dates, status.
6. Sum quantity and sales across retrieved pages.

Record:

```text
Endpoint:
________________________________

Parameters:
________________________________

Pages processed:
________________________________

Records returned:
________________________________

Total quantity:
________________________________

Total sales:
________________________________

Validation completed:
________________________________
```

## Lab Completion Checklist

```text
[ ] Inspected REST endpoints
[ ] Inspected JSON objects (flat live envelope)
[ ] Extracted JSON fields with inline SELECT (no CREATE)
[ ] Handled NULL/missing values
[ ] Called REST API
[ ] Used region / status / date_from|date_to parameters
[ ] Inspected headers
[ ] Checked HTTP status codes
[ ] Auth N/A noted (training API has no auth)
[ ] Implemented page / page_size pagination
[ ] Handled API errors
[ ] Prepared API data for reporting (no product_id on orders)
[ ] (Stretch) Final API-to-reporting challenge
```
