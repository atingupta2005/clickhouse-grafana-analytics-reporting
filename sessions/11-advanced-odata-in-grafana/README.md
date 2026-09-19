# Session 11 — Advanced OData Querying in Grafana

## Overview

<!-- training-diagrams:v1 -->
![Build a dynamic OData URL](./assets/odata-url-build.svg)


This session builds on OData querying from Session 07, Infinity + OData from Session 09, and Grafana variables from Session 10.

The focus is using Grafana variables to construct dynamic OData queries and control filtering, selected fields, sorting, and pagination.

The main flow is:

**Grafana Variable → OData Query → JSON → Grafana Panel**

The lab OData service supports `$filter`, `$select`, `$orderby`, `$top`, `$skip`, and `$count`. Related-entity expansion is discussed as theory only because `$expand` is not supported by the lab OData service.

## Topics

- Using Grafana variables in `$filter`
- Dynamic `$filter` construction
- Multiple filter conditions using `AND` / `OR`
- Date and time filtering
- Multi-value variables
- Dynamic `$select`
- Dynamic `$orderby`
- `$top` and `$skip`
- Pagination concepts
- `$expand` and related entities — **theory / unsupported on the lab OData service**
- Dynamic query parameters and URL construction
- JSON response handling
- Empty-result handling
- Query troubleshooting
- Reducing unnecessary API data retrieval

## Practical Focus

By the end of the session, the practical workflow covers:

1. Using Grafana variables with an OData `$filter`.
2. Filtering Orders dynamically by region and status.
3. Combining multiple OData conditions.
4. Applying date filters against the training seed.
5. Using a multi-value variable where appropriate.
6. Dynamically controlling selected fields and sorting.
7. Using `$top` and `$skip` for limited result sets and pagination.
8. Handling an empty result deliberately, including **Region 2 + Completed**.
9. Validating the JSON returned by the OData endpoint.
10. Troubleshooting common Infinity/OData query problems.

## Core vs Stretch

| Level | Coverage |
|---|---|
| **Core** | Infinity with the provisioned OData datasource |
| **Core** | Grafana variables used in OData `$filter` |
| **Core** | Region/status filtering |
| **Core** | Date filtering using the training seed range |
| **Core** | Multiple filter conditions with `AND` / `OR` |
| **Core** | `$select`, `$orderby`, `$top`, and `$skip` |
| **Core** | JSON response and empty-result validation |
| **Core** | Query troubleshooting and reducing unnecessary data retrieval |
| **Stretch** | More advanced combinations of dynamic query parameters |
| **Stretch** | Optional CMF `/cmf/plants` demonstration |
| **Theory / Unsupported** | `$expand` and related entities |
| **Theory / Unsupported** | `$search` |
| **Theory / Unsupported** | OData key URLs such as `Orders(id)` |
| **Theory / Unsupported** | Nested related-entity responses |

> **Important:** `$expand` must not be treated as a required lab capability. The lab OData service does not support it.

## Lab Seed Reminders

Use the lab OData service:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/
```

Orders are backed by the training reporting view and use PascalCase OData fields such as:

```text
RegionId
Status
SalesAmount
OrderDate
```

Important seed facts:

- Database: `training`
- Reporting view: `training.v_lab_orders`
- Status used in the lab: `Completed`
- Completed regions: **1, 3, 5**
- **Region 2 + Completed intentionally returns an empty result**
- Order dates: **2023-01-01 → 2025-06-18**
- Example quarter: **Q1 2023**

For Grafana time-based work, use the absolute range:

```text
2023-01-01 → 2025-06-18
```

Do not use **Last 30 days** as the primary lab range.

## Grafana Reminders

Grafana:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/
```

Sign in:

* User: `student`
* Password: `StudentLab!2026`

Use the provisioned **Infinity** datasource.

Infinity parser:

```text
JSON
```

OData root selector:

```text
value
```

Use complete HTTPS URLs in Infinity panel queries.

Do not recreate the datasource during the Core lab.

## Suggested Dashboard

```text
Session 11 - Advanced OData Lab
```

## Timing

**TOC duration:** 3 hours

With slower PAX (~2× hands-on):

- **Core (~90–120 min):** Grafana login → absolute time → Infinity `value` → region/status variables → `$filter` AND/OR → Region 2 empty demo → Q1 2023 date filter → `$select` / `$orderby` / `$top` / `$skip` → final table panel
- **Stretch / homework:** multi-value OData `or` chain, dynamic `$select`/`$orderby`/`$skip`, optional `/cmf/plants`

Seed: Completed regions **1 / 3 / 5**; include region **2** in the variable only for the empty demo; dates **2023-01-01** … **2025-06-18**.

## Files

Diagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.
 in This Session

```text
README.md       Session overview and scope
notes.md        Teaching notes and OData/Grafana concepts
lab.md          Guided Core and Stretch hands-on lab
```
