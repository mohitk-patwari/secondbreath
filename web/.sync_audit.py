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
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import ventilation as v  # noqa: E402  the shared core, same file the Lambdas copy
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
           '  <div class="tablewrap"><table class="narrow"><thead><tr><th>Dataset</th><th>Rooms analysed</th><th>Confident decay</th>'
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


# ---- Hero: "Where are you sitting right now?" ----
# Pre-rendered with the same ventilation.predict the API runs, so the page shows a real
# answer with JavaScript off, and the first animation needs no network. The page's JS
# replaces these numbers with live POST /predict results once the visitor changes anything.
ACTIVITY, OUTDOOR = "seated_quiet", 420.0  # the audit's buildup assumption; the hero says so
PEOPLE, MINUTES = 60, 90                  # the Predict panel's defaults, so the two agree
DOTS = 24                                 # people drawn; "+N" past that


def presets(audit) -> list[dict]:
    by = {h["hall"]: h for h in audit["halls"]}
    a, c = by["Hall A"], by["Hall C"]
    # Hall B is left out on purpose: its fits are uncertain and it must never read as a headline.
    assert a["decay"]["confident"] and c["decay"]["confident"], "hero presets assume Halls A and C fit cleanly"
    spain = next(d for d in audit["other_datasets"] if "Spain" in d["label"])
    best = max((r for r in spain["rooms"] if r["decay"]["confident"]), key=lambda r: r["decay"]["ach_teaching"])
    assert best["volume_m3"] is None  # if Spain ever publishes volumes, use the room's own
    rate = lambda h: f'{n(h["decay"]["ach_teaching"])}/h, {h["decay"]["fits_teaching"]} decay fits'
    return [
        {"name": "Lecture hall A", "sub": f'{loc(a["volume_m3"])} m³, measured {rate(a)}',
         "vol": a["volume_m3"], "ach": a["decay"]["ach_teaching"]},
        {"name": "Lecture hall C", "sub": f'{loc(c["volume_m3"])} m³, measured {rate(c)}',
         "vol": c["volume_m3"], "ach": c["decay"]["ach_teaching"]},
        {"name": "Hall A as designed", "sub": f'{loc(a["volume_m3"])} m³ at its specified {n(a["design_ach"])}/h',
         "vol": a["volume_m3"], "ach": a["design_ach"]},
        # Spain publishes no room volumes, so this classroom cannot be simulated as itself
        # without inventing one. Its measured rate goes into Hall A's real volume instead, labelled.
        {"name": "Hall A, aired like Spain's best classroom",
         "sub": f'{loc(a["volume_m3"])} m³ at {n(best["decay"]["ach_teaching"])}/h, measured in Spain',
         "vol": a["volume_m3"], "ach": best["decay"]["ach_teaching"],
         "note": f"\"Aired like Spain's best classroom\" uses Hall A's real {loc(a['volume_m3'])} m³ with the {rate(best)} "
                 f'measured in {html.escape(best["hall"])} ({html.escape(spain["dataset"])}). Spain publishes no room volumes, '
                 'so that classroom cannot be simulated as itself, and no volume is invented for it.'},
    ]


def simulate(p: dict, people: int, minutes: int) -> dict:
    """The fields of POST /predict the hero reads, from the same functions (backend/src/api.py)."""
    pr = v.predict(p["vol"], p["ach"], people, minutes, ACTIVITY, None, OUTDOOR)
    return {"curve": [{"minute": s.minute, "ppm": s.co2_ppm, "rebreathedFraction": s.rebreathed_fraction} for s in pr.curve],
            "withinValidatedRange": pr.within_validated_range, "validatedMaxPpm": v.VALIDATED_MAX_PPM,
            "maxOccupancy": {"1000": v.max_occupancy(p["vol"], p["ach"], minutes, 1000.0, ACTIVITY, OUTDOOR)}}


# Text and levels below are mirrored line for line by heroText() in index.html. Rounding
# never flatters the room: "1 in N" and ACH down, ppm, percentages and red breaths up.
def hero_text(p: dict, res: dict, people: int, minutes: int, m: int) -> dict:
    s = res["curve"][m]
    f = min(1.0, s["rebreathedFraction"])
    cap = res["maxOccupancy"]["1000"]
    held = "500 or more" if cap >= 500 else f"{cap:,}"
    t = {"conseq": f"For {minutes} minutes, this room's air can take <b>{held}</b> {'person' if cap == 1 else 'people'} "
                   f"before CO2 passes 1,000 ppm. You set {people}."}
    if not res["withinValidatedRange"]:
        t.update(head=f"{people} people for {minutes} minutes would take this room past {loc(res['validatedMaxPpm'])} ppm, "
                      "the 8-hour workplace exposure limit. Past that the useful answer is to leave the room, not a number: "
                      "try fewer people or a shorter session.",
                 red=0, level="na", detail=f"{loc(p['vol'])} m³ at {n(p['ach'])} air changes an hour")
        return t
    t["head"] = (f"After {m} minute{'' if m == 1 else 's'}, <b>1 breath in {max(1, math.floor(1 / f))}</b> "
                 "has already been through someone else's lungs." if f > 0 else "The air in the room is still outdoor air.")
    t["red"] = min(100, math.ceil(f * 100))
    t["level"] = "ok" if s["ppm"] < 1000 else "warn" if s["ppm"] < 1400 else "bad"
    t["detail"] = (f"{math.ceil(s['ppm']):,} ppm · {math.ceil(f * 1000) / 10:.1f}% of each breath rebreathed · "
                   f"{loc(p['vol'])} m³ at {n(p['ach'])} air changes an hour · seated, quiet · outdoor {n(OUTDOOR)} ppm")
    return t


