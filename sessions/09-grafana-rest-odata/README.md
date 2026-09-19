# Session 9 — Grafana and REST/OData Integration

**Duration:** 4 hours

## Overview

Connect Grafana to the training REST and OData APIs with the **Infinity** data source, and build API-based panels.

![API data into Grafana Infinity](./assets/infinity-architecture.svg)

## Topics

* Infinity data source (REST and OData)
* Full HTTPS URLs, JSON parser, root selectors (`data` / `value`)
* Query parameters, filters, dates, pagination
* Empty results vs errors
* Basic troubleshooting

## Hands-on

* Sign in to Grafana (`student` / `StudentLab!2026`)
* Use the **Infinity** data source
* Build REST panels on `/api/sales` (root **`data`**)
* Build an OData panel on `/odata/Orders` (root **`value`**)
* Add a regional panel (`/api/sales/by-region` or ClickHouse)
* Save the dashboard

**Core:** login → Infinity → REST sales (region 3 + Completed + dates) → one OData panel → regional panel → save 

**Stretch:** empty-region checks, OData pagination, `/cmf/plants`

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**; training API has no auth

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| API-based reporting | [ch-grafana-s09-api-reporting](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s09-api-reporting) |
| Requests, headers, parameters | [ch-grafana-s09-request-shape](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s09-request-shape) |
| JSON roots: data vs value | [ch-grafana-s09-json-roots](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s09-json-roots) |
| Infinity lab checkpoint | [ch-grafana-s09-infinity-lab](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s09-infinity-lab) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
