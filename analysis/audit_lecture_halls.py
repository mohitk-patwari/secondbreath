"""
SecondBreath -- reproducible audit of three university lecture halls.

Downloads an open dataset and measures each hall's air-change rate two
independent ways, then compares both against the design specification:

  decay    -- fit_decays() on falling CO2 after occupancy (room emptying)
  buildup  -- fit_buildups() on rising CO2 during weekday teaching hours
              (room occupied), keeping only identifiable fits

Data source
-----------
"Indoor Environmental Quality Measurements of University Lecture Halls"
Zenodo record 18385830, CC BY 4.0. Three lecture halls in Limassol, Cyprus,
monitored with Airthings Space Pro sensors for a full academic year
(Sept 2023 - Aug 2024). The record ships a characteristics file giving each
hall's volume and designed ventilation.

Design specification, quoted from that characteristics file:
    Hall A   363 m3    2,100 m3/h   100% fresh air   ~6 ACH
    Hall B   283 m3    1,700 m3/h   100% fresh air   ~6 ACH
    Hall C  1,520 m3   9,000 m3/h   100% fresh air   ~6 ACH

Usage
-----
    python analysis/audit_lecture_halls.py            # download (once) and analyse
    python analysis/audit_lecture_halls.py --json     # also write analysis/audit.json

Downloaded CSVs go to <repo>/data/ (gitignored).
"""

from __future__ import annotations

import argparse
import csv
import inspect
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from statistics import median

# ventilation.py lives at the repo root (shared by backend and analysis).
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import ventilation  # noqa: E402
from ventilation import (  # noqa: E402
    OUTDOOR_PPM_DEFAULT,
    fingerprint,
    fit_buildups,
    fit_decays,
    one_breath_in,
)

ZENODO = "https://zenodo.org/records/18385830/files"
DATA_DIR = ROOT / "data"

HALLS = [
    # name, filename, volume m^3, design airflow m^3/h
    ("Hall A", "Lecture Hall A_raw_data.csv", 363.0, 2100.0),
    ("Hall B", "Lecture Hall B_raw_data.csv", 283.0, 1700.0),
    ("Hall C", "Lecture Hall C_raw_data.csv", 1520.0, 9000.0),
]

# Weekday teaching hours used to separate "in use" from "building asleep".
TEACHING_START_HOUR = 8
TEACHING_END_HOUR = 18

# Readings below this are a known low-cost-sensor artefact (automatic baseline
# correction drift). Dropped, not clamped, and the drop count is reported.
SENSOR_FLOOR_PPM = 350.0

BUILDUP_ACTIVITY = "seated_quiet"

# Occupancy sanity bounds for buildup fits. A rise of >= 250 ppm needs at
# least one person; packing people tighter than 2 m3 of room air each is not
# physically possible in a lecture hall (~0.6 m2 of floor x 3 m of ceiling is
# already ~1.8 m3). Out-of-bounds fits are flagged, listed and excluded from
# the medians: an absurd source term means the fitted rate is suspect too.
MIN_OCCUPANTS = 1.0
MIN_M3_PER_PERSON = 2.0


def download(filename: str) -> Path:
    DATA_DIR.mkdir(exist_ok=True)
    dest = DATA_DIR / filename.replace(" ", "_")
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    url = f"{ZENODO}/{urllib.parse.quote(filename)}?download=1"
    print(f"  downloading {filename} ...", file=sys.stderr)
    urllib.request.urlretrieve(url, dest)
    return dest


def load_series(path: Path) -> tuple[list[tuple[datetime, float]], int]:
    """Read the semicolon-delimited export; rows alternate between sensors,
    so many rows have an empty CO2 field and are skipped. Returns the series
    and the number of readings dropped below SENSOR_FLOOR_PPM."""
    out: list[tuple[datetime, float]] = []
    dropped = 0
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=";"):
            raw = (row.get("CO2 ppm") or "").strip()
            if not raw:
                continue
            try:
                co2 = float(raw)
                stamp = datetime.fromisoformat(row["recorded"].strip())
            except (ValueError, KeyError):
                continue
            if co2 < SENSOR_FLOOR_PPM:
                dropped += 1
                continue
            out.append((stamp, co2))
    out.sort()
    return out, dropped


def in_teaching_hours(stamp: datetime) -> bool:
    return stamp.weekday() < 5 and TEACHING_START_HOUR <= stamp.hour < TEACHING_END_HOUR


