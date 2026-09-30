# Method: every filter, every threshold, everything discarded

This file is for a reviewer who wants to challenge a number. Each rule below
gives its value, where it lives in code, why it was chosen, and what it removed.
Where a threshold is a judgment call rather than something derived, it says so.

All counts are from `analysis/audit.json` as committed, or from a stated
one-off check against the same data.

---

## 1. Reproduce it

```
git clone <repo> && cd <repo>
python analysis/audit_lecture_halls.py --json    # downloads 30 CSVs from Zenodo, ~6 min
python analysis/test_loaders.py                   # loader checks
python ventilation.py                             # physics self-tests
sha256sum analysis/audit.json analysis/figures/*.svg
```

Python 3.12 standard library only (no numpy, no pip installs). The script also
writes the run time to SSM `/secondbreath/lastAuditRun`. That step only warns
if AWS is unreachable, and the numbers do not depend on it.

**Verified 29 Sep 2026, in two steps.** First, a fresh clone of commit
8960f6b with no `data/` directory downloaded all 30 files and reproduced
`audit.json` and all five figures with **identical content**. On Windows that
code wrote CRLF line endings, so only the line endings differed. The outputs
are now written with LF on every OS. Second, a rerun after that change matched
the committed files **byte for byte**, at these hashes:

| Output | sha256 |
|---|---|
| audit.json | `4e5689cc95c382f1b576bbf6aa6f930b884d623e88ec6a9c9d8eb8ef1129dc51` |
| figures/all_rooms.svg | `30c6003f70fc4a76e165b5fc245aea30cf901afc414eb382dddff60798e4d269` |
| figures/design_vs_measured.svg | `8d9f9301914eed50cff7103b0d96cf0b2694aa47aab583531ccaca7b2a03d853` |
| figures/hall_a.svg | `4cbd3826722b4e31898a5026cc70f9726b5fc205f84ca5044333bcccc431c445` |
| figures/hall_b.svg | `d4d108dc737ffd97c4d0dadd6065ef1717bfed307c299c610d4febdc94b929da` |
| figures/hall_c.svg | `a63f91d0a81235d96c108899959f10f341cc462356057cbd84b0e1c83c0532c3` |

The freshly downloaded inputs were also byte-identical to the copies used
during development. Their hashes are in section 9, so a later change to a
Zenodo file would be visible.

---

## 2. Data

| Dataset | Rooms | Sampling | Time zone handling | Design figure |
|---|---|---|---|---|
| Zenodo 18385830, lecture halls, Limassol, Cyprus, Sep 2023 – Aug 2024 | 3 | 5 min | `recorded` used as-is (see 7.6) | Yes: volume and airflow from the record's characteristics file |
| Zenodo 5062837, primary schools, Castellón, Spain, May–Jun 2021 | 12 (6 sensors × 2 schools) | 5 min | UTC (`published_at` ends in `Z` and equals `date_time`) → Europe/Madrid | No |
| Zenodo 18195710, ENSENSIA, 25 schools, 2023–2025 | 25 (one sensor per school file) | 10 min | UTC per the record's README → Europe/Athens | No |

Zenodo 5062837 is version 2 of concept record 5036227. The Data in Brief paper
(doi:10.1016/j.dib.2021.107489) cites version 1, 5036228. Checked 1 Oct 2026:
version 1's `CEIP_SantMiquel_Vilafames.csv` has the same md5 as ours, and its
`CEIP_Albea_ValldAlba.csv` holds exactly the rows of our `CEIP_LAlbea_ValldAbav2.csv`
in a different order. The loader sorts by timestamp, so both versions give
identical results. We cite 5062837 because it is the one we download and checksum (section 9).

All three are CC BY 4.0. **The two school datasets publish no room volume and no
design airflow, so no design comparison is possible for them.** They report
fitted rates and rebreathed air only, and `audit.json` says so in each
dataset's `design_note`. For the same reason they have no implied occupancy
(section 5.4).

ENSENSIA location: the device coordinates put nearly every device in Patras,
Greece. A few rows carry Athens or Turku coordinates. Both are in the
same time zone offset as Athens, so the local-time conversion is unaffected.

---

## 3. Order of operations

