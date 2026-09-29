"""HTTP handlers for SecondBreath. All maths lives in ventilation.py; this file
only parses input, calls the solver and shapes JSON."""

import base64
import csv
import io
import json
import math
import os
from datetime import datetime, timedelta, timezone

import ventilation as v

# Lambda rejects any invoke event over 6 MiB (6,291,456 bytes) before our code
# runs. Checking at 6,000,000 leaves room for headers so bodies in between get
# a clear message instead of a bare gateway error.
MAX_BODY_BYTES = 6_000_000
MAX_SERIES_POINTS = 1000
AUDIT_PARAM = os.environ.get("AUDIT_PARAM", "/secondbreath/lastAuditRun")
AUDIT_STALE_AFTER = timedelta(days=7)


class BadRequest(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def _handle(fn):
    def wrapper(event, context):
        try:
            return _response(200, fn(event))
        except BadRequest as e:
            return _response(e.status, {"error": str(e)})
    return wrapper


def _body(event):
    raw = event.get("body") or ""
    data = base64.b64decode(raw) if event.get("isBase64Encoded") else raw.encode()
    if len(data) > MAX_BODY_BYTES:
        raise BadRequest(
            f"payload is {len(data):,} bytes; the limit is {MAX_BODY_BYTES:,}. "
            "Send only the timestamp and CO2 columns, or a shorter period.",
            status=413,
        )
    try:
        body = json.loads(data)
    except ValueError:
        raise BadRequest("body must be JSON")
    if not isinstance(body, dict):
        raise BadRequest("body must be a JSON object")
    return body


def _number(body, key, lo, hi, default=None):
    val = body.get(key, default)
    if val is None:
        raise BadRequest(f"{key} is required")
    # bool is an int subclass; true must not pass as 1.
    if isinstance(val, bool) or not isinstance(val, (int, float)) or not lo <= val <= hi:
        raise BadRequest(f"{key} must be a number between {lo} and {hi}")
    return float(val)


def _activity(body, default):
    activity = body.get("activity", default)
    if activity not in v.GENERATION_M3H:
        raise BadRequest(f"activity must be one of {sorted(v.GENERATION_M3H)}")
    return activity


def _finite(x):
    # JSON has no infinity; one_breath_in() returns inf at outdoor level.
    return None if math.isinf(x) else x


# ---------------------------------------------------------------------------
# CSV parsing
# ---------------------------------------------------------------------------

def _pick(header, wanted, hints, what):
    if wanted is not None:
        if wanted not in header:
            raise BadRequest(f"column {wanted!r} not found; header is {header}")
        return header.index(wanted)
    for i, name in enumerate(header):
        if any(h in name.lower() for h in hints):
            return i
    raise BadRequest(f"could not find a {what} column in {header}; pass columns.{what}")


def _parse_time(s):
    try:
        t = datetime.fromisoformat(s)
    except ValueError:
        t = datetime.fromtimestamp(float(s), tz=timezone.utc)  # epoch seconds
    # The fits only need consistent intervals; drop tz so naive and aware stamps compare.
    return t.replace(tzinfo=None) if t.tzinfo else t


def parse_csv(text, columns, outdoor_ppm):
    """Return (series, dropped_below_outdoor, rows_skipped)."""
    lines = text.lstrip("﻿").splitlines()
    if len(lines) < 2:
        raise BadRequest("csv needs a header row and at least one data row")
    delim = columns.get("delimiter") or max(";,\t", key=lines[0].count)
    rows = csv.reader(lines, delimiter=delim)
    header = [h.strip() for h in next(rows)]
    ti = _pick(header, columns.get("timestamp"), ("time", "date", "recorded"), "timestamp")
    ci = _pick(header, columns.get("co2"), ("co2",), "co2")

    series, dropped, skipped = [], 0, 0
    for row in rows:
        try:
            raw = row[ci].strip()
            if not raw:
                continue  # multi-sensor exports interleave rows; empty CO2 is normal
            co2 = float(raw)
            t = _parse_time(row[ti].strip())
        except (ValueError, IndexError, OverflowError, OSError):
            skipped += 1
            continue
        # Below outdoor is sensor drift, not cleaner-than-outside air. Drop, don't clamp.
        if co2 < outdoor_ppm:
            dropped += 1
            continue
        series.append((t, co2))
    series.sort()
    return series, dropped, skipped


def _in_teaching_hours(t):
    # Mirrors analysis/audit_lecture_halls.py: Mon-Fri, 08:00 <= hour < 18, local
    # wall-clock time as written in the CSV.
    return t.weekday() < 5 and 8 <= t.hour < 18


def _segments(fits):
    return [[f.start.isoformat(), f.end.isoformat(), f.ach] for f in fits]


def _fingerprint_json(fp):
    if fp is None:
        return None
    return {
        "achMedian": fp.ach_median, "achP25": fp.ach_p25, "achP75": fp.ach_p75,
        "nFits": fp.n_fits, "totalMinutes": fp.total_minutes, "confident": fp.confident,
    }


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

@_handle
def fit(event):
    body = _body(event)
    csv_text = body.get("csv")
    if not isinstance(csv_text, str) or not csv_text.strip():
        raise BadRequest("csv is required and must be a string")
    volume = _number(body, "volumeM3", 1, 1_000_000)
    outdoor = _number(body, "outdoorPpm", 300, 600, v.OUTDOOR_PPM_DEFAULT)
    columns = body.get("columns") or {}
    if not isinstance(columns, dict):
        raise BadRequest("columns must be an object")
    teaching = body.get("teachingHoursOnly", False)
    if not isinstance(teaching, bool):
        raise BadRequest("teachingHoursOnly must be true or false")

    series, dropped, skipped = parse_csv(csv_text, columns, outdoor)
    if len(series) < 2:
        raise BadRequest("fewer than 2 usable CO2 readings after parsing")

    decays = v.fit_decays(series, outdoor_ppm=outdoor)
    build_series = series
    if teaching:
        # Same split as the audit. Decays are fitted on everything and kept by
        # start time, since a room emptying at 17:55 decays past 18:00. Buildups
        # are fitted on the filtered series, so the overnight gap ends every
        # segment and none can straddle the window.
        decays = [f for f in decays if _in_teaching_hours(f.start)]
        build_series = [p for p in series if _in_teaching_hours(p[0])]
    buildups = v.fit_buildups(build_series, volume_m3=volume, outdoor_ppm=outdoor)
    # Unidentifiable buildups are counted but never enter the fingerprint.
    good = [b for b in buildups if b.identifiable]

    # ponytail: stride downsample for the chart; peakPpm is reported exactly, so a
    # skipped spike only affects the plot. Min/max buckets if the chart needs it.
    stride = max(1, math.ceil(len(series) / MAX_SERIES_POINTS))
    peak = max(c for _, c in series)
    return {
        "readings": len(series),
        "readingsDroppedBelowOutdoor": dropped,
        "rowsUnparseable": skipped,
        "span": [series[0][0].isoformat(), series[-1][0].isoformat()],
        "outdoorPpm": outdoor,
        "volumeM3": volume,
        "teachingHoursOnly": teaching,
        "peakPpm": peak,
        "peakRebreathedFraction": v.rebreathed_fraction(peak, outdoor),
        "peakOneBreathIn": _finite(v.one_breath_in(peak, outdoor)),
        "decay": {
            "fingerprint": _fingerprint_json(v.fingerprint(decays)),
            "fits": len(decays),
            "segments": _segments(decays),
        },
        # fingerprint() only reads .ach and .minutes, which BuildupFit also has.
        "buildup": {
            "fingerprint": _fingerprint_json(v.fingerprint(good)),
            "identifiable": len(good),
            "discarded": len(buildups) - len(good),
            "segments": _segments(good),  # identifiable only; discarded fits are never drawn
        },
        "series": [[t.isoformat(), c] for t, c in series[::stride]],
    }


@_handle
def predict(event):
    body = _body(event)
    volume = _number(body, "volumeM3", 1, 1_000_000)
    ach = _number(body, "ach", 0.01, 50)
    occupants = int(_number(body, "occupants", 0, 10_000))
    minutes = _number(body, "minutes", 1, 1440)
    outdoor = _number(body, "outdoorPpm", 300, 600, v.OUTDOOR_PPM_DEFAULT)
    start = body.get("startPpm")
    if start is not None:
        start = _number(body, "startPpm", outdoor, 10_000)
    activity = _activity(body, "seated_speaking")

    p = v.predict(volume, ach, occupants, minutes, activity, start, outdoor)
    return {
        "curve": [
            {"minute": s.minute, "ppm": s.co2_ppm, "rebreathedFraction": s.rebreathed_fraction}
            for s in p.curve
        ],
        "peakPpm": p.peak_ppm,
        "peakRebreathedFraction": v.rebreathed_fraction(p.peak_ppm, outdoor),
        "peakOneBreathIn": _finite(p.peak_one_in),
        "meanRebreathedFraction": p.mean_rebreathed_fraction,
        "minutesAbove1000": p.minutes_above_1000,
        "steadyStatePpm": p.steady_state_ppm,
        "maxOccupancy": {
            str(limit): v.max_occupancy(volume, ach, minutes, limit, activity, outdoor)
            for limit in (1000, 1400)
        },
    }


_clients = {}


def _client(name):
    # boto3 is only in the Lambda runtime and costs seconds to import at low
    # memory, so fit/predict never load it. Short timeouts, no retries: a slow
    # dependency must not push /health past its Lambda timeout.
    if name not in _clients:
        import boto3
        from botocore.config import Config
        _clients[name] = boto3.client(name, config=Config(
            connect_timeout=2, read_timeout=2, retries={"max_attempts": 1}))
    return _clients[name]


def site(event, context):
    """Serve web/index.html from the private bucket. Stand-in for CloudFront
    until the account is verified; see EnableCloudFront in template.yaml."""
    obj = _client("s3").get_object(Bucket=os.environ["WEB_BUCKET"], Key="index.html")
    return {
        "statusCode": 200,
        "headers": {
            "content-type": "text/html; charset=utf-8",
            # Short, so a deploy_web.py push is visible within a minute.
            "cache-control": "public, max-age=60",
            "strict-transport-security": "max-age=31536000",
            "x-content-type-options": "nosniff",
            "referrer-policy": "strict-origin-when-cross-origin",
        },
        "body": obj["Body"].read().decode("utf-8"),
    }


@_handle
def health(event):
    last = None
    try:
        last = _client("ssm").get_parameter(Name=AUDIT_PARAM)["Parameter"]["Value"]
    except Exception:
        pass  # missing parameter or SSM trouble: degraded, not down
    stale = True
    if last:
        try:
            t = datetime.fromisoformat(last)
            t = t if t.tzinfo else t.replace(tzinfo=timezone.utc)
            stale = datetime.now(timezone.utc) - t > AUDIT_STALE_AFTER
        except ValueError:
            pass
    return {"ok": True, "service": "secondbreath", "lastAuditRun": last, "auditStale": stale}
