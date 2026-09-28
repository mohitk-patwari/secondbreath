# STATUS — 29 Sep 2026, 01:25 IST (T3 block ends 01:20 IST)

## Phase
2 — data and evidence (T3). T1/T2 phase-1 state below is carried over, not re-verified by T3.

## Done since last update
- T3: every audit run writes UTC time to SSM `/secondbreath/lastAuditRun` (ap-south-1). /health now returns `lastAuditRun: 2026-09-28T19:46:00+00:00`, `auditStale: false`. If AWS is unreachable the run warns and carries on
- T3: `analysis/export_cloudtrail.py` → evidence/cloudtrail-timeline.md + cloudtrail-raw.json: 349 events from 18:45Z to 19:43Z, one principal (the build IAM user), IP and access key redacted
- T3: analysis/figures/ has plain SVG with no library: hall_a/b/c.svg (the week with the most fits, trace plus decay in blue and buildup in orange, hover titles) and design_vs_measured.svg. Themed for light and dark, checked by rendering in both
- T3: evidence/README.md explains each file and its limits
- T1 (01:25): /fit, /predict, /health live; build.py drift check; docs/API.md exact shapes. T2: web/index.html ready, static single file

## Audit table (analysis/audit.json, the single source of truth)
| Hall | Design | Decay ACH (n) | Buildup ACH (kept) | Occupants | Shortfall dec/bld |
|---|---|---|---|---|---|
| A | 5.8 | 0.74 (252) | 1.02 (27) | 42 | 7.8x / 5.7x |
| B | 6.0 | 1.10 (323) **uncertain** | 0.93 (31) **uncertain** | 30 | 5.5x / 6.4x |
| C | 5.9 | 0.88 (259) | 1.09 (8, thin) | 135 | 6.8x / 5.4x |

## Live state
- API: https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com — /health 200 at 01:17 IST (three checks)
- Deployed stack: secondbreath, ap-south-1, UPDATE_COMPLETE 19:46Z
- Site: not hosted yet (T2/T1)

## Broken or blocked
- **evidence/mcp-connection-verified.txt not created.** No AWS MCP server is configured in any session here (`claude mcp list` shows only claude.ai Docs, Canva, Calendar, Gmail). It won't be faked. The human needs to add one (e.g. awslabs aws-api-mcp-server); T3 then captures the tool list, ARN and timestamp
- **/health returned 500 twice (19:43Z, ~19:46Z)** while T1's stack updates were running, the first ending in UPDATE_ROLLBACK. Both recovered within a minute. With a live gate, deploys need to be quiet or run off-hours (→ T1)
- CloudTrail export is a snapshot and Event history lags ~15 min. Rerun `python analysis/export_cloudtrail.py` at the end of the build
- Bedrock: 2 Converse calls → ValidationException in CloudTrail (18:56Z, 18:57Z); /explain not started

## Next 3 actions
1. Human: configure an AWS MCP server → T3 writes mcp-connection-verified.txt
2. T2: embed analysis/figures/*.svg (copy them or `<img>`; each has its own surface and a dark-mode media query)
3. T3: Zenodo 5062837 / 18195710 through the two-method pipeline; README attribution block

## Decisions taken
- Per-hall figure shows the ISO week with the most fits of both kinds, not a hand-picked week; the choice rule is in figures.busiest_week
- CloudTrail split is by userAgent: agent and human share one IAM user, so principal alone can't separate them. Stated in the evidence README
- Home IP and access key ID are masked in the raw export; nothing else is edited
- SSM is written through the aws CLI subprocess, so analysis/ gains no boto3 dependency
