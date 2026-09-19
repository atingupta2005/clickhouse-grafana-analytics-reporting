# Session 7 — OData

**Duration:** 4 hours

## Overview

Query the training OData service with `$filter`, `$select`, `$orderby`, `$top`, and `$skip`, and inspect JSON under `value`.

![OData query options](./assets/odata-options.svg)

## Topics

* OData vs REST
* `$filter` / `$select` / `$orderby` / `$top` / `$skip` / `$count`
* Unsupported lab features (`$expand`, `$search`, key URLs) — theory only

## Hands-on

* Open `/odata/Orders` in the browser
* Build filtered and projected queries
* Confirm responses use the `value` array

**Core:** basic Orders query → `$filter` Completed → `$select` / `$orderby` / `$top` 

**Stretch:** `$skip` pagination, unsupported-feature checks

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**


## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
