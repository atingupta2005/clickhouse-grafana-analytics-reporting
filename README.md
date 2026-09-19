# ClickHouse and Grafana — Training Materials

Classroom materials for analytics and reporting with ClickHouse and Grafana.

## Lab access

**Lab home (HTTPS):** https://vmclickhouse.canadacentral.cloudapp.azure.com/

| App | URL |
|-----|-----|
| Lab home | https://vmclickhouse.canadacentral.cloudapp.azure.com/ |
| Grafana | https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/ |
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| REST API | https://vmclickhouse.canadacentral.cloudapp.azure.com/api |
| OData | https://vmclickhouse.canadacentral.cloudapp.azure.com/odata |

Login details for class tools are provided at the start of the course.

More URL notes: [`docs/ACCESS.md`](docs/ACCESS.md)

## Course outline

See [`course-content.md`](course-content.md) for modules, sessions, topics, and timing.

## Sessions

Each session folder has:

| File | Purpose |
|------|---------|
| `README.md` | Overview, timing, Core vs Stretch |
| `notes.md` | Teaching notes and concepts |
| `lab.md` | Guided hands-on steps |

| # | Folder |
|---|--------|
| 01 | [`sessions/01-architecture-and-data-modeling`](sessions/01-architecture-and-data-modeling/) |
| 02 | [`sessions/02-clickhouse-sql`](sessions/02-clickhouse-sql/) |
| 03 | [`sessions/03-advanced-clickhouse-sql`](sessions/03-advanced-clickhouse-sql/) |
| 04 | [`sessions/04-sql-server-to-clickhouse`](sessions/04-sql-server-to-clickhouse/) |
| 05 | [`sessions/05-clickhouse-optimization`](sessions/05-clickhouse-optimization/) |
| 06 | [`sessions/06-json-and-rest-api`](sessions/06-json-and-rest-api/) |
| 07 | [`sessions/07-odata`](sessions/07-odata/) |
| 08 | [`sessions/08-grafana-and-clickhouse`](sessions/08-grafana-and-clickhouse/) |
| 09 | [`sessions/09-grafana-rest-odata`](sessions/09-grafana-rest-odata/) |
| 10 | [`sessions/10-grafana-variables`](sessions/10-grafana-variables/) |
| 11 | [`sessions/11-advanced-odata-in-grafana`](sessions/11-advanced-odata-in-grafana/) |
| 12 | [`sessions/12-advanced-grafana-dashboards`](sessions/12-advanced-grafana-dashboards/) |
| 13 | [`sessions/13-reporting-dashboard-workshop`](sessions/13-reporting-dashboard-workshop/) |
| 14 | [`sessions/14-grafana-alerting`](sessions/14-grafana-alerting/) |
| 15 | [`sessions/15-dbt-for-clickhouse`](sessions/15-dbt-for-clickhouse/) |
| 16 | [`sessions/16-kafka-concepts`](sessions/16-kafka-concepts/) |

## How to use in class

1. Open the session `README.md`.
2. Follow `notes.md` for concepts.
3. When you see a **Checkpoint quiz** link, open it and submit once.
4. Complete the guided work in `lab.md`.

## Checkpoint quizzes

Short knowledge checks are linked inside each session `notes.md` after logical topics.

Quiz host: https://vmreact.eastus2.cloudapp.azure.com:18094

Use the class login shared by the trainer (prefer the Login tab). One attempt per quiz.

## Lab data reminders

- Reporting view: `training.v_lab_orders`
- Status filter: `Completed`
- Completed regions: **1, 3, 5** (region 2 + Completed is empty)
- Dates: **2023-01-01** … **2025-06-18**
- Prefer absolute Grafana time ranges (not “Last 30 days”)
