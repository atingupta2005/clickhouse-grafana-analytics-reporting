# Lab — OData Fundamentals and Querying

## Lab Objective

In this lab, you will explore the training OData V4 service and build queries for manufacturing and sales reporting.

You will work with:

* OData service discovery
* `$metadata`
* Entity sets
* `$filter`
* `$select`
* `$orderby`
* `$top`
* `$skip`
* `$count` (`?$count=true`; mention `/$count`)
* `$search` (stretch theory — **not** supported here)
* `$expand` (stretch theory — **not** supported here)
* String, numeric, and date filters
* Combined query options
* JSON responses
* Pagination
* Query troubleshooting

Use the OData endpoint provided in the training environment.

**Service root:** `https://vmclickhouse.canadacentral.cloudapp.azure.com/odata`

Useful starting points:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/$metadata
https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/Orders?$top=10
```

Entity sets include: `Regions`, `Plants`, `Categories`, `Products`, `Customers`, `Orders`.


---

## 1. Discover the OData Service

Open the training OData service root.

For example:

```text
/odata/
```

### Tasks

Identify:

* Service URL
* Available entity sets
* Service version
* Available resources

Record:

```text
Service URL:
____________________________

Entity sets:
____________________________
```

---

## 2. Inspect `$metadata`

Open:

```text
/odata/$metadata
```

Review the metadata document.

Identify:

* Entity types
* Entity sets
* Properties
* Data types
* Keys
* Navigation properties

Create a simple mapping:

```text
Entity Set | Key | Important Properties
-----------|-----|----------------------
Orders     |     |
Customers  |     |
Products   |     |
Plants     |     |
Regions    |     |
```

---

## 3. Query an Entity Set

Start with:

```text
/odata/Orders
```

Inspect the JSON response.

Identify:

* HTTP status
* Response structure
* Record collection
* Available fields
* Pagination information, if present

Look for the `value` collection in a typical OData JSON response.

---

## 4. Query by Key — not supported (Stretch demo)

Key-style URLs such as:

```text
/odata/Orders(100001)
```

are **not implemented** by this lab OData service (error/404).

### Core alternative

```text
/odata/Orders?$filter=OrderId eq 100001&$top=1
```

### Tasks

1. Try the key URL once and record the failure (optional stretch).
2. Use `$filter` on `OrderId` for a single-order lookup.
3. Confirm OrderId, OrderDate, CustomerId, Quantity, SalesAmount, Status from the `value` array.

---

## 5. Use `$select`

Request only the fields needed for a report:

```text
/odata/Orders?$select=OrderId,OrderDate,CustomerId,SalesAmount
```

### Tasks

Compare the response with the unfiltered entity-set request.

Identify:

* Which fields were removed
* Which fields remain
* Whether the response is easier to consume

---

## 6. Basic `$filter`

Filter orders for Region 2 (**any status** — Region 2 has rows, but **not** Completed):

```text
/odata/Orders?$filter=RegionId eq 2
```

### Tasks

Verify that every returned record belongs to Region 2.

> Warning: do **not** add `Status eq 'Completed'` to Region 2 — that combination is **empty**. Completed seed data exists only for regions **1, 3, 5**.

Record the number of matching records.

---

## 7. Filter by Status

Run:

```text
/odata/Orders?$filter=Status eq 'Completed'
```

Verify that every returned order has:

```text
Status = Completed
```

---

## 8. Combine `$filter` Conditions

Request Completed orders from Region 3:

```text
/odata/Orders?$filter=RegionId eq 3 and Status eq 'Completed'
```

### Task

Compare this result with the individual Region and Status queries.

Explain why the combined query returns fewer records.

---

## 9. Use OR

Request orders from Region 1 or Region 2 (any status):

```text
/odata/Orders?$filter=RegionId eq 1 or RegionId eq 2
```

Verify the returned records.

Now combine with status using Completed regions only:

```text
/odata/Orders?$filter=(RegionId eq 1 or RegionId eq 3) and Status eq 'Completed'
```

(Region 1 **or** 2 with Completed would drop Region 2 to empty — prefer 1 and 3.)

### Task

Explain the purpose of the parentheses.

---

## 10. Numeric Filtering

Find orders with quantity greater than 5:

```text
/odata/Orders?$filter=Quantity gt 5
```

Now find orders with sales of at least 2,000:

```text
/odata/Orders?$filter=SalesAmount ge 2000
```

Verify the results.

---

## 11. String Filtering

Seed customer names look like `Customer-N` / `Industrial-N` (not `ABC Manufacturing`).

Try:

```text
/odata/Customers?$filter=startswith(CustomerName,'Industrial')
```

and:

```text
/odata/Customers?$filter=contains(CustomerName,'Customer')
```

### Task

Record whether each function is supported by the service.

---

## 12. Date Filtering

Use the service metadata to determine the type and expected format of `OrderDate`.

Retrieve orders from Q1 2023.

For a date-valued property, a query may look like:

```text
/odata/Orders?$filter=OrderDate ge 2023-01-01 and OrderDate lt 2023-04-01
```

### Tasks

Verify:

* Earliest returned date
* Latest returned date
* No records outside the requested period

If the service uses date-time values, adapt the literal to the format required by the service.

---

## 13. `$orderby`

Sort orders by sales amount descending:

```text
/odata/Orders?$orderby=SalesAmount desc
```

Now sort by:

```text
/odata/Orders?$orderby=OrderDate desc,SalesAmount desc
```

### Task

Explain the effect of the second sort field.

---

## 14. `$top`

Return the ten highest-value orders:

```text
/odata/Orders?$orderby=SalesAmount desc&$top=10
```

Verify that:

* Exactly ten records are returned, where at least ten exist.
* Results are ordered by sales amount.
* The first record has the highest sales amount in the returned set.

---

## 15. `$skip` and `$top`

Retrieve records in pages.

First page:

```text
/odata/Orders?$orderby=OrderId&$top=10&$skip=0
```

Second page:

```text
/odata/Orders?$orderby=OrderId&$top=10&$skip=10
```

Third page:

```text
/odata/Orders?$orderby=OrderId&$top=10&$skip=20
```

### Tasks

Check:

* Number of records per page
* First and last Order ID
* Duplicate records
* Missing records

The stable `$orderby` is important when using offset pagination.

---

## 16. `$count`

Request the count of matching records:

```text
/odata/Orders?$count=true
```

Combine with a filter:

```text
/odata/Orders?$filter=Status eq 'Completed'&$count=true
```

Also try the count path if exposed:

```text
/odata/Orders/$count
```

### Task

Locate the count in the response and compare it with the number of records returned in `value`.

---

## 17. `$search` (Stretch / theory only)

**Not supported by this lab OData service.** Optional demo:

```text
/odata/Customers?$search="Industrial"
```

### Task

Record the unsupported response. Prefer `$filter` with `contains` / `startswith` for real lab work. Do not mark Core complete based on `$search`.

---

## 18. Explore Relationships

Review `$metadata` and identify the navigation properties between:

```text
Orders
Customers
Products
Plants
Regions
```

Determine which entities can be related.

Create:

```text
Order
  |
  +-- Customer
  |
  +-- Product
  |
  +-- Plant
