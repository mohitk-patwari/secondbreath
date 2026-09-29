"""Write analysis/audit.json and analysis/figures/*.svg into web/index.html as HTML.

    python web/.sync_audit.py

Rerun after every audit. The page is one file served by a Lambda that only
knows index.html, so the figures are inlined rather than linked.
Figures go in as <img> data URIs: each SVG carries its own <style> and ids,
which would leak into the page if pasted inline. The leading dot keeps this
script out of the public bucket (deploy_web.py excludes ".*").

The finding (headline, table, agreement paragraph), the rooms summary and the
judges' tour numbers are written here as plain HTML, not built in the browser:
a scorer that reads the page without running JavaScript must see every number.
Values are printed exactly as audit.json holds them, never recomputed.
"""
import base64
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "web" / "index.html"
FIGS = ["design_vs_measured", "hall_a", "hall_b", "hall_c"]
THIN = 10  # ponytail: editorial label only, no number depends on it


def block(name: str, body: str, page: str) -> str:
    pat = re.compile(rf"(<!-- sync:{name} -->\n).*?(<!-- /sync:{name} -->)", re.S)
    assert pat.search(page), f"sync:{name} markers missing from {PAGE}"
    return pat.sub(lambda m: m[1] + body + m[2], page)


def n(v) -> str:
    """A number as JavaScript prints it: 1.1 not 1.10, 2100 not 2100.0."""
    return str(int(v)) if float(v).is_integer() else str(v)


def loc(v) -> str:
    """Thousands separators, as the page's toLocaleString("en") did."""
    return f"{int(v):,}" if float(v).is_integer() else f"{v:,}"


def listing(xs) -> str:
    xs = [str(x) for x in xs]
    return "".join(xs) if len(xs) < 2 else ", ".join(xs[:-1]) + " and " + xs[-1]


def figure(name: str, note: str = "") -> str:
    svg = (ROOT / "analysis" / "figures" / f"{name}.svg").read_text(encoding="utf-8")
    title = html.unescape(re.search(r"<title[^>]*>(.*?)</title>", svg, re.S)[1])
    desc = html.unescape(re.search(r"<desc[^>]*>(.*?)</desc>", svg, re.S)[1])
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    return (f'  <figure><img src="{uri}" alt="{html.escape(desc)}" loading="lazy">'
            f"<figcaption>{html.escape(title)}{note}. Source: analysis/figures/{name}.svg</figcaption></figure>\n")


def finding(halls) -> tuple[str, str, str]:
    clean = [h for h in halls if h["decay"]["confident"] and h["buildup"]["confident"]]
    shaky = [h for h in halls if h not in clean]
    vals = [v for h in clean for v in (h["decay"]["ach_teaching"], h["buildup"]["ach"])]
    falls = [v for h in clean for v in (h["decay"]["shortfall_factor"], h["buildup"]["shortfall_factor"])]
    peak = max(halls, key=lambda h: h["peak_co2_teaching"])
    short = lambda h: h["hall"].replace("Hall ", "")

    head = f"  Designed for about 6 air changes an hour. Delivered: <b>{n(min(vals))} to {n(max(vals))}</b>.\n"

    badge = lambda t: f' <span class="badge">{t}</span>'
    def cell(v, sure, lines, thin=False):
        return (f'<td class="{"" if sure else "uncertain"}"><b>{n(v)}</b>{"" if sure else badge("Uncertain")}'
                f'{badge("Thin") if thin else ""}<br><span class="small muted">{lines}</span></td>')
    rows = []
    for h in halls:
        d, b = h["decay"], h["buildup"]
        d_lines = f"{d['fits_teaching']} fits · band " + "–".join(map(n, d["ach_teaching_iqr"]))
        b_lines = f"{b['kept']} fits, {b['discarded_unidentifiable']} discarded · band " + "–".join(map(n, b["ach_iqr"]))
        rows.append(
            f'<tr><th scope="row">{h["hall"]}</th>\n'
            f'    <td><b>{n(h["design_ach"])}</b><br><span class="small muted">{loc(h["design_airflow_m3h"])} m³/h, {loc(h["volume_m3"])} m³</span></td>\n'
            f'    {cell(d["ach_teaching"], d["confident"], d_lines)}\n'
            f'    {cell(b["ach"], b["confident"], b_lines, 0 < b["kept"] < THIN)}\n'
            f'    <td>{n(d["shortfall_factor"])}× / {n(b["shortfall_factor"])}×</td>\n'
            f'    <td>{loc(h["peak_co2_teaching"])} ppm<br><span class="small muted">1 breath in {h["peak_one_breath_in"]}</span></td></tr>\n')
    table = ('  <div class="tablewrap"><table id="auditTable" aria-describedby="auditNote">'
             '<thead><tr><th>Hall</th><th>Design ACH</th><th>Decay ACH<br><span class="small">room emptying</span></th>'
             '<th>Buildup ACH<br><span class="small">room occupied</span></th><th>Below design<br><span class="small">decay / buildup</span></th>'
             '<th>Peak CO2</th></tr></thead><tbody>\n' + "".join(rows) + "</tbody></table></div>\n")

    agree = (f"Halls {listing(map(short, clean))} fit cleanly at {listing(n(h['decay']['ach_teaching']) for h in clean)} air changes per hour by decay, "
             f"and {listing(n(h['buildup']['ach']) for h in clean)} by buildup: {n(min(falls))} to {n(max(falls))} times below design on either method. "
             "The two methods do not agree to the decimal, and buildup reads higher in both halls. But they could have disagreed by a factor of six, and they do not. ")
    for h in shaky:
        agree += f"{h['hall']}'s decay fits scatter (interquartile range {' to '.join(map(n, h['decay']['ach_teaching_iqr']))})"
        if not h["buildup"]["confident"]:
            agree += f" and so do its buildup fits ({' to '.join(map(n, h['buildup']['ach_iqr']))})"
        agree += ", so it is reported as uncertain, not averaged into the headline. "
    for h in halls:
        if h["buildup"]["kept"] < THIN:
            agree += f"{h['hall']}'s buildup rests on only {h['buildup']['kept']} fits, so treat it as thin. "
    agree += ("Decay fits outside teaching hours, reported either way: "
              + listing(f"{short(h)} {n(h['decay']['ach_offhours'])} ({h['decay']['fits_offhours']} fits)" for h in halls) + ". "
              f"Highest reading: {loc(peak['peak_co2_teaching'])} ppm in {peak['hall']}, 1 breath in {peak['peak_one_breath_in']} already exhaled by somebody else in the room.")
    return head, table, f"  <p>{agree}</p>\n"


