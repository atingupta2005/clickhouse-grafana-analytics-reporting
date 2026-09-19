# Session 4 — SQL Server to ClickHouse Migration

**Duration:** 4 hours

## Overview

Rewrite common SQL Server reporting patterns for ClickHouse and compare results on both engines.

![SQL Server to ClickHouse migration](./assets/migration-pipeline.svg)

## Connect

| Item | Value |
|------|--------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| ClickHouse | **Session 01–05 — ClickHouse training (LAN RO)** / `training_ro` |
| SQL Server | Lab SQL Server connection (as provided in class) |

Compare **logic and shape**, not identical row counts (SQL Server sample is smaller than the ClickHouse seed).

## Topics

* `TOP` → `LIMIT`, `ISNULL` → `COALESCE`, `CASE`, dates, aggregates
* Dialect differences that affect reporting SQL

## What you will do

**Core:** rewrite and run TOP→LIMIT, ISNULL/COALESCE, CASE, one date pattern, one aggregate on both engines  

**Stretch:** window functions, fuller migration set

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
