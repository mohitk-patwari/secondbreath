"""Copy analysis/audit.json and analysis/figures/*.svg into web/index.html.

    python web/.sync_audit.py

Rerun after every audit. The page is one file served by a Lambda that only
knows index.html, so the audit and figures are inlined rather than linked.
Figures go in as <img> data URIs: each SVG carries its own <style> and ids,
which would leak into the page if pasted inline. The leading dot keeps this
script out of the public bucket (deploy_web.py excludes ".*").
"""
import base64
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "web" / "index.html"
FIGS = ["design_vs_measured", "hall_a", "hall_b", "hall_c"]


def block(name: str, body: str, page: str) -> str:
    pat = re.compile(rf"(<!-- sync:{name} -->\n).*?(<!-- /sync:{name} -->)", re.S)
    assert pat.search(page), f"sync:{name} markers missing from {PAGE}"
    return pat.sub(lambda m: m[1] + body + m[2], page)


audit = (ROOT / "analysis" / "audit.json").read_text(encoding="utf-8")
assert "</" not in audit  # would close the <script> early
figs = []
for name in FIGS:
    svg = (ROOT / "analysis" / "figures" / f"{name}.svg").read_text(encoding="utf-8")
    title = html.unescape(re.search(r"<title[^>]*>(.*?)</title>", svg, re.S)[1])
    desc = html.unescape(re.search(r"<desc[^>]*>(.*?)</desc>", svg, re.S)[1])
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    figs.append(f'  <figure><img src="{uri}" alt="{html.escape(desc)}" loading="lazy">'
                f"<figcaption>{html.escape(title)}. Source: analysis/figures/{name}.svg</figcaption></figure>\n")

page = PAGE.read_text(encoding="utf-8")
page = block("audit", f'<script type="application/json" id="audit">\n{audit}</script>\n', page)
page = block("figures", "".join(figs), page)
PAGE.write_text(page, encoding="utf-8", newline="\n")
print(f"synced audit.json and {len(figs)} figures into {PAGE.relative_to(ROOT)}")
