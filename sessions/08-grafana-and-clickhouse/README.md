# Session 8 — Grafana Fundamentals and ClickHouse Integration

**Duration:** 4 hours

## Overview

Introduce Grafana and connect it to ClickHouse for basic reporting panels and a simple dashboard.

![ClickHouse to Grafana panel](./assets/grafana-ch-flow.svg)

## Topics

* Grafana UI, dashboards, panels, Explore
* ClickHouse data source
* SQL in Grafana, time ranges, refresh

## Hands-on

* Sign in (`student` / `StudentLab!2026`)
* Use the **ClickHouse** data source
* Absolute time **2023-01-01** → **2025-06-18**
* Build KPI / trend / by-region panels on `training.v_lab_orders`
* Save one dashboard

**Core:** login → ClickHouse DS → absolute time → 3 panels (Completed, regions **1/3/5**) → save 

**Stretch:** extra visualizations, Completed vs all comparison

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| Grafana UI and data sources | [ch-grafana-s08-grafana-basics](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s08-grafana-basics) |
| ClickHouse queries and time ranges | [ch-grafana-s08-ch-query-time](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s08-ch-query-time) |
| Panels and KPIs | [ch-grafana-s08-panels-kpi](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s08-panels-kpi) |
| Dashboard refresh | [ch-grafana-s08-dashboard-refresh](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s08-dashboard-refresh) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
