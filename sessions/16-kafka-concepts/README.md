# Session 16 — Kafka Concepts and Kafka Jobs

**Duration:** 3 hours

## Overview

Understand Kafka as an event-streaming layer and where it fits before ClickHouse analytics and Grafana reporting.

![Kafka into ClickHouse analytics](./assets/kafka-to-clickhouse.svg)

## Topics

* Topics, partitions, producers, consumers, consumer groups
* Events / JSON messages
* Kafka → ClickHouse flow
* When Kafka helps — and when it is not needed

## Hands-on

* Walk through an order-event example end to end
* Trace partitions and consumer groups
* Relate Kafka to ClickHouse (`training.v_lab_orders`) and Grafana

**Core:** concepts + architecture walkthrough (no produce/consume exercise required) 

**Stretch:** optional Redpanda profile walkthrough when available

Reporting still reads ClickHouse; Grafana does not query Kafka in Core.

## Checkpoint quizzes

After each topic block in `notes.md`, open the matching quiz and submit once. Class login is shared in class. Prefer **Login**. One attempt.

| After topic | Quiz |
|-------------|------|
| Kafka concepts | [ch-grafana-s16-kafka-basics](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s16-kafka-basics) |
| Kafka vs ClickHouse reporting | [ch-grafana-s16-kafka-vs-reporting](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s16-kafka-vs-reporting) |
| Architecture wrap | [ch-grafana-s16-wrap](https://vmreact.eastus2.cloudapp.azure.com:18094/a/ch-grafana-s16-wrap) |

## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided walkthrough |
| `assets/` | Diagrams |
