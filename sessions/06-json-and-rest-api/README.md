# Session 6 — JSON and REST API Data

## Session Overview

<!-- training-diagrams:v1 -->
![REST JSON into a report shape](./assets/rest-json-report.svg)


This session introduces JSON data and REST APIs as data sources for analytics and reporting.

The focus is on understanding JSON structures, extracting useful fields, consuming REST APIs, handling parameters and responses, and preparing API data for reporting.

## Topics

* JSON objects and arrays
* Nested JSON structures
* Field extraction
* JSON functions
* Missing values and `NULL`
* JSON transformation and flattening
* REST API fundamentals
* HTTP methods
* Headers
* Query parameters
* Authentication concepts
* HTTP status codes
* Request and response structure
* JSON API responses
* Pagination
* Error handling

## Practical Work

Participants will:

* Call a REST API
* Work with query parameters
* Inspect JSON responses
* Extract fields from JSON
* Work with nested objects and arrays
* Handle missing values
* Process paginated responses
* Transform API data into a reporting-friendly structure
* Handle common API errors

## Data Flow

```text
REST API
   |
   v
JSON Response
   |
   v
Inspect Structure
   |
   v
Extract / Transform
   |
   v
Reporting Data
```

## Timing (PAX ~2×)

TOC: **4 hours**. Do **not** attempt the full lab + all exercises in class.

**Core (must finish):** call `/api`, inspect `{data,count}` envelope, filter `/api/orders` / `/api/sales` by `region_id` / `status=Completed` / Q1 **2023** (`date_from`/`date_to` or `from_date`/`to_date`), one `page`/`page_size` example, one inline JSON `SELECT` (no CREATE).

**Stretch / homework:** nested-JSON theory, error drills, final reporting challenge.

Seed facts: Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**. Live `/api/orders` is **flat** (no nested customer/plant, no `product_id`). Training API has **no auth**. Students are **`training_ro`** (no CREATE/INSERT).

## Files

Diagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.


| File           | Purpose                       |
| -------------- | ----------------------------- |
| `README.md`    | Session overview              |
| `notes.md`     | JSON and REST API concepts    |
| `lab.md`       | Guided API and JSON lab       |
| `assets/`      | Supporting files, if required |
