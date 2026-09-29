# STATUS — 30 Sep 2026 (T2 block; T1 bounds deployed)

## Phase
4 complete, plus a T1 fix: physical bounds on the forward model (deployed)

## Done since last update
- T2 (30 Sep): **out-of-range handling on the API's own flag, deployed** (live md5 = local 48cfa31c…). Hero and Predict panel read `withinValidatedRange` (peak-based); steady-state fallback removed. Past 5,000 ppm both say "the 8-hour workplace exposure limit … leave the room" instead of a number (T4's framing); Predict keeps max occupancy, hides peak/chart. A 400 (impossible density) shows the API's message with no stale result. Pre-render re-synced to current ventilation.py: live no-JS state = JS state; 19/20 cases identical to live /predict, the 20th differs by 1 ulp in one ppm value (exp() on Windows vs Lambda), never visible after rounding
- T2 (20:50): **new hero, deployed** (live md5 = local 90e6363a…). "Where are you sitting right now?": 4 room presets from audit.json, people + duration sliders, room-from-above (fill green/amber/red at 1,000/1,400 ppm), "Your next 100 breaths" grid, headline, capacity line, clock with scrubber (12 modelled min/s; reduced motion shows the finished session). Default Hall A, 60 people, 90 min: "1 breath in 17", 6 of 100 red. Pre-rendered at sync time from ventilation.predict (matches live /predict in 16/16 cases); JS off shows the same text as JS end state
- T2: page reordered: hero → explainer (ppm slider, big thumb, "drag me") → 40 rooms/finding → rooms → Predict → Fingerprint (folded) → caveats → footer. Word-diff vs the previous live page: no finding, rooms, predict, caveat or footer text removed. Judges tour opens with the hero
- T2: anime.js **not** used: native range inputs + requestAnimationFrame + CSS transitions cover it, zero dependencies; scroll-reveal skipped (would hide sections from full-page screenshots). 80 KB gzipped
- T1 (20:30): **forward model bounded.** /predict gave rebreathed fraction 2.36 (2,000 people) and 11.82 (10,000) in 363 m³ at 0.74 ACH. Now `rebreathed_fraction` is capped at 1.0. A session **peak** above 5,000 ppm (OSHA 8-h PEL / ACGIH TLV, an exposure limit we use as our ceiling) returns `withinValidatedRange: false`, and /explain says it's out of range instead of giving a number. Under 0.2 m³ per person (`MIN_INPUT_M3_PER_PERSON`, a judgment call, no source; deliberately 10x looser than the audit's `MIN_M3_PER_PERSON` = 2.0) returns 400. T3 agreed (audit.json + SVGs byte-identical on re-run). **Deployed 21:50 IST**; live: 60 people → 200 in range; 1,000 → 200 flagged, /explain gives no number; 10,000 → 400
- T3: **final CloudTrail export** (the last one, 13:56:55Z): 1,554 events, 2026-09-28T18:45:22Z → 2026-09-29T13:49:42Z, 133 errors, none a failed deploy. By caller: service:cloudformation 983, aws-cli 232, sam-cli 163, service:lambda 96, aws-mcp 41, Boto3 21, mcp-proxy 15, console 2, service:apigateway 1. Breakdown in evidence/README.md
- T3: **METHOD 7.6** (commit 2b4273e): the halls' timestamps run straight through both 2023–24 clock changes, so they are UTC or a fixed offset, not DST local time. Under the UTC reading the shortfall stands (all ≤ 1.17 ACH), Hall A is robust, and **Hall C decay turns uncertain** (spread 0.83 vs the 0.8 cut) with buildup 0.50. Left open; audit unchanged
- T3: CLAUDE.md sensor-floor sentence now matches the code (drop < 350, keep 350–420; /fit drops below outdoorPpm), pointing to METHOD 4.1
- T3: HANDOFF T3 → T4: final counts, the three WRITEUP.md line-128/131 numbers to change, and the Hall C qualifier
- Earlier this phase: reproducibility verified byte for byte from a fresh clone (METHOD §1); METHOD.md written; the finding rendered as plain HTML

## Audit table (halls, unchanged; analysis/audit.json is the source)
| Hall | Design | Decay ACH (n) | Buildup ACH (kept) | Shortfall dec/bld |
|---|---|---|---|---|
| A | 5.8 | 0.74 (252) | 1.02 (27) | 7.8x / 5.7x |
| B | 6.0 | 1.10 (323) **uncertain** | 0.93 (31) **uncertain** | 5.5x / 6.4x |
| C | 5.9 | 0.88 (259)* | 1.09 (8, thin)* | 6.8x / 5.4x |

\* Confident only if the timestamps are local time; see METHOD 7.6.

## Live state
- Site / and /judges: https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/ — 200, 297,853 B / 80,340 B gzip, 20:45 IST
- /health: 200, lastAuditRun 2026-09-29T13:35:13Z, auditStale false, 19:28 IST
- Stack secondbreath, ap-south-1; uptime alarm OK, SNS confirmed

## Broken or blocked
- CloudFront + Bedrock blocked on account verification (unchanged; the site runs on API Gateway)
- Uncommitted: T1's ventilation.py (shared) + backend/ + docs changes (deployed and live). T3's audit re-run refreshed SSM lastAuditRun
- The final CloudTrail export predates this deploy, so it won't show it; re-export if the evidence must cover it
- Halls timestamp zone: open question (METHOD 7.6), deliberately unresolved

## Next 3 actions
1. Human: commit ventilation.py + backend/ + docs
2. T4: apply the WRITEUP.md line 128/131 numbers from HANDOFF; keep the Hall C qualifier
3. T2: decide whether the Hall C tile/table carry the METHOD 7.6 qualifier (T3 asked in HANDOFF)

## Decisions taken
- T2: "Spain's best classroom" preset = Hall A's real 363 m³ at ValldAba CO2_05's measured 3.65/h, labelled — Spain publishes no volumes, so that room can't be simulated as itself without inventing one
- T2: .sync_audit.py imports root ventilation.py to pre-render the hero; the page reads the API's withinValidatedRange as is, never re-derives it
- The export ran after every other terminal committed, so it covers the build; its own lookups can't be in it, by definition
- Hall C qualifier added to the table, not a changed number — the question is open, so the reported value stays and its dependence is flagged
- 40 is never printed without 24 / 9 beside it; outputs written with LF so the reproducibility claim is checkable by sha256
