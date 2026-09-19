# Session 14 — Grafana Alerting and Generic Webhooks

## 1. Grafana Alerting Overview

Grafana alerting allows a query result to be evaluated against a condition and converted into an alert state.

The basic flow is:

**Data source → Query → Condition → Evaluation → Alert state → Contact point → Notification policy**

An alert is not simply a dashboard visualization. The alert rule evaluates data independently according to its configured evaluation schedule.

### Core

Understand these components:

| Component | Purpose |
|---|---|
| Query | Retrieves the metric or business value |
| Expression / condition | Determines whether the value meets the alert condition |
| Threshold | Defines the condition that should trigger the alert |
| Evaluation interval | Determines how often Grafana evaluates the rule |
| Pending period | Requires a condition to remain true before firing |
| Alert state | Represents the current result of evaluation |
| Contact point | Defines where notifications are sent |
| Notification policy | Determines how alerts are routed |

### Trainer Tip

Keep the first explanation simple:

> A dashboard tells you what is happening. An alert rule tells Grafana when it needs to notify someone.

---

## 2. Query-Based Alerts

A query-based alert starts with a query against a data source.

For this course, ClickHouse can provide business metrics from:

```text
training.v_lab_orders
```

Examples include:

- Completed sales amount
- Completed order volume
- Sales by region
- High-value completed rows
- Data availability

The alert should evaluate a value that has a clear business meaning.

### Example Scenario

Suppose the business wants to know when the selected KPI falls below a target.

The query can calculate a completed-sales metric, and the alert condition can compare the resulting value with a threshold.

The important separation is:

**Query answers:**  
"What is the current metric value?"

**Condition answers:**  
"Does that value require attention?"

---

## 3. Alert Conditions and Thresholds

A threshold converts a metric into a condition.

Common comparisons include:

- Greater than
- Greater than or equal to
- Less than
- Less than or equal to
- Equal to

Example:

```text
Completed sales < target
```

The target should be chosen for the scenario being demonstrated. It should not be presented as an actual business target from the training seed.

### Trainer Tip

Do not describe an arbitrary training threshold as a production business requirement.

Use language such as:

> "For this demonstration, we will use this threshold to show how the alert behaves."

---

## 4. Conditions and Expressions

Grafana can use query results and expressions to build alert conditions.

A simple alert can follow:

```text
Query
  ↓
Reduce / evaluate value
  ↓
Threshold
  ↓
Alert state
```

For example:

```text
Completed order metric
        ↓
Evaluate the returned value
        ↓
Compare with threshold
        ↓
Alert if condition is true
```

Expressions become useful when the alert requires more processing than a direct threshold comparison.

### Core

Students should understand the difference between:

- the query producing data
- the expression transforming or evaluating data
- the condition determining whether the alert should fire

---

## 5. Evaluation Interval

An alert rule is evaluated repeatedly.

For example:

```text
Evaluate every 1 minute
```

means Grafana checks the rule approximately once per minute.

The evaluation interval affects how quickly Grafana can detect a change.

A shorter interval can detect changes sooner, while a longer interval reduces evaluation frequency.

### Trainer Tip

Do not equate evaluation interval with notification frequency.

The rule may be evaluated frequently while notification behavior is controlled separately by alert state and notification configuration.

---

## 6. Pending State

An alert does not always need to fire immediately when its condition becomes true.

A pending period can require the condition to remain true for a specified duration.

Example:

```text
Condition:
Completed sales < target

Pending:
5 minutes
```

If the condition becomes true briefly and then returns to normal, the alert may never reach the firing state.

Conceptually:

```text
Normal
   ↓
Condition becomes true
   ↓
Pending
   ↓
Condition remains true
   ↓
Firing
```

If the condition clears during the pending period:

```text
Pending
   ↓
Condition becomes false
   ↓
Normal
```

### Why This Matters

Pending periods help avoid notifications caused by short-lived fluctuations.

---

## 7. No-Data Handling

A query can return no usable data.

This is different from a metric returning zero.

For example:

```text
Metric = 0
```

means the query returned a value of zero.

Whereas:

```text
No data
```

means Grafana did not receive a usable result for evaluation.

These states should not automatically be treated as the same business condition.

### Training Seed Example

Completed data exists for regions:

```text
1
3
5
```

Region `2` with `Completed` has no completed data.

This makes Region 2 useful for demonstrating the difference between:

- a valid zero/low metric
- no returned data

### Trainer Tip

Explicitly ask:

> "Is this a business condition, or is the data itself unavailable?"

That distinction is important when designing production alerts.

---

## 8. Error Handling

A query can also fail.

Examples include:

- Data source unavailable
- Query syntax error
- Permission problem
- Timeout
- Invalid configuration

An error should not automatically be interpreted as a business metric crossing a threshold.

For example:

```text
Sales = 0
```

is different from:

```text
Query failed
```

and different again from:

```text
No data
```

Alert configuration should make these states understandable to the operator.

---

## 9. KPI Alert Scenario

A useful training scenario is a completed-sales KPI alert.

The conceptual flow is:

```text
training.v_lab_orders
        ↓
Completed sales KPI
        ↓
Evaluate returned value
        ↓
Compare against demonstration threshold
        ↓
Pending period
        ↓
Firing / Normal
```

