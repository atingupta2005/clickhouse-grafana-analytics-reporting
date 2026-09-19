# Session 15 — dbt for ClickHouse

## Session Overview

<!-- training-diagrams:v1 -->
![dbt workflow](./assets/dbt-workflow.svg)


This session introduces **dbt (data build tool)** as an analytics engineering workflow for transforming and testing data in ClickHouse.

The session uses the existing `training_dbt` project to show how dbt projects are structured, how ClickHouse source tables are declared, how SQL models are created, and how transformations can be managed outside application code.

## Topics

- Introduction to dbt and analytics engineering
- dbt project structure
- dbt with ClickHouse
- Sources and source definitions
- dbt models and SQL transformations
- `dbt_project.yml` and `profiles.yml`
- Basic dbt tests
- dbt documentation
- dbt workflow: source → model → test → validate
- Where transformations can be performed
- dbt vs application-layer transformation
- dbt vs REST/OData/Grafana transformations

## Practical Work

### Core

Guided walkthrough of the existing dbt project:

- Review the `stacks/app/dbt/` project
- Identify the `training_dbt` project and profile
- Review the configured ClickHouse connection
- Review source definitions for:
  - `training.orders`
  - `training.order_items`
  - `training.plants`
  - `training.regions`
- Review `models/mart_sales_by_region.sql`
- Trace how source data is transformed into a reporting model
- Understand how the model would be written to the `training_dbt` schema
- Review the basic test and documentation approach

### Stretch

**Stretch (optional):** If the dbt profile is available, run the existing project from the `lab-dbt` container and validate the resulting model in ClickHouse.

- Run `dbt run`
- Run `dbt test`
- Validate the resulting model in `training_dbt`

Students do not need SSH access to the App VM for the Core path.

## Timing

| Activity | Approx. Time |
|---|---:|
| dbt concepts and analytics engineering | 25 min |
| Project structure and configuration walkthrough | 20 min |
| Sources and models walkthrough | 25 min |
| dbt workflow, tests and documentation | 15 min |
| Transformation architecture discussion | 10 min |
| **Core guided path** | **~95 min** |
| Stretch (optional): `dbt run` / `dbt test` | Optional |

The Core path is designed to fit within the 3-hour session while allowing time for questions and discussion.

## Lab and Environment Reminders

- Existing project: `stacks/app/dbt/`
- dbt project / profile: `training_dbt`
- Target schema: `training_dbt`
- Sources file: `models/sources.yml` (not project-root `sources.yml`)
- Existing example model: `models/mart_sales_by_region.sql`
- dbt container: `lab-dbt` · Compose profile: `dbt`
- Source data remains in `training`; models write to `training_dbt`
- This project currently has **no** dbt test YAML — teach test concepts; Stretch `dbt test` may be a no-op
- Students do not need App VM SSH for Core
- Do not invent Snowflake/BigQuery targets

## Files

Diagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.


- `README.md` — Session overview and timing
- `notes.md` — dbt and ClickHouse teaching notes
- `lab.md` — Guided Core walkthrough and optional Stretch
