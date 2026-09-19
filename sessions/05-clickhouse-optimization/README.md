# Session 5 — ClickHouse Query Optimization

## Connect (do this first)

| Item | Value |
|------|--------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| Connection | **Session 01–05 — ClickHouse training (LAN RO)** |
| User | `training_ro` / `TrainingReadOnly!2026` |
| Tailscale fallback | `100.86.105.24:8123` |

## Session Overview

This session focuses on identifying and improving slow ClickHouse queries.

The emphasis is on understanding how query execution, table design, sorting keys, partitioning, data types, filtering, aggregation, and joins affect analytical query performance.

**Live sort key** (confirm with `SHOW CREATE TABLE training.orders`):

```text
ORDER BY (order_date, plant_id, order_id)
```

Date- and plant-aligned filters benefit most. Region filters still work, but `region_id` is **not** leading in the sort key.

## Topics

* ClickHouse query execution
* Sorting keys and query performance
* Partitioning
* Data skipping
* Data types and storage
* Filtering and aggregation
* JOIN performance
* `EXPLAIN`
* Query profiling
* `system.query_log`
* Identifying bottlenecks
* Query rewriting
* Table design considerations

## Practical Work

Participants will:

* Run representative analytical queries
* Establish a baseline
* Inspect query execution
* Use `EXPLAIN`
* Review query statistics
* Identify performance bottlenecks
* Rewrite inefficient queries
* Compare before-and-after results
* Review table design choices

## Optimization Flow

<!-- training-diagrams:v1 -->
![Optimization loop](./assets/optimize-loop.svg)


```text
Query
  |
  v
Measure Baseline
  |
  v
Inspect Execution
  |
  v
Identify Bottleneck
  |
  v
Rewrite / Adjust Design
  |
  v
Run Again
  |
  v
Compare Results
```

## Files

Diagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.


| File           | Purpose                            |
| -------------- | ---------------------------------- |
| `README.md`    | Session overview                   |
| `notes.md`     | Query optimization concepts        |
| `lab.md`       | Guided optimization lab            |
| `assets/`      | Supporting files, if required      |