For each room: load → drop readings below 350 ppm → (school datasets only)
drop flatlines → convert to local time → fit decays on the whole series and
classify each fit by its start time → fit buildups on the teaching-hours
readings only → summarise with `fingerprint()`.

---

## 4. Reading-level filters (applied before any fitting)

### 4.1 Sensor floor: drop readings below 350 ppm

- **Where:** `SENSOR_FLOOR_PPM = 350.0`, `analysis/audit_lecture_halls.py:95`
- **Why:** outdoor air is about 420 ppm, so an indoor reading well below that
  is not air. It is a low-cost-sensor artefact: automatic baseline correction
  pulls the zero point down. **Dropped, not clamped:** clamping would invent
  a value, while dropping leaves a gap the fitters already handle.
- **Discarded:**

  | | Readings kept | Dropped < 350 |
  |---|---|---|
  | Halls | 265,213 | 0 |
  | Spain | 72,691 | 186, all in Vilafamés CO2_06 |
  | ENSENSIA | 1,086,871 | 19,694, of which School 19 is 10,198 |

  School 19 lost more readings to the floor (10,198) than it kept (9,082).
  Its sensor is unreliable, and its decay fit is not confident (section 6).
- **Challenge it:** CLAUDE.md words the rule as "readings below outdoor level
  are dropped". The code uses 350, not 420. **Readings from 350 to 420 ppm
  are kept.** They are 1.2% (Hall A), 1.3% (B), 3.0% (C) and 11.0% (schools)
  of all readings. They are kept because 420 is an assumed constant (4.4),
  while the true outdoor level varies by tens of ppm and a sensor can
  read slightly low. Dropping everything under 420 would delete real
  empty-room baselines. These readings can't create a fit: a decay segment
  ends at 480 ppm (420 + 60), and the rebreathed fraction treats anything at
  or below 420 as zero. The 350 figure itself is a judgment call.

### 4.2 Flatline filter: ENSENSIA and Spain only

- **Where:** `FLATLINE_MINUTES = 120.0`, `FLATLINE_POINTS = 13`,
  `_drop_flatlines()`, `analysis/audit_lecture_halls.py:107-108, 170`.
  Test: `analysis/test_loaders.py`
- **Rule:** one value, unchanged, for at least 13 consecutive readings **and**
  at least 120 minutes is a dead sensor. The whole run is dropped.
- **Why:** ENSENSIA devices emit exactly **658 ppm** for days while the same
  row's temperature and humidity keep changing. School 18 holds that value
  for 46,826 readings in a row, which is 90% of its data. A live NDIR sensor
  never repeats one value for hours: occupants, drift and read noise all move
  it. Left in, the fill value made fake room medians (Schools 19 and 21 both
  reported a "median" of exactly 658).
- **How the threshold was set:** outside runs of 658, the longest identical
  run in any ENSENSIA file is 11 readings (110 minutes, School 12). The rule
  sits just above that. The 13-point minimum exists because a duration-only
  rule dropped pairs of coincidentally equal readings on either side of a
  data gap. That bug was caught and fixed before the numbers were committed.
- **Discarded:** 99,763 ENSENSIA readings in 8 schools: School 18 46,826 ·
  School 19 25,445 · School 21 22,927 · School 6 2,088 · School 9 1,156 ·
  School 15 1,131 · School 13 137 · School 23 53. Spain: 0.
- **Not applied to the halls.** A one-off check found 0 flatline readings in
  all three halls, so applying it there would change nothing. It was left out
  so the halls' pipeline stays exactly as it was.

### 4.3 Duplicate timestamps (school datasets)

The last reading for a timestamp wins. This rarely matters. It exists so a
repeated timestamp can't end a decay segment early.

### 4.4 Outdoor CO2: 420 ppm, assumed, not measured

- **Where:** `OUTDOOR_PPM_DEFAULT = 420.0`, `ventilation.py:58`
- **Why:** none of the datasets record outdoor CO2. 420 ppm is the typical
  present-day background. It is an assumption, and it matters for decay:
  the fit is on `ln(C − outdoor)`.