```

using the actual navigation-property names from the service.

---

## 19. Use `$expand` (Stretch / theory only)

**Not supported by this lab OData service** for real nested entities.

Optional demo (expect failure / ignore):

```text
/odata/Orders?$expand=Customer
```

### Core alternative

Select `CustomerId` on Orders; look up Customers separately if needed:

```text
/odata/Orders?$select=OrderId,CustomerId,SalesAmount&$top=10
```

Do not require `$expand` for lab completion.

---

## 20. Combine Query Options

Build a query for:

> The ten highest-value Completed orders from Region 3.

Use:

* `$filter`
* `$select`
* `$orderby`
* `$top`

A possible query is:

```text
/odata/Orders?$filter=RegionId eq 3 and Status eq 'Completed'&$select=OrderId,OrderDate,CustomerId,SalesAmount&$orderby=SalesAmount desc&$top=10
```

### Task

Execute the query and validate every condition.

---

## 21. Build a Regional Sales Query

Create an OData query that retrieves Completed orders from Region 3 during Q1 2023.

Start with:

```text
/odata/Orders
```

Add the options incrementally:

```text
$filter
```

then:

```text
$select
```

then:

```text
$orderby
```

and finally:

```text
$top
```

### Task

Explain each part of the final URL.

---

## 22. Inspect the JSON Response

Take the query from the previous exercise and inspect the JSON response.

Identify:

```text
@odata.context
value
individual record fields
pagination information, if present
```

### Task

Draw the response structure:

```text
OData Response
     |
     +-- @odata.context
     |
     +-- value
          |
          +-- Order
          +-- Order
          +-- Order
