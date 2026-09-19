#!/usr/bin/env python3
"""Wire round-2 SVG heroes into notes (idempotent by asset filename)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "sessions"
MARK = "<!-- training-diagrams:v2 -->"


def block(alt: str, svg: str, mermaid: str | None = None) -> str:
    parts = [MARK, f"![{alt}](./assets/{svg})"]
    if mermaid:
        parts += ["", "Same idea in Mermaid (GitHub theme colors):", "", "```mermaid", mermaid.strip(), "```"]
    return "\n".join(parts)


def insert(path: Path, heading: str, blk: str) -> bool:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"\./assets/([\w-]+\.svg)", blk)
    if not m:
        return False
    name = m.group(1)
    if f"](./assets/{name})" in text:
        return False
    # resolve heading: exact, or unique startswith
    if heading not in text:
        cands = [ln.strip() for ln in text.splitlines() if ln.startswith("#") and heading.lstrip("# ").split()[0] in ln]
        # better: find line that equals ignoring unicode dashes
        found = None
        key = re.sub(r"[^a-z0-9]+", " ", heading.lower()).strip()
        for ln in text.splitlines():
            if not ln.startswith("#"):
                continue
            k2 = re.sub(r"[^a-z0-9]+", " ", ln.lower()).strip()
            if key in k2 or k2.endswith(key.split(" ", 1)[-1] if " " in key else key):
                # prefer numbered match
                if any(tok in k2 for tok in key.split()[:3]):
                    found = ln.strip()
                    if key[:12] in k2:
                        break
        if not found:
            print(f"  MISS heading {heading!r} in {path.name}")
            return False
        heading = found
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
    print(f"OK {path.parent.name}/{path.name} <- {name}")
    return True


def main() -> None:
    jobs = [
        ("02-clickhouse-sql", "## 3. ORDER BY", "SQL ORDER BY vs MergeTree ORDER BY", "orderby-sql-vs-mergetree.svg", None),
        ("02-clickhouse-sql", "## 10. Date and Time Functions", "Half-open date ranges", "date-half-open.svg",
         "flowchart LR\n    A[\">= start\"] --> B[\"< end\"]\n    B --> C[Safe month bucket]"),
        ("03-advanced-clickhouse-sql", "## 7. Window Functions", "Window function on sample rows", "window-anatomy-rows.svg",
         "flowchart TB\n    R[Detail rows] --> P[PARTITION BY region]\n    P --> W[sum OVER window]\n    W --> O[Same rows + region_sales]"),
        ("03-advanced-clickhouse-sql", "## 7. Window Functions", "GROUP BY vs window", "groupby-vs-window.svg", None),
        ("03-advanced-clickhouse-sql", "## 9. Running Totals", "Running total over dates", "running-total.svg", None),
        ("03-advanced-clickhouse-sql", "## 5. CTEs", "CTE vs subquery", "cte-vs-subquery.svg", None),
        ("03-advanced-clickhouse-sql", "# 5. CTEs", "CTE vs subquery", "cte-vs-subquery.svg", None),
        ("05-clickhouse-optimization", "## 11. EXPLAIN", "EXPLAIN mental model", "explain-layers.svg",
         "flowchart LR\n    A[Parts] --> B[Columns]\n    B --> C[Filter]\n    C --> D[Aggregate]\n    D --> E[Result]"),
        ("05-clickhouse-optimization", "## 4. Partitioning", "Partition prune vs sort-key skip", "partition-prune-vs-skip.svg", None),
        ("07-odata", "## 14. `$skip`", "$skip/$top on ordered rows", "odata-skip-top-window.svg", None),
        ("07-odata", "## 20. Pagination", "$skip/$top on ordered rows", "odata-skip-top-window.svg", None),
        ("08-grafana-and-clickhouse", "## 18. Query Validation", "Empty vs broken query", "empty-vs-broken.svg", None),
        ("10-grafana-variables", "## 7. Variable formatting", "Variable expansion in ClickHouse", "variable-expansion.svg", None),
        ("10-grafana-variables", "## 6. Multi-value and the All option", "Multi-value equals vs IN", "equals-vs-in.svg", None),
        ("11-advanced-odata-in-grafana", "## 6. Multi-Value Variables", "Multi-value to OData OR chain", "odata-or-chain.svg", None),
        ("11-advanced-odata-in-grafana", "## 10. `$top` and `$skip`", "$skip is not a page number", "skip-vs-page.svg", None),
        ("12-advanced-grafana-dashboards", "## 12. Drill-Down Design", "Drill-down navigation", "drilldown-map.svg",
         "flowchart LR\n    A[Overview] --> B[Click region]\n    B --> C[Detail dash]\n    C --> D[Table]"),
        ("13-reporting-dashboard-workshop", "## 2. Choosing the Reporting Data Source", "ClickHouse vs OData chooser", "ch-vs-odata-chooser.svg", None),
        ("14-grafana-alerting", "## 6. Pending State", "Alert state transitions", "alert-state-machine.svg", None),
        ("14-grafana-alerting", "## 7. No-Data Handling", "Zero vs NoData vs Error", "zero-nodata-error.svg", None),
        ("15-dbt-for-clickhouse", "## 8. Transformation Example", "dbt model DAG to mart", "model-dag-mart.svg", None),
        ("15-dbt-for-clickhouse", "## 6. Model Materialization", "Materialization types", "materialization-types.svg", None),
        ("16-kafka-concepts", "## 7. Consumer Groups", "Consumer group partitions and offsets", "consumer-group-offsets.svg", None),
        ("16-kafka-concepts", "## 7. Consumer Groups", "Two consumer groups on one topic", "two-consumer-groups.svg", None),
    ]
    # Discover real headings for CTEs / Running Totals in S03
    n3 = (SESSIONS / "03-advanced-clickhouse-sql" / "notes.md").read_text(encoding="utf-8")
    for ln in n3.splitlines():
        if ln.startswith("#") and "CTE" in ln:
            print("S03 CTE heading:", repr(ln))
        if ln.startswith("#") and "Running" in ln:
            print("S03 Running heading:", repr(ln))

    ok = 0
    for sess, heading, alt, svg, mm in jobs:
        path = SESSIONS / sess / "notes.md"
        if insert(path, heading, block(alt, svg, mm)):
            ok += 1
    print(f"Inserted {ok}")


if __name__ == "__main__":
    main()
