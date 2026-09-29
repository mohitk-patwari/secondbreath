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

Other datasets
--------------
The same fits run over two school datasets, to test whether the halls are
unusual. Neither publishes room volumes or design airflow, so for these rooms
there is no design comparison and no implied occupancy: only fitted rates and
rebreathed air.

  Zenodo 5062837  (doi:10.5281/zenodo.5062837), CC BY 4.0. Six SCD30 sensors
                  in each of two primary schools, Castellon, Spain, May-June
                  2021 (Covid-19 ventilation measures in force). 5-min, UTC.
  Zenodo 18195710 (doi:10.5281/zenodo.18195710), CC BY 4.0. ENSENSIA sensors,
                  one per school, 25 schools, 2023-2025. Device coordinates
                  put nearly all of them in Patras, Greece. 10-min, UTC.
"""

from __future__ import annotations

import argparse
import csv
import inspect
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo

# ventilation.py lives at the repo root (shared by backend and analysis).
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import figures  # noqa: E402
import ventilation  # noqa: E402
from ventilation import (  # noqa: E402
    OUTDOOR_PPM_DEFAULT,
    fingerprint,
    fit_buildups,
    fit_decays,
    one_breath_in,
    rebreathed_fraction,
)

DATA_DIR = ROOT / "data"

# /health reports this so a judge can see how fresh the audit is.
SSM_PARAM = "/secondbreath/lastAuditRun"
AWS_REGION = "ap-south-1"

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

# A CO2 sensor never repeats one value for hours: occupants, drift and read
# noise all move it. ENSENSIA devices emit exactly 658 ppm for days while
# temperature and humidity keep changing (School 18: 46,826 readings in a
# row). Runs this long are a dead sensor and are dropped, and the count is
# reported. Outside such runs, no ENSENSIA file holds a value longer than
# 110 minutes (11 readings). Applied to the school datasets only; the halls
# have no fill value. The point minimum stops two equal readings either side
# of a data gap from counting as a flatline.
FLATLINE_MINUTES = 120.0
FLATLINE_POINTS = 13

# Occupancy sanity bounds for buildup fits. A rise of >= 250 ppm needs at
# least one person; packing people tighter than 2 m3 of room air each is not
# physically possible in a lecture hall (~0.6 m2 of floor x 3 m of ceiling is
# already ~1.8 m3). Out-of-bounds fits are flagged, listed and excluded from
# the medians: an absurd source term means the fitted rate is suspect too.
MIN_OCCUPANTS = 1.0
MIN_M3_PER_PERSON = 2.0


SPAIN = ("5062837", "spain", ZoneInfo("Europe/Madrid"),
         ["CEIP_LAlbea_ValldAbav2.csv", "CEIP_SantMiquel_Vilafames.csv"])
ENSENSIA = ("18195710", "ensensia", ZoneInfo("Europe/Athens"),
            [f"ensensia_raw_20230728-20251202_school_{i}.csv" for i in range(1, 26)])


def download(filename: str, record: str = "18385830", subdir: str = "") -> Path:
    folder = DATA_DIR / subdir
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / filename.replace(" ", "_")
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    url = f"https://zenodo.org/records/{record}/files/{urllib.parse.quote(filename)}?download=1"
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


def _to_local(stamp: str, tz: ZoneInfo) -> datetime:
    # Naive local time, matching the halls' export, so one teaching-hours rule
    # serves every dataset. ponytail: the repeated hour at the autumn clock
    # change interleaves two readings; it falls at 02:00-03:00, outside every
    # teaching window, so only an off-hours fit could be touched.
    t = datetime.fromisoformat(stamp.strip().replace("Z", "+00:00"))
    return t.replace(tzinfo=t.tzinfo or timezone.utc).astimezone(tz).replace(tzinfo=None)


def _drop_flatlines(series: list) -> tuple[list, int]:
    out, i, n = [], 0, len(series)
    while i < n:
        j = i
        while j + 1 < n and series[j + 1][1] == series[i][1]:
            j += 1
        if (j - i + 1 < FLATLINE_POINTS
                or (series[j][0] - series[i][0]).total_seconds() / 60.0 < FLATLINE_MINUTES):
            out.extend(series[i:j + 1])
        i = j + 1
    return out, n - len(out)


def _collect(rows, tz: ZoneInfo, stamp_col: str, room_of) -> dict[str, tuple[list, int, int]]:
    """Group rows into one CO2 series per room. Duplicate timestamps keep the
    last reading; sub-floor readings are dropped and counted, as for the halls,
    and so are flatlines. Returns room -> (series, dropped_floor, dropped_flat)."""
    rooms: dict[str, dict[datetime, float]] = {}
    dropped: dict[str, int] = {}
    for r in rows:
        try:
            co2 = float(r["co2"])
            t = _to_local(r[stamp_col], tz)
        except (ValueError, KeyError, TypeError):
            continue
        room = room_of(r)
        if co2 < SENSOR_FLOOR_PPM:
            dropped[room] = dropped.get(room, 0) + 1
            continue
        rooms.setdefault(room, {})[t] = co2
    out = {}
    for k, v in rooms.items():
        series, flat = _drop_flatlines(sorted(v.items()))
        out[k] = (series, dropped.get(k, 0), flat)
    return out


def load_spain(path: Path, tz: ZoneInfo) -> dict[str, tuple[list, int, int]]:
    """Two layouts in one record: L'Albea is plain CSV; Sant Miquel wraps each
    whole line in quotes (inner quotes doubled), so it parses as one field that
    is itself a CSV line. Timestamps are UTC (published_at ends in Z and equals
    date_time). One room per sensor_id within a school."""
    def rows():
        with path.open(encoding="utf-8-sig", newline="") as fh:
            lines = (r if len(r) > 1 else next(csv.reader([r[0]])) for r in csv.reader(fh))
            header = next(lines)
            for r in lines:
                yield dict(zip(header, r))
    school = path.stem.split("_")[-1].replace("v2", "")
    return _collect(rows(), tz, "published_at", lambda r: f"{school} {r['sensor_id'].strip()}")


def load_ensensia(path: Path, tz: ZoneInfo) -> dict[str, tuple[list, int, int]]:
    """Plain CSV, `date` in UTC per the record's README. Each school file holds
    one sensor_id, so each school is one room."""
    school = "School " + path.stem.split("_")[-1]
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return _collect(csv.DictReader(fh), tz, "date", lambda r: school)


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


def analyse(name: str, series: list, dropped: int, volume: float | None = None,
            design_flow: float | None = None) -> tuple[dict, list, list, list] | None:
    """Returns the summary plus the series and kept fits the figures draw, or
    None if the room has no readings inside teaching hours.

    Without a volume (the school datasets) the buildup rate is unchanged: the
    fitted rate, its profile band and identifiability never use volume, which
    only scales the implied occupancy. So occupancy is not reported and the
    occupancy sanity bound, which needs volume, is not applied."""
    design_ach = design_flow / volume if volume and design_flow else None

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
    if not occupied_series:
        return None
    # ponytail: 1.0 is a placeholder that only scales implied_occupants, which
    # is never reported when volume is None.
    raw_builds = fit_buildups(occupied_series, volume_m3=volume or 1.0, activity=BUILDUP_ACTIVITY)
    ident = [b for b in raw_builds if b.identifiable]
    max_people = volume / MIN_M3_PER_PERSON if volume else None
    sane = lambda b: max_people is None or MIN_OCCUPANTS <= b.implied_occupants <= max_people  # noqa: E731
    kept = [b for b in ident if sane(b)]
    absurd = [b for b in ident if not sane(b)]
    fp_build = fingerprint(kept)  # only reads .ach and .minutes, both on BuildupFit

    occupied = sorted(c for _, c in occupied_series)

    def share_above(threshold: float) -> float:
        return 100.0 * sum(1 for c in occupied if c > threshold) / len(occupied)

    worst = occupied[-1]
    mid = occupied[len(occupied) // 2]
    discarded = len(raw_builds) - len(ident)
    ratio = lambda fp: round(design_ach / fp.ach_median, 1) if fp and design_ach else None  # noqa: E731

    summary = {
        "hall": name,
        "volume_m3": volume,
        "design_airflow_m3h": design_flow,
        "design_ach": round(design_ach, 2) if design_ach else None,
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
            "shortfall_factor": ratio(fp_day),
        },
        "buildup": {
            "fits_passing_r2": len(raw_builds),
            "identifiable": len(ident),
            "discarded_unidentifiable": discarded,
            "discard_rate_pct": round(100.0 * discarded / len(raw_builds), 1) if raw_builds else None,
            "occupancy_bounds": [MIN_OCCUPANTS, round(max_people)] if max_people else None,
            "flagged_absurd_occupancy": [
                {"start": b.start.isoformat(), "ach": round(b.ach, 2),
                 "implied_occupants": round(b.implied_occupants, 1)}
                for b in absurd
            ],
            "kept": len(kept),
            "ach": rnd(fp_build.ach_median) if fp_build else None,
            "ach_iqr": [rnd(fp_build.ach_p25), rnd(fp_build.ach_p75)] if fp_build else None,
            "confident": bool(fp_build and fp_build.confident),
            "implied_occupants_median": (round(median(b.implied_occupants for b in kept))
                                         if kept and volume else None),
            "shortfall_factor": ratio(fp_build),
        },
        "median_co2_teaching": round(mid),
        "p95_co2_teaching": round(occupied[len(occupied) * 95 // 100]),
        "peak_co2_teaching": round(worst),
        "peak_one_breath_in": round(one_breath_in(worst)),
        "median_rebreathed_pct_teaching": round(100.0 * rebreathed_fraction(mid), 2),
        "peak_rebreathed_pct_teaching": round(100.0 * rebreathed_fraction(worst), 2),
        "pct_time_above_1000": round(share_above(1000.0), 1),
        "pct_time_above_1400": round(share_above(1400.0), 1),
        "pct_time_above_2000": round(share_above(2000.0), 1),
    }
    return summary, series, day_fits, kept


def method() -> dict:
    return {
        "dataset": "Zenodo 18385830 (doi:10.5281/zenodo.18385830), CC BY 4.0",
        "other_datasets": "Zenodo 5062837 and 18195710, CC BY 4.0: same fits, same parameters, "
                          "UTC timestamps converted to local time before the teaching-hours split; "
                          f"any value repeated unchanged for >= {FLATLINE_POINTS} readings and "
                          f">= {FLATLINE_MINUTES:.0f} min is a dead "
                          "sensor and dropped (count per room in readings_dropped_flatline); "
                          "no volume, so no design comparison, no implied occupancy and no "
                          "occupancy sanity bound",
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


def record_run(stamp: str) -> None:
    """Publish the run time to SSM. Failure only warns: the audit's numbers
    are valid without AWS, and /health treats a missing value as stale."""
    cmd = ["aws", "ssm", "put-parameter", "--region", AWS_REGION, "--name", SSM_PARAM,
           "--type", "String", "--overwrite", "--value", stamp]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"{SSM_PARAM} = {stamp}", file=sys.stderr)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"warning: could not write {SSM_PARAM}: {getattr(exc, 'stderr', exc)}",
              file=sys.stderr)


def run_dataset(record: str, subdir: str, tz: ZoneInfo, files: list[str], loader, label: str) -> dict:
    rooms, empty = [], []
    for filename in files:
        print(f"{label}: {filename}", file=sys.stderr)
        for room, (series, dropped, flat) in sorted(loader(download(filename, record, subdir), tz).items()):
            got = analyse(room, series, dropped) if series else None
            if got:
                got[0]["readings_dropped_flatline"] = flat
                rooms.append(got[0])
            else:
                empty.append(room)
    return {
        "label": label,
        "dataset": f"Zenodo {record} (doi:10.5281/zenodo.{record}), CC BY 4.0",
        "timezone": str(tz),
        "design_comparison": None,
        "design_note": "No room volumes or design ventilation are published for this dataset, so "
                       "no design comparison and no implied occupancy are possible. Reported: "
                       "fitted air-change rates and rebreathed air only.",
        "rooms_without_teaching_hours_data": empty,
        "rooms": rooms,
    }


def rooms_analysed(halls: list[dict], others: list[dict]) -> dict:
    """How many rooms the finding rests on. A room counts once it has any
    teaching-hours readings; the confident counts are the ones worth quoting."""
    groups = [("Zenodo 18385830 lecture halls", halls)] + [(ds["label"], ds["rooms"]) for ds in others]
    per = {
        label: {
            "rooms": len(rs),
            "confident_decay": sum(r["decay"]["confident"] for r in rs),
            "confident_buildup": sum(r["buildup"]["confident"] for r in rs),
            "with_design_figure": sum(r["design_ach"] is not None for r in rs),
        }
        for label, rs in groups
    }
    return {"total": sum(v["rooms"] for v in per.values()),
            "confident_decay": sum(v["confident_decay"] for v in per.values()),
            "confident_buildup": sum(v["confident_buildup"] for v in per.values()),
            "with_design_figure": sum(v["with_design_figure"] for v in per.values()),
            "by_dataset": per}


def fmt(v: float | None, n: str) -> str:
    return f"{v:.2f} ({n})" if v is not None else f"- ({n})"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="also write analysis/audit.json")
    args = ap.parse_args()

    results = []
    fig_dir = ROOT / "analysis" / "figures"
    fig_dir.mkdir(exist_ok=True)
    for name, filename, volume, flow in HALLS:
        print(f"{name}:", file=sys.stderr)
        summary, series, decay, build = analyse(name, *load_series(download(filename)), volume, flow)
        results.append(summary)
        figures.hall_svg(summary, series, decay, build,
                         fig_dir / f"{name.lower().replace(' ', '_')}.svg")
    figures.summary_svg(results, fig_dir / "design_vs_measured.svg")

    others = [run_dataset(*SPAIN, load_spain, "Primary classrooms, Castellon, Spain (2021)"),
              run_dataset(*ENSENSIA, load_ensensia, "ENSENSIA schools, Patras, Greece (2023-25)")]
    figures.rooms_svg(results, others, fig_dir / "all_rooms.svg")
    rooms = rooms_analysed(results, others)

    if args.json:
        out = {"method": method(), "halls": results, "rooms_analysed": rooms, "other_datasets": others}
        # LF on every OS, so a rerun can be checked against the commit by hash.
        (ROOT / "analysis" / "audit.json").write_text(json.dumps(out, indent=2) + "\n",
                                                      encoding="utf-8", newline="\n")

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

    print()
    for ds in others:
        print(f"{ds['label']} ({ds['dataset']}): {len(ds['rooms'])} rooms, "
              f"{len(ds['rooms_without_teaching_hours_data'])} without teaching-hours data")
        for r in ds["rooms"]:
            d, b = r["decay"], r["buildup"]
            print(f"  {r['hall']:<22} decay {fmt(d['ach_teaching'], str(d['fits_teaching']))}"
                  f"{'' if d['confident'] else ' ?':<3} buildup {fmt(b['ach'], str(b['kept']))}"
                  f"{'' if b['confident'] else ' ?':<3} median {r['median_co2_teaching']} ppm "
                  f"({r['median_rebreathed_pct_teaching']}% rebreathed), p95 {r['p95_co2_teaching']}, "
                  f"peak {r['peak_co2_teaching']}")
    print(json.dumps(rooms, indent=1))

    record_run(datetime.now(timezone.utc).isoformat(timespec="seconds"))


if __name__ == "__main__":
    main()
