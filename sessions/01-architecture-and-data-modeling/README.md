# Session 1 — ClickHouse Architecture and Data Modeling

**Duration:** 4 hours

## Connect

| Item | Value |
|------|--------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| Connection | **ClickHouse training** |
| User | `training_ro` |

Open CloudBeaver, select that connection, and run `SELECT version();`.

For CREATE practice (when provided in class), use database `training_student_<yourname>`.

## Overview

How ClickHouse stores and queries analytical data, and how to explore the lab model.

![Explore vs sandbox paths](./assets/explore-vs-sandbox.svg)

| Path | What you do |
|------|-------------|
| **Explore** | `SHOW` / `DESCRIBE` on `training.*`, analytics on `training.v_lab_orders` |
| **Sandbox** | Create tables in `training_student_<yourname>` |

## Topics

* OLTP vs OLAP, columnar storage, MergeTree
* `ORDER BY`, `PARTITION BY`, basic types
* Shards/replicas (overview)

## Hands-on

**Core:** explore lab tables/views → simple analytics on `training.v_lab_orders`

**Stretch:** sandbox DDL when the write login is available

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| OLTP vs OLAP | [ch-grafana-s01-oltp-olap](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s01-oltp-olap) |
| Columnar storage and architecture | [ch-grafana-s01-columnar-architecture](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s01-columnar-architecture) |
| MergeTree and ORDER BY | [ch-grafana-s01-mergetree-orderby](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s01-mergetree-orderby) |
| Partitioning and data types | [ch-grafana-s01-partition-types](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s01-partition-types) |
| Modeling checkpoint | [ch-grafana-s01-lab-modeling](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s01-lab-modeling) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
