#!/usr/bin/env python3
"""Extra high-value UTF-8 SVG heroes (round 2) for sessions 02-16."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "sessions"

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
    "red": "#dc2626",
    "white": "#ffffff",
    "soft": "#e2e8f0",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def write_svg(path: Path, body: str, w: int = 920, h: int = 280) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img">
{body}
</svg>
'''
    cleaned = "".join(ch for ch in xml if ord(ch) >= 32 or ch in "\n\t")
    path.write_text(cleaned, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    if any(b < 32 and b not in (9, 10, 13) for b in raw):
        raise SystemExit(f"controls in {path}")


def defs() -> str:
    return f'''  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="{C["muted"]}"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" rx="12" fill="{C["bg"]}"/>'''


def title(t: str, y: int = 28) -> str:
    return (
        f'<text x="460" y="{y}" text-anchor="middle" fill="{C["title"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="16" font-weight="700">{esc(t)}</text>'
    )


def footer(t: str, y: int) -> str:
    return (
        f'<text x="460" y="{y}" text-anchor="middle" fill="{C["muted"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="12">{esc(t)}</text>'
    )


def box(x, y, w, h, fill, label, sub="", fs=13, sfs=11):
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}"/>']
    cy = y + h / 2 - (6 if sub else 0)
    parts.append(
        f'<text x="{x+w/2}" y="{cy}" text-anchor="middle" fill="{C["white"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="{fs}" font-weight="700">{esc(label)}</text>'
    )
    if sub:
        parts.append(
            f'<text x="{x+w/2}" y="{cy+16}" text-anchor="middle" fill="#e2e8f0" '
            f'font-family="Segoe UI, Arial, sans-serif" font-size="{sfs}">{esc(sub)}</text>'
        )
    return "\n".join(parts)


def two_panel(path, heading, lt, ll, lc, rt, rl, rc, foot, h=260):
    parts = [defs(), title(heading)]
    parts.append(f'<rect x="40" y="50" width="400" height="165" rx="12" fill="{C["white"]}" stroke="#cbd5e1"/>')
    parts.append(f'<rect x="40" y="50" width="400" height="38" rx="12" fill="{C[lc]}"/>')
    parts.append(f'<rect x="40" y="72" width="400" height="16" fill="{C[lc]}"/>')
    parts.append(
        f'<text x="240" y="76" text-anchor="middle" fill="{C["white"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700">{esc(lt)}</text>'
    )
    yy = 112
    for line in ll:
        parts.append(
            f'<text x="60" y="{yy}" fill="#334155" font-family="Segoe UI, Arial, sans-serif" font-size="13">{esc(line)}</text>'
        )
        yy += 22
    parts.append(f'<rect x="480" y="50" width="400" height="165" rx="12" fill="{C["white"]}" stroke="#cbd5e1"/>')
    parts.append(f'<rect x="480" y="50" width="400" height="38" rx="12" fill="{C[rc]}"/>')
    parts.append(f'<rect x="480" y="72" width="400" height="16" fill="{C[rc]}"/>')
    parts.append(
        f'<text x="680" y="76" text-anchor="middle" fill="{C["white"]}" '
        f'font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700">{esc(rt)}</text>'
    )
    yy = 112
    for line in rl:
        parts.append(
            f'<text x="500" y="{yy}" fill="#334155" font-family="Segoe UI, Arial, sans-serif" font-size="13">{esc(line)}</text>'
        )
        yy += 22
    parts.append(footer(foot, h - 18))
    write_svg(path, "\n".join(parts), h=h)


def flow(path, heading, items, foot, h=240):
    n = len(items)
    gap = 16
    left = 28
    usable = 920 - left * 2 - gap * (n - 1)
    bw = usable / n
    y, bh = 70, 95
    parts = [defs(), title(heading)]
    x = left
    for i, (lab, sub, col) in enumerate(items):
        parts.append(box(x, y, bw, bh, C[col], lab, sub))
        if i < n - 1:
            parts.append(
                f'<path d="M{x+bw+2} {y+bh/2} H{x+bw+gap-2}" stroke="{C["muted"]}" stroke-width="3" fill="none" marker-end="url(#arr)"/>'
            )
        x += bw + gap
    parts.append(footer(foot, h - 18))
    write_svg(path, "\n".join(parts), h=h)


def window_anatomy(path: Path) -> None:
    """Concrete PARTITION / ORDER / result columns on sample rows."""
    parts = [defs(), title("Window function on sample rows")]
    # table header
    headers = ["order_id", "region", "amount", "region_sales (window)"]
    widths = [110, 100, 110, 220]
    x0, y0 = 80, 55
    x = x0
    for hdg, w in zip(headers, widths):
        parts.append(f'<rect x="{x}" y="{y0}" width="{w}" height="32" fill="{C["slate"]}"/>')
        parts.append(
            f'<text x="{x+w/2}" y="{y0+21}" text-anchor="middle" fill="{C["white"]}" '
            f'font-family="Segoe UI, Arial, sans-serif" font-size="12" font-weight="700">{esc(hdg)}</text>'
        )
        x += w
    rows = [
        ("1001", "1", "120", "500", C["blue"]),
        ("1002", "1", "380", "500", C["blue"]),
        ("2001", "3", "200", "350", C["green"]),
        ("2002", "3", "150", "350", C["green"]),
    ]
    y = y0 + 32
    for oid, reg, amt, tot, fill in rows:
        vals = [oid, reg, amt, tot]
        x = x0
        for i, (val, w) in enumerate(zip(vals, widths)):
            bg = fill if i == 3 else C["white"]
            fg = C["white"] if i == 3 else "#334155"
            stroke = fill if i < 3 else fill
            parts.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="28" fill="{bg}" stroke="{stroke}" stroke-width="1"/>'
            )
            parts.append(
                f'<text x="{x+w/2}" y="{y+19}" text-anchor="middle" fill="{fg}" '
                f'font-family="Segoe UI, Arial, sans-serif" font-size="12">{esc(val)}</text>'
            )
            x += w
        y += 28
    # callouts
    parts.append(box(70, 210, 200, 50, C["orange"], "PARTITION BY region", "groups rows", fs=12))
    parts.append(box(300, 210, 240, 50, C["purple"], "KEEP all order rows", "not collapsed", fs=12))
    parts.append(box(570, 210, 280, 50, C["teal"], "sum(...) OVER (...)", "region_sales column", fs=12))
    parts.append(footer("Unlike GROUP BY, every input row stays in the result", 280))
    write_svg(path, "\n".join(parts), h=300)


def running_total(path: Path) -> None:
    parts = [defs(), title("Running total over ordered dates")]
    # timeline boxes
    days = [("Day 1", "100", "100"), ("Day 2", "80", "180"), ("Day 3", "50", "230"), ("Day 4", "70", "300")]
    x = 60
    for i, (day, amt, run) in enumerate(days):
        parts.append(box(x, 60, 170, 70, C["blue"], day, f"+{amt}", fs=13))
        parts.append(
            f'<text x="{x+85}" y="160" text-anchor="middle" fill="{C["green"]}" '
            f'font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700">running = {run}</text>'
        )
        if i < len(days) - 1:
            parts.append(
                f'<path d="M{x+170+4} 95 H{x+200-4}" stroke="{C["muted"]}" stroke-width="3" fill="none" marker-end="url(#arr)"/>'
            )
        x += 200
    parts.append(
        f'<text x="460" y="200" text-anchor="middle" fill="#334155" font-family="Segoe UI, Arial, sans-serif" font-size="13">'
        f'{esc("sum(amount) OVER (ORDER BY day) grows as you move forward")}</text>'
    )
    parts.append(footer("Use ORDER BY inside OVER for cumulative metrics", 240))
    write_svg(path, "\n".join(parts), h=260)


def alert_machine(path: Path) -> None:
    parts = [defs(), title("Alert state transitions")]
    # nodes
    nodes = [
        (80, 90, "Normal", "green"),
        (320, 90, "Pending", "amber"),
        (560, 90, "Firing", "orange"),
        (200, 190, "NoData", "slate"),
        (480, 190, "Error", "red"),
    ]
    for x, y, lab, col in nodes:
        parts.append(box(x, y, 160, 55, C[col], lab, fs=14))
    # arrows as labeled lines
    parts.append(f'<path d="M240 117 H320" stroke="{C["muted"]}" stroke-width="2" marker-end="url(#arr)"/>')
    parts.append(
        f'<text x="270" y="108" fill="{C["muted"]}" font-family="Segoe UI, Arial, sans-serif" font-size="11">condition true</text>'
    )
    parts.append(f'<path d="M480 117 H560" stroke="{C["muted"]}" stroke-width="2" marker-end="url(#arr)"/>')
    parts.append(
        f'<text x="500" y="108" fill="{C["muted"]}" font-family="Segoe UI, Arial, sans-serif" font-size="11">pending met</text>'
    )
    parts.append(f'<path d="M560 145 L400 190" stroke="{C["muted"]}" stroke-width="2" marker-end="url(#arr)"/>')
    parts.append(f'<path d="M160 145 L240 190" stroke="{C["muted"]}" stroke-width="2" marker-end="url(#arr)"/>')
    parts.append(footer("Pending duration is not the same as evaluation interval", 270))
    write_svg(path, "\n".join(parts), h=290)


def odata_skip_top(path: Path) -> None:
    parts = [defs(), title("$skip / $top on an ordered result")]
    # row strip
    x0, y0 = 50, 70
    for i in range(12):
        x = x0 + i * 70
        fill = C["orange"] if 4 <= i < 8 else C["blue"]
        parts.append(f'<rect x="{x}" y="{y0}" width="64" height="50" rx="8" fill="{fill}"/>')
        parts.append(
            f'<text x="{x+32}" y="{y0+30}" text-anchor="middle" fill="{C["white"]}" '
            f'font-family="Segoe UI, Arial, sans-serif" font-size="12" font-weight="700">r{i+1}</text>'
        )
    parts.append(
        f'<text x="460" y="150" text-anchor="middle" fill="#334155" font-family="Segoe UI, Arial, sans-serif" font-size="13">'
        f'{esc("Orange window: $skip=4 and $top=4  (rows 5-8 after $orderby)")}</text>'
    )
    parts.append(box(120, 175, 280, 50, C["slate"], "$skip is an OFFSET", "not a page number", fs=13))
    parts.append(box(520, 175, 280, 50, C["green"], "Page 3 of size 10", "skip=20 top=10", fs=13))
    parts.append(footer("Always apply $orderby before relying on $skip/$top", 255))
    write_svg(path, "\n".join(parts), h=275)


def var_expand(path: Path) -> None:
    two_panel(
        path,
        "Variable expansion (ClickHouse)",
        "In the panel (template)",
        [
            "WHERE region_id IN (${region})",
            "  AND status IN (${status:sqlstring})",
        ],
        "blue",
        "After Grafana expands",
        [
            "WHERE region_id IN (1,3)",
            "  AND status IN ('Completed')",
        ],
        "green",
        "Multi-value must use IN (...) - not a single = comparison",
        h=250,
    )


def odata_or(path: Path) -> None:
    two_panel(
        path,
        "Multi-value becomes OData OR (not SQL IN)",
        "UI selection",
        ["Region = 1 and 3", "Status = Completed"],
        "orange",
        "OData $filter fragment",
        [
            "(RegionId eq 1 or RegionId eq 3)",
            "and Status eq 'Completed'",
        ],
        "green",
        "Do not paste ClickHouse :sqlstring / IN syntax into OData",
        h=250,
    )


def consumer_offsets(path: Path) -> None:
    parts = [defs(), title("Consumer group, partitions, and offsets")]
    parts.append(box(40, 60, 200, 70, C["slate"], "Topic orders", "3 partitions", fs=13))
    parts.append(box(280, 50, 160, 55, C["blue"], "P0", "offset 42", fs=13))
    parts.append(box(280, 115, 160, 55, C["orange"], "P1", "offset 17", fs=13))
    parts.append(box(280, 180, 160, 55, C["purple"], "P2", "offset 9", fs=13))
    parts.append(box(500, 50, 180, 55, C["green"], "Consumer A", "reads P0", fs=12))
    parts.append(box(500, 115, 180, 55, C["green"], "Consumer B", "reads P1", fs=12))
    parts.append(box(500, 180, 180, 55, C["green"], "Consumer C", "reads P2", fs=12))
    parts.append(box(720, 100, 160, 70, C["teal"], "Group G1", "shared progress", fs=13))
    for y in (77, 142, 207):
        parts.append(
            f'<path d="M440 {y} H500" stroke="{C["muted"]}" stroke-width="2" marker-end="url(#arr)"/>'
        )
    parts.append(footer("Lag = latest offset - committed offset (per partition)", 270))
    write_svg(path, "\n".join(parts), h=290)


def model_dag(path: Path) -> None:
    parts = [defs(), title("dbt model DAG to a sales mart")]
    sources = [("orders", 60), ("order_items", 230), ("plants", 400), ("regions", 570)]
    for name, x in sources:
        parts.append(box(x, 55, 150, 50, C["blue"], name, "source", fs=12))
    parts.append(box(280, 140, 280, 55, C["orange"], "join + clean", "staging / intermediate", fs=13))
    parts.append(box(300, 220, 240, 50, C["green"], "mart_sales_by_region", "training_dbt", fs=12))
    parts.append(
        f'<path d="M135 105 V140 H420" stroke="{C["muted"]}" stroke-width="2" fill="none"/>'
    )
    parts.append(
        f'<path d="M305 105 V140" stroke="{C["muted"]}" stroke-width="2" fill="none"/>'
    )
    parts.append(
        f'<path d="M475 105 V140" stroke="{C["muted"]}" stroke-width="2" fill="none"/>'
    )
    parts.append(
        f'<path d="M645 105 V140 H420" stroke="{C["muted"]}" stroke-width="2" fill="none"/>'
    )
    parts.append(
        f'<path d="M420 195 V220" stroke="{C["muted"]}" stroke-width="3" marker-end="url(#arr)"/>'
    )
    parts.append(footer("Sources are inputs; the mart is what dbt materializes", 290))
    write_svg(path, "\n".join(parts), h=310)


def main() -> None:
    # S02
    s = SESSIONS / "02-clickhouse-sql" / "assets"
    two_panel(
        s / "orderby-sql-vs-mergetree.svg",
        "Two different ORDER BY meanings",
        "SELECT ... ORDER BY",
        ["Sorts the query result", "Does not change table layout", "Happens at read time"],
        "blue",
        "MergeTree ORDER BY",
        ["Table sorting key", "Affects skipping / index", "Design-time decision"],
        "green",
        "Do not confuse result sorting with the table sorting key",
    )
    flow(
        s / "date-half-open.svg",
        "Prefer half-open date ranges",
        [
            (">= start", "include start", "blue"),
            ("< end", "exclude end", "orange"),
            ("No overlap", "safe buckets", "green"),
        ],
        "Example: day >= '2023-01-01' AND day < '2023-02-01'",
    )

    # S03 - windows focus
    s = SESSIONS / "03-advanced-clickhouse-sql" / "assets"
    window_anatomy(s / "window-anatomy-rows.svg")
    running_total(s / "running-total.svg")
    two_panel(
        s / "groupby-vs-window.svg",
        "GROUP BY vs window",
        "GROUP BY",
        ["Collapses rows", "One row per group", "Good for summary KPIs"],
        "orange",
        "Window OVER (...)",
        ["Keeps every row", "Adds calculated columns", "Good for detail + totals"],
        "green",
        "Choose based on whether you still need the detail rows",
    )
    two_panel(
        s / "cte-vs-subquery.svg",
        "CTE vs subquery (same idea)",
        "WITH cte AS (...)",
        ["Named step", "Easier to read", "Chain multiple steps"],
        "blue",
        "Nested subquery",
        ["Inline SELECT", "Can get deep fast", "Harder to debug"],
        "purple",
        "Prefer CTEs when teaching multi-step analytics",
    )

    # S05
    s = SESSIONS / "05-clickhouse-optimization" / "assets"
    flow(
        s / "explain-layers.svg",
        "EXPLAIN mental model",
        [
            ("Parts", "which files", "slate"),
            ("Columns", "which fields", "blue"),
            ("Filter", "row predicates", "orange"),
            ("Aggregate", "GROUP BY", "purple"),
            ("Result", "output", "green"),
        ],
        "Use EXPLAIN to see what work the engine plans to do",
    )
    two_panel(
        s / "partition-prune-vs-skip.svg",
        "Two ways to read less data",
        "PARTITION prune",
        ["Skip whole months/folders", "PARTITION BY toYYYYMM(...)", "Coarse cut"],
        "orange",
        "Sort-key skipping",
        ["Skip granules inside parts", "ORDER BY leading columns", "Fine-grained cut"],
        "green",
        "Both help - they are not the same knob",
    )

    # S07
    s = SESSIONS / "07-odata" / "assets"
    odata_skip_top(s / "odata-skip-top-window.svg")

    # S08
    s = SESSIONS / "08-grafana-and-clickhouse" / "assets"
    two_panel(
        s / "empty-vs-broken.svg",
        "Empty result vs broken query",
        "Empty (often correct)",
        ["Region 2 + Completed", "Valid SQL / filter", "Zero matching rows"],
        "orange",
        "Broken (fix it)",
        ["Syntax / auth error", "Wrong table / column", "Wrong time range"],
        "red",
        "Teach students to distinguish empty from error",
    )

    # S10
    s = SESSIONS / "10-grafana-variables" / "assets"
    var_expand(s / "variable-expansion.svg")
    two_panel(
        s / "equals-vs-in.svg",
        "Multi-value: = vs IN",
        "Wrong with Multi-value",
        ["status = ${status:sqlstring}", "Breaks or picks one value"],
        "red",
        "Correct with Multi-value",
        ["status IN (${status:sqlstring})", "Expands to a list"],
        "green",
        "When Multi-value is on, use IN (...) for ClickHouse",
    )

    # S11
    s = SESSIONS / "11-advanced-odata-in-grafana" / "assets"
    odata_or(s / "odata-or-chain.svg")
    two_panel(
        s / "skip-vs-page.svg",
        "$skip is not a page number",
        "Page thinking",
        ["Page 3 of size 10", "Students may write skip=3"],
        "orange",
        "Correct offset",
        ["skip = (page-1)*size", "Page 3 size 10 => skip=20"],
        "green",
        "Compute skip from page size; keep $orderby stable",
    )

    # S12
    s = SESSIONS / "12-advanced-grafana-dashboards" / "assets"
    flow(
        s / "drilldown-map.svg",
        "Drill-down navigation",
        [
            ("Overview", "KPIs", "blue"),
            ("Click region", "link / var", "orange"),
            ("Detail dash", "filtered", "purple"),
            ("Table", "orders", "green"),
        ],
        "Carry variables and time range into the target dashboard",
    )

    # S13
    s = SESSIONS / "13-reporting-dashboard-workshop" / "assets"
    two_panel(
        s / "ch-vs-odata-chooser.svg",
        "Choose the reporting source",
        "ClickHouse SQL",
        ["Heavy aggregates", "Flexible joins", "Best for KPIs"],
        "green",
        "OData / REST",
        ["App-shaped JSON", "Standard filters", "Infinity panels"],
        "blue",
        "Pick the source that matches the question and skill path",
    )

    # S14
    s = SESSIONS / "14-grafana-alerting" / "assets"
    alert_machine(s / "alert-state-machine.svg")
    two_panel(
        s / "zero-nodata-error.svg",
        "Zero vs NoData vs Error",
        "Zero",
        ["Query succeeds", "Metric is 0", "May be a real KPI"],
        "green",
        "NoData / Error",
        ["NoData: empty series", "Error: query failed", "Different alert paths"],
        "orange",
        "Configure no-data and error handling explicitly in the rule",
    )

    # S15
    s = SESSIONS / "15-dbt-for-clickhouse" / "assets"
    model_dag(s / "model-dag-mart.svg")
    flow(
        s / "materialization-types.svg",
        "Materialization choices",
        [
            ("View", "query each time", "blue"),
            ("Table", "rebuild all", "orange"),
            ("Incremental", "append/merge", "green"),
        ],
        "Choose based on cost, freshness, and ClickHouse merge behavior",
    )

    # S16
    s = SESSIONS / "16-kafka-concepts" / "assets"
    consumer_offsets(s / "consumer-group-offsets.svg")
    two_panel(
        s / "two-consumer-groups.svg",
        "Two consumer groups on one topic",
        "Group analytics",
        ["Own offsets", "Builds CH tables", "Independent lag"],
        "blue",
        "Group audit",
        ["Own offsets", "Writes elsewhere", "Does not affect analytics"],
        "green",
        "Groups do not share committed offsets",
    )

    print("Generated extra SVG heroes")


if __name__ == "__main__":
    main()
