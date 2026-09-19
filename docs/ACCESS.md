# Student lab access

**Primary entry (HTTPS):** https://vmclickhouse.canadacentral.cloudapp.azure.com/

`http://20.151.116.123/` redirects to the same HTTPS site.

## Applications

| App | URL |
|-----|-----|
| Lab home | https://vmclickhouse.canadacentral.cloudapp.azure.com/ |
| Health | https://vmclickhouse.canadacentral.cloudapp.azure.com/healthz |
| Grafana | https://vmclickhouse.canadacentral.cloudapp.azure.com/grafana/ |
| CloudBeaver | https://vmclickhouse.canadacentral.cloudapp.azure.com/cloudbeaver/ |
| REST API | https://vmclickhouse.canadacentral.cloudapp.azure.com/api |
| OData | https://vmclickhouse.canadacentral.cloudapp.azure.com/odata/ |
| CMF demo | https://vmclickhouse.canadacentral.cloudapp.azure.com/cmf/plants |

Use the CloudBeaver path **`/cloudbeaver/`** (not the site-root `#/` UI alone).

## Sign-in

Usernames and passwords for Grafana, CloudBeaver, and ClickHouse are provided at the start of the course.

## Data used in labs

| Item | Value |
|------|-------|
| Database | `training` |
| Reporting view | `training.v_lab_orders` |
| Status in queries | `Completed` |
| Completed regions | 1, 3, 5 |
| Date range | 2023-01-01 … 2025-06-18 |

In Grafana, set an **absolute** time range to that date window when panels look empty.
