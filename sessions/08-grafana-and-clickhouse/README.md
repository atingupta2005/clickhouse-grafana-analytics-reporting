# Session 8 — Grafana Fundamentals and ClickHouse Integration

## Session Overview

<!-- training-diagrams:v1 -->
![ClickHouse to Grafana panel](./assets/grafana-ch-flow.svg)


This session introduces Grafana for analytics and reporting and connects Grafana to ClickHouse.

The focus is on the Grafana interface, data sources, ClickHouse connectivity, SQL queries, time ranges, refresh, Explore, panels, and basic dashboards.

## Topics

* Grafana overview
* Grafana interface
* Dashboards
* Panels
* Data sources
* ClickHouse data source
* Connection and authentication
* ClickHouse SQL in Grafana
* Query editor
* Time ranges
* Dashboard refresh
* Explore
* Basic dashboard creation

## Practical Work

Participants will:

* Use the **provisioned** ClickHouse data source (do not add a new one).
* Confirm ClickHouse connectivity
* Execute ClickHouse queries
* Use the query editor
* Set absolute time range **2023-01-01** → **2025-06-18**
* Use Explore
* Create basic panels
* Build a simple reporting dashboard
* Optionally open the lab verify dashboard `lab-s08-clickhouse-kpis`

## Reporting Flow

```text
ClickHouse
     |
     v
Grafana Data Source
     |
     v
ClickHouse SQL
     |
     v
Panel
     |
     v
Dashboard
```

## Timing (PAX ~2×)

TOC: **4 hours**. Borderline feasible if Grafana + ClickHouse datasource are pre-provisioned.

**Core:** open Grafana (`student` / `StudentLab!2026`), confirm provisioned ClickHouse DS, absolute time **2023-01-01→2025-06-18**, 3 panels on `training.v_lab_orders` (KPI / trend / by region for Completed regions **1/3/5**), save one dashboard. Optional: open verify dashboard `/grafana/d/lab-s08-clickhouse-kpis/...`.

**Stretch:** extra visualizations, Completed vs all comparison exercises.

Use Q1 **2023** and Completed regions **1 / 3 / 5**. Seed dates **2023-01-01** … **2025-06-18**.

## Files

Diagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.


| File           | Purpose                         |
| -------------- | ------------------------------- |
| `README.md`    | Session overview                |
| `notes.md`     | Grafana and ClickHouse concepts |
| `lab.md`       | Guided Grafana integration lab  |
| `assets/`      | Supporting files, if required   |
