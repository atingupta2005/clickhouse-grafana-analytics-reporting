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


## Files

| File | Purpose |
|------|---------|
| `notes.md` | Concepts |
| `lab.md` | Guided walkthrough |
| `assets/` | Diagrams |
