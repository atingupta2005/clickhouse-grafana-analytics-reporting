# Session 2 — ClickHouse SQL for Analytics and Reporting

**Duration:** 4 hours

## Connect

| Item | Value |
|------|--------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| Connection | **ClickHouse training** |
| User | `training_ro` |

**Tip:** Use `/cloudbeaver/` (not site-root `/#/` alone).

## Overview

Analytical SQL on `training.v_lab_orders`: filters, aggregates, dates, and KPI-style queries.

![ClickHouse SELECT clause order](./assets/sql-clause-pipeline.svg)

## Topics

* `SELECT` / `WHERE` / `ORDER BY` / `LIMIT` / `GROUP BY` / `HAVING`
* Aggregates, strings, dates, `CASE`, `NULL` handling

## Hands-on

**Core:** explore the view → filter Completed + regions **1/3/5** → aggregates and simple KPIs 

**Stretch:** extra date/string patterns

**Seed:** dates **2023-01-01** … **2025-06-18**

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| SELECT, WHERE, ORDER BY, LIMIT | [ch-grafana-s02-select-filter](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s02-select-filter) |
| Aggregates and GROUP BY | [ch-grafana-s02-groupby-agg](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s02-groupby-agg) |
| Strings, dates, conditionals | [ch-grafana-s02-strings-dates](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s02-strings-dates) |
| KPI and period reporting | [ch-grafana-s02-kpi-reporting](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s02-kpi-reporting) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
