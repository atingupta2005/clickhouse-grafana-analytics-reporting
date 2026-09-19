# Session 3 — Advanced ClickHouse SQL

## Session Overview

<!-- training-diagrams:v1 -->
![Joins build a reporting row](./assets/join-to-report.svg)


This session extends the reporting queries from the previous session.

The focus is on combining data from multiple tables and performing more advanced analytical calculations.

## Topics

* `INNER JOIN`
* `LEFT JOIN`
* Join considerations
* CTEs
* Subqueries
* Window functions
* Ranking
* Running totals
* Period calculations
* Conditional aggregation
* Arrays
* Selected analytical functions

## Practical Work

Participants will build queries for:

* Combining orders with customers, products and plants
* Regional and product-level reports
* Customer and product analysis
* Ranking products and customers
* Running sales totals
* Period-based calculations
* Conditional KPIs
* Reports using CTEs and subqueries

The exercises continue to use the manufacturing and sales data in the `training` database.

**Reporting view:** for sales, quantity, and region columns, always query **`training.v_lab_orders`** (not the base `training.orders` table — that table is normalized and does not expose those reporting columns).

## Files

Diagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.


| File           | Purpose                            |
| -------------- | ---------------------------------- |
| `README.md`    | Session overview                   |
| `notes.md`     | Advanced SQL concepts and examples |
| `lab.md`       | Guided hands-on lab                |
| `assets/`      | Supporting files, if required      |
