#!/usr/bin/env python3
"""Generate UTF-8-safe colorful SVG heroes for sessions 02-16 (GitHub-compatible)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "sessions"

# Colors (ASCII hex only)
C = {
    "bg": "#f8fafc",
    "title": "#0f172a",
    "muted": "#64748b",
    "blue": "#2563eb",
    "orange": "#ea580c",
    "purple": "#7c3aed",
    "green": "#059669",
    "teal": "#0f766e",
    "amber": "#d97706",
    "slate": "#475569",
    "white": "#ffffff",
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def write_svg(path: Path, body: str, width: int = 920, height: int = 240) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">
{body}
</svg>
'''
    # Enforce ASCII-safe / UTF-8 clean (no C0 controls)
    cleaned = "".join(ch for ch in xml if ord(ch) >= 32 or ch in "\n\t")
    path.write_text(cleaned, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    bad = [b for b in raw if b < 32 and b not in (9, 10, 13)]
    if bad:
        raise SystemExit(f"control bytes in {path}: {bad[:5]}")


def box(x, y, w, h, fill, label, sub="", fs=14, sfs=11) -> str:
    lines = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}"/>',
        f'<text x="{x + w/2}" y="{y + h/2 - (6 if sub else 0)}" text-anchor="middle" fill="{C["white"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="{fs}" font-weight="700">{esc(label)}</text>',
    ]
    if sub:
        lines.append(
            f'<text x="{x + w/2}" y="{y + h/2 + 16}" text-anchor="middle" fill="#e2e8f0" '
            f'font-family="Segoe UI, Arial, sans-serif" font-size="{sfs}">{esc(sub)}</text>'
        )
    return "\n".join(lines)


def arrow_h(x1, x2, y) -> str:
    return (
        f'<path d="M{x1} {y} H{x2}" stroke="{C["muted"]}" stroke-width="3" fill="none" '
        f'marker-end="url(#arr)"/>'
    )


def arrow_v(x, y1, y2) -> str:
    return (
        f'<path d="M{x} {y1} V{y2}" stroke="{C["muted"]}" stroke-width="3" fill="none" '
        f'marker-end="url(#arr)"/>'
    )


def defs() -> str:
    return f'''  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="{C["muted"]}"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" rx="12" fill="{C["bg"]}"/>'''


def title(text: str, y: int = 32) -> str:
    return (
        f'<text x="460" y="{y}" text-anchor="middle" fill="{C["title"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="17" font-weight="700">{esc(text)}</text>'
    )


def footer(text: str, y: int = 220) -> str:
    return (
        f'<text x="460" y="{y}" text-anchor="middle" fill="{C["muted"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="12">{esc(text)}</text>'
    )


def flow_row(path: Path, heading: str, items: list[tuple[str, str, str]], foot: str, height=240):
    """items: (label, sub, color_key)"""
    n = len(items)
    gap = 18
    left = 36
    usable = 920 - left * 2 - gap * (n - 1)
    w = usable / n
    y = 70
    h = 90
    parts = [defs(), title(heading)]
    x = left
    for i, (lab, sub, col) in enumerate(items):
        parts.append(box(x, y, w, h, C[col], lab, sub))
        if i < n - 1:
            parts.append(arrow_h(x + w + 2, x + w + gap - 2, y + h / 2))
        x += w + gap
    parts.append(footer(foot, height - 20))
    write_svg(path, "\n".join(parts), height=height)


def two_panel(path: Path, heading: str, left_title: str, left_lines: list[str], left_color: str,
              right_title: str, right_lines: list[str], right_color: str, foot: str):
    parts = [defs(), title(heading)]
    # left card
    parts.append(f'<rect x="40" y="56" width="400" height="150" rx="12" fill="{C["white"]}" stroke="#cbd5e1"/>')
    parts.append(f'<rect x="40" y="56" width="400" height="40" rx="12" fill="{C[left_color]}"/>')
    parts.append(f'<rect x="40" y="80" width="400" height="16" fill="{C[left_color]}"/>')
    parts.append(
        f'<text x="240" y="82" text-anchor="middle" fill="{C["white"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700">{esc(left_title)}</text>'
    )
    yy = 120
    for line in left_lines:
        parts.append(
            f'<text x="60" y="{yy}" fill="#334155" font-family="Segoe UI, Arial, sans-serif" font-size="13">{esc(line)}</text>'
        )
        yy += 24
    # right card
    parts.append(f'<rect x="480" y="56" width="400" height="150" rx="12" fill="{C["white"]}" stroke="#cbd5e1"/>')
    parts.append(f'<rect x="480" y="56" width="400" height="40" rx="12" fill="{C[right_color]}"/>')
    parts.append(f'<rect x="480" y="80" width="400" height="16" fill="{C[right_color]}"/>')
    parts.append(
        f'<text x="680" y="82" text-anchor="middle" fill="{C["white"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700">{esc(right_title)}</text>'
    )
    yy = 120
    for line in right_lines:
        parts.append(
            f'<text x="500" y="{yy}" fill="#334155" font-family="Segoe UI, Arial, sans-serif" font-size="13">{esc(line)}</text>'
        )
        yy += 24
    parts.append(footer(foot, 230))
    write_svg(path, "\n".join(parts), height=250)


def main() -> None:
    specs: list[tuple[str, str, callable]] = []

    # ---- Session 02 ----
    s = SESSIONS / "02-clickhouse-sql" / "assets"
    flow_row(
        s / "sql-clause-pipeline.svg",
        "ClickHouse SELECT clause order",
        [
            ("FROM", "table / view", "slate"),
            ("WHERE", "filter rows", "blue"),
            ("GROUP BY", "buckets", "orange"),
            ("HAVING", "filter groups", "purple"),
            ("ORDER BY", "sort", "green"),
            ("LIMIT", "top N", "teal"),
        ],
        "Lab analytics use training.v_lab_orders",
        height=240,
    )
    two_panel(
        s / "where-vs-having.svg",
        "WHERE vs HAVING",
        "WHERE",
        ["Filters individual rows", "Before aggregation", "Example: status = Completed"],
        "blue",
        "HAVING",
        ["Filters groups", "After GROUP BY", "Example: sum(sales) > 10000"],
        "orange",
        "Use WHERE for row filters; HAVING for aggregate conditions",
    )
    flow_row(
        s / "aggregation-funnel.svg",
        "From rows to a KPI",
        [
            ("Many rows", "v_lab_orders", "blue"),
            ("GROUP BY", "region / month", "orange"),
            ("Aggregate", "sum / count / avg", "purple"),
            ("KPI result", "few numbers", "green"),
        ],
        "Analytical SQL reads many rows and returns a small result",
    )

    # ---- Session 03 ----
    s = SESSIONS / "03-advanced-clickhouse-sql" / "assets"
    flow_row(
        s / "join-to-report.svg",
        "Joins build a reporting row",
        [
            ("Orders", "fact", "blue"),
            ("Customers", "dim", "orange"),
            ("Products", "dim", "purple"),
            ("Plants", "dim", "amber"),
            ("Report", "wide row", "green"),
        ],
        "Lab shortcut: training.v_lab_orders already joins for reporting columns",
    )
    two_panel(
        s / "inner-vs-left.svg",
        "INNER JOIN vs LEFT JOIN",
        "INNER JOIN",
        ["Only matching rows", "Drops orphans", "Strict matches"],
        "blue",
        "LEFT JOIN",
        ["Keeps left-side rows", "NULLs if no match", "Useful for gaps"],
        "green",
        "Pick the join that matches the business question",
    )
    flow_row(
        s / "window-frame.svg",
        "Window function mental model",
        [
            ("Partition", "e.g. region", "blue"),
            ("Order", "e.g. date", "orange"),
            ("Frame", "running window", "purple"),
            ("Result", "rank / total", "green"),
        ],
        "Windows calculate across related rows without collapsing the grain",
    )

    # ---- Session 04 ----
    s = SESSIONS / "04-sql-server-to-clickhouse" / "assets"
    flow_row(
        s / "migration-pipeline.svg",
        "SQL Server to ClickHouse migration",
        [
            ("Identify", "SS query", "slate"),
            ("Map types", "dialect", "blue"),
            ("Rewrite", "ClickHouse SQL", "orange"),
            ("Run", "on lab CH", "purple"),
            ("Validate", "compare", "green"),
        ],
        "Same business question - different engine syntax and types",
    )
    two_panel(
        s / "dialect-cheats.svg",
        "Common dialect swaps",
        "SQL Server",
        ["TOP n", "ISNULL(a, b)", "CONVERT(date, x)", "GETDATE()"],
        "blue",
        "ClickHouse",
        ["LIMIT n", "coalesce(a, b)", "toDate(x) / CAST", "now() / today()"],
        "green",
        "Rewrite functions; do not paste T-SQL unchanged",
    )
    flow_row(
        s / "dual-engine-lab.svg",
        "Session 04 lab topology",
        [
            ("CloudBeaver", "SQL client", "slate"),
            ("SQL Server", "TrainingDB", "blue"),
            ("ClickHouse", "training view", "green"),
            ("Compare", "results", "orange"),
        ],
        "Use the provisioned CloudBeaver connections for each engine",
    )

    # ---- Session 05 ----
    s = SESSIONS / "05-clickhouse-optimization" / "assets"
    flow_row(
        s / "optimize-loop.svg",
        "Optimization loop",
        [
            ("Baseline", "time / rows", "slate"),
            ("EXPLAIN", "plan", "blue"),
            ("Bottleneck", "read / join", "orange"),
            ("Rewrite", "filter / key", "purple"),
            ("Compare", "faster?", "green"),
        ],
        "Measure before and after - do not guess",
    )
    two_panel(
        s / "sortkey-alignment.svg",
        "Sort key alignment (live seed)",
        "Aligned filters",
        ["order_date first", "then plant_id", "Helps skipping"],
        "green",
        "Misaligned filters",
        ["region_id only", "Not leading key", "More data scanned"],
        "orange",
        "Live training.orders key: (order_date, plant_id, order_id)",
    )
    flow_row(
        s / "data-skipping.svg",
        "Data skipping (concept)",
        [
            ("Query filter", "date range", "blue"),
            ("Index marks", "granules", "orange"),
            ("Skip blocks", "not needed", "purple"),
            ("Read less", "faster", "green"),
        ],
        "Good ORDER BY and tight filters reduce bytes read",
    )

    # ---- Session 06 ----
    s = SESSIONS / "06-json-and-rest-api" / "assets"
    flow_row(
        s / "rest-json-report.svg",
        "REST JSON into a report shape",
        [
            ("Client", "browser / app", "slate"),
            ("REST API", "/api/...", "blue"),
            ("JSON", "envelope", "orange"),
            ("Extract", "fields", "purple"),
            ("Report", "rows / KPI", "green"),
        ],
        "Lab REST: https://vmclickhouse.../api",
    )
    two_panel(
        s / "json-envelope.svg",
        "JSON envelope vs flat rows",
        "Envelope",
        ['{ "data": [ ... ],', '  "count": N }', "Root often: data"],
        "blue",
        "Flat array",
        ["[ {row}, {row} ]", "No wrapper", "Root: $ or empty"],
        "green",
        "Know the root path before parsing in Grafana Infinity",
    )
    flow_row(
        s / "pagination.svg",
        "Pagination walk",
        [
            ("page=1", "first slice", "blue"),
            ("page=2", "next slice", "orange"),
            ("page=3", "next slice", "purple"),
            ("Done", "no more", "green"),
        ],
        "Lab REST uses page and page_size (not always offset)",
    )

    # ---- Session 07 ----
    s = SESSIONS / "07-odata" / "assets"
    flow_row(
        s / "odata-pipeline.svg",
        "OData query pipeline",
        [
            ("Service", "/odata", "slate"),
            ("Entity set", "Orders", "blue"),
            ("$ options", "filter/select", "orange"),
            ("JSON", "value[]", "purple"),
            ("App", "consume", "green"),
        ],
        "Lab OData root collection uses value (not data)",
    )
    two_panel(
        s / "rest-vs-odata.svg",
        "REST vs OData",
        "REST",
        ["Custom query params", "Flexible shapes", "App-specific"],
        "blue",
        "OData",
        ["Standard $filter etc.", "Metadata-aware", "Uniform options"],
        "green",
        "Same lab data - different query language on the wire",
    )
    flow_row(
        s / "odata-options.svg",
        "OData option toolbox",
        [
            ("$filter", "which rows", "blue"),
            ("$select", "which cols", "orange"),
            ("$orderby", "sort", "purple"),
            ("$top/$skip", "page", "amber"),
            ("$count", "totals", "green"),
        ],
        "$expand / $search are theory-only in this lab (not Core)",
    )

    # ---- Session 08 ----
    s = SESSIONS / "08-grafana-and-clickhouse" / "assets"
    flow_row(
        s / "grafana-ch-flow.svg",
        "ClickHouse to Grafana panel",
        [
            ("ClickHouse", "v_lab_orders", "green"),
            ("Data source", "provisioned", "blue"),
            ("SQL panel", "query", "orange"),
            ("Visualization", "stat / chart", "purple"),
            ("Dashboard", "layout", "teal"),
        ],
        "Use absolute seed dates - not Last 30 days",
    )
    two_panel(
        s / "explore-vs-dashboard.svg",
        "Explore vs Dashboard",
        "Explore",
        ["Ad-hoc queries", "Quick checks", "Not the final report"],
        "blue",
        "Dashboard",
        ["Saved panels", "Shared layout", "Classroom deliverable"],
        "green",
        "Prototype in Explore; publish as a dashboard",
    )
    flow_row(
        s / "time-range-seed.svg",
        "Seed-friendly time range",
        [
            ("Seed start", "2023-01-01", "blue"),
            ("Seed end", "2025-06-18", "orange"),
            ("Absolute", "Grafana range", "purple"),
            ("Panels fill", "with data", "green"),
        ],
        "Relative Last 30 days is usually empty on this seed",
    )

    # ---- Session 09 ----
    s = SESSIONS / "09-grafana-rest-odata" / "assets"
    flow_row(
        s / "infinity-architecture.svg",
        "API data into Grafana (Infinity)",
        [
            ("API", "REST / OData", "blue"),
            ("JSON", "response", "orange"),
            ("Infinity DS", "provisioned", "purple"),
            ("Root path", "data / value", "amber"),
            ("Panel", "table / KPI", "green"),
        ],
        "Do not invent hosts - use the lab HTTPS FQDN",
    )
    two_panel(
        s / "root-data-vs-value.svg",
        "Root selector fork",
        "REST",
        ["Often root: data", "count may exist", "/api/..."],
        "blue",
        "OData",
        ["Root: value", "OData JSON", "/odata/..."],
        "green",
        "Wrong root = empty panel even when the URL works",
    )
    flow_row(
        s / "same-kpi-two-sources.svg",
        "Same KPI - two sources",
        [
            ("Question", "sales by region", "slate"),
            ("ClickHouse", "SQL panel", "green"),
            ("REST", "/api/sales", "blue"),
            ("Compare", "shape / totals", "orange"),
        ],
        "Validate both paths against the same seed rules",
    )

    # ---- Session 10 ----
    s = SESSIONS / "10-grafana-variables" / "assets"
    flow_row(
        s / "variable-to-panel.svg",
        "Variables drive the panel query",
        [
            ("Variable", "Region / Status", "blue"),
            ("Pick values", "UI dropdown", "orange"),
            ("Expand", "IN / or", "purple"),
            ("Query runs", "filtered", "green"),
            ("Panel", "updates", "teal"),
        ],
        "Multi-value formatting differs for ClickHouse vs OData",
    )
    flow_row(
        s / "cascade-region-plant.svg",
        "Cascading variables",
        [
            ("Region", "parent", "blue"),
            ("Plant query", "WHERE region", "orange"),
            ("Plant list", "filtered", "purple"),
            ("Panel SQL", "both vars", "green"),
        ],
        "Child variable query must reference the parent variable",
    )
    two_panel(
        s / "multivalue-ch-vs-odata.svg",
        "Multi-value expansion",
        "ClickHouse SQL",
        ["status IN (${status:sqlstring})", "region_id IN (${region})", "SQL list syntax"],
        "green",
        "OData $filter",
        ["RegionId eq 1 or RegionId eq 3", "Quoted strings for Status", "Not :sqlstring"],
        "blue",
        "Do not copy ClickHouse variable formats into OData filters",
    )

    # ---- Session 11 ----
    s = SESSIONS / "11-advanced-odata-in-grafana" / "assets"
    flow_row(
        s / "odata-url-build.svg",
        "Build a dynamic OData URL",
        [
            ("Base", "/odata/Orders", "slate"),
            ("$filter", "vars + dates", "blue"),
            ("$select", "columns", "orange"),
            ("$orderby", "sort", "purple"),
            ("Panel", "Infinity", "green"),
        ],
        "Keep Core filters to supported OData options only",
    )
    two_panel(
        s / "empty-region2.svg",
        "Intentional empty result",
        "Region 2 + Completed",
        ["Valid filter", "Zero matching rows", "Seed property"],
        "orange",
        "What to do",
        ["Do not invent data", "Teach empty panels", "Use 1 / 3 / 5 for demos"],
        "green",
        "Empty can be the correct answer on this seed",
    )
    flow_row(
        s / "filter-and-or.svg",
        "Combine filter clauses",
        [
            ("Region", "eq / or", "blue"),
            ("AND", "combine", "slate"),
            ("Status", "Completed", "orange"),
            ("AND", "combine", "slate"),
            ("Dates", "ge / lt", "green"),
        ],
        "Parentheses matter when mixing and / or",
    )

    # ---- Session 12 ----
    s = SESSIONS / "12-advanced-grafana-dashboards" / "assets"
    flow_row(
        s / "dashboard-reading-order.svg",
        "Dashboard reading order",
        [
            ("KPI row", "summary", "blue"),
            ("Trend", "time series", "orange"),
            ("Compare", "bar / region", "purple"),
            ("Detail", "table", "green"),
        ],
        "Top-left answers the main question first",
    )
    flow_row(
        s / "panel-purpose-map.svg",
        "Match viz to the question",
        [
            ("Stat", "one number", "blue"),
            ("Time series", "over time", "orange"),
            ("Bar", "categories", "purple"),
            ("Table", "rows", "green"),
        ],
        "Avoid chart junk - one panel, one job",
    )
    flow_row(
        s / "transform-pipeline.svg",
        "Transform pipeline",
        [
            ("Query", "raw rows", "slate"),
            ("Transform", "join / calc", "blue"),
            ("Field config", "units", "orange"),
            ("Display", "panel", "green"),
        ],
        "Prefer pushing heavy logic to SQL when possible",
    )

    # ---- Session 13 ----
    s = SESSIONS / "13-reporting-dashboard-workshop" / "assets"
    flow_row(
        s / "workshop-pipeline.svg",
        "Workshop pipeline",
        [
            ("Requirements", "questions", "slate"),
            ("KPIs", "metrics", "blue"),
            ("Queries", "SQL / API", "orange"),
            ("Variables", "filters", "purple"),
            ("Panels", "layout", "amber"),
            ("Validate", "seed rules", "green"),
        ],
        "Ship a coherent dashboard - not disconnected panels",
        height=250,
    )
    flow_row(
        s / "kpi-card-set.svg",
        "Core KPI set (example)",
        [
            ("Orders", "count", "blue"),
            ("Revenue", "sum sales", "orange"),
            ("High-value", "amount>=2000", "purple"),
            ("By region", "breakdown", "green"),
        ],
        "Completed status + absolute seed range",
    )
    flow_row(
        s / "validation-checklist.svg",
        "Validation checklist",
        [
            ("Region 2", "empty OK", "orange"),
            ("Dates", "absolute", "blue"),
            ("Status", "Completed", "purple"),
            ("Sources", "agree", "green"),
        ],
        "If validation fails, fix queries before polishing layout",
    )

    # ---- Session 14 ----
    s = SESSIONS / "14-grafana-alerting" / "assets"
    flow_row(
        s / "alert-lifecycle.svg",
        "Alert lifecycle",
        [
            ("Query", "KPI SQL", "blue"),
            ("Rule", "threshold", "orange"),
            ("Evaluate", "interval", "purple"),
            ("Contact", "point", "amber"),
            ("Webhook", "HTTP POST", "green"),
        ],
        "Demo with a threshold you can force true and false",
    )
    flow_row(
        s / "alert-states.svg",
        "Alert states",
        [
            ("Normal", "OK", "green"),
            ("Pending", "waiting", "amber"),
            ("Firing", "alert on", "orange"),
            ("NoData", "empty", "slate"),
            ("Error", "query fail", "purple"),
        ],
        "Pending reduces flapping from brief spikes",
    )
    flow_row(
        s / "webhook-path.svg",
        "Webhook notification path",
        [
            ("Rule fires", "state change", "orange"),
            ("Policy", "route", "blue"),
            ("Contact", "webhook", "purple"),
            ("Receiver", "HTTP endpoint", "green"),
        ],
        "Inspect the payload in the receiver logs during class",
    )

    # ---- Session 15 ----
    s = SESSIONS / "15-dbt-for-clickhouse" / "assets"
    flow_row(
        s / "dbt-workflow.svg",
        "dbt workflow",
        [
            ("Sources", "training.*", "blue"),
            ("Models", "SQL select", "orange"),
            ("dbt run", "build", "purple"),
            ("Tests", "assert", "amber"),
            ("Validate", "query mart", "green"),
        ],
        "Models land in training_dbt (lab convention)",
    )
    two_panel(
        s / "source-vs-model.svg",
        "Source vs model",
        "Source",
        ["Declared input", "Already exists", "training.orders etc."],
        "blue",
        "Model",
        ["dbt builds it", "SQL transformation", "training_dbt.mart_..."],
        "green",
        "Sources are inputs; models are outputs you materialize",
    )
    flow_row(
        s / "transform-layers.svg",
        "Where should transforms live?",
        [
            ("ClickHouse", "SQL / views", "green"),
            ("dbt", "versioned SQL", "blue"),
            ("App / API", "serving", "orange"),
            ("Grafana", "light only", "purple"),
        ],
        "Prefer dbt/CH for reusable analytics logic",
    )

    # ---- Session 16 ----
    s = SESSIONS / "16-kafka-concepts" / "assets"
    flow_row(
        s / "kafka-to-clickhouse.svg",
        "Kafka into ClickHouse analytics",
        [
            ("Producer", "events", "blue"),
            ("Topic", "log", "orange"),
            ("Consumer", "job", "purple"),
            ("ClickHouse", "INSERT", "green"),
            ("Grafana", "report", "teal"),
        ],
        "Streaming path when continuous ingest matters",
    )
    flow_row(
        s / "topic-partitions.svg",
        "Topic and partitions",
        [
            ("Topic", "orders", "slate"),
            ("Partition 0", "ordered", "blue"),
            ("Partition 1", "ordered", "orange"),
            ("Partition 2", "ordered", "purple"),
        ],
        "Key chooses partition; order is per partition",
    )
    two_panel(
        s / "when-kafka.svg",
        "When Kafka helps",
        "Good fit",
        ["Many producers", "Buffer / replay", "Decouple systems"],
        "green",
        "Often not needed",
        ["Batch file load", "Simple API pull", "Tiny lab demos"],
        "orange",
        "Choose Kafka for streaming needs - not by default",
    )

    print("Generated SVG heroes for sessions 02-16")


if __name__ == "__main__":
    main()
