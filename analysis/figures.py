"""
Plain-SVG figures for the audit. No chart library: each figure is a string.

Written to analysis/figures/ by audit_lecture_halls.py. Colours follow the
dataviz reference palette (categorical slots 1 and 2, validated as a pair in
light and dark); text and axes use currentColor-style ink tokens so the files
sit on either theme. Hover text is native <title>, which works in <img> and
inline embeds alike.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta
from html import escape
from pathlib import Path

STYLE = """<style>
  svg { --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e; --grid: #e4e3df; --trace: #8a8984;
        --decay: #2a78d6; --build: #eb6834; --design: #b9b8b2;
        font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
  @media (prefers-color-scheme: dark) {
    svg { --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7; --grid: #3a3a37; --trace: #8f8e88;
          --decay: #3987e5; --build: #d95926; --design: #5e5d58; }
  }
  .t { fill: var(--ink); font-size: 15px; font-weight: 600; }
  .s { fill: var(--ink-2); font-size: 12px; }
  .a { fill: var(--ink-2); font-size: 11px; }
  .g { stroke: var(--grid); stroke-width: 1; }
  .trace { fill: none; stroke: var(--trace); stroke-width: 1.25; stroke-linejoin: round; }
  .decay { fill: none; stroke: var(--decay); stroke-width: 3; stroke-linecap: round; }
  .build { fill: none; stroke: var(--build); stroke-width: 3; stroke-linecap: round; }
  .ref { stroke: var(--ink-2); stroke-width: 1; stroke-dasharray: 4 4; }
</style>"""

W, H = 800, 360
L, R, T, B = 56, 16, 78, 40  # plot margins


def _svg(body: list[str], title: str, desc: str, h: int = H) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="100%" '
        f'role="img" aria-labelledby="t d">\n<title id="t">{escape(title)}</title>\n'
        f'<desc id="d">{escape(desc)}</desc>\n{STYLE}\n'
        # Own surface: an SVG opened on its own sits on the browser's white
        # canvas even in dark mode, which would swallow the dark-mode ink.
        f'<rect width="{W}" height="{h}" rx="8" fill="var(--surface)"/>\n'
        + "\n".join(body) + "\n</svg>\n"
    )


def _legend(x: float, y: float, items: list[tuple[str, str]]) -> list[str]:
    out = []
    for cls, label in items:
        out.append(f'<line class="{cls}" x1="{x}" y1="{y}" x2="{x + 22}" y2="{y}"/>')
        out.append(f'<text class="s" x="{x + 28}" y="{y + 4}">{escape(label)}</text>')
        x += 36 + 7 * len(label)
    return out


def busiest_week(decay, build) -> datetime:
    """Monday of the ISO week holding the most fits of both kinds, so the
    figure shows each method working rather than a hand-picked week."""
    def key(t: datetime) -> datetime:
        return datetime(t.year, t.month, t.day) - timedelta(days=t.weekday())
    d = Counter(key(f.start) for f in decay)
    b = Counter(key(f.start) for f in build)
    return max(set(d) | set(b), key=lambda w: (min(d[w], b[w]), d[w] + b[w], -w.timestamp()))


def hall_svg(r: dict, series, decay, build, path: Path) -> None:
    mon = busiest_week(decay, build)
    t0, t1 = mon, mon + timedelta(days=5)
    pts = [(t, c) for t, c in series if t0 <= t < t1]
    wd = [f for f in decay if t0 <= f.start < t1]
    wb = [f for f in build if t0 <= f.start < t1]

    ymax = max(1500.0, max(c for _, c in pts) * 1.05)
    ymax = 500 * -(-ymax // 500)
    ymin = 400.0
    pw, ph = W - L - R, H - T - B

    def x(t: datetime) -> float:
        return L + pw * (t - t0).total_seconds() / (t1 - t0).total_seconds()

    def y(c: float) -> float:
        return T + ph * (1 - (c - ymin) / (ymax - ymin))

    def line(seg, cls: str, tip: str) -> str:
        p = " ".join(f"{x(t):.1f},{y(c):.1f}" for t, c in seg)
        return f'<polyline class="{cls}" points="{p}"><title>{escape(tip)}</title></polyline>'

    body = [
        f'<text class="t" x="{L}" y="24">{r["hall"]}: CO₂, week of {mon:%d %b %Y}</text>',
        f'<text class="s" x="{L}" y="42">Design {r["design_ach"]:.1f} ACH · '
        f'year median: decay {r["decay"]["ach_teaching"]:.2f}, buildup {r["buildup"]["ach"]:.2f} ACH'
        f'{"" if r["decay"]["confident"] and r["buildup"]["confident"] else " (uncertain)"}'
        f' · busiest week for fits, Mon–Fri</text>',
        *_legend(L, 62, [("trace", "CO₂ reading"), ("decay", f"decay fit ({len(wd)})"),
                         ("build", f"buildup fit ({len(wb)})")]),
    ]
    step = 500 if ymax > 2500 else 250
    c = step * -(-ymin // step)  # first gridline on a step multiple
    while c <= ymax:
        body.append(f'<line class="g" x1="{L}" x2="{W - R}" y1="{y(c):.1f}" y2="{y(c):.1f}"/>')
        body.append(f'<text class="a" x="{L - 6}" y="{y(c) + 4:.1f}" text-anchor="end">{c:.0f}</text>')
        c += step
    body.append(f'<line class="ref" x1="{L}" x2="{W - R}" y1="{y(1000):.1f}" y2="{y(1000):.1f}"/>')
    body.append(f'<text class="a" x="{W - R}" y="{y(1000) - 5:.1f}" text-anchor="end">1000 ppm</text>')
    body.append(f'<text class="a" x="12" y="{T - 8}">ppm</text>')
    for d in range(6):
        xd = x(t0 + timedelta(days=d))
        body.append(f'<line class="g" x1="{xd:.1f}" x2="{xd:.1f}" y1="{T}" y2="{H - B}"/>')
        if d < 5:
            body.append(f'<text class="a" x="{xd + pw / 10:.1f}" y="{H - B + 18}" text-anchor="middle">'
                        f'{t0 + timedelta(days=d):%a %d %b}</text>')

    # Break the trace at gaps > 30 min so missing data is not drawn as a ramp.
    run: list = []
    for p in pts:
        if run and (p[0] - run[-1][0]).total_seconds() > 1800:
            body.append(line(run, "trace", "CO₂ reading"))
            run = []
        run.append(p)
    if run:
        body.append(line(run, "trace", "CO₂ reading"))

    for f in wd:
        seg = [(t, c) for t, c in pts if f.start <= t <= f.end]
        body.append(line(seg, "decay", f"Decay fit {f.start:%a %H:%M}–{f.end:%H:%M}: {f.ach:.2f} ACH"))
    for f in wb:
        seg = [(t, c) for t, c in pts if f.start <= t <= f.end]
        body.append(line(seg, "build", f"Buildup fit {f.start:%a %H:%M}–{f.end:%H:%M}: "
                                       f"{f.ach:.2f} ACH, ~{f.implied_occupants:.0f} people"))

    path.write_text(_svg(
        body,
        f"{r['hall']} CO2, week of {mon:%d %b %Y}, with fitted segments",
        f"CO2 readings Monday to Friday. {len(wd)} decay fits (blue) and {len(wb)} "
        f"identifiable buildup fits (orange) are highlighted. Source: Zenodo 18385830, "
        f"CC BY 4.0; fits from ventilation.py via analysis/audit_lecture_halls.py.",
    ), encoding="utf-8")


def summary_svg(results: list[dict], path: Path) -> None:
    h = 330
    pw = W - 150 - 70
    vmax = 7.0

    def x(v: float) -> float:
        return 150 + pw * v / vmax

    rows = [("design", "Design", "design_ach"), ("decay", "Decay (emptying)", None),
            ("build", "Buildup (occupied)", None)]
    body = [
        f'<text class="t" x="{L}" y="24">Design vs measured air changes per hour</text>',
        f'<text class="s" x="{L}" y="42">Teaching-hours medians, full academic year 2023–24 '
        f'· “uncertain” = fits disagree too much to quote</text>',
    ]
    lx = L
    for cls, label, _ in rows:
        fill = {"design": "var(--design)", "decay": "var(--decay)", "build": "var(--build)"}[cls]
        body.append(f'<rect x="{lx}" y="56" width="12" height="12" rx="2" fill="{fill}"/>')
        body.append(f'<text class="s" x="{lx + 18}" y="66">{label}</text>')
        lx += 40 + 7 * len(label)

    for v in range(0, 8):
        body.append(f'<line class="g" x1="{x(v):.1f}" x2="{x(v):.1f}" y1="84" y2="{h - 30}"/>')
        body.append(f'<text class="a" x="{x(v):.1f}" y="{h - 12}" text-anchor="middle">{v}</text>')
    body.append(f'<text class="a" x="{x(vmax):.1f}" y="{h - 12}" text-anchor="end" dx="40">ACH</text>')

    bar, gap, y0 = 16, 2, 96
    for r in results:
        body.append(f'<text class="t" x="{150 - 12}" y="{y0 + 30}" text-anchor="end">{r["hall"]}</text>')
        vals = [
            ("var(--design)", r["design_ach"], f"design, {r['design_airflow_m3h']:.0f} m³/h", True),
            ("var(--decay)", r["decay"]["ach_teaching"], f"decay, {r['decay']['fits_teaching']} fits",
             r["decay"]["confident"]),
            ("var(--build)", r["buildup"]["ach"], f"buildup, {r['buildup']['kept']} fits",
             r["buildup"]["confident"]),
        ]
        for i, (fill, v, what, sure) in enumerate(vals):
            yb = y0 + i * (bar + gap)
            w = x(v) - x(0)
            # Square at the baseline, 4px rounded at the data end.
            body.append(
                f'<path d="M{x(0):.1f},{yb} h{w - 4:.1f} a4,4 0 0 1 4,4 v{bar - 8} a4,4 0 0 1 -4,4 '
                f'h{-(w - 4):.1f} z" fill="{fill}"><title>{r["hall"]} {what}: {v:.2f} ACH'
                f'{"" if sure else " (uncertain)"}</title></path>'
            )
            label = f"{v:.2f}" + ("" if sure else " uncertain")
            body.append(f'<text class="s" x="{x(v) + 6:.1f}" y="{yb + 12}">{label}</text>')
        y0 += 3 * (bar + gap) + 20

    path.write_text(_svg(
        body, "Design vs measured air changes per hour, three lecture halls",
        "; ".join(
            f"{r['hall']}: design {r['design_ach']:.1f}, decay {r['decay']['ach_teaching']:.2f}"
            f"{'' if r['decay']['confident'] else ' (uncertain)'}, buildup {r['buildup']['ach']:.2f}"
            f"{'' if r['buildup']['confident'] else ' (uncertain)'}"
            for r in results
        ) + ". Source: Zenodo 18385830, CC BY 4.0; analysis/audit.json.",
        h=h,
    ), encoding="utf-8")