The query should use the reporting view because the view contains the normalized reporting fields needed for sales analytics.

Do not use `training.orders` for quantity, sales amount, or region-based reporting calculations.

### Trainer Tip

Keep the first alert simple. One query and one threshold are enough to demonstrate the complete lifecycle.

For a classroom **firing** demo, use a condition that is clearly true against the returned Completed sales (for example **Is above 0**, or **Is below** a very large number). Say explicitly that the threshold is for demonstration only.

---

## 10. Other Alert Scenarios

The same pattern can be applied to different business or operational questions.

### Sales Below Target

```text
Completed sales
        ↓
Below target?
        ↓
Alert
```

### Volume Condition

```text
Completed order volume
        ↓
Above / below threshold?
        ↓
Alert
```

### Data Availability

```text
Expected data
        ↓
Data available?
        ↓
Alert when expected data is missing
```

### Business Metric

```text
Business KPI
        ↓
Evaluate KPI
        ↓
Threshold / condition
        ↓
Alert
```

The metric and threshold should be defined according to the actual business requirement in a production implementation.

---

## 11. Contact Points

A contact point defines where Grafana sends an alert notification.

Examples can include:

- Email
- Webhook
- Other supported notification integrations

For this session, the important example is a **Generic Webhook**.

Conceptually:

```text
Alert Rule
    ↓
Alert fires
    ↓
Notification Policy
    ↓
Contact Point
    ↓
Webhook endpoint
```

### Core

Students should understand the role of a contact point and inspect the configuration during the instructor demonstration.

### Permission Note

The `student` account may not have permission to create or save contact points.

Therefore, creating a contact point is an instructor demonstration, not a required student Core task.

---

## 12. Notification Policies

A notification policy controls how alerts are routed to contact points.

Conceptually:

```text
Alert
  ↓
Notification Policy
  ↓
Contact Point
  ↓
Notification destination
```

This separates the alert condition from the destination.

For example, the same alerting logic can remain unchanged while its notification destination is changed through routing configuration.

### Trainer Tip

Explain the difference clearly:

- **Alert rule:** When should Grafana consider something an alert?
- **Contact point:** Where should the notification go?
- **Notification policy:** Which contact point should receive the alert?

---

## 13. Generic Webhooks

A webhook allows Grafana to send alert information to an HTTP endpoint.

The basic interaction is:

```text
Grafana
   |
   | HTTP request
   ↓
Webhook endpoint
```

The receiving application can then process the notification.

Possible consumers include:

- Incident-management systems
- Automation services
- Internal applications
- Custom notification services

The training lab does not require students to build a webhook receiver.

### Instructor Demo

The instructor may use:

- an instructor-provided webhook URL, or
- a clearly identified public demonstration request endpoint

Do not assume a particular third-party request-bin service is available.

---

## 14. Webhook Payloads

A webhook request normally contains structured alert information.

The useful concepts to inspect are:

- Alert status
- Alert rule information
- Labels
- Annotations
- Evaluation-related information
- Notification metadata

The exact payload structure should be inspected from the Grafana version and configuration used in the lab rather than invented in the training material.

### Trainer Tip

The goal is to teach students how to read and use the payload, not to turn the session into webhook application development.

Ask students to identify:

1. What alert generated the notification?
2. What state is the alert in?
3. What labels or metadata identify the alert?
4. What information would a receiving system need?

---

## 15. Alert Testing

Testing should verify the complete path:

```text
Query
  ↓
Condition
  ↓
Evaluation
  ↓
Alert state
  ↓
Notification routing
  ↓
Contact point
  ↓
Webhook
```

The instructor should demonstrate the test using the available Grafana administrator account.

Students can observe:

- Rule configuration
- Evaluation behavior
- State changes
- Notification routing
- Webhook request

### Important

A student does **not** need to successfully send a webhook from their own laptop to complete the Core session.

---

## 16. Grafana Time Range for This Lab

The training seed contains data from:

```text
2023-01-01
```

through:

```text
2025-06-18
```

For demonstrations involving Grafana time-based queries, use the absolute range:

```text
2023-01-01 → 2025-06-18
```

Do not use **Last 30 days** as the primary training range because the seeded data ends in 2025.

---

## 17. Grafana Permissions

The student Grafana account is:

```text
student
```

with password:

```text
StudentLab!2026
```

The instructor administrator account is:

```text
admin
```

with password:

```text
GrafanaLab!2026
```

The student account may not have permission to create or save alert rules or contact points.

Therefore:

- Alert creation is an instructor Core demonstration.
- Contact-point creation is an instructor Core demonstration.
- Student recreation is Stretch only where permissions allow.
- The session does not depend on students having administrator privileges.

---

## 18. Recommended Teaching Sequence

Use this sequence during the live session:

```text
1. What is Grafana Alerting?
        ↓
2. Query-based alert
        ↓
3. Condition and threshold
        ↓
4. Evaluation interval
        ↓
5. Pending state
        ↓
6. No-data and error states
        ↓
7. Contact point
        ↓
8. Notification policy
        ↓
9. Generic webhook
        ↓
10. Test the complete flow
```

Keep the first example simple and introduce webhook routing only after students understand how the alert rule itself works.