def hero(audit) -> str:
    ps = presets(audit)
    p, res = ps[0], simulate(ps[0], PEOPLE, MINUTES)
    t = hero_text(p, res, PEOPLE, MINUTES, MINUTES)
    buttons = "".join(
        f'    <button type="button" class="preset" aria-pressed="{"true" if i == 0 else "false"}" data-vol="{n(q["vol"])}" data-ach="{n(q["ach"])}">'
        f'<b>{q["name"]}</b><span>{q["sub"]}</span></button>\n' for i, q in enumerate(ps))
    dots = "".join(f'<circle cx="{25 + (i % 6) * 30}" cy="{24 + (i // 6) * 28}" r="8"{"" if i < PEOPLE else " hidden"}/>' for i in range(DOTS))
    more = f"+{PEOPLE - DOTS}" if PEOPLE > DOTS else ""
    grid = "".join('<i class="r"></i>' if i < t["red"] else "<i></i>" for i in range(100))
    data = json.dumps({"minutes": MINUTES, "people": PEOPLE, "result": res}, separators=(",", ":"))
    return f'''  <div class="presets" role="group" aria-label="Choose a room">
{buttons}  </div>
  <div class="sliders">
    <div class="slide"><label for="hPeople">People in the room</label><output id="hPeopleOut" for="hPeople">{PEOPLE}</output>
      <input class="bigrange" id="hPeople" type="range" min="1" max="120" step="1" value="{PEOPLE}"></div>
    <div class="slide"><label for="hMins">How long</label><output id="hMinsOut" for="hMins">{MINUTES} min</output>
      <input class="bigrange" id="hMins" type="range" min="5" max="240" step="5" value="{MINUTES}"></div>
  </div>
  <div class="answer">
    <figure class="panel"><figcaption>The room from above</figcaption>
      <svg viewBox="0 0 200 150" role="img" aria-label="Room seen from above with {PEOPLE} people">
        <rect id="hRoom" class="room {t["level"]}" x="3" y="3" width="194" height="144" rx="18"/>
        <g id="hDots">{dots}</g>
        <text id="hMore" x="186" y="138" text-anchor="end">{more}</text>
      </svg>
    </figure>
    <figure class="panel"><figcaption>Your next 100 breaths</figcaption>
      <div id="hGrid" class="breaths{" na" if t["level"] == "na" else ""}" role="img" aria-label="{t["red"]} of 100 breaths already exhaled by someone else">{grid}</div>
    </figure>
  </div>
  <p class="headline" id="hHead" aria-live="polite">{t["head"]}</p>
  <p id="hConseq">{t["conseq"]}</p>
  <p class="small muted" id="hDetail">{t["detail"]}</p>
  <div class="clock"><button type="button" id="hPlay" class="ghost" aria-label="Play the session">▶</button>
    <input class="bigrange" id="hScrub" type="range" min="0" max="{MINUTES}" step="1" value="{MINUTES}" aria-label="Minute of the session">
    <output id="hMinute" for="hScrub">{MINUTES} min</output></div>
  <p class="small muted">Room colour: green under 1,000 ppm, amber to 1,400, red above. Red breaths: the share of each breath already exhaled by someone else, rounded up. If the session's peak would pass {loc(v.VALIDATED_MAX_PPM)} ppm, the 8-hour workplace exposure limit (OSHA PEL, ACGIH TLV) used here as a ceiling, the page says so instead of giving a number. Predicted with the same model as <a href="#predict">Predict a session</a>, seated and quiet, outdoor air at {n(OUTDOOR)} ppm. Rates are each hall's decay-fit median over teaching hours; Hall B is left out because its fits are uncertain. {ps[3]["note"]}</p>
  <script type="application/json" id="heroData">{data}</script>
'''


def tour_hero(audit) -> str:
    ps = presets(audit)
    txt = [hero_text(q, simulate(q, PEOPLE, MINUTES), PEOPLE, MINUTES, MINUTES) for q in ps]
    plain = lambda s: re.sub(r"<[^>]+>", "", s)
    return (f'    <li><a href="#hero">Where are you sitting right now?</a> No click, no file: it has already run and plays once on arrival.\n'
            f'      <span class="expect">Expect: {ps[0]["name"]}, {PEOPLE} people, {MINUTES} minutes. "{plain(txt[0]["head"])}" '
            f'{txt[0]["red"]} of the 100 breaths are red. Now tap "{ps[3]["name"]}": {txt[3]["red"]} red, '
            f'"{plain(txt[3]["head"])}" Drag the clock to watch the session build.</span></li>\n')


def tour_values(audit, page: str) -> str:
    """Fill <span data-a="halls.0.decay.fits_teaching"> in the judges' tour from audit.json."""
    def val(path):
        v = audit
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
r = audit["rooms_analysed"]
page = block("forty", f'  <p class="muted">{r["confident_decay"]} of them with a confident decay fit and {r["confident_buildup"]} with a confident '
                      f'buildup fit, across {len(r["by_dataset"])} open datasets. Only the {r["with_design_figure"]} lecture halls publish '
                      'a design figure, so the finding starts there.</p>\n', page)
page = block("hero", hero(audit), page)
# The explainer slider starts at 2,000 ppm; same wording and rounding as explain() in the page.
page = block("explain", f"  At 2,000 ppm, <b>1 breath in {math.floor(v.one_breath_in(2000.0, OUTDOOR))}</b> "
                        "has already been through someone else's lungs.\n", page)
page = block("tourhero", tour_hero(audit), page)
page = tour_values(audit, page)
PAGE.write_text(page, encoding="utf-8", newline="\n")
print(f"synced audit.json, the finding, {audit['rooms_analysed']['total']} rooms and {len(FIGS) + 1} figures into {PAGE.relative_to(ROOT)}")