- **Sensitivity** (halls, teaching hours, same data, one-off check):

  | Hall | outdoor 400 | **420 (reported)** | outdoor 440 | Buildup at 400 / 420 / 440 |
  |---|---|---|---|---|
  | A | 0.71 (252) | **0.74 (252)** | 0.78 (252) | 1.02 / 1.02 / 1.02 |
  | B | 1.07 (326), uncertain | **1.10 (323), uncertain** | 1.16 (321), uncertain | 0.93 / 0.93 / 0.93 |
  | C | 0.81 (257) | **0.88 (259)** | 0.95 (256) | 1.09 / 1.09 / 1.09 |

  A ±20 ppm error moves decay rates by roughly ±5–8%. That is nowhere near
  the gap to a ~6 ACH design. Buildup rates do not move at all: the fitted
  rate comes from the curvature of the rise, and outdoor CO2 only enters the
  rejection check and the occupancy conversion. That independence is part of
  why buildup is the stronger check.
- The Spanish data is from 2021, when background CO2 was a few ppm lower.
  The same constant is used anyway, and the table above bounds the effect.

---

## 5. Fit-level filters

### 5.1 Teaching hours: Monday–Friday, 08:00 to 18:00 local

- **Where:** `TEACHING_START_HOUR = 8`, `TEACHING_END_HOUR = 18`,
  `analysis/audit_lecture_halls.py:90-91`
- **Why:** it separates "room in use" from "building asleep". Decay fits are
  classified by their **start** time. The headline uses teaching-hours fits,
  and off-hours fits are reported beside them (halls: 834 teaching,
  192 off-hours). Buildup is fitted on a series **filtered** to teaching hours,
  so the overnight gap is longer than `max_gap_seconds` and no segment can
  straddle the window.
- **Challenge it:** the window is generic. It is not each school's timetable.
  Public holidays and exam periods are not excluded; they add empty-room data,
  which gives few decay starts above 700 ppm and few rises of 250 ppm, so the
  fitters mostly ignore it.

### 5.2 Decay: `ventilation.fit_decays`

| Parameter | Value | Why | Judgment or derived |
|---|---|---|---|
| `min_start_ppm` | 700 | Only fit clearly elevated air. Near outdoor, `ln(C − 420)` is dominated by sensor noise | Judgment |
| `min_headroom_ppm` | 60 | Stop the segment 60 ppm above outdoor, for the same reason | Judgment |
| `min_points` / `min_minutes` | 6 / 20 | A slope needs enough points and enough time to be more than two readings | Judgment |
| `max_gap_seconds` | 600 | No interpolation across gaps. 600 s also admits ENSENSIA's 10-minute sampling exactly | Judgment |
| Monotonic fall | each step more than 1 ppm lower | The segment ends when CO2 stops falling, meaning someone came back or a door changed | Rule |
| `min_r2` | 0.90 | Must look like a single exponential. Anything else is not the model | Judgment |
| `ach_bounds` | 0.05–20 | Physically plausible range for a room | Judgment |

Fits that fail any test are **discarded, not reported with a caveat**. The
docstring puts it this way: a bad fit is not weak evidence, it is no evidence.
Segments rejected by these tests are not counted anywhere; only kept fits are.

**The known weakness of decay:** it measures the room while it empties. If the
air handler switches off with occupancy, decay reports leakage, not delivered
ventilation. Section 5.3 is the test of that.

### 5.3 Buildup: `ventilation.fit_buildups`

| Parameter | Value | Why (the reasoning is ours; the code records the value, not a derivation) |
|---|---|---|
| `min_rise_ppm` | 250 | Too small a rise is too close to noise to have curvature worth fitting. The audit's own comment adds that a 250 ppm rise needs at least one person |
| `min_points` / `min_minutes` | 8 / 35 | The curve must be long enough to bend |
| `dip_tolerance_ppm` | 40 | Real traces are noisy; a door opening briefly should not end a segment |
| `min_r2` | 0.95 | Stricter than decay because the model has one more free parameter |
| `ach_bounds` | 0.05–15 | Log grid, step ×1.03 (`ventilation.py:298`) |
| Steady state | must be > outdoor and ≤ 38,000/4 ppm | A fitted asymptote above a quarter of exhaled-breath CO2 means the curve never bent. It is a failed fit (`ventilation.py:306`) |

