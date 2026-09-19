# Session 10 — Grafana Variables and Dynamic Queries

## Session Overview

This session makes dashboards interactive. Students define Grafana variables, cascade them (region → plant), and use them in ClickHouse SQL and Infinity REST/OData URLs.

```text
Dashboard variables
        |
        v
  Panel query (CH / API)
        |
        v
  Filtered panel result
```

## Topics

* Grafana variables
* Query variables
* Custom variables
* Multi-value and All option
* Variable formatting
* Dynamic filtering
* Dependencies and cascading
* Time variables
* Variables in ClickHouse SQL
* Variables in REST/OData (Infinity)
* Dynamic query construction
* Defaults

## Practical Work

Participants will:

* Open Grafana (`student` / `StudentLab!2026`)
* Use provisioned **ClickHouse** and **Infinity** data sources (do not recreate)
* Create dashboard **Session 10 - Variables Lab**
* Add filters: Region, Plant, Product, Category, Customer, Status, date/time
* Wire variables into Stat + Table panels (optional time series)
* Confirm cascading plant list and multi-value `IN (...)` patterns
* Optionally drive one Infinity REST or OData panel from the same variables

## Timing (PAX ~2×)

TOC: **4 hours**.

**Core:** login → absolute time **2023-01-01→2025-06-18** → variables (Region query, Status custom default Completed, Plant cascading, multi-value + All) → 2–3 ClickHouse panels on `training.v_lab_orders` → save dashboard → prove Region 2 + Completed is empty.

**Stretch:** Category → Product cascade, Customer variable, Infinity REST/OData with variables, `${__from}` / `${__to}` in API dates, polish.

Seed: Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**. REST uses `page` / `page_size` and `region_id` — not `top`/`skip`. OData: `$filter` with `Status` / `RegionId`; **no `$expand`** on the lab API (stretch note only).

## Files

| File | Purpose |
| ---- | ------- |
| `README.md` | Session overview |
| `notes.md` | Concepts and patterns |
| `lab.md` | Guided variables lab |
| `assets/` | Supporting files, if required |
