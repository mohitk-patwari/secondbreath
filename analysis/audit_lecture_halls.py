"""
SecondBreath -- reproducible audit of three university lecture halls.

Downloads an open dataset, fits every usable CO2 decay segment, and compares
the delivered air-change rate against each room's design specification.

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
    python analysis/audit_lecture_halls.py --json     # machine-readable output

Writes downloaded CSVs to <repo>/data/ and, with --json, analysis/audit.json
to commit as evidence beside the write-up.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# ventilation.py belongs at the repo root (shared by backend and analysis);
# put the root on the path so this runs from any cwd.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ventilation import (
    OUTDOOR_PPM_DEFAULT,
    fingerprint,
    fit_decays,
    one_breath_in,
    required_ach,
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


def download(filename: str) -> Path:
    DATA_DIR.mkdir(exist_ok=True)
    dest = DATA_DIR / filename.replace(" ", "_")
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    url = f"{ZENODO}/{urllib.parse.quote(filename)}?download=1"
    print(f"  downloading {filename} ...", file=sys.stderr)
    urllib.request.urlretrieve(url, dest)
    return dest


def load_series(path: Path) -> list[tuple[datetime, float]]:
    """Read the semicolon-delimited export; rows alternate between sensors,
    so many rows have an empty CO2 field and are skipped."""
    out: list[tuple[datetime, float]] = []
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
            # Readings below outdoor are a known low-cost-sensor artefact
            # (automatic baseline correction drift). Drop rather than clamp.
            if co2 < 350.0:
                continue
            out.append((stamp, co2))
    out.sort()
    return out


def in_teaching_hours(stamp: datetime) -> bool:
    return stamp.weekday() < 5 and TEACHING_START_HOUR <= stamp.hour < TEACHING_END_HOUR


def analyse(name: str, path: Path, volume: float, design_flow: float) -> dict:
    series = load_series(path)
    design_ach = design_flow / volume

    fits = fit_decays(series, outdoor_ppm=OUTDOOR_PPM_DEFAULT)
    day_fits = [f for f in fits if in_teaching_hours(f.start)]
    off_fits = [f for f in fits if not in_teaching_hours(f.start)]

    fp_day = fingerprint(day_fits)
    fp_off = fingerprint(off_fits)

    occupied = [c for t, c in series if in_teaching_hours(t)]
    occupied.sort()

    def share_above(threshold: float) -> float:
        return 100.0 * sum(1 for c in occupied if c > threshold) / len(occupied)

    worst = occupied[-1]
    median = occupied[len(occupied) // 2]

    return {
        "hall": name,
        "volume_m3": volume,
        "design_airflow_m3h": design_flow,
        "design_ach": round(design_ach, 2),
        "readings_total": len(series),
        "readings_teaching_hours": len(occupied),
        "span": [series[0][0].isoformat(), series[-1][0].isoformat()],
        "fitted_ach_teaching": round(fp_day.ach_median, 2) if fp_day else None,
        "fitted_ach_teaching_iqr": (
            [round(fp_day.ach_p25, 2), round(fp_day.ach_p75, 2)] if fp_day else None
        ),
        "fits_teaching": len(day_fits),
        "fitted_ach_offhours": round(fp_off.ach_median, 2) if fp_off else None,
        "fits_offhours": len(off_fits),
        "shortfall_factor": (
            round(design_ach / fp_day.ach_median, 1) if fp_day and fp_day.ach_median else None
        ),
        "median_co2_teaching": round(median),
        "peak_co2_teaching": round(worst),
        "peak_one_breath_in": round(one_breath_in(worst)),
        "pct_time_above_1000": round(share_above(1000.0), 1),
        "pct_time_above_1400": round(share_above(1400.0), 1),
        "pct_time_above_2000": round(share_above(2000.0), 1),
        "confident": bool(fp_day and fp_day.confident),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="write audit.json and print it")
    args = ap.parse_args()

    results = []
    for name, filename, volume, flow in HALLS:
        print(f"{name}:", file=sys.stderr)
        results.append(analyse(name, download(filename), volume, flow))

    if args.json:
        (ROOT / "analysis" / "audit.json").write_text(json.dumps(results, indent=2))
        print(json.dumps(results, indent=2))
        return

    print()
    print(f"{'Hall':<8}{'Design':>8}{'Fitted':>8}{'IQR':>14}{'Fits':>6}{'Off-hrs':>9}{'Short':>7}")
    print("-" * 60)
    for r in results:
        iqr = r["fitted_ach_teaching_iqr"]
        print(
            f"{r['hall']:<8}{r['design_ach']:>8.1f}{r['fitted_ach_teaching']:>8.2f}"
            f"{f'{iqr[0]}-{iqr[1]}':>14}{r['fits_teaching']:>6}"
            f"{r['fitted_ach_offhours']:>9.2f}{r['shortfall_factor']:>6.1f}x"
        )

    print()
    for r in results:
        print(
            f"{r['hall']}: peak {r['peak_co2_teaching']} ppm "
            f"(1 breath in {r['peak_one_breath_in']}), "
            f"{r['pct_time_above_1000']}% of teaching hours over 1000 ppm, "
            f"{r['pct_time_above_1400']}% over 1400."
        )

    # What it would take to meet a 1000 ppm ceiling at realistic occupancy.
    print()
    for r in results:
        seats = int(r["volume_m3"] / 2.5)  # rough seat count from volume
        need = required_ach(r["volume_m3"], seats, limit_ppm=1000.0)
        print(
            f"{r['hall']}: holding {seats} people under 1000 ppm needs "
            f"{need:.1f} ACH; measured {r['fitted_ach_teaching']:.2f}."
        )


if __name__ == "__main__":
    main()