All of these are judgment calls, except the steady-state cap, which follows
from physics.

### 5.4 Identifiability: the main discard for buildup

- **Where:** `BuildupFit.identifiable`, `ventilation.py:263`; profile
  tolerance 1.10, `ventilation.py:272`
- **Rule:** keep a fit only if every rate whose squared error is within 10% of
  the best lies inside a band with `ach_hi / ach_lo < 3`.
- **Why:** a rise still far from steady state looks almost linear, and it fits
  nearly as well at many rates. Such a fit can't pin the rate down, so its
  number means nothing. **Unidentifiable fits are discarded and never quoted.**
  The 10% tolerance and the 3× width are judgment calls.
- **Discarded:**

  | | Passed r² | Identifiable (kept) | Discarded | Share |
  |---|---|---|---|---|
  | Halls | 82 | 66 | 16 | 19.5% |
  | Spain | 9 | 6 | 3 | 33% |
  | ENSENSIA | 767 | 589 | 178 | 23.2% |

  "Passed r²" counts only segments the fitter returned. Segments that failed
  earlier tests (too short, rise too small, r² too low) are not counted, so
  the true discard rate across all rising segments is higher than shown.

### 5.5 Occupancy sanity bound: halls only

- **Where:** `MIN_OCCUPANTS = 1.0`, `MIN_M3_PER_PERSON = 2.0`,
  `analysis/audit_lecture_halls.py:115-116`
- **Rule:** a buildup fit implying fewer than 1 person, or more than one
  person per 2 m³ of room air, is flagged, listed in `audit.json` and
  excluded from the medians.
- **Why:** an absurd source term means the fitted rate is suspect too.
  About 0.6 m² of floor per seat × 3 m of ceiling is already ~1.8 m³ per
  person, so 2 m³ is the densest a lecture hall can physically be packed.
- **Discarded:** 0 fits in all three halls.
- **Not applied to the school datasets**, because it needs a volume. There
  the rate is still valid (`_fit_single_buildup` uses volume only to convert
  the asymptote into people), but occupancy is not reported. The code passes
  `volume_m3=1.0` as a placeholder (`analysis/audit_lecture_halls.py:274`),
  and the resulting occupancy is never written out.
- Implied occupancy uses 0.0145 m³/h of CO2 per seated, quiet person
  (`ventilation.py:66`). **That constant has no citation in the code**, and
  the nearby comment quotes 0.018 m³/h for light office work. It affects only
  implied occupancy, never any rate. Implied occupancy is a model output,
  not a measurement, and is labelled that way.

---

## 6. Summarising a room: `fingerprint()` and "confident"

- **Where:** `ventilation.py:195-198`
- **Rule:** the room's rate is the **median** of its kept fits, reported with
  the interquartile range. It is **confident** only if there are at least 5
  fits **and** (p75 − p25) / median < 0.8.
- **Why a median:** one mis-detected segment (a window thrown open, a sensor
  gap) should not move the headline.
- **Why 0.8:** a judgment call. It means the middle half of the fits spans
  less than 80% of the typical value.
- **What it excludes from quotation:**
  - **Hall B decay:** 323 fits, but the IQR is 0.47–1.70 around 1.10, a
    spread of 1.12. It is **reported as uncertain and kept out of the
    headline.**
  - **Hall B buildup:** also not confident.
  - **Hall C buildup:** confident by the rule, but it rests on only 8 fits;
    the page calls it thin.
  - **Spain decay:** 4 of 12 rooms are not confident. ValldAba CO2_06 fails
    only on count: 4 fits, with a tight IQR of 3.23–3.60.
  - **ENSENSIA decay:** 11 of 25 rooms are not confident. School 18 has no
    fits at all.
- The headline counts in `audit.json.rooms_analysed` are 40 rooms, **24 with a
  confident decay rate and 9 with a confident buildup rate**. A room counts as
  analysed once it has any teaching-hours data. **Always quote the confident
  counts next to 40.**

---

## 7. Known limits a reviewer should weigh

1. **Well-mixed assumption.** One sensor per room. Air near a source can be
   worse than the room average.
2. **Decay may be leakage.** See 5.2. It is the reason buildup is reported
   beside it, always.
