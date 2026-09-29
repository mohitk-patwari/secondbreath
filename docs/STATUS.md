# STATUS — 29 Sep 2026, 18:55 IST (T3 block; T1 18:50)

## Phase
3 — T3 data: more rooms; T1 /judges, /explain (templates), uptime alarm

## Done since last update
- T3: **audit now covers 40 rooms in 3 open datasets**: 3 halls, 12 Spanish primary classrooms (Zenodo 5062837), 25 ENSENSIA schools (Zenodo 18195710, one sensor per school, device coordinates in Patras, Greece). `audit.json.rooms_analysed`: 24 confident decay, 9 confident buildup, 3 with a design figure
- T3: the school datasets publish no volumes or design airflow. **No design comparison is possible for them**, and no implied occupancy; audit.json says so in each `design_note`. Buildup rates are still valid without volume (volume only scales occupancy; checked in ventilation.py)
- T3: format handling lives in the loader only (analysis/audit_lecture_halls.py); **ventilation.py untouched**. UTC → local (Madrid, Athens) before the same 8–18 weekday split; Sant Miquel's quoted-line CSV handled
- T3: **ENSENSIA fill value found and dropped**: devices emit exactly 658 ppm for days while temp/humidity move (School 18: 46,826 readings in a row, 90% of its data). Rule: one value unchanged for ≥13 readings and ≥2 h = dead sensor; counts per room in `readings_dropped_flatline`. The halls have none, so their numbers are identical to before
- T3: new analysis/figures/all_rooms.svg; other figures regenerated; web/.sync_audit.py run (page audit block current, not deployed); analysis/test_loaders.py passes
- T1 (18:50): GET /judges live; POST /explain live (templates, `source: "template"`); uptime Lambda + `secondbreath-down` alarm; backend tests 10/10

## What the new rooms say (confident fits only, teaching hours)
| Dataset | Rooms | Decay ACH, confident | Buildup ACH, confident | Median CO2 / rebreathed |
|---|---|---|---|---|
| Halls, Cyprus (design ~6) | 3 | 0.74, 0.88 (A, C) | 1.02, 1.09 (A, C) | see audit table |
| Spain 2021, Covid measures in force | 12 | 8 rooms, 0.68–3.65, median 2.32 | none | 440–507 ppm / 0.05–0.23% |
| ENSENSIA 2023–25 | 25 | 14 rooms, 0.24–1.75, median 1.40 | 7 rooms, 0.40–1.05, median 0.72 | 465–1,091 ppm / 0.12–1.77% |
- No design figure for Spain or ENSENSIA, so none of these is a shortfall. The honest use is context: the halls' 0.74 and 0.88 ACH (A, C) sit inside the ordinary-school range, far below their own 6 ACH design
- ENSENSIA single-reading peaks reach 7,950 ppm (School 14, p95 3,892). They are raw readings from uncleaned sensors, so quote p95 beside any peak

## Audit table (halls, unchanged)
| Hall | Design | Decay ACH (n) | Buildup ACH (kept) | Shortfall dec/bld |
|---|---|---|---|---|
| A | 5.8 | 0.74 (252) | 1.02 (27) | 7.8x / 5.7x |
| B | 6.0 | 1.10 (323) **uncertain** | 0.93 (31) **uncertain** | 5.5x / 6.4x |
| C | 5.9 | 0.88 (259) | 1.09 (8, thin) | 6.8x / 5.4x |

## Live state
- Site / and /judges — 200 (T1, 18:45 IST). /health lastAuditRun now 2026-09-29T13:16:23Z (this run)
- Deployed stack: secondbreath, ap-south-1, UPDATE_COMPLETE

## Broken or blocked
- Human: confirm the SNS subscription email (uptime alerts go nowhere until then)
- CloudFront + Bedrock still blocked on account verification
- Uncommitted: T3's analysis/ + docs/ + web/index.html sync; T1's backend/ (uptime.py is new)

## Next 3 actions
1. T2: add `all_rooms` to .sync_audit.py FIGS, show `rooms_analysed` + `design_note` (HANDOFF), deploy
2. T3: README attribution for 5062837 and 18195710 (CC BY 4.0 obligation; the app footer needs them too, T2)
3. Human: commit; confirm SNS

## Decisions taken
- Flatline filter in the school loaders only — halls verified to have zero flatline readings; the fill value is an ENSENSIA device artefact
- Same fit parameters for every dataset, not tuned per dataset — tuning to 10-min sampling would be fitting to the answer
- A room counts as analysed once it has teaching-hours data; confident counts reported beside the total so 40 is never quoted alone
