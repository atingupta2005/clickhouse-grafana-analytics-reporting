# ClickHouse and Grafana for Analytics and Reporting

**Duration:** 60 Hours
**Format:** Instructor-led, Hands-on Training
**Target Audience:** BI Developers, Reporting Developers, SQL Developers and Application/Analytics Developers

---

## Course Overview

This training is designed for teams migrating their reporting and analytics workloads from SQL Server to ClickHouse and from traditional reporting tools such as SSRS toward Grafana.

The training focuses on developing analytical queries in ClickHouse and using the resulting data through the application/API layer for Grafana-based reporting.

The course provides practical coverage of ClickHouse SQL, SQL Server query migration, query optimization, REST/OData data consumption, Grafana dashboard development, Grafana variables and advanced dashboard capabilities.

dbt and Kafka are covered to provide an understanding of their role in the overall data and transformation architecture.

---

# Module 1 — ClickHouse Fundamentals and Data Modeling

**Duration: 8 Hours**

## Session 1 — ClickHouse Architecture and Data Modeling

**Duration: 4 Hours**

### Topics

* Introduction to ClickHouse
* ClickHouse use cases for analytics and reporting
* OLTP and OLAP
* SQL Server and ClickHouse — key differences
* Columnar storage and compression
* ClickHouse architecture
* Databases and tables
* Table engines
* MergeTree
* Sorting keys and primary key concepts
* ORDER BY
* Partitioning
* ClickHouse data types
* Nullable data
* Basic storage considerations
* Overview of distributed ClickHouse environments
* High-level replication concepts

### Hands-on

* Connect to ClickHouse
* Create database and tables
* Select appropriate data types
* Define sorting key and partitioning
* Load sample data
* Inspect table structure
* Execute basic analytical queries

---

## Session 2 — ClickHouse SQL for Analytics and Reporting

**Duration: 4 Hours**

### Topics

* SELECT and filtering
* WHERE, ORDER BY and LIMIT
* DISTINCT
* GROUP BY and HAVING
* Aggregate functions
* String functions
* Date and time functions
* Conditional expressions
* NULL handling
* KPI calculations
* Daily, monthly and period-based reporting

### Hands-on

* Sales reports
* Customer analysis
* Product analysis
* Regional reporting
* Daily/monthly trends
* KPI queries
* Aggregated reports

---

# Module 2 — Advanced ClickHouse SQL, Migration and Optimization

**Duration: 12 Hours**

## Session 3 — Advanced ClickHouse SQL

**Duration: 4 Hours**

### Topics

* INNER JOIN and LEFT JOIN
* JOIN considerations in ClickHouse
* CTEs
* Subqueries
* Window functions
* Ranking
* Running totals
* Period-based calculations
* Conditional aggregation
* Arrays and selected array functions
* Selected ClickHouse analytical functions

### Hands-on

* Multi-table reporting
* Customer and product analysis
* Ranking reports
* Running totals
* Period comparisons
* Complex KPI queries

---

## Session 4 — SQL Server to ClickHouse Query Migration

**Duration: 4 Hours**

### Topics

* SQL Server and ClickHouse SQL differences
* Data type mapping
* Common syntax differences
* TOP and LIMIT
* ISNULL and COALESCE
* CAST and CONVERT
* CASE
* Date and time functions
* String functions
* JOIN migration
* CTEs and subqueries
* Window functions
* NULL handling
* Common migration issues
* Query validation

### Hands-on: SQL Server Query Migration

* Analyze existing SQL Server queries
* Identify incompatible syntax/functions
* Map data types and functions
* Rewrite queries for ClickHouse
* Execute and validate results
* Compare results with the original queries

---

## Session 5 — ClickHouse Query Optimization

**Duration: 4 Hours**

### Topics

* Query execution in ClickHouse
* Sorting key and query performance
* Partitioning
* Data skipping
* Data types and storage considerations
* Filtering and aggregation optimization
* JOIN performance considerations
* EXPLAIN
* Query profiling
* system.query_log
* Identifying query bottlenecks
* Query rewriting
* Table design considerations

### Hands-on