3. **Low-cost sensors drift.** Floor (4.1) and flatline (4.2) filters catch
   the gross failures, not slow calibration drift.
4. **Spanish room identity.** Each school file has sensors CO2_01 to CO2_06.
   They are counted as 12 rooms because two schools cannot share a room. The
   record's wording ("six nodes … six classrooms in two different schools")
   is ambiguous about how many classrooms each school had.
5. **Covid-era Spain.** Those classrooms were measured under 2021 Covid
   ventilation measures, so their high rates (confident median 2.32 ACH) are
   not a picture of normal practice. They are reported as measured.
6. **Halls time zone: an open question, and it matters for Hall C.**

   *What we do:* the halls' `recorded` column carries no time zone. The
   audit treats it as Cyprus local time and applies the 08:00–18:00 weekday
   window to it as written.

   *What we don't know:* whether it really is local time. The dataset record
   does not say.

   *Evidence either way:*
   - Weekday readings above 1,000 ppm run from 06:00 to 18:59 in this column.
     That fits local time with early classes, or UTC (which is 09:00–21:59 in
     Cyprus summer time). Taken as local, 6.1% of them (274 of 4,477 in
     Hall A) fall before 08:00, outside the window.
   - The timestamps run straight through both clock changes (29 Oct 2023 and
     31 Mar 2024). All three halls have 144 readings between 00:00 and 06:00
     on each day, with no step longer than 5 minutes. A clock following Cyprus
     summer time would have repeated an hour in October and skipped one in
     March. **So the column is not local time with daylight saving.** It is UTC
     or a fixed offset, and the data cannot tell which.

   *What changes if it is UTC* (same code and parameters, times shifted to
   Asia/Nicosia before the window is applied; one-off check):

   | Hall | Decay, as reported | Decay if UTC | Buildup, as reported | Buildup if UTC |
   |---|---|---|---|---|
   | A | 0.74 (252), confident | 0.75 (181), confident | 1.02 (27), confident | 0.85 (10), confident |
   | B | 1.10 (323), uncertain | 1.17 (322), uncertain | 0.93 (31), uncertain | 0.96 (20), uncertain |
   | C | 0.88 (259), confident | 0.87 (244), **uncertain** | 1.09 (8), confident | 0.50 (10), **uncertain** |

   *What does not change:* every hall stays at or below 1.17 air changes per
   hour against a design of about 6, on both methods and under both readings.
   The shortfall stands.

   *What does change:* Hall A is robust. **Hall C's confidence is not.** Under
   the UTC reading, its decay spread is (1.30 − 0.58) / 0.87 = 0.83, just
   over the 0.8 cut, and its buildup falls to 0.50 on 10 fits. So the line
   "Halls A and C fit cleanly" holds for A under both readings, and for C
   only under the local-time reading the audit uses.

   Not resolved; left open on purpose, and the audit is unchanged. The
   dataset's authors could settle it.
7. **Clock changes.** Converting to naive local time repeats one hour at the
   autumn change. That hour is 02:00–03:00, outside every teaching window.
8. **Single-reading peaks.** Peaks in the school data are raw readings from
   uncleaned sensors (the ENSENSIA README says so). The highest is 7,950 ppm
   (School 14), whose 95th percentile is 3,892. Quote p95 beside any peak.
9. **Parameters are not tuned per dataset.** The same values run on 5- and
   10-minute data. Tuning them per dataset would be fitting to the answer.

---

## 8. What the model is not used for

No language model computes any number in `audit.json`. Every value comes from
a function in `ventilation.py` or from this script's counting, and
`audit.json.method` records the parameters that actually ran. They are read
from the function signatures at run time, so the record can't drift from
the code.

---

## 9. Input checksums (sha256, as downloaded 29 Sep 2026)

