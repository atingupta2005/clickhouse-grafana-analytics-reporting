# Session 15 — dbt for ClickHouse

## Lab Overview

This lab uses the existing dbt project under:

```text
the course dbt project/
```

The Core path is a guided walkthrough. You do not need server login.

The project uses:

- dbt project: `training_dbt`
- Target schema: `training_dbt`
- ClickHouse user: `training_rw`
- Source database: `training`
- dbt container: `lab-dbt`
- Example model: `models/mart_sales_by_region.sql`

---

# Core Lab

## Step 1 — Identify the dbt Project

In the Core walkthrough, review the existing project:

```text
the course dbt project/
```

Identify these files:

```text
dbt_project.yml
profiles.yml
models/sources.yml
models/mart_sales_by_region.sql
```

### Expected Result

You can identify:

- The dbt project configuration.
- The connection profile.
- The source definitions.
- The example transformation model.

### Tip

Do not create another dbt project. The Core lab uses the existing project so you can focus on the dbt workflow.

---

## Step 2 — Review `dbt_project.yml`

Open:

```text
the course dbt project/dbt_project.yml
```

Identify:

- Project name.
- Model configuration.
- Model directory.
- Other project-level settings relevant to the existing project.

Confirm that the project is:

```text
training_dbt
```

### Expected Result

You should understand that `dbt_project.yml` defines the dbt project and its project-level configuration.

### Tip

Do not confuse the project name with the ClickHouse target schema. The project is named `training_dbt`; the configured target schema is also `training_dbt`, but they represent different concepts.

---

## Step 3 — Review `profiles.yml`

Open:

```text
the course dbt project/profiles.yml
```

Locate the profile:

```text
training_dbt
```

Review the configured ClickHouse connection.

The profile uses:

```text
training_rw
```

and targets the:

```text
training_dbt
```

schema.

### Expected Result

You can explain:

```text
dbt_project.yml
 |
 +-- identifies/configures the project

profiles.yml
 |
 +-- defines the database connection
```

### Tip

Focus on the profile structure and target — not on copying secrets.

---

## Step 4 — Review the Source Definitions

Open:

```text
the course dbt project/models/sources.yml
```

Identify the declared source tables:

```text
training.orders
training.order_items
training.plants
training.regions
```

Discuss the role of each source:

| Source | Role |
|---|---|
| `training.orders` | Order-level source data |
| `training.order_items` | Order-line source data |
| `training.plants` | Plant/reference information |
| `training.regions` | Region/reference information |

### Expected Result

You should understand that these are existing ClickHouse tables used as inputs to dbt models.

### Tip

A dbt source definition does not create a copy of the source table. It describes an existing database object that the dbt project consumes.

This project reads **normalized** `training` tables (`orders`, `order_items`, …), not `training.v_lab_orders`. That Grafana reporting view is a different consumer path from Sessions 08–14.

---

## Step 5 — Trace the Example Model

Open:

```text
the course dbt project/models/mart_sales_by_region.sql
```

Read the SQL from top to bottom.

Identify:

1. Which source tables are used.
2. How the source tables are joined.
3. Which fields are selected.
4. Which calculations or aggregations are performed.
5. Which fields form the resulting reporting structure.

Draw the transformation on the board:

```text
training.orders
 +
training.order_items
 +
training.plants
 +
training.regions
 |
 v
mart_sales_by_region
```

### Expected Result

You can explain the purpose of the model without needing to write the SQL themselves.

### Tip

Focus on **data flow**, not line-by-line SQL syntax. You already have SQL experience from earlier sessions.

---

## Step 6 — Identify the Target Schema

Explain where the model is intended to be materialized.

```text
Source:
training.*

 |
 | dbt transformation
 v

Target:
training_dbt.*
```

The model should not modify the shared source tables in `training`.

### Expected Result

You should understand the separation between source data and dbt-managed analytical outputs.

### Tip

This separation is  Do not use `DROP` or `TRUNCATE` against `training.*` objects.

---

## Step 7 — Trace the dbt Workflow

Use the existing project to walk through the normal workflow:

```text
Source definitions
 |
 v
SQL model
 |
 v
dbt run
 |
 v
Target model
 |
 v
dbt test
 |
 v
Validate in ClickHouse
```

Note: the Core session is a walkthrough; you do not need to execute the commands yourself.

### Expected Result

You can describe the purpose of each stage:

- **Source** — identifies input data.
- **Model** — defines transformation.
- **Run** — executes the transformation.
- **Test** — checks defined data assumptions.
- **Validate** — confirms the resulting database object.

---

## Step 8 — Review Testing

Open the existing project and check whether any dbt test definitions exist (for example a `schema.yml` next to models).

**Note:** the `the course dbt project/` tree ships sources + `mart_sales_by_region.sql` but **does not yet include configured dbt tests**. Learn the *ideas* of common tests:

- Not-null checks
- Uniqueness checks
- Relationship checks
- Accepted-value checks

Discuss the difference between:

```text
dbt run
```

and:

```text
dbt test
```

### Expected Result

You should understand that successful SQL execution (`dbt run`) and data-quality validation (`dbt test`) are different checks — even when this lab project has not added YAML tests yet.

### Tip

Do not invent fake test YAML for Core. Stretch `dbt test` may report that there is nothing to test; that is an honest outcome for this project.

---

## Step 9 — Compare Transformation Locations

Discuss the following scenario:

```text
ClickHouse source data
 |
 +---- dbt
 |
 +---- Application
 |
 +---- REST/OData
 |
 +---- Grafana
```

Check:
> Which transformation should be reusable across multiple analytical consumers?

Use the discussion to distinguish:

- Analytical transformation → dbt/database layer.
- Application-specific transformation → application layer.
- API response shaping → REST/OData layer.
- Presentation/query-specific transformation → Grafana.

### Expected Result

You should be able to explain why the same transformation should not automatically be duplicated in every consuming application.

---

