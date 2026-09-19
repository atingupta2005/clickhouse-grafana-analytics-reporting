# Session 9 — Grafana and REST/OData Integration

## Session Overview

This session focuses on integrating Grafana with REST and OData APIs for reporting.

The main reporting flow is:

```text
CMF Application
      |
      v
 REST / OData API
      |
      v
   JSON Data
      |
      v
    Grafana
      |
      v
 Reporting Panel
```

## Topics

* REST and OData data-source concepts
* Grafana API integration approaches
* Connecting Grafana to REST/OData endpoints
* API parameters
* Headers and authentication concepts
* JSON response handling
* Filtering
* Date and time parameters
* Pagination
* Empty and invalid responses
* Basic troubleshooting

## Practical Work

Participants will:

* Open Grafana (`student` / `StudentLab!2026`)
* Use the **provisioned Infinity** data source (uid `infinity`)
* Set full HTTPS URLs; parser JSON; root selector `data` (REST) / `value` (OData)
* Execute REST queries with `page` / `page_size` and `date_from` / `date_to`
* Apply OData `$filter` / `$select` / `$top`
* Build a regional panel via `/api/sales/by-region` (or ClickHouse)
* Optionally open verify dashboard `lab-s09-rest-odata`
* Optional stretch: `/cmf/plants`

## Reporting Flow

<!-- training-diagrams:v1 -->
![API data into Grafana Infinity](./assets/infinity-architecture.svg)


```text
Grafana
   |
   v
REST / OData Data Source
   |
   v
API Request
   |
   v
CMF / Application API
   |
   v
JSON Response
   |
   v
Grafana Panel
```

## Timing (PAX ~2×)

TOC: **4 hours**. Feasible with Infinity plugin pre-installed.

**Core:** Grafana login → provisioned Infinity → `GET /api/sales` (region **3** + Completed + Q1 2023, `page`/`page_size`, root **`data`**) → one OData panel (root **`value`**) → `/api/sales/by-region` → save dashboard. Optional: `lab-s09-rest-odata` verify.

**Stretch:** empty-region drills, OData pagination, `/cmf/plants`.

Seed: Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**. Training API has **no auth**. Do not use REST `top`/`skip`.

## Files

Diagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.


* `README.md` — Session overview
* `notes.md` — Concepts and technical notes
* `lab.md` — Guided hands-on lab
* `assets/` — Supporting files, if required