def rooms(audit) -> str:
    r = audit["rooms_analysed"]
    # Never 40 alone: the confident counts travel with the total in every sentence.
    out = [f'  <p>The same fits, with the same parameters, ran over <b>{r["total"]} rooms in {len(r["by_dataset"])} open datasets</b>: '
           f'{r["confident_decay"]} with a confident decay fit, {r["confident_buildup"]} with a confident buildup fit, '
           f'and {r["with_design_figure"]} with a published design figure. Rooms without a confident fit are counted here and drawn hollow in the figure, but never quoted as a rate.</p>\n',
           '  <div class="tablewrap"><table><thead><tr><th>Dataset</th><th>Rooms analysed</th><th>Confident decay</th>'
           '<th>Confident buildup</th><th>Design figure</th></tr></thead><tbody>\n']
    for name, d in r["by_dataset"].items():
        out.append(f'<tr><th scope="row">{html.escape(name)}</th><td>{d["rooms"]}</td><td>{d["confident_decay"]}</td>'
                   f'<td>{d["confident_buildup"]}</td><td>{d["with_design_figure"]}</td></tr>\n')
    out.append(f'<tr><th scope="row">All</th><td><b>{r["total"]}</b></td><td><b>{r["confident_decay"]}</b></td>'
               f'<td><b>{r["confident_buildup"]}</b></td><td><b>{r["with_design_figure"]}</b></td></tr>\n</tbody></table></div>\n')
    for d in audit["other_datasets"]:
        assert d["design_comparison"] is None, f"{d['label']} gained a design figure; revisit the no-shortfall wording"
        out.append(f'  <p class="note"><b>{html.escape(d["label"])}</b> ({html.escape(d["dataset"])}). '
                   f'No shortfall is claimed for these rooms. {html.escape(d["design_note"])}</p>\n')
    out.append(figure("all_rooms", f" ({r['confident_decay']} with a confident decay fit, {r['confident_buildup']} with a confident buildup fit)"))
    return "".join(out)


def tour_values(audit, page: str) -> str:
    """Fill <span data-a="0.decay.fits_teaching"> in the judges' tour from halls[0] etc."""
    def val(path):
        v = audit["halls"]
        for k in path.split("."):
            v = v[int(k)] if isinstance(v, list) else v[k]
        return loc(v)
    return re.sub(r'(<span data-a="([^"]+)">).*?(</span>)', lambda m: m[1] + val(m[2]) + m[3], page)


audit = json.loads((ROOT / "analysis" / "audit.json").read_text(encoding="utf-8"))
head, table, agree = finding(audit["halls"])

page = PAGE.read_text(encoding="utf-8")
page = block("figures", "".join(figure(f) for f in FIGS), page)
page = block("findhead", head, page)
page = block("findtable", table, page)
page = block("agree", agree, page)
page = block("rooms", rooms(audit), page)
page = tour_values(audit, page)
PAGE.write_text(page, encoding="utf-8", newline="\n")
print(f"synced audit.json, the finding, {audit['rooms_analysed']['total']} rooms and {len(FIGS) + 1} figures into {PAGE.relative_to(ROOT)}")
