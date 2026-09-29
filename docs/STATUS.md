# STATUS — 29 Sep 2026, 19:30 IST (T2 block; T3 19:15, T1 19:00)

## Phase
4 — T3 reproducibility + method; T2 frontend: static finding, 40 rooms, attribution; T1 backend complete

## Done since last update
- T2 (19:30): **phone pass at 380px** (real mobile emulation over DevTools): page never scrolls sideways. Hall table scrolls in its own box with the Hall column pinned and a CSS-only "scroll sideways" hint; rooms table now fits 380px with all 5 columns (the 24 / 9 always visible). New judges-tour step for the 40 rooms. Deployed, live md5 = local (4174644…)
- T2: **the finding is plain HTML now.** `web/.sync_audit.py` writes the headline, hall table (design, decay + fit count, buildup + kept/discarded, shortfall, peak), the two-methods paragraph and the judges' tour numbers at sync time. JS builders deleted, not duplicated. Word-for-word identical to the old JS output (diffed); curl with scripts stripped shows every number
- T2: dropped the inlined audit.json blob (67 KB, nothing read it any more): page 339 KB → 271 KB, 73 KB gzipped
- T2: new section "Are the halls unusual?": 40 rooms / 3 datasets **with 24 confident decay, 9 confident buildup, 3 design figures in the same sentence**, a per-dataset table, each dataset's `design_note` verbatim with "No shortfall is claimed", and the all_rooms figure (its caption carries the confident counts too)
- T2: footer cites all three datasets with authors, year, title, DOI and CC BY 4.0 (titles/creators from the Zenodo API), plus "no shortfall claimed" for Spain/ENSENSIA
- T2: **deployed**; live checksum = local web/index.html; demo still fits on load (4,254 readings, decay 34 fits); no JS errors
- T1 (19:00): HEAD returns 200 on /, /judges, /health; / and /judges gzipped; backend tests 11/11
- T3: **reproducibility verified.** A fresh clone of 8960f6b with no data/ downloaded all 30 CSVs from Zenodo (~6 min) and reproduced audit.json + all 5 SVGs with identical content; the inputs matched the dev copies byte for byte. Outputs are now written with LF on every OS, and a rerun matches the committed files byte for byte (audit.json sha256 4e5689cc…). Hashes of outputs and inputs are in METHOD.md
- T3: **analysis/METHOD.md**: every filter and threshold, where it lives, why, and what it discarded. Floor <350: halls 0, Spain 186, ENSENSIA 19,694. Flatline: 99,763 ENSENSIA readings in 8 schools. Unidentifiable buildup: halls 16/82, Spain 3/9, ENSENSIA 178/767. Judgment calls are labelled as such
- T3: outdoor-CO2 sensitivity (METHOD 4.4): ±20 ppm moves hall decay rates 0.71–0.78 (A) and 0.81–0.95 (C); buildup does not move at all
- T3: CloudTrail re-exported: 1,516 events through 29 Sep 13:33Z (130 errors, all benign: 105 are CFN/SAM probing unset S3 bucket configs, 12 are GetFunction before a function existed)

## Audit table (halls, unchanged; analysis/audit.json is the source)
| Hall | Design | Decay ACH (n) | Buildup ACH (kept) | Shortfall dec/bld |
|---|---|---|---|---|
| A | 5.8 | 0.74 (252) | 1.02 (27) | 7.8x / 5.7x |
| B | 6.0 | 1.10 (323) **uncertain** | 0.93 (31) **uncertain** | 5.5x / 6.4x |
| C | 5.9 | 0.88 (259) | 1.09 (8, thin) | 6.8x / 5.4x |

## Live state
- Site: https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/ — 200, 272,979 B / 73,068 B gzip, 19:30 IST
- /judges 200 (19:10 IST); /health 200, lastAuditRun 2026-09-29T13:35:13Z, auditStale false (19:09 IST)
- Uptime alarm `secondbreath-down` OK; SNS confirmed. Stack secondbreath, ap-south-1

## Broken or blocked
- CloudFront + Bedrock still blocked on account verification
- **Uncommitted:** web/ (this block, deployed), T1 backend/ (deployed), T3 analysis/ + docs/, CLAUDE.md. The live site runs code that is not in git
- ENSENSIA peaks are raw single readings; the page shows no school peaks, so nothing to fix yet
- **Open question, recorded in METHOD 7.6:** the halls' `recorded` column has no timezone. Readings above 1,000 ppm run 06:00–18:59, which fits local time or UTC. If it is UTC, the teaching window is 2–3 h off. Decay fits are unaffected (they're labelled, not filtered). Not changed; data work is closed
- **CLAUDE.md wording vs code:** it says readings "below outdoor level" are dropped, but the code drops below 350 and keeps 350–420 (11% of school readings). METHOD 4.1 explains why. Human: fix the CLAUDE.md sentence, or ask for the code to change

## Next 3 actions
1. Human: commit everything that is deployed
2. T3: README attribution for 5062837 and 18195710 (README.md exists, untracked; check it cites all three DOIs)
3. T2: nothing queued; open to review feedback

## Decisions taken
- Finding rendered at sync time, not in the browser — scorers without JS must see the numbers; one renderer, not two
- Removed the audit.json blob from the page — dead after the above; the repo file stays the source of truth
- Same fit parameters for every dataset — tuning per dataset would be fitting to the answer
- 40 is never printed without 24 / 9 beside it, including the figure caption (the SVG title alone didn't)
- T3: outputs written with LF, not the platform default — a reproducibility claim should be checkable by sha256 on any OS
