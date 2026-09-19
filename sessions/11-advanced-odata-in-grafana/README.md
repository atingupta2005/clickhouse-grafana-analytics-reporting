# Session 11 — Advanced OData Querying in Grafana

**Duration:** 3 hours

## Overview

Use Grafana variables to build dynamic OData queries in Infinity (`$filter`, `$select`, `$orderby`, `$top`, `$skip`).

![Build a dynamic OData URL](./assets/odata-url-build.svg)

Builds on Sessions 07, 09, and 10.

## Topics

* Variables in `$filter` (AND / OR, dates, multi-value)
* Dynamic `$select` and `$orderby`
* `$top` / `$skip` pagination
* Empty results (Region 2 + Completed)
* Troubleshooting Infinity/OData panels
* `$expand` / `$search` / key URLs — theory only (not supported on the lab OData service)

## Hands-on

* Sign in (`student` / `StudentLab!2026`)
* Use **Infinity**; root selector **`value`**
* Absolute time **2023-01-01** → **2025-06-18**
* Build dashboard `Session 11 - Advanced OData Lab`

**Core:** variables → `$filter` → Region 2 empty demo → date filter → `$select` / `$orderby` / `$top` / `$skip` → table panel 

**Stretch:** multi-value `or` chains, dynamic select/order/skip, optional `/cmf/plants`

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| OData setup and variables | [ch-grafana-s11-setup-vars](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s11-setup-vars) |
| Multi-value OData filters | [ch-grafana-s11-multifilter](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s11-multifilter) |
| Dates, $select, $orderby | [ch-grafana-s11-dates-select](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s11-dates-select) |
| Advanced OData lab checkpoint | [ch-grafana-s11-lab-checkpoint](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s11-lab-checkpoint) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
