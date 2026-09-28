# STATUS — 29 Sep 2026, 01:20 IST

## Phase
1 — data (T3): two-method audit

## Done since last update
- analysis/audit_lecture_halls.py runs decay + buildup per hall (seated_quiet, weekday 08–18, identifiable only)
- Removed seats = volume/2.5 and the required_ach projection entirely
- Implied occupancy sanity check: 1 ≤ occupants ≤ volume / 2 m³; out-of-bounds fits are flagged, listed in JSON and excluded. Result: 0 flagged in any hall
- analysis/audit.json now `{method, halls}`; method block records every threshold (fitter params read from the function signatures, so it cannot drift)

## Final table (`python analysis/audit_lecture_halls.py`)
| Hall | Design ACH | Decay ACH (n) | Buildup ACH (kept / identifiable of r²-passing) | Implied occupants (median) | Shortfall decay / buildup |
|---|---|---|---|---|---|
| A | 5.8 | 0.74 (252), IQR 0.63–0.90 | 1.02 (27, 27/33, 18% discarded), IQR 0.52–1.18 | 42 | 7.8x / 5.7x |
| B | 6.0 | 1.10 (323), IQR 0.47–1.70 **uncertain** | 0.93 (31, 31/39, 21% discarded), IQR 0.64–1.50 **uncertain** | 30 | 5.5x / 6.4x |
| C | 5.9 | 0.88 (259), IQR 0.58–1.26 | 1.09 (8, 8/10, 20% discarded), IQR 0.80–1.25 | 135 | 6.8x / 5.4x |

Reading: the occupied-phase rate agrees with the decay rate to within ~0.3 ACH in every hall. Both methods put every hall at 5–8x below design, so the infiltration objection does not rescue the design figure.

## Live state
- Site: none yet (T2)
- /health: https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/health — last checked by T1 at 00:22 IST; T3 has not re-checked
- Deployed stack: secondbreath, ap-south-1

## Broken or blocked
- **The CLAUDE.md headline table does not match this run.** It gives buildup A 0.72 and B 0.78; this run gives 1.02 and 0.93 (C matches at 1.09). Two other variants I tried (no hour filter, and filtering fits by start time) also miss: A 0.95 / 0.91, B 0.93. Someone needs to trace where 0.72/0.78 came from, or replace them with audit.json values.
- Buildup for Hall B is also not confident (IQR/median ≥ 0.8), so Hall B stays uncertain under both methods.
- Hall C has only 8 kept buildup fits; it is confident, but the sample is thin.
- Discard counts cover only fits that already passed r² ≥ 0.95; segments that fit_buildups rejected earlier are not counted (recorded in method.buildup.discard_note).

## Next 3 actions
1. Settle the headline buildup figures (audit.json vs CLAUDE.md) with the human
2. Pull Zenodo 5062837 and 18195710 and run the same two-method pipeline on them
3. README dataset attribution block (all three DOIs, CC BY 4.0)

## Decisions taken
- Buildup: the series is filtered to teaching hours, not the fits, so the overnight gap stops segments crossing the window
- Out-of-bounds occupancy fits are excluded from both ACH and occupancy medians — an absurd source term makes the rate suspect too
- audit.json shape changed to {method, halls[]}; nothing in backend/ or web/ reads it yet
