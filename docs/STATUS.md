# STATUS — 29 Sep 2026, 00:35 IST

## Phase
0 — data (T3). T1's backend skeleton from 00:25 still stands (see Live state).

## Done since last update
- `python analysis/ventilation.py` → "all self-tests passed"
- analysis/audit_lecture_halls.py imports ventilation from repo root (falls back to its own dir); data/ and audit.json paths are anchored to the repo, not the cwd
- Downloaded 3 Zenodo 18385830 CSVs (26 MB) into data/, which is gitignored
- analysis/audit.json written. Teaching-hours fits: A 0.74 ACH (252 fits), B 1.10 (323), C 0.88 (259) = 834; design ~6 ACH; shortfall 7.8x / 5.5x / 6.8x; peak 4,957 ppm (B) = 1 breath in 8
- evidence/README.md describes the three proof sets (agent screenshots, CloudTrail, MCP)

## Live state
- Site: none yet (T2)
- /health: https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/health — 200 at 00:22 IST (T1's check; not re-checked by T3)
- Deployed stack: secondbreath, ap-south-1

## Broken or blocked
- **ventilation.py is still at analysis/ventilation.py, not the repo root.** Moving it was refused by the permission guard because it is a shared file. The human needs to run `git mv analysis/ventilation.py ventilation.py` or approve the move. The audit script needs no change after the move. T1's /fit is waiting on this.
- **Hall B fingerprint is `confident: false`** (IQR 0.47–1.7). The CLAUDE.md headline quotes B's 1.10 ACH without a caveat, and rule 7 says it needs one.
- Off-hours vs teaching: A 0.75 vs 0.74 and C 0.90 vs 0.88 are almost identical, which is consistent with the AHU being off at decay time, i.e. an infiltration reading. Only B differs (0.45 off vs 1.10 on). This has to be reported in the write-up.
- The audit's "holding N people needs 12.4 ACH" line uses seats = volume / 2.5, which is not in the dataset. It is console-only today; do not surface it in the UI.

## Next 3 actions
1. Move ventilation.py to root once approved, then re-run self-tests plus the audit
2. Pull Zenodo 5062837 and 18195710 and check whether the same fit pipeline runs on them
3. Draft the README dataset attribution block (all three DOIs, CC BY 4.0)

## Decisions taken
- audit.json is committed, raw CSVs are not — they are reproducible from Zenodo in one command
- Import path: repo root is inserted into sys.path so the script runs the same from any cwd, before and after the move