```
8168226c95dcd95d5c4472928f5ff19be05db2ae7e4c3bf57d9b7e5fb6702301  Lecture_Hall_A_raw_data.csv
f2f44a3d26e991cf7844ef7d5a9d2070184df50515d5c560665306e54be5dd1c  Lecture_Hall_B_raw_data.csv
73c1221c731abde28f2fef05cc2f9c3b575129bfab483049db669dee77c9e70f  Lecture_Hall_C_raw_data.csv
147f898b1e80ab2c07b6dc806e7470ca4fbd0fd7691359937ce6a15d74ce8186  spain/CEIP_LAlbea_ValldAbav2.csv
6670fcf85d3de8c098b033a3aedcb1af248415c4b2aafca4e1736bcbbcb5fc58  spain/CEIP_SantMiquel_Vilafames.csv
b4318de70adfcaf5d76eb0b7cb3c1150ffd2105125a51340991b39dbff848cf4  ensensia/..._school_1.csv
df9a880c2c2b7683680b389e1b774dbc5b548748781498fdde089a6465e7ae57  ensensia/..._school_2.csv
cad7d2f4f0e5fe0205a38d6837b1c66971f89327d060eee63f421d0910e3ae6e  ensensia/..._school_3.csv
5b4cef22275e2a7565d0a43008123fb6838fa88d0643cd84960fffba8a294c6b  ensensia/..._school_4.csv
eec28f3fb0804c624ae34624bb90aa0f32a7f8d3e06600e1c683ff4e4683409e  ensensia/..._school_5.csv
043e5b7afed1e5fde6c35c9250233a67d993c27ea431cedbe6226bd6eeae8319  ensensia/..._school_6.csv
047bc5533df04ed6075d841ffe8080fe0ab8c1b65ea302f5095f1153f0b94235  ensensia/..._school_7.csv
0b45590392694f2d5fd788263abaa86aee1784fb591db681758dc5d3abeeccd8  ensensia/..._school_8.csv
c6ca946f68ec94e76b8032faa9b8ab574c6b7ea9120bc4e75f37ebfd366e9b58  ensensia/..._school_9.csv
3c550fc4f4b853f1254597b73304f0396315e297c744c16b39a98a61fb4604dd  ensensia/..._school_10.csv
116cf9f8f1c0269f10c311ef803fdec28a850cded58489bdea4d683bba1b8f20  ensensia/..._school_11.csv
3be94173588d6b7f4ad6952a8306f2890ec90f9672a1f6aae27d84461db76e31  ensensia/..._school_12.csv
8fab503df237d9d8585af3a6aa9b426bc9487e5a24f395fc07d177aeedada81d  ensensia/..._school_13.csv
c8c1a9a1c3ec02b9d73ba00a7813c245077426ca2ffbee6f159b3896add570ec  ensensia/..._school_14.csv
2fc8cb6723e6f217f9c2a81665061ed550a9aa675bc5b9c4cc702713c3330b27  ensensia/..._school_15.csv
93b7fd339d65210cb24ba90b112d52123b9b406d1ba36a18bc05cf7c1c5fdef2  ensensia/..._school_16.csv
5ebf87b2c52f8e1df5bc22af64c73c0eb3a5dc3d98ae8cca4e1574c0b13da51b  ensensia/..._school_17.csv
1f37755391a365b0ab16bb9f5cb5c22ce07b094a3594fd6dc479adb7cfd182ab  ensensia/..._school_18.csv
6a17988833852d80e30fce14906e3c5199859893f10b8ac5c424dbc05c34dc4c  ensensia/..._school_19.csv
8b00683ee53673017b24d315b061143fb66cecc3733d9af41713ffed6a4d4355  ensensia/..._school_20.csv
f075ffd85430cdefb105d868712b2937b2ce71c2c5ea41183c7005446eced326  ensensia/..._school_21.csv
2086fdb8aa6810c2653b13d9020080c7cb746a4cf6bbfce41321d8d3abf5dab7  ensensia/..._school_22.csv
64c81f14bd46af61d1b48c5936fff2671b1d097a332d167011c2715ccfd53bb7  ensensia/..._school_23.csv
edee2fcd27e95742f892564532d933aa5ee8f04de869d3d4f31bd188c485a0ac  ensensia/..._school_24.csv
83e69c18cc35995c8b8ad20cbd82ffba982cd462b94331b8403cca7ec1806021  ensensia/..._school_25.csv
```

`ensensia/...` stands for `ensensia/ensensia_raw_20230728-20251202`. Local
copies live under `data/` (gitignored), with the Lecture Hall files renamed
from spaces to underscores on download.
