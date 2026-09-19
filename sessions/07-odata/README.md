# Session 7 — OData Fundamentals and Querying

## Session Overview

<!-- training-diagrams:v1 -->
![OData query pipeline](./assets/odata-pipeline.svg)


This session introduces OData as a standard way to query application data over HTTP.

The focus is on understanding OData services, entities, metadata, query options, filtering, sorting, pagination, relationships, and JSON responses.

## Topics

* OData concepts
* OData vs REST
* OData service structure
* Entities and entity sets
* Properties
* Relationships
* Metadata
* `$filter`
* `$select`
* `$orderby`
* `$top`
* `$skip`
* `$expand` (stretch theory — **not** supported by this lab service)
* `$count` (`?$count=true` and mention `/$count`)
* `$search` (stretch theory — **not** supported by this lab service)
* String, numeric, and date-time filters
* `AND` / `OR`
* Pagination
* Related entities
* Nested and expanded data
* URL encoding
* JSON response handling

## Practical Work

Participants will:

* Explore an OData service
* Inspect metadata
* Identify entities and properties
* Build basic OData queries
* Apply filters
* Select specific fields
* Sort results
* Limit and paginate results
* Work with date and numeric conditions
* Query related entities
* Combine multiple query options
* Inspect and validate JSON responses
* Troubleshoot invalid OData queries

## OData Query Flow

```text
OData Service
      |
      v
Entity / Entity Set
      |
      v
Query Options
      |
      +---- $filter
      +---- $select
      +---- $orderby
      +---- $top / $skip
      +---- $expand
      |
      v
JSON Response
      |
      v
Reporting Application
```

## Timing (PAX ~2×)

TOC: **4 hours**. Highest overrun risk in Modules 1–4.

**Core (must finish):** service root + `$metadata`, `$filter` (Status / RegionId), `$select`, `$orderby`, `$top` / `$skip`, one Combined Completed + Region **3** query for Q1 **2023**.

**Stretch / homework:** `$count`, OR / parentheses, string functions (`startswith` / `contains` with `Industrial`), unsupported-option demos (`$expand` / `$search` / `Orders(id)`), full exercise set.

Seed facts: PascalCase properties on `Orders`; `Status eq 'Completed'`; Completed regions **1 / 3 / 5**; names `Customer-N` / `Industrial-N`. No real `$expand` / `$search` / key lookup.

## Files

Diagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.


| File           | Purpose                           |
| -------------- | --------------------------------- |
| `README.md`    | Session overview                  |
| `notes.md`     | OData concepts and query examples |
| `lab.md`       | Guided OData querying lab         |
| `assets/`      | Supporting files, if required     |
