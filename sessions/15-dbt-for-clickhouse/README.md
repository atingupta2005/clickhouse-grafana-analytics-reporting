# Session 15 — dbt for ClickHouse

**Duration:** 3 hours

## Overview

See how dbt structures analytics transformations for ClickHouse (sources → models → test concepts), using the existing `training_dbt` project.

![dbt workflow](./assets/dbt-workflow.svg)

## Topics

* dbt project layout, `profiles.yml`, sources, models
* Where transforms belong (dbt vs app vs API vs Grafana)
* Tests and docs (concepts; this project has no test YAML yet)

## Hands-on

* Walk through the course dbt project (sources + `mart_sales_by_region`)
* Trace source `training.*` → model schema `training_dbt`

**Core:** project walkthrough (no server login required) 

**Stretch:** optional `dbt run` / `dbt test` if shown in class

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
