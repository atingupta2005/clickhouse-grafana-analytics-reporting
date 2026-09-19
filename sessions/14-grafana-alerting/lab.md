# Session 14 — Grafana Alerting and Generic Webhooks

## Core Lab — Observation and watch-along
### Lab Scope

The Core path is designed for all students, including students whose Grafana account cannot create or save alerting resources.

Watch the alert configuration (admin account) and reproduce the reasoning behind each step.

Configuration that requires administrator permissions is done in the watch-along.

---

## 1. Open Grafana

Open:

```text
https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/
```

Sign in with:

```text
Username: student
Password: StudentLab!2026
```

### Expected Result

The Grafana interface opens and you can access the available dashboards and Grafana navigation.

### Tip

If you cannot access alerting configuration or save an alert rule, do not treat permissions as a Core blocker. Continue with the watch-along demonstration.

---

## 2. Review the Alerting Area

Open the Grafana **Alerting** area from the main navigation.

Review the available sections for:

- Alert rules
- Contact points
- Notification policies
- Alert instances

### Expected Result

Students can identify the main parts of the Grafana alerting interface.

### Tip

Explain that the exact options visible to a student depend on Grafana permissions.

---

## 3. Review the Alert Lifecycle

Before creating the demonstration rule, review this flow:

```text
ClickHouse query
      ↓
Metric value
      ↓
Condition / threshold
      ↓
Evaluation
      ↓
Pending
      ↓
Firing
      ↓
Notification policy
      ↓
Contact point
      ↓
Webhook
```

Ask students to identify which component answers each question:

| Question | Component |
|---|---|
| What data should be checked? | Query |
| What value should trigger attention? | Condition / threshold |
| How often should it be checked? | Evaluation interval |
| How long must it remain true? | Pending period |
| Where should the notification go? | Contact point |
| How is the destination selected? | Notification policy |

---

# Watch-along — KPI Alert

## 4. Open the ClickHouse Data Source

For the watch-along, sign in using:

```text
Username: admin
Password: GrafanaLab!2026
```

Use the provisioned **ClickHouse** datasource.

Do not create another ClickHouse datasource.

### Expected Result

Use the existing ClickHouse datasource for the alert demonstration.

---

## 5. Run the KPI Query

Use the reporting view:

```sql
SELECT
    sum(sales_amount) AS completed_sales
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND order_date >= toDate('2023-01-01')
  AND order_date <= toDate('2025-06-18')
```

### Expected Result

The query returns a single numeric value named:

```text
completed_sales
```

This value represents completed sales for the seeded reporting data in the selected absolute date range.

### Tip

Explain why the reporting view is used:

- `training.v_lab_orders` is the reporting source for sales analytics.
- `training.orders` should not be used for this sales calculation.

---

## 6. Explain the Alert Condition

Use the returned KPI as the input to the alert condition.

**Concrete demo approach (admin account):**

1. Note the approximate `completed_sales` value returned by the query (full seed Completed sales is a large positive number).
2. For a **firing** demonstration, configure a condition such as:
   - **Is below** `999999999999` (or any threshold clearly **above** the returned sales), **or**
   - **Is above** `0` (condition true whenever sales exist).
3. Say aloud: this threshold is a **classroom demonstration value**, not a real business target.

To show **Normal** instead, temporarily use a condition that is false (for example **Is above** a number larger than returned sales).

Explain:

```text
Query returns metric
        ↓
Grafana evaluates metric
        ↓
Metric is compared with threshold
        ↓
Condition becomes true or false
```

### Expected Result

Students can explain the difference between the query and the alert condition, and see at least one clear true/false demonstration.

### Tip

Do not ask students to treat the demonstration threshold as a production SLA or business target.

---

## 7. Configure Evaluation Behavior

Configure the demonstration rule with an evaluation interval suitable for observing the alert lifecycle.

Discuss the following settings:

- Evaluation interval
- Pending period
- What happens when the condition becomes true
- What happens when the condition becomes false

### Expected Result

Students understand that an alert is evaluated repeatedly rather than only when a dashboard is opened.

---

## 8. Demonstrate Pending State

Explain the state transition:

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

Then explain the alternative:

```text
Pending
  ↓
Condition becomes false
  ↓
Normal
```

### Expected Result

Students understand why a temporary threshold violation does not necessarily produce an immediate firing notification.

### Tip

Do not require students to reproduce the timing manually. The objective is understanding the state transition.

---

## 9. Demonstrate No-Data Behavior

Use the training seed to explain a no-data / empty-result scenario.

Completed data exists for regions **1, 3, 5**. Region **2** + `Completed` has none.

Show a second query (still on the provisioned ClickHouse datasource):

