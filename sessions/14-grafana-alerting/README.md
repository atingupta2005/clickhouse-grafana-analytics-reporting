# Session 14 — Grafana Alerting and Generic Webhooks

**Duration:** 4 hours

## Overview

Learn the Grafana alerting flow: **Query → Alert Rule → Evaluation → Contact Point → Webhook**, using ClickHouse on `training.v_lab_orders`.

![Alert lifecycle](./assets/alert-lifecycle.svg)

## Topics

* Alert rules, thresholds, evaluation, pending / no-data / errors
* Contact points and notification policies
* Generic webhooks and testing

## Hands-on

* Sign in as `student` / `StudentLab!2026` to inspect Alerting
* admin steps with `admin` / `GrafanaLab!2026` for rule and webhook setup
* Discuss KPI and no-data scenarios (including Region 2 + Completed)

**Core:** review UI → admin steps KPI alert → contact point / webhook → test discussion 

**Stretch:** recreate a simplified rule if your account allows saving alerts

**Seed:** Completed regions **1 / 3 / 5**; dates **2023-01-01** … **2025-06-18**

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| Alerting flow | [ch-grafana-s14-alert-flow](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s14-alert-flow) |
| Contact points and webhooks | [ch-grafana-s14-contacts-webhook](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s14-contacts-webhook) |
| Alerting lab checkpoint | [ch-grafana-s14-lab-checkpoint](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s14-lab-checkpoint) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided lab |
| `assets/` | Diagrams |
