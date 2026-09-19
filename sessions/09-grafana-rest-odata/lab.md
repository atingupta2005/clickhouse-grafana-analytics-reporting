# Session 9 — Grafana and REST/OData Integration

## Lab Objective

Connect Grafana to the training REST and OData APIs using the **provisioned Infinity** data source, and build API-based reporting panels.

**Core vs Stretch:** Core steps are marked. Stretch items are optional / homework.

---

## 0. Access Grafana (Core)

Open:

**https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/**

Sign in:

* User: `student`
* Password: `StudentLab!2026`

**Verify dashboard (optional reference):** 
https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/d/lab-s09-rest-odata/session-09-rest-and-odata-infinity-lab-verify 

Set the dashboard time range to absolute **2023-01-01** → **2025-06-18** if panels look empty.

---

## 1. Identify the Training APIs (Core)

<!-- training-diagrams:v2 -->
![ClickHouse DS vs Infinity DS](./assets/ch-vs-infinity.svg)

Public base: `https://vmclickhouse.canadacentral.cloudapp.azure.com`

```text
/api/regions
/api/plants
/api/products
/api/customers
/api/orders
/api/sales
/api/sales/by-region
/api/kpis
/odata/Orders
```

List REST responses use `{ "data": [ ... ], "count": N }`. 
OData collections use a `value` array.

Training `/api` and `/odata` have **no authentication**.

---

## 2. Test a REST Endpoint in the Browser (Core)

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/api/sales?page=1&page_size=10
```

Confirm `200`, JSON, fields such as `order_date`, `region_id`, `order_id`, `status`, `sales_amount`, `quantity`.

---

## 3. Inspect the JSON Envelope (Core)

```json
{
 "data": [
 {
 "order_date": "2023-01-05",
 "region_id": 1,
 "order_id": 100001,
 "status": "Completed",
 "sales_amount": 1250.50,
 "quantity": 12
 }
 ],
 "count": 1
}
```

Records live under **`data`**.

---

## 4. Use the Provisioned Infinity Data Source (Core)

<!-- training-diagrams:v2 -->
![Infinity request anatomy](./assets/request-anatomy.svg)

<!-- training-diagrams:v2 -->
![REST vs OData roots](./assets/rest-vs-odata-roots.svg)

Do **not** create a new Infinity data source. Use the existing provisioned one (uid often shown as **`infinity`**).

### Infinity panel settings (REST)

| Setting | Value |
| -------- | ----- |
| Data source | **Infinity** (provisioned) |
| Type | URL / API |
| Parser | **JSON** |
| Source | URL |
| Method | GET |
| URL | Full HTTPS, e.g. `https://vmclickhouse.canadacentral.cloudapp.azure.com/api/sales?page=1&page_size=50` |
| **Root / Rows selector** | **`data`** |

### Infinity panel settings (OData)

Same Infinity source; change URL and selector:

| Setting | Value |
| -------- | ----- |
| URL | e.g. `https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$top=20` |
| **Root / Rows selector** | **`value`** |

If `root_selector` / Rows path is wrong, the panel is empty even when the URL works in the browser.

---

## 5. Create a Basic REST Panel (Core)

1. New dashboard → Add panel → Infinity.
2. URL: `https://vmclickhouse.canadacentral.cloudapp.azure.com/api/sales?page=1&page_size=50`
3. Parser: JSON · Root selector: **`data`**
4. Visualization: Table
5. Confirm rows appear before styling.

**Expected result:** A table with sales rows. If empty, check root selector **`data`** and absolute time **2023-01-01 → 2025-06-18**.

---

## 6. Filter Sales by Region (Core)

<!-- training-diagrams:v2 -->
![Stack filters on /api/sales](./assets/rest-param-stack.svg)

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/api/sales?region_id=3&status=Completed&page=1&page_size=50
```

Root selector remains **`data`**.

> **Tip:** `region_id=2&status=Completed` returns **empty** — Completed seed data exists only for regions **1, 3, 5**.

Optional any-status Region 2 demo (expect rows, not Completed):

```text
/api/sales?region_id=2&page=1&page_size=20
```

**Expected result:** Region 3 + Completed returns rows; Region 2 + Completed returns an empty `data` array (HTTP 200).

---

## 7. Filter by Status (Core)

```text
/api/sales?status=Completed&page=1&page_size=50
```

---

## 8. Combine Parameters + Dates (Core)

```text
/api/sales?region_id=3&status=Completed&date_from=2023-01-01&date_to=2023-03-31&page=1&page_size=50
```

Aliases `from_date` / `to_date` also work. Pagination on REST is **`page` / `page_size`** — not `top` / `skip` / `limit`.

<!-- training-diagrams:v2 -->
![REST page and page_size](./assets/rest-page-page-size.svg)

**Expected result:** Rows limited to Q1 2023 Completed sales for region 3.

---

## 9. Headers (Core)

Accept JSON is enough. **No Authorization header** is required for the training API.

---

## 10. Authentication — not applicable

Training REST/OData APIs have **no auth**. Do not expect `401`. Soften any auth drill to theory only.

```text
[ ] N/A — training API has no auth
```

---

## 11. Create a REST Reporting Panel (Core)

Table fields: order_date, region_id, order_id, sales_amount, quantity, status.

Confirm Infinity root selector is **`data`**.

---

## 12. Regional Aggregate Panel (Core)

Prefer the dedicated endpoint:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/api/sales/by-region
```

Infinity: parser JSON, root selector **`data`**.

If that endpoint is unavailable in your environment, use the provisioned **ClickHouse** data source with `training.v_lab_orders` grouped by `region_id` (Completed filter) — still valid for this session’s regional panel.

---

## 13. Test the OData Endpoint (Core)

Browser:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$top=10
```

Records live under **`value`**.

---

## 14–17. OData Filter / Select / Order / Top (Core)

Examples (full HTTPS URLs in Infinity; root selector **`value`**):

```text
/odata/Orders?$filter=Status eq 'Completed'&$top=20
/odata/Orders?$select=OrderId,OrderDate,SalesAmount&$top=20
/odata/Orders?$filter=RegionId eq 3 and Status eq 'Completed'&$select=OrderId,OrderDate,CustomerId,SalesAmount&$orderby=SalesAmount desc&$top=10
```

OData pagination uses `$top` / `$skip` (different from REST `page` / `page_size`).

---

## 18. Create an OData Table Panel (Core)

<!-- training-diagrams:v2 -->
![Incremental API panel workflow](./assets/api-query-workflow.svg)

Infinity → full OData HTTPS URL → parser JSON → root selector **`value`** → Table.

**Expected result:** Rows appear under root **`value`**. If the browser shows JSON but Grafana is empty, the root selector is almost always wrong.

---

## 19. Empty Result vs Error (Core)

<!-- training-diagrams:v2 -->
![Empty HTTP 200 vs HTTP errors](./assets/empty-vs-http-error.svg)

Empty but successful:

```text
/api/sales?region_id=2&status=Completed&page=1&page_size=10
```

Invalid path:

```text
/api/invalid
```

Discuss `200` + empty `data` vs `404`.

**Expected result:** Region 2 + Completed → empty table (not an error). Invalid path → HTTP error in Infinity / Explore.

---

## 20. Build the API Dashboard (Core)

Create a dashboard with:

1. REST sales table (`/api/sales` … root `data`)
2. OData completed orders (root `value`)
3. Recent orders (`$orderby` + `$top`)
4. Regional sales (`/api/sales/by-region` or ClickHouse)

Optional open verify: `lab-s09-rest-odata`.

---

## 21. Stretch — CMF plants (optional)

Brief look at the CMF mock:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/cmf/plants
```

Optional Infinity panel (inspect JSON structure first; selector may differ from `/api`). Not required for Core completion.

---

## 22. Validate

```text
[ ] Grafana login works (student)
[ ] Infinity provisioned DS used (not recreated)
[ ] REST URL is full HTTPS
[ ] REST root_selector = data
[ ] OData root_selector = value
[ ] REST pagination uses page / page_size
[ ] Auth N/A noted
[ ] region_id=2 + Completed empty understood
[ ] Regional panel uses /api/sales/by-region (or ClickHouse)
[ ] (Optional) lab-s09-rest-odata verify dashboard opened
[ ] (Stretch) /cmf/plants peeked
```

## Completion Checklist

```text
[ ] REST endpoint tested
[ ] JSON envelope inspected (data / count)
[ ] Infinity used with root_selector data / value
[ ] Parameters tested (incl. date_from/date_to)
[ ] Auth N/A noted
[ ] REST panel created
[ ] OData panel created ($filter / $select / $top)
[ ] OData $top/$skip pagination tested
[ ] Empty Completed+Region2 response tested
[ ] Invalid endpoint tested
[ ] REST/OData dashboard created
[ ] Final dashboard validated
```