* Analyze slow queries
* Establish performance baseline
* Use EXPLAIN
* Review query execution information
* Identify bottlenecks
* Rewrite queries
* Compare performance before and after optimization

---

# Module 3 — JSON, REST APIs and OData

**Duration: 8 Hours**

## Session 6 — JSON and REST API Data

**Duration: 4 Hours**

### JSON

* JSON objects and arrays
* Nested JSON structures
* JSON field extraction
* JSON functions
* Arrays
* Missing values and NULL
* JSON transformation
* Flattening nested data

### REST APIs

* REST fundamentals
* HTTP methods
* GET and POST concepts
* Headers
* Query parameters
* Authentication concepts
* Status codes
* Request and response structure
* JSON responses
* Pagination
* Error handling

### Hands-on

* Call a REST API
* Pass query parameters
* Read JSON responses
* Extract fields
* Work with nested objects
* Process arrays
* Handle pagination
* Transform API data for reporting

---

## Session 7 — OData Fundamentals and Querying

**Duration: 4 Hours**

### OData Fundamentals

* OData concepts
* OData and REST
* OData service structure
* Entities and entity sets
* Properties
* Relationships
* Metadata

### OData Query Options

* `$filter`
* `$select`
* `$orderby`
* `$top`
* `$skip`
* `$expand`
* `$count`
* `$search` where supported
* Combining query options
* String filtering
* Numeric filtering
* Date/time filtering
* Multiple filter conditions
* AND / OR conditions
* Sorting
* Pagination
* Related entities
* Nested/expanded data
* URL encoding
* JSON response handling

### Hands-on

* Build OData queries
* Apply multiple filters
* Filter by dates
* Select required fields
* Sort results
* Implement pagination
* Retrieve related data
* Combine OData query options
* Validate and troubleshoot OData responses

---

# Module 4 — Grafana Fundamentals and Data Integration

**Duration: 8 Hours**

## Session 8 — Grafana Fundamentals and ClickHouse Integration

**Duration: 4 Hours**

### Topics

* Grafana overview
* Grafana interface
* Dashboards and panels
* Data sources
* ClickHouse datasource
* Connection and authentication
* ClickHouse SQL in Grafana
* Query editor
* Time ranges
* Refresh intervals
* Explore

### Hands-on

* Connect Grafana to ClickHouse
* Validate the connection
* Execute ClickHouse queries
* Explore ClickHouse data
* Create panels
* Build a basic reporting dashboard

---

## Session 9 — Grafana and REST/OData Integration

**Duration: 4 Hours**

This session focuses specifically on the **CMF Application → REST/OData → Grafana** flow.

### Topics

* Grafana data-source concepts
* API-based data consumption
* REST API integration approaches
* OData integration approaches
* Connecting Grafana to an OData endpoint
* API request parameters
* Headers and authentication
* JSON responses
* API/OData filtering
* Date/time parameters
* Pagination
* API response structure
* Handling empty and invalid responses
* Data-source troubleshooting

### Hands-on

* Connect Grafana to a representative REST/OData endpoint
* Configure the required connection
* Execute API/OData queries
* Apply filters
* Pass parameters
* Retrieve selected fields
* Work with date/time filters
* Validate JSON responses
* Display API/OData data in Grafana panels

---

# Module 5 — Grafana Variables and Advanced OData

**Duration: 10 Hours**

## Session 10 — Grafana Variables and Dynamic Queries

**Duration: 4 Hours**

### Topics

* Grafana variables
* Query variables
* Custom variables
* Multi-value variables
* All option
* Variable formatting
* Dynamic filtering
* Variable dependencies
* Cascading variables
* Time variables
* Variables in ClickHouse queries
* Variables in REST/OData queries
* Dynamic query construction
* Query parameters
* Default values

### Hands-on

Create interactive filters for:

* Region
* Plant
* Product
* Category
* Customer
* Status
* Date/time

Use the variables to dynamically change ClickHouse and OData queries.

---

## Session 11 — Advanced OData Querying in Grafana

**Duration: 3 Hours**

### OData Query Techniques in Grafana

