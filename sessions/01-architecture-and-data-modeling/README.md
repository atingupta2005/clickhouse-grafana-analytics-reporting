# Session 1 — ClickHouse Architecture and Data Modeling

**Duration:** 4 hours

## Connect

| Item | Value |
|------|--------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| Connection | **Session 01–05 — ClickHouse training (LAN RO)** |
| User | `training_ro` (read-only) |

Open CloudBeaver, pick that connection, and run `SELECT version();`.

> **DDL:** default path is read-only. Sandbox DDL uses `training_rw` and `training_student_<yourname>` when write access is provided. Never DROP `training`.

## Overview

How ClickHouse stores and queries analytical data, and how to explore the lab model (or build a small sandbox).

![Explore vs sandbox paths](./assets/explore-vs-sandbox.svg)

| Path | What you do |
|------|-------------|
| **Explore** | `SHOW` / `DESCRIBE` on `training.*`, analytics on `training.v_lab_orders` |
| **Sandbox** | Create tables only in `training_student_<yourname>` |

## Topics

* OLTP vs OLAP, columnar storage, MergeTree
* `ORDER BY`, `PARTITION BY`, basic types
* Shards/replicas (overview)

## What you will do

**Core:** explore lab tables/views → simple analytics on `training.v_lab_orders`  

**Stretch:** sandbox DDL if you have write access

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