```sql
SELECT
    sum(sales_amount) AS completed_sales
FROM training.v_lab_orders
WHERE status = 'Completed'
  AND region_id = 2
  AND order_date >= toDate('2023-01-01')
  AND order_date <= toDate('2025-06-18')
```

### Expected Result

This filtered query returns **no rows** or a null/empty metric suitable for discussing Grafana **No Data** handling versus a real zero KPI.

You should be able to explain why no-data handling should be considered separately from a threshold condition.

### Tip

Do not describe Region 2 + Completed as a normal successful KPI scenario. After the demo, return to the unfiltered Completed sales query for the main alert rule.

---

## 10. Discuss Error Handling

Explain that an alert query can also fail.

Discuss examples such as:

- Query failure
- Data source failure
- Permission failure
- Timeout

Compare the three states:

| Situation | Meaning |
|---|---|
| Metric returns a value | Query succeeded |
| No data | Query did not produce usable data |
| Error | Query/evaluation encountered an error |

### Expected Result

Students understand that a query error should not automatically be interpreted as a business KPI failure.

---

# Watch-along — Contact Point and Webhook

## 11. Open Contact Points

From Grafana Alerting, open **Contact points**.

Explain that a contact point defines the notification destination.

Create or demonstrate a **Generic Webhook** contact point (admin account).

### Expected Result

Students can identify:

```text
Alert Rule → Contact Point → Webhook
```

### Tip

Do not require students to create a contact point. The student account may not have sufficient permissions.

---

## 12. Configure the Generic Webhook

Use either:

- a provided webhook URL, or
- a clearly identified demonstration webhook endpoint available for the shared demo.

Do not invent or require a specific public webhook service.

The configuration should demonstrate the destination concept without requiring students to build a webhook receiver.

### Expected Result

Note where the webhook destination is configured.

---

## 13. Review the Webhook Payload

When the webhook is tested or triggered, inspect the request received by the demonstration endpoint.

Discuss the information carried by the notification, such as:

- Alert status
- Alert identity
- Labels
- Annotations
- Notification metadata

### Expected Result

Students can identify the important information that a receiving application could use.

### Tip

Do not turn this step into webhook application development. The objective is to understand the integration boundary.

---

## 14. Review Notification Policies

Open **Notification policies**.

Explain:

```text
Alert Rule
    ↓
Notification Policy
    ↓
Contact Point
    ↓
Webhook
```

Discuss why routing is separate from the alert condition.

### Expected Result

Students understand that the alert rule determines when an alert exists, while routing determines where its notification goes.

---

## 15. Test the Alerting Flow

the demonstration shows the complete flow:

```text
ClickHouse
    ↓
KPI Query
    ↓
Alert Condition
    ↓
Evaluation
    ↓
Alert State
    ↓
Notification Policy
    ↓
Webhook Contact Point
```

Review the resulting alert state and, where the demonstration endpoint supports it, inspect the webhook request.

### Expected Result

Students can describe the complete path from database metric to webhook notification.

### Tip

The Core requirement is observation and understanding. Students do not need to successfully fire a webhook from their own account.

---

# Core Lab Checklist

Students should be able to explain:

- [ ] What an alert rule is
- [ ] How a query supplies an alert metric
- [ ] How a threshold creates a condition
- [ ] What an evaluation interval does
- [ ] What the pending state means
- [ ] Difference between no-data and zero
- [ ] Difference between no-data and query error
- [ ] What a contact point does
- [ ] What a notification policy does
- [ ] What a generic webhook does
- [ ] The complete alert-to-webhook flow

---

# Stretch — Student Alert Recreation

> Perform this section only if the student's Grafana role allows alert-rule creation and saving.

## 16. Create a Simplified Alert Rule

Create a simplified version of the KPI alert from the watch-along using the provisioned ClickHouse datasource.

Use the same reporting source:

```text
training.v_lab_orders
```

and the same absolute data range:

```text
2023-01-01 → 2025-06-18
```

The query must evaluate completed data.

### Expected Result

The student can create and save an alert rule if their Grafana permissions allow it.

If Grafana prevents saving the rule, return to the watch-along demonstration. This is not a Core failure.

---

## 17. Review the Rule Configuration

Check:

- Query
- Condition
- Threshold
- Evaluation interval
- Pending behavior
- No-data behavior
- Error behavior

### Expected Result

The student can explain what each configuration controls.

---

## 18. Review Alert Routing

If the student's permissions allow access, inspect the available notification-policy and contact-point configuration.

Do not modify shared alert configuration unless specifically instructed.

### Expected Result

The student understands how the rule connects to notification routing.

---

## 19. End of Lab

Return to the main Alerting view and review the alert lifecycle one final time:

```text
Query
  ↓
Condition
  ↓
Evaluation
  ↓
Pending / Firing / Normal
  ↓
Notification Policy
  ↓
Contact Point
  ↓
Webhook
```

The Core lab is complete.
