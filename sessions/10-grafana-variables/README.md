# Session 10 — Grafana Variables and Dynamic Queries

**Duration:** 4 hours

## Overview

Make dashboards interactive with Grafana variables (including region → plant cascade) in ClickHouse SQL and Infinity URLs.

![Variables drive the panel query](./assets/variable-to-panel.svg)

## Topics

* Query, custom, and multi-value variables
* Cascading variables
* Variables in ClickHouse SQL and REST/OData

## Hands-on

* Sign in (`student` / `StudentLab!2026`)
* Use the **ClickHouse** and **Infinity** data sources
* Create `Session 10 - Variables Lab`
* Wire Region, Plant, Status (and related filters) into panels
* Confirm multi-value `IN (...)` patterns and Region 2 + Completed empty

**Core:** absolute time → variables → 2–3 ClickHouse panels on `training.v_lab_orders` → save → empty demo 

**Stretch:** Category → Product, Customer, Infinity with variables, time macros

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| Why variables | [ch-grafana-s10-why-variables](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s10-why-variables) |
| Multi-value and formatting | [ch-grafana-s10-multivalue-format](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s10-multivalue-format) |
| Cascading and time variables | [ch-grafana-s10-cascade-time](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s10-cascade-time) |
| Variables lab checkpoint | [ch-grafana-s10-lab-defaults](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s10-lab-defaults) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