def defaults(fn) -> dict:
    """Keyword defaults of a ventilation.py function, read from the code
    itself so the method block can never drift from what actually ran."""
    return {
        k: list(p.default) if isinstance(p.default, tuple) else p.default
        for k, p in inspect.signature(fn).parameters.items()
        if p.default is not inspect.Parameter.empty
    }


def rnd(x: float | None) -> float | None:
    return round(x, 2) if x is not None else None


def analyse(name: str, path: Path, volume: float, design_flow: float) -> dict:
    series, dropped = load_series(path)
    design_ach = design_flow / volume

    # Decay: the room while it empties.
    fits = fit_decays(series, outdoor_ppm=OUTDOOR_PPM_DEFAULT)
    day_fits = [f for f in fits if in_teaching_hours(f.start)]
    off_fits = [f for f in fits if not in_teaching_hours(f.start)]
    fp_day = fingerprint(day_fits)
    fp_off = fingerprint(off_fits)

    # Buildup: the room while occupied. Filter the series, not the fits: the
    # overnight gap then exceeds max_gap_seconds, so no segment can straddle
    # the teaching window.
    occupied_series = [(t, c) for t, c in series if in_teaching_hours(t)]
    raw_builds = fit_buildups(occupied_series, volume_m3=volume, activity=BUILDUP_ACTIVITY)
    ident = [b for b in raw_builds if b.identifiable]
    max_people = volume / MIN_M3_PER_PERSON
    sane = lambda b: MIN_OCCUPANTS <= b.implied_occupants <= max_people  # noqa: E731
    kept = [b for b in ident if sane(b)]
    absurd = [b for b in ident if not sane(b)]
    fp_build = fingerprint(kept)  # only reads .ach and .minutes, both on BuildupFit

    occupied = sorted(c for _, c in occupied_series)

    def share_above(threshold: float) -> float:
        return 100.0 * sum(1 for c in occupied if c > threshold) / len(occupied)

    worst = occupied[-1]
    discarded = len(raw_builds) - len(ident)

    return {
        "hall": name,
        "volume_m3": volume,
        "design_airflow_m3h": design_flow,
        "design_ach": round(design_ach, 2),
        "readings_total": len(series),
        "readings_dropped_below_floor": dropped,
        "readings_teaching_hours": len(occupied),
        "span": [series[0][0].isoformat(), series[-1][0].isoformat()],
        "decay": {
            "ach_teaching": rnd(fp_day.ach_median) if fp_day else None,
            "ach_teaching_iqr": [rnd(fp_day.ach_p25), rnd(fp_day.ach_p75)] if fp_day else None,
            "fits_teaching": len(day_fits),
            "confident": bool(fp_day and fp_day.confident),
            "ach_offhours": rnd(fp_off.ach_median) if fp_off else None,
            "fits_offhours": len(off_fits),
            "shortfall_factor": round(design_ach / fp_day.ach_median, 1) if fp_day else None,
        },
        "buildup": {
            "fits_passing_r2": len(raw_builds),
            "identifiable": len(ident),
            "discarded_unidentifiable": discarded,
            "discard_rate_pct": round(100.0 * discarded / len(raw_builds), 1) if raw_builds else None,
            "occupancy_bounds": [MIN_OCCUPANTS, round(max_people)],
            "flagged_absurd_occupancy": [
                {"start": b.start.isoformat(), "ach": round(b.ach, 2),
                 "implied_occupants": round(b.implied_occupants, 1)}
                for b in absurd
            ],
            "kept": len(kept),
            "ach": rnd(fp_build.ach_median) if fp_build else None,
            "ach_iqr": [rnd(fp_build.ach_p25), rnd(fp_build.ach_p75)] if fp_build else None,
            "confident": bool(fp_build and fp_build.confident),
            "implied_occupants_median": round(median(b.implied_occupants for b in kept)) if kept else None,
            "shortfall_factor": round(design_ach / fp_build.ach_median, 1) if fp_build else None,
        },
        "median_co2_teaching": round(occupied[len(occupied) // 2]),
        "peak_co2_teaching": round(worst),
        "peak_one_breath_in": round(one_breath_in(worst)),
        "pct_time_above_1000": round(share_above(1000.0), 1),
        "pct_time_above_1400": round(share_above(1400.0), 1),
        "pct_time_above_2000": round(share_above(2000.0), 1),
    }


def method() -> dict:
    return {
        "dataset": "Zenodo 18385830 (doi:10.5281/zenodo.18385830), CC BY 4.0",
        "outdoor_ppm": OUTDOOR_PPM_DEFAULT,
        "sensor_floor_ppm": SENSOR_FLOOR_PPM,
        "teaching_hours": {"weekdays": "Mon-Fri", "start_hour": TEACHING_START_HOUR,
                           "end_hour_exclusive": TEACHING_END_HOUR},
        "decay": {
            "function": "ventilation.fit_decays",
            "params": defaults(fit_decays),
            "teaching_split": "each fit classified by its start timestamp",
            "summary": "ventilation.fingerprint: median and IQR; confident if n >= 5 and IQR/median < 0.8",
        },
        "buildup": {
            "function": "ventilation.fit_buildups",
            "activity": BUILDUP_ACTIVITY,
            "generation_m3h_per_person": ventilation.GENERATION_M3H[BUILDUP_ACTIVITY],
            "params": defaults(fit_buildups),
            "profile_tolerance": defaults(ventilation._fit_single_buildup)["profile_tolerance"],
            "series_filter": "only readings inside teaching hours are passed in",
            "identifiable_rule": "ach_lo > 0 and ach_hi / ach_lo < 3.0",
            "discard_note": "fits_passing_r2 counts only segments fit_buildups returned "
                            "(r2 >= min_r2); segments rejected before that are not counted",
            "occupancy_sanity": {"min_occupants": MIN_OCCUPANTS,
                                 "min_m3_per_person": MIN_M3_PER_PERSON,
                                 "action": "flagged, listed, excluded from medians"},
            "summary": "ventilation.fingerprint over kept fits",
        },
    }


def fmt(v: float | None, n: str) -> str:
    return f"{v:.2f} ({n})" if v is not None else f"- ({n})"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="also write analysis/audit.json")
    args = ap.parse_args()

    results = []
    for name, filename, volume, flow in HALLS:
        print(f"{name}:", file=sys.stderr)
        results.append(analyse(name, download(filename), volume, flow))

    if args.json:
        out = {"method": method(), "halls": results}
        (ROOT / "analysis" / "audit.json").write_text(json.dumps(out, indent=2) + "\n")

    print()
    print(f"{'Hall':<8}{'Design':>6}  {'Decay ACH (n)':<22}{'Buildup ACH (kept/ident)':<28}"
          f"{'Occ.':>5}  Shortfall dec / bld")
    print("-" * 90)
    for r in results:
        d, b = r["decay"], r["buildup"]
        dec = fmt(d["ach_teaching"], str(d["fits_teaching"])) + ("" if d["confident"] else " ?")
        bld = fmt(b["ach"], f"{b['kept']}/{b['identifiable']}") + ("" if b["confident"] else " ?")
        occ = b["implied_occupants_median"]
        print(f"{r['hall']:<8}{r['design_ach']:>6.1f}  {dec:<22}{bld:<28}"
              f"{occ if occ is not None else '-':>5}  "
              f"{d['shortfall_factor']}x / {b['shortfall_factor']}x")
    print("? = fingerprint not confident (n < 5 or IQR/median >= 0.8)")

    print()
    for r in results:
        d, b = r["decay"], r["buildup"]
        print(f"{r['hall']}: decay IQR {d['ach_teaching_iqr']}, off-hours {d['ach_offhours']} "
              f"({d['fits_offhours']}); buildup IQR {b['ach_iqr']}, discarded "
              f"{b['discarded_unidentifiable']}/{b['fits_passing_r2']} unidentifiable "
              f"({b['discard_rate_pct']}%), flagged {len(b['flagged_absurd_occupancy'])} "
              f"outside {b['occupancy_bounds'][0]:.0f}-{b['occupancy_bounds'][1]} occupants.")

    print()
    for r in results:
        print(f"{r['hall']}: peak {r['peak_co2_teaching']} ppm "
              f"(1 breath in {r['peak_one_breath_in']}), "
              f"{r['pct_time_above_1000']}% of teaching hours over 1000 ppm, "
              f"{r['pct_time_above_1400']}% over 1400; "
              f"{r['readings_dropped_below_floor']} readings dropped below "
              f"{SENSOR_FLOOR_PPM:.0f} ppm.")


if __name__ == "__main__":
    main()
