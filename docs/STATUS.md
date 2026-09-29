# STATUS — 29 Sep 2026, 19:30 IST (T3 final block; T2 19:30, T1 19:00)

## Phase
4 complete — all terminals finished; final CloudTrail export done

## Done since last update
- T3: **final CloudTrail export** (the last one, 13:56:55Z): 1,554 events, 2026-09-28T18:45:22Z → 2026-09-29T13:49:42Z, 133 errors, none a failed deploy. By caller: service:cloudformation 983, aws-cli 232, sam-cli 163, service:lambda 96, aws-mcp 41, Boto3 21, mcp-proxy 15, console 2, service:apigateway 1. Breakdown in evidence/README.md
- T3: **METHOD 7.6** (commit 2b4273e): the halls' timestamps run straight through both 2023–24 clock changes, so they are UTC or a fixed offset, not DST local time. Under the UTC reading the shortfall stands (all ≤ 1.17 ACH), Hall A is robust, and **Hall C decay turns uncertain** (spread 0.83 vs the 0.8 cut) with buildup 0.50. Left open; audit unchanged
- T3: CLAUDE.md sensor-floor sentence now matches the code (drop < 350, keep 350–420; /fit drops below outdoorPpm), pointing to METHOD 4.1
- T3: HANDOFF T3 → T4: final counts, the three WRITEUP.md line-128/131 numbers to change, and the Hall C qualifier
- T2 (19:30): phone pass at 380 px, judges-tour step for the 40 rooms, deployed (live md5 = local)
- Earlier this phase: reproducibility verified byte for byte from a fresh clone (METHOD §1); METHOD.md written; the finding rendered as plain HTML

## Audit table (halls, unchanged; analysis/audit.json is the source)
| Hall | Design | Decay ACH (n) | Buildup ACH (kept) | Shortfall dec/bld |
|---|---|---|---|---|
| A | 5.8 | 0.74 (252) | 1.02 (27) | 7.8x / 5.7x |
| B | 6.0 | 1.10 (323) **uncertain** | 0.93 (31) **uncertain** | 5.5x / 6.4x |
| C | 5.9 | 0.88 (259)* | 1.09 (8, thin)* | 6.8x / 5.4x |

\* Confident only if the timestamps are local time; see METHOD 7.6.

## Live state
- Site / and /judges: https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/ — 200, 272,979 B, 19:28 IST
- /health: 200, lastAuditRun 2026-09-29T13:35:13Z, auditStale false, 19:28 IST
- Stack secondbreath, ap-south-1; uptime alarm OK, SNS confirmed

## Broken or blocked
- CloudFront + Bedrock blocked on account verification (unchanged; the site runs on API Gateway)
- **Bedrock evidence file not found.** It was reported as done, but no file matching *bedrock* exists in the working tree or in any git ref (`git log --all`). CloudTrail has the 5 Bedrock events, and WRITEUP.md §6 describes them. Human: point me to the file, or confirm it isn't needed
- Uncommitted: this block's evidence/ + docs/ changes (the export, evidence/README.md, HANDOFF, STATUS)
- Halls timestamp zone: open question (METHOD 7.6), deliberately unresolved

## Next 3 actions
1. Human: commit and push this block
2. T4: apply the WRITEUP.md line 128/131 numbers from HANDOFF; keep the Hall C qualifier
3. Nothing queued for T3

## Decisions taken
- The export ran after every other terminal committed, so it covers the build; its own lookups can't be in it, by definition
- Hall C qualifier added to the table, not a changed number — the question is open, so the reported value stays and its dependence is flagged
- 40 is never printed without 24 / 9 beside it; outputs written with LF so the reproducibility claim is checkable by sha256
