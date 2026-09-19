# Session 15 — dbt for ClickHouse

## Lab Overview

This lab uses the existing dbt project under:

```text
stacks/app/dbt/
```

The Core path is a guided walkthrough. Students do not need SSH access to the App VM.

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
stacks/app/dbt/
```

Identify these files:

```text
dbt_project.yml
profiles.yml
models/sources.yml
models/mart_sales_by_region.sql
```

### Expected Result

Students can identify:

- The dbt project configuration.
- The connection profile.
- The source definitions.
- The example transformation model.

### Tip

Do not ask students to create another dbt project. The Core lab uses the existing project so that the class can focus on the dbt workflow.

---

## Step 2 — Review `dbt_project.yml`

Open:

```text
stacks/app/dbt/dbt_project.yml
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

Students understand that `dbt_project.yml` defines the dbt project and its project-level configuration.

### Tip

Do not confuse the project name with the ClickHouse target schema. The project is named `training_dbt`; the configured target schema is also `training_dbt`, but they represent different concepts.

---

## Step 3 — Review `profiles.yml`

Open:

```text
stacks/app/dbt/profiles.yml
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

Students can explain:

```text
dbt_project.yml
 |
 +-- identifies/configures the project

profiles.yml
 |
 +-- defines the database connection
```

### Tip

Do not expose or copy sensitive connection secrets into student notes or chat. The purpose of this step is to understand the profile structure and target.

---

## Step 4 — Review the Source Definitions

Open:

```text
stacks/app/dbt/models/sources.yml
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

Students understand that these are existing ClickHouse tables used as inputs to dbt models.

### Tip

A dbt source definition does not create a copy of the source table. It describes an existing database object that the dbt project consumes.

This project reads **normalized** `training` tables (`orders`, `order_items`, …), not `training.v_lab_orders`. That Grafana reporting view is a different consumer path from Sessions 08–14.

---

## Step 5 — Trace the Example Model

Open:

```text
stacks/app/dbt/models/mart_sales_by_region.sql
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

Students can explain the purpose of the model without needing to write the SQL themselves.

### Tip

Focus on **data flow**, not line-by-line SQL syntax. Students already have SQL experience from earlier sessions.

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

Students understand the separation between source data and dbt-managed analytical outputs.

### Tip

Emphasize that this separation is particularly useful in a class lab environment. Do not use `DROP` or `TRUNCATE` against `training.*` objects.

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

Explain that the Core session is a walkthrough; students do not need to execute the commands themselves.

### Expected Result

Students can describe the purpose of each stage:

- **Source** — identifies input data.
- **Model** — defines transformation.
- **Run** — executes the transformation.
- **Test** — checks defined data assumptions.
- **Validate** — confirms the resulting database object.

---

## Step 8 — Review Testing

Open the existing project and check whether any dbt test definitions exist (for example a `schema.yml` next to models).

**Current lab project note:** the `stacks/app/dbt/` tree ships sources + `mart_sales_by_region.sql` but **does not yet include configured dbt tests**. Teach the *ideas* of common tests:

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

Students understand that successful SQL execution (`dbt run`) and data-quality validation (`dbt test`) are different checks — even when this lab project has not added YAML tests yet.

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

Ask students:

> Which transformation should be reusable across multiple analytical consumers?

Use the discussion to distinguish:

- Analytical transformation → dbt/database layer.
- Application-specific transformation → application layer.
- API response shaping → REST/OData layer.
- Presentation/query-specific transformation → Grafana.

### Expected Result

You should be able to explain why the same transformation should not automatically be duplicated in every consuming application.

---

# Stretch (optional) — shared demo
## Step 10 — Check the dbt Container

If the App VM Compose stack can start the optional profile, from the App compose directory run:

```bash
docker compose --profile dbt up -d dbt
```

Container name:

```text
lab-dbt
```

Then open a shell in the container (example):

```bash
docker compose --profile dbt exec dbt bash
```

Working directory inside the container should be the mounted project (`/dbt`).

### Expected Result

The `lab-dbt` container is available and can reach ClickHouse at the host configured in `profiles.yml` (default LAN `192.168.29.4:8123` via `CH_HOST`).

### Tip

If the profile or container is not available, stop the execution path and continue with the Core walkthrough. Do not modify unrelated services (Grafana, ClickHouse seed, gateway) during the session.

---

## Step 11 — Shared demo: `dbt run`
From the existing `lab-dbt` container, run:

```bash
dbt run
```

### Expected Result

The existing dbt models are processed using the configured ClickHouse connection.

The expected target area is:

```text
training_dbt
```

### Tip

Do not treat a successful command as proof that the data is correct. Follow it with testing and database validation.

---

## Step 12 — Shared demo: `dbt test`
After the model run completes, run:

```bash
dbt test
```

### Expected Result

If the project still has **no** test YAML, dbt may report that there is nothing to test — that is acceptable for this lab.

If tests were added later, configured assertions run against the built models.

### Tip

Do not invent or inventively “fix” missing tests by changing shared `training` data. Prefer discussing what a `not_null` / `unique` test on `region` would mean for `mart_sales_by_region`.

---

## Step 13 — Validate the Result in ClickHouse

Use CloudBeaver to inspect the target schema:

```text
training_dbt
```

Locate the model generated from:

```text
models/mart_sales_by_region.sql
```

Review the resulting columns and sample records.

### Expected Result

Confirm that the dbt model has produced an analytical object in the `training_dbt` schema without modifying the source tables in `training`.

### Tip

The CloudBeaver validation is an optional Stretch activity. Do not make student access to CloudBeaver or direct database execution a prerequisite for completing Core.

---

# Lab Checklist

Students should be able to explain:

- [ ] What dbt is.
- [ ] What analytics engineering means.
- [ ] The purpose of `dbt_project.yml`.
- [ ] The purpose of `profiles.yml`.
- [ ] What a dbt source represents.
- [ ] The four source tables used by this project.
- [ ] What a dbt model represents.
- [ ] The purpose of `mart_sales_by_region.sql`.
- [ ] The difference between source data and target models.
- [ ] The purpose of `dbt run`.
- [ ] The purpose of `dbt test`.
- [ ] Why dbt outputs are separated into `training_dbt`.
- [ ] When transformation may belong in dbt versus the application, API, or Grafana layer.
