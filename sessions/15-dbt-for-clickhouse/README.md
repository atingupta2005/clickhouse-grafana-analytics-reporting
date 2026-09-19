# Session 15 — dbt for ClickHouse

**Duration:** 3 hours

## Overview

See how dbt structures analytics transformations for ClickHouse (sources → models → test concepts), using the existing `training_dbt` project.

![dbt workflow](./assets/dbt-workflow.svg)

## Topics

* dbt project layout, `profiles.yml`, sources, models
* Where transforms belong (dbt vs app vs API vs Grafana)
* Tests and docs (concepts; this project has no test YAML yet)

## What you will do

* Walk through `stacks/app/dbt/` (sources + `mart_sales_by_region`)
* Trace source `training.*` → model schema `training_dbt`

**Core:** project walkthrough (no App VM SSH required)  

**Stretch:** shared demo of `dbt run` / `dbt test` when the `dbt` profile is available

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