* Using Grafana variables in `$filter`
* Dynamic `$filter` construction
* Multiple filter conditions
* AND / OR conditions
* Date and time filtering
* Multi-value variables
* Dynamic `$select`
* Dynamic `$orderby`
* `$top` and `$skip`
* Pagination
* `$expand`
* Related entities
* Dynamic query parameters
* URL construction
* JSON response handling
* Empty-result handling
* Query troubleshooting
* Reducing unnecessary API data retrieval

### Hands-on Workshop

**Grafana Variable → OData Query → CMF/API → JSON Response → Grafana Panel**

Exercises include:

* Dynamic filtering
* Multi-value selection
* Date filtering
* Sorting
* Pagination
* Related data
* Dynamic parameters
* API response validation

---

## Session 12 — Advanced Grafana Dashboards

**Duration: 3 Hours**

### Topics

* Dashboard layout and organization
* Time-series panels
* Tables
* Bar charts
* Stat panels
* Thresholds
* Units and formatting
* Legends
* Field configuration
* Transformations
* Calculated values
* Field organization
* Panel links
* Dashboard links
* Drill-down
* Annotations
* Dashboard usability
* Query performance

### Hands-on

Enhance the reporting dashboard with:

* Interactive filters
* Multiple variables
* Dynamic queries
* Transformations
* Calculated KPIs
* Drill-down
* Navigation
* Annotations

---

# Module 6 — Advanced Reporting and Grafana Alerting

**Duration: 8 Hours**

## Session 13 — End-to-End Reporting Dashboard Workshop

**Duration: 4 Hours**

A practical reporting requirement is used to build a complete dashboard.

### Activities

* Understand reporting requirements
* Identify required KPIs
* Identify data sources
* Develop ClickHouse queries
* Develop OData queries where required
* Create Grafana variables
* Build dashboard panels
* Apply transformations
* Implement filtering
* Add drill-down/navigation
* Validate report results
* Review dashboard usability
* Review query performance

### Workshop Deliverable

An interactive reporting dashboard using ClickHouse and/or API/OData data.

---

## Session 14 — Grafana Alerting and Generic Webhooks

**Duration: 4 Hours**

### Topics

* Grafana alerting
* Alert rules
* Query-based alerts
* Conditions and expressions
* Thresholds
* Evaluation intervals
* Pending state
* No-data handling
* Error handling
* Contact points
* Notification policies
* Generic webhooks
* Webhook payloads
* Alert testing

### Hands-on

Create alerts for scenarios such as:

* KPI threshold exceeded
* Sales below target
* Transaction volume condition
* Data availability
* Business metric condition

Implement:

**Query → Alert Rule → Evaluation → Contact Point → Webhook**

---

# Module 7 — dbt and Kafka Concepts

**Duration: 6 Hours**

## Session 15 — dbt for ClickHouse

**Duration: 3 Hours**

### Topics

* Introduction to dbt
* Role of dbt in analytics engineering
* dbt and ClickHouse
* Sources
* Models
* Transformations
* Tests
* Documentation
* dbt workflow
* Where transformations can be performed
* dbt versus application-layer transformation

### Hands-on

* Create/use a dbt project
* Configure ClickHouse connection
* Define a source
* Create a model
* Apply a transformation
* Run the model
* Add a basic test
* Validate the resulting ClickHouse data

---

## Session 16 — Kafka Concepts and Kafka Jobs

**Duration: 3 Hours**

### Topics

* Why Kafka is used in modern data platforms
* Kafka architecture
* Topics
* Partitions
* Producers and consumers
* Consumer groups
* Events and messages
* JSON events
* Kafka in data movement
* Kafka and ClickHouse
* Kafka jobs and processing concepts
* Where Kafka fits into the overall architecture
* Typical Kafka-to-ClickHouse data flow
* When Kafka is required and when it is not

### Demonstration

* Example Kafka event flow
* Topic and partition behavior
* Producer/consumer interaction
* Example Kafka job
* Kafka-to-ClickHouse data movement

> **Note:** Kafka is covered as a conceptual and architecture topic; a dedicated Kafka hands-on lab is not part of this course.
