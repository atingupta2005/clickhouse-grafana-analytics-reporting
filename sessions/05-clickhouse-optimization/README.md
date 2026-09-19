# Session 5 — ClickHouse Query Optimization

**Duration:** 4 hours

## Connect

| Item | Value |
|------|--------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| Connection | **ClickHouse training** |
| User | `training_ro` |

## Overview

Improve analytical query performance using sort keys, partitions, skipping indexes, filters, and `EXPLAIN`.

![Optimization loop](./assets/optimize-loop.svg)

**Live sort key** (confirm with `SHOW CREATE TABLE training.orders`):

```text
ORDER BY (order_date, plant_id, order_id)
```

## Topics

* Sort keys, partitions, data skipping
* Filter/aggregate/join habits
* `EXPLAIN` and basic profiling

## Hands-on

**Core:** compare filter alignment to the sort key → `EXPLAIN` → rewrite one slow pattern 

**Stretch:** deeper `system.query_log` / skipping demos

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| Sort keys and partitions | [ch-grafana-s05-sortkey-partition](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s05-sortkey-partition) |
| Skipping, filters, aggregation | [ch-grafana-s05-skipping-filters](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s05-skipping-filters) |
| EXPLAIN and profiling | [ch-grafana-s05-explain-profile](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s05-explain-profile) |
| Bottlenecks lab checkpoint | [ch-grafana-s05-bottlenecks-lab](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s05-bottlenecks-lab) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
