# Session 2 — ClickHouse SQL for Analytics and Reporting

## Connect (do this first)

| Item | Value |
|------|--------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| Connection | **Session 01–05 — ClickHouse training (LAN RO)** |
| User | `training_ro` (read-only) |

Open CloudBeaver, pick that connection, and run `SELECT version();` to confirm you are in.

**Tip:** Use the path `/cloudbeaver/` (not site-root `/#/` alone). If the navigator is empty, hard-refresh the browser.

## Session Overview

<!-- training-diagrams:v1 -->
![ClickHouse SELECT clause order](./assets/sql-clause-pipeline.svg)


This session focuses on the SQL used for common analytical and reporting requirements in ClickHouse.

The examples use the manufacturing and sales data created in Session 1.

## Topics

* `SELECT`
* `WHERE`
* `ORDER BY`
* `LIMIT`
* `DISTINCT`
* Aggregate functions
* `GROUP BY`
* `HAVING`
* String functions
* Date and time functions
* Conditional expressions
* `NULL` handling
* KPI calculations
* Daily reporting
* Monthly reporting

## Practical Work

Participants will create analytical queries for:

* Sales by region
* Sales by plant
* Sales by product
* Order counts
* Total quantities
* Total sales
* Daily sales trends
* Monthly sales trends
* High-value orders
* Conditional KPIs

Labs use `training.v_lab_orders` (lab reporting view).

## Files

Diagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.


| File           | Purpose                            |
| -------------- | ---------------------------------- |
| `README.md`    | Session overview                   |
| `notes.md`     | ClickHouse SQL theory and examples |
| `lab.md`       | Guided SQL lab                     |
| `assets/`      | Supporting files, if required      |
