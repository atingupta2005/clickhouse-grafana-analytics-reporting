#!/usr/bin/env python3
"""Wire SVG heroes into sessions 02-16 using exact H2 headings (idempotent)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "sessions"
MARK = "<!-- training-diagrams:v1 -->"


def block(alt: str, svg: str, mermaid: str | None = None) -> str:
    parts = [MARK, f"![{alt}](./assets/{svg})"]
    if mermaid:
        parts += ["", "Same idea in Mermaid (GitHub theme colors):", "", "```mermaid", mermaid.strip(), "```"]
    return "\n".join(parts)


def insert(path: Path, heading: str, blk: str) -> bool:
    if not path.exists():
        print(f"  missing file {path}")
        return False
    text = path.read_text(encoding="utf-8")
    m = re.search(r"\./assets/([\w-]+\.svg)", blk)
    if m and f"](./assets/{m.group(1)})" in text:
        return False
    if heading not in text:
        print(f"  heading not found: {heading!r} in {path.relative_to(ROOT)}")
        return False
    # insert after heading line
    lines = text.splitlines(keepends=True)
    out = []
    done = False
    for line in lines:
        out.append(line)
        if not done and line.rstrip("\r\n") == heading:
            out.append("\n")
            out.append(blk.rstrip() + "\n\n")
            done = True
    if not done:
        return False
    path.write_text("".join(out), encoding="utf-8", newline="\n")
    return True


def patch_files_table(readme: Path) -> None:
    text = readme.read_text(encoding="utf-8")
    if "| `assets/` |" in text or "Diagrams live under `assets/`" in text:
        return
    for old, new in [
        (
            "| `lab.md` | Guided hands-on lab |",
            "| `lab.md` | Guided hands-on lab |\n| `assets/` | Colorful SVG diagrams (plus Mermaid in Markdown) |",
        ),
        (
            "| `lab.md` | Hands-on lab |",
            "| `lab.md` | Hands-on lab |\n| `assets/` | Colorful SVG diagrams (plus Mermaid in Markdown) |",
        ),
    ]:
        if old in text:
            readme.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
            return
    if "## Files" in text:
        readme.write_text(
            text.replace(
                "## Files",
                "## Files\n\nDiagrams live under `assets/` (SVG heroes) and as Mermaid blocks in the Markdown.\n",
                1,
            ),
            encoding="utf-8",
            newline="\n",
        )


def main() -> None:
    jobs = [
        # session, relfile, heading, alt, svg, mermaid?
        ("02-clickhouse-sql", "notes.md", "## 1. SELECT", "ClickHouse SELECT clause order", "sql-clause-pipeline.svg",
         "flowchart LR\n    A[FROM] --> B[WHERE]\n    B --> C[GROUP BY]\n    C --> D[HAVING]\n    D --> E[ORDER BY]\n    E --> F[LIMIT]"),
        ("02-clickhouse-sql", "notes.md", "## 2. WHERE", "WHERE vs HAVING", "where-vs-having.svg", None),
        ("02-clickhouse-sql", "notes.md", "# 6. Aggregate Functions", "From rows to a KPI", "aggregation-funnel.svg", None),
        ("02-clickhouse-sql", "notes.md", "## 6. Aggregate Functions", "From rows to a KPI", "aggregation-funnel.svg", None),
        ("02-clickhouse-sql", "README.md", "## Session Overview", "ClickHouse SELECT clause order", "sql-clause-pipeline.svg", None),

        ("03-advanced-clickhouse-sql", "notes.md", "## 1. Working with Multiple Tables", "Joins build a reporting row", "join-to-report.svg",
         "flowchart LR\n    O[Orders] --> J[JOIN]\n    C[Customers] --> J\n    P[Products] --> J\n    J --> R[Report row]"),
        ("03-advanced-clickhouse-sql", "notes.md", "## 2. INNER JOIN", "INNER JOIN vs LEFT JOIN", "inner-vs-left.svg", None),
        ("03-advanced-clickhouse-sql", "notes.md", "## 7. Window Functions", "Window function mental model", "window-frame.svg", None),
        ("03-advanced-clickhouse-sql", "notes.md", "# 7. Window Functions", "Window function mental model", "window-frame.svg", None),
        ("03-advanced-clickhouse-sql", "README.md", "## Session Overview", "Joins build a reporting row", "join-to-report.svg", None),

        ("04-sql-server-to-clickhouse", "notes.md", "## 1. SQL Server and ClickHouse", "SQL Server to ClickHouse migration", "migration-pipeline.svg",
         "flowchart LR\n    A[Identify] --> B[Map types]\n    B --> C[Rewrite]\n    C --> D[Run]\n    D --> E[Validate]"),
        ("04-sql-server-to-clickhouse", "notes.md", "## 2. Common Syntax Differences", "Common dialect swaps", "dialect-cheats.svg", None),
        ("04-sql-server-to-clickhouse", "notes.md", "## 13. Query Validation", "Session 04 lab topology", "dual-engine-lab.svg", None),
        ("04-sql-server-to-clickhouse", "README.md", "## Migration Approach", "SQL Server to ClickHouse migration", "migration-pipeline.svg", None),

        ("05-clickhouse-optimization", "notes.md", "## 1. Why Query Performance Matters", "Optimization loop", "optimize-loop.svg",
         "flowchart LR\n    A[Baseline] --> B[EXPLAIN]\n    B --> C[Bottleneck]\n    C --> D[Rewrite]\n    D --> E[Compare]"),
        ("05-clickhouse-optimization", "notes.md", "## 3. Sorting Keys", "Sort key alignment", "sortkey-alignment.svg", None),
        ("05-clickhouse-optimization", "notes.md", "## 5. Data Skipping", "Data skipping concept", "data-skipping.svg", None),
        ("05-clickhouse-optimization", "README.md", "## Optimization Flow", "Optimization loop", "optimize-loop.svg", None),

        ("06-json-and-rest-api", "notes.md", "## 1. JSON", "REST JSON into a report shape", "rest-json-report.svg",
         "flowchart LR\n    A[Client] --> B[REST API]\n    B --> C[JSON]\n    C --> D[Extract]\n    D --> E[Report]"),
        ("06-json-and-rest-api", "notes.md", "## 2. JSON Objects", "JSON envelope vs flat rows", "json-envelope.svg", None),
        ("06-json-and-rest-api", "notes.md", "## 16. Pagination", "Pagination walk", "pagination.svg", None),
        ("06-json-and-rest-api", "README.md", "## Session Overview", "REST JSON into a report shape", "rest-json-report.svg", None),

        ("07-odata", "notes.md", "## 1. What is OData?", "OData query pipeline", "odata-pipeline.svg",
         "flowchart LR\n    A[Service] --> B[Entity set]\n    B --> C[Query options]\n    C --> D[JSON value]\n    D --> E[App]"),
        ("07-odata", "notes.md", "## 2. OData and REST", "REST vs OData", "rest-vs-odata.svg", None),
        ("07-odata", "notes.md", "## 17. Combining Query Options", "OData option toolbox", "odata-options.svg", None),
        ("07-odata", "README.md", "## Session Overview", "OData query pipeline", "odata-pipeline.svg", None),

        ("08-grafana-and-clickhouse", "notes.md", "## 1. What is Grafana?", "ClickHouse to Grafana panel", "grafana-ch-flow.svg",
         "flowchart LR\n    A[(ClickHouse)] --> B[Data source]\n    B --> C[SQL panel]\n    C --> D[Visualization]\n    D --> E[Dashboard]"),
        ("08-grafana-and-clickhouse", "notes.md", "## 8. Time Ranges", "Seed-friendly time range", "time-range-seed.svg", None),
        ("08-grafana-and-clickhouse", "notes.md", "## 10. Explore", "Explore vs Dashboard", "explore-vs-dashboard.svg", None),
        ("08-grafana-and-clickhouse", "README.md", "## Session Overview", "ClickHouse to Grafana panel", "grafana-ch-flow.svg", None),

        ("09-grafana-rest-odata", "notes.md", "## 1. API-Based Reporting", "API data into Grafana Infinity", "infinity-architecture.svg",
         "flowchart LR\n    A[API] --> B[JSON]\n    B --> C[Infinity DS]\n    C --> D[Root path]\n    D --> E[Panel]"),
        ("09-grafana-rest-odata", "notes.md", "## 2. REST API and OData", "Root selector fork", "root-data-vs-value.svg", None),
        ("09-grafana-rest-odata", "notes.md", "## 22. End-to-End Reporting Flow", "Same KPI two sources", "same-kpi-two-sources.svg", None),
        ("09-grafana-rest-odata", "README.md", "## Reporting Flow", "API data into Grafana Infinity", "infinity-architecture.svg", None),

        ("10-grafana-variables", "notes.md", "## 1. Why variables?", "Variables drive the panel query", "variable-to-panel.svg",
         "flowchart LR\n    A[Variable] --> B[UI pick]\n    B --> C[Expand]\n    C --> D[Query]\n    D --> E[Panel]"),
        ("10-grafana-variables", "notes.md", "## 6. Multi-value and the All option", "Multi-value expansion", "multivalue-ch-vs-odata.svg", None),
        ("10-grafana-variables", "notes.md", "## 9. Dependencies and cascading", "Cascading variables", "cascade-region-plant.svg", None),
        ("10-grafana-variables", "README.md", "## Session Overview", "Variables drive the panel query", "variable-to-panel.svg", None),

        ("11-advanced-odata-in-grafana", "notes.md", "## 1. Session Flow", "Build a dynamic OData URL", "odata-url-build.svg", None),
        ("11-advanced-odata-in-grafana", "notes.md", "## 5. Multiple Filter Conditions", "Combine filter clauses", "filter-and-or.svg", None),
        ("11-advanced-odata-in-grafana", "notes.md", "## 13. Empty Results", "Intentional empty result Region 2", "empty-region2.svg", None),
        ("11-advanced-odata-in-grafana", "README.md", "## Overview", "Build a dynamic OData URL", "odata-url-build.svg", None),

        ("12-advanced-grafana-dashboards", "notes.md", "## 1. Dashboard Organization", "Dashboard reading order", "dashboard-reading-order.svg",
         "flowchart LR\n    A[KPI row] --> B[Trend]\n    B --> C[Compare]\n    C --> D[Detail]"),
        ("12-advanced-grafana-dashboards", "notes.md", "## 2. Choosing Panel Types", "Match viz to the question", "panel-purpose-map.svg", None),
        ("12-advanced-grafana-dashboards", "notes.md", "## 7. Transformations", "Transform pipeline", "transform-pipeline.svg", None),
        ("12-advanced-grafana-dashboards", "README.md", "## Session Overview", "Dashboard reading order", "dashboard-reading-order.svg", None),

        ("13-reporting-dashboard-workshop", "notes.md", "## 1. Reporting Requirements → Dashboard Design", "Workshop pipeline", "workshop-pipeline.svg",
         "flowchart LR\n    A[Requirements] --> B[KPIs]\n    B --> C[Queries]\n    C --> D[Variables]\n    D --> E[Panels]\n    E --> F[Validate]"),
        ("13-reporting-dashboard-workshop", "notes.md", "## 3. KPI Design", "Core KPI set", "kpi-card-set.svg", None),
        ("13-reporting-dashboard-workshop", "notes.md", "## 14. Validation", "Validation checklist", "validation-checklist.svg", None),
        ("13-reporting-dashboard-workshop", "README.md", "## Session Overview", "Workshop pipeline", "workshop-pipeline.svg", None),

        ("14-grafana-alerting", "notes.md", "## 1. Grafana Alerting Overview", "Alert lifecycle", "alert-lifecycle.svg",
         "flowchart LR\n    A[Query] --> B[Rule]\n    B --> C[Evaluate]\n    C --> D[Contact]\n    D --> E[Webhook]"),
        ("14-grafana-alerting", "notes.md", "## 6. Pending State", "Alert states", "alert-states.svg", None),
        ("14-grafana-alerting", "notes.md", "## 13. Generic Webhooks", "Webhook notification path", "webhook-path.svg", None),
        ("14-grafana-alerting", "README.md", "## Session Overview", "Alert lifecycle", "alert-lifecycle.svg", None),

        ("15-dbt-for-clickhouse", "notes.md", "## 1. dbt and Analytics Engineering", "dbt workflow", "dbt-workflow.svg",
         "flowchart LR\n    A[Sources] --> B[Models]\n    B --> C[dbt run]\n    C --> D[Tests]\n    D --> E[Validate]"),
        ("15-dbt-for-clickhouse", "notes.md", "## 4. Sources", "Source vs model", "source-vs-model.svg", None),
        ("15-dbt-for-clickhouse", "notes.md", "## 14. Where Should Transformation Happen?", "Where transforms should live", "transform-layers.svg", None),
        ("15-dbt-for-clickhouse", "README.md", "## Session Overview", "dbt workflow", "dbt-workflow.svg", None),

        ("16-kafka-concepts", "notes.md", "## 1. Why Kafka?", "Kafka into ClickHouse analytics", "kafka-to-clickhouse.svg",
         "flowchart LR\n    A[Producer] --> B[Topic]\n    B --> C[Consumer]\n    C --> D[(ClickHouse)]\n    D --> E[Grafana]"),
        ("16-kafka-concepts", "notes.md", "## 4. Partitions", "Topic and partitions", "topic-partitions.svg", None),
        ("16-kafka-concepts", "notes.md", "## 15. When Kafka Is Required", "When Kafka helps", "when-kafka.svg", None),
        ("16-kafka-concepts", "README.md", "## Session Overview", "Kafka into ClickHouse analytics", "kafka-to-clickhouse.svg", None),
    ]

    ok = 0
    for session, rel, heading, alt, svg, mm in jobs:
        path = SESSIONS / session / rel
        if insert(path, heading, block(alt, svg, mm)):
            ok += 1
            print(f"OK {session}/{rel}")

    for d in SESSIONS.iterdir():
        if d.is_dir() and not d.name.startswith("01"):
            r = d / "README.md"
            if r.exists():
                patch_files_table(r)

    print(f"Inserted {ok} blocks")


if __name__ == "__main__":
    main()
