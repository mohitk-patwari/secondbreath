"""Uptime check, run every 5 minutes by EventBridge. Raising marks the invocation
as an error; a CloudWatch alarm on this function's Errors metric emails the
alert address. Stdlib only, so the cold start stays small at 128 MB."""

import json
import os
import urllib.request


def _get(url):
    req = urllib.request.Request(url, headers={"user-agent": "secondbreath-uptime"})
    # 15 s: the site and health functions can cold-start (~1 s) and still pass.
    with urllib.request.urlopen(req, timeout=15) as r:  # non-2xx raises HTTPError
        return r.read().decode("utf-8", "replace")


def handler(event, context):
    failures = []
    try:
        # Content check too: a 200 with an empty or error body is still down to a judge.
        if "<html" not in _get(os.environ["SITE_URL"]).lower():
            failures.append("site: 200 but no <html> in body")
    except Exception as e:
        failures.append(f"site: {e!r}")
    try:
        health = json.loads(_get(os.environ["HEALTH_URL"]))
        if health.get("ok") is not True:
            failures.append(f"health: {health}")
        elif health.get("auditStale"):
            print("health ok but audit stale (degraded, not down):", health)
    except Exception as e:
        failures.append(f"health: {e!r}")
    if failures:
        raise RuntimeError("; ".join(failures))
    return "ok"
