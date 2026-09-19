# Session 13 — End-to-End Reporting Dashboard Workshop

## Overview

This session is a practical workshop for building one complete reporting dashboard in Grafana.

Students move through the reporting workflow:

**Requirements → KPIs → ClickHouse queries → Grafana variables → Panels → Filtering → Validation**

The workshop uses `training.v_lab_orders` reporting view and the provisioned Grafana **ClickHouse** datasource.

## Workshop Brief

Build:

**`Session 13 - Reporting Workshop`**

Report focus:

- Completed sales by region and plant
- Q1 2023 analysis
- Full seed-range overview where required
- Order count
- Revenue
- High-value lines (`sales_amount >= 2000`)

### Required Filters

- **Region**
- **Plant**
- **Status**
  - Default: `Completed`

Completed data is available for regions **1, 3, and 5**. Region **2 + Completed** intentionally returns no rows.

## Core Topics

- Translate reporting requirements into measurable KPIs
- Use `training.v_lab_orders` for reporting queries
- Write ClickHouse queries for dashboard panels
- Create Grafana variables
- Apply variables to panels
- Build KPI and analytical panels
- Use Grafana transformations where useful
- Configure an absolute dashboard time range
- Add dashboard filtering and navigation
- Validate dashboard results against the lab data
- Consider query performance and dashboard usability

## Dashboard Scope

### Core

Build a compact dashboard containing:

1. KPI — distinct Completed orders
2. KPI — Completed revenue
3. KPI — high-value lines
4. Sales by region
5. Sales/order analysis by plant or another useful reporting view
6. Region, plant, and status variables
7. Absolute time range:
   - `2023-01-01` → `2025-06-18`

The Core dashboard should remain small enough to complete during the guided workshop.

### Stretch

Optional extensions:

- One REST or OData panel using the provisioned **Infinity** datasource
- Additional KPI or analytical panel
- Drill-down/navigation between dashboard views
- Additional transformations
- Further query-performance refinement
- Optional CMF plants endpoint:
  - `https://vmclickhouse.canadacentral.cloudapp.azure.com/cmf/plants`

CMF is Stretch only.

## Expected Seed Checks

Use the lab data for validation:

| Check | Expected |
|---|---:|
| Completed rows in `training.v_lab_orders` | ≈ 300,000 |
| Completed distinct orders | ≈ 125,000 |
| Completed regions | 1, 3, 5 |
| Region 2 + Completed | Empty |
| Order-date range | 2023-01-01 → 2025-06-18 |
| High-value line threshold | `sales_amount >= 2000` |

Small differences may occur where a panel applies additional filters or a different time period.

## Timing

| Activity | Target |
|---|---:|
| Reporting requirements and KPI design | 20 min |
| Query and panel design | 25 min |
| Guided dashboard build | 80–90 min |
| Validation and usability review | 20–25 min |
| Stretch | Remaining time |

The Core guided work is designed for approximately **2–2.5 hours** of hands-on activity within the 4-hour session.

## Lab Access

### Grafana

`https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/`

Student login:

- Username: `student`
- Password: `StudentLab!2026`

Use the provisioned **ClickHouse** datasource. Do not recreate the datasource.

### CloudBeaver

`https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/`

### REST API

`https://vmclickhouse.canadacentral.cloudapp.azure.com/api`

### OData

`https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/`

## Seed and Query Reminders

- Primary reporting view: `training.v_lab_orders`
- Status used in reporting: `Completed`
- Stored source status may differ; use the reporting view's `Status`
- Completed regions: `1`, `3`, `5`
- Region `2` with `Completed` is intentionally empty
- Do not use `Last 30 days` as the primary dashboard range
- Use the absolute seed range `2023-01-01` → `2025-06-18`
- Use ClickHouse variable syntax: `region_id IN (${region})`, `plant_id IN (${plant})`, `status IN (${status:sqlstring})`
- Prefer cascading Plant on Region (`WHERE region_id IN (${region})`) as in Session 10
- REST/OData variable syntax is different and must not be copied from ClickHouse examples

## Files

| File | Purpose |
|---|---|
| `README.md` | Workshop overview, scope, timing, and reminders |
| `notes.md` | Teaching notes and reporting/dashboard concepts |
| `lab.md` | Guided Core dashboard build |

## Core / Stretch Rule

**Core** activities must work with the lab environment and be completed during the session.

**Stretch** activities extend the dashboard but are not required for Core completion.

Do not require unsupported OData features such as `$expand`, `$search`, or key URL syntax.