```

---

## 23. Troubleshoot an Invalid Property

Try a query using an invalid property:

```text
/odata/Orders?$filter=InvalidField eq 1
```

### Tasks

Record:

```text
HTTP status:
Error response:
Error message:
```

Then compare the property name with `$metadata`.

Explain how metadata can help prevent this problem.

---

## 24. Troubleshoot an Unsupported Query Option

Try a query using an option that the service does not support, or use `$search` if it is not supported.

Record:

```text
Query:
________________________________

HTTP status:
________________________________

Response:
________________________________
```

Explain how you determined that the problem was unsupported functionality rather than an incorrect endpoint.

---

## 25. URL Encoding

Construct an OData filter containing a string value that needs encoding.

Seed-style example:

```text
Industrial-1
```

Logical expression:

```text
CustomerName eq 'Industrial-1'
```

Then represent it correctly as part of the URL.

### Task

Explain why URL encoding is important when OData URLs are generated programmatically.

---

## 26. Final OData Reporting Challenge

### Requirement

The reporting team needs:

> Completed orders from Region 3 during Q1 2023, showing order ID, order date, customer, quantity, and sales amount. Results should be ordered by sales amount descending and retrieved using pagination.

### Tasks

1. Inspect `$metadata`.
2. Identify the correct entity set.
3. Identify the required property names.
4. Build the `$filter`.
5. Add `$select`.
6. Add `$orderby`.
7. Add `$top` and `$skip`.
8. Execute the request.
9. Inspect the JSON response.
10. Retrieve the next page.
11. Check for duplicates.
12. Validate the date range.
13. Validate Region **3**.
14. Validate completed status.
15. Calculate total quantity and total sales from the returned dataset.

Do **not** use `$expand` or Region 2 + Completed.

Record:

```text
Entity Set:
________________________________

Filter:
________________________________

Select:
________________________________

Order By:
________________________________

Page Size:
________________________________

Pages Retrieved:
________________________________

Records Retrieved:
________________________________

Total Quantity:
________________________________

Total Sales:
________________________________
```

## Lab Completion Checklist

```text
[ ] Discovered the OData service
[ ] Inspected $metadata
[ ] Identified entity sets
[ ] Queried entities ($filter by OrderId — not Orders(id) key URL)
[ ] Used $filter (Completed + Region 3)
[ ] Used AND / OR (Completed regions 1/3/5)
[ ] Used numeric filters
[ ] Used string filters (Industrial / Customer)
[ ] Used date filters
[ ] Used $select
[ ] Used $orderby
[ ] Used $top
[ ] Used $skip
[ ] Used $count (?$count=true; noted /$count)
[ ] Noted $search not supported (stretch only)
[ ] Noted $expand not supported (stretch only)
[ ] Combined query options
[ ] Inspected JSON responses (value array)
[ ] Tested pagination
[ ] Troubleshot invalid queries
[ ] (Stretch) Final reporting challenge
```
