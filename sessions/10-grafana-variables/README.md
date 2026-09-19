# Session 10 — Grafana Variables and Dynamic Queries

**Duration:** 4 hours

## Overview

Make dashboards interactive with Grafana variables (including region → plant cascade) in ClickHouse SQL and Infinity URLs.

![Variables drive the panel query](./assets/variable-to-panel.svg)

## Topics

* Query, custom, and multi-value variables
* Cascading variables
* Variables in ClickHouse SQL and REST/OData

## What you will do

* Sign in (`student` / `StudentLab!2026`)
* Use provisioned ClickHouse and Infinity data sources
* Create `Session 10 - Variables Lab`
* Wire Region, Plant, Status (and related filters) into panels
* Confirm multi-value `IN (...)` patterns and Region 2 + Completed empty

**Core:** absolute time → variables → 2–3 ClickHouse panels on `training.v_lab_orders` → save → empty demo 

**Stretch:** Category → Product, Customer, Infinity with variables, time macros

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
