# Session 4 — SQL Server to ClickHouse Query Migration

## Session Overview

This session focuses on migrating reporting queries from SQL Server to ClickHouse.

The focus is on understanding common SQL differences, identifying incompatible syntax, rewriting queries, and validating the results.

## Topics

* SQL Server and ClickHouse SQL differences
* Data type mapping
* `TOP` and `LIMIT`
* `ISNULL` and `COALESCE`
* `CAST` and `CONVERT`
* `CASE`
* Date and time functions
* String functions
* `JOIN`
* CTEs
* Subqueries
* Window functions
* `NULL` handling
* Common migration issues
* Query validation

## Practical Work

Participants will work with representative SQL Server reporting queries and:

* Identify SQL Server-specific syntax
* Map SQL Server data types to ClickHouse types
* Replace incompatible functions
* Rewrite date and string expressions
* Convert `TOP` queries to ClickHouse
* Review joins, CTEs and subqueries
* Handle `NULL` values
* Rewrite window-function queries
* Compare SQL Server and ClickHouse results
* Identify common migration problems

## Lab connections

| System | Connection |
|--------|------------|
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| SQL Server | Connection **Session 04 — SQL Server TrainingDB** · host `192.168.29.4:1433` (Tailscale fallback `100.86.105.24:1433`) · DB `TrainingDB` · `sa` / `SqlServerLab!2026` |
| ClickHouse | Connection **Session 01–05 — ClickHouse training (LAN RO)** · host `192.168.29.4:8123` (Tailscale fallback `100.86.105.24:8123`) · DB `training` · view `training.v_lab_orders` · `training_ro` / `TrainingReadOnly!2026` |

Open CloudBeaver at `/cloudbeaver/`. If the LAN connection fails, use **ClickHouse training (Tailscale fallback RO)** or create a connection to `100.86.105.24`.

SQL Server holds a compact sample; ClickHouse holds the full seed. Compare **logic and shape**, not identical row counts, unless the instructor provides a matched extract.

**Expected result:** SQL Server row counts are **much smaller** than ClickHouse. That is normal — do not treat mismatched totals as a failed migration.

## Timing (PAX ~2×)

TOC: **4 hours**.

**Core:** TOP→LIMIT, ISNULL/COALESCE, CASE, one date rewrite, one aggregate — run each on both engines.

**Stretch:** windows, full exercise migration set.

## Migration Approach

The session follows a simple migration process:

```text
SQL Server Query
       |
       v
Identify SQL Server-specific syntax
       |
       v
Map data types and functions
       |
       v
Rewrite for ClickHouse
       |
       v
Run Query
       |
       v
Validate Result
```

## Files

| File           | Purpose                         |
| -------------- | ------------------------------- |
| `README.md`    | Session overview                |
| `notes.md`     | Migration concepts and examples |
| `lab.md`       | Guided migration lab            |
| `assets/`      | Supporting files, if required   |
