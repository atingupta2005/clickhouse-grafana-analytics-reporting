# Session 13 — End-to-End Reporting Dashboard Workshop

**Duration:** 4 hours

## Overview

Build one complete reporting dashboard: requirements → KPIs → queries → variables → panels → validation.

![Workshop pipeline](./assets/workshop-pipeline.svg)

Dashboard name: **`Session 13 - Reporting Workshop`**

## Topics

* KPI design from reporting requirements
* ClickHouse queries on `training.v_lab_orders`
* Variables, panels, filtering, validation

## Hands-on

* Sign in (`student` / `StudentLab!2026`)
* Use the **ClickHouse** data source
* Absolute time **2023-01-01** → **2025-06-18**
* Build Core KPIs (orders, revenue, high-value lines) plus region/plant views
* Filters: Region, Plant, Status (default Completed)

**Core:** compact dashboard with the panels above + variables 

**Stretch:** Infinity panel, extra drill-down, more transformations, `/cmf/plants`

**Seed:** Completed regions **1 / 3 / 5**; Region 2 + Completed empty; `sales_amount >= 2000` for high-value lines

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| Workshop goals | [ch-grafana-s13-workshop-plan](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s13-workshop-plan) |
| KPI build | [ch-grafana-s13-kpi-build](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s13-kpi-build) |
| Filters and layout | [ch-grafana-s13-filters-layout](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s13-filters-layout) |
| Validation wrap | [ch-grafana-s13-validate-wrap](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s13-validate-wrap) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided workshop |
| `assets/` | Diagrams |
