# STATUS — 29 Sep 2026, 18:35 IST (T3 block; T2 02:00, T1 01:40)

## Phase
2 — T1 hosting + API additions; T3 data and evidence; T2 finding + judges tour

## Done since last update
- T1: **site live** at https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/ (GET / on the API, served from a private S3 bucket; direct S3 returns 403)
- T1: `python backend/deploy_web.py` syncs web/ to the bucket (and invalidates CloudFront once it exists). T2 ships with it
- T1: **API change, additive**: /fit returns `decay.segments` and `buildup.segments` as `[[startIso, endIso, ach], ...]` (buildup: identifiable only), plus optional `teachingHoursOnly`, which reproduces audit.json Hall A exactly (0.744 from 252 fits, 1.019 from 27). docs/API.md updated
- T1: $20/month AWS Budget (actual + forecast), email alert; address kept out of git as a stack parameter
- T1: **fixed /health 500s.** Cause: boto3 cold start took more than 5 s at 128 MB, so the Lambda timed out; deploys weren't the cause. Now 512 MB / 10 s with 2 s SSM timeouts; cold start ~0.9 s, 5 of 5 parallel cold hits returned 200
- T2: web/index.html now has The finding (the table rendered from the embedded audit.json, the 4 SVG figures, the two-methods explanation; B uncertain on both methods, C buildup thin), fitted-segment highlighting, a teaching-hours checkbox, an "upload ≠ audit" note, the judges tour at #judges, and the CLAUDE.md caveats verbatim. Tested locally, not deployed yet
- T2: verified the tour's reproduce step: the page's own upload path on the full Hall A CSV (8.2 MB trimmed to 2.3 MB) gives live decay 0.7438 (252) and buildup 1.0195 (27, 6 discarded)
- T3: audit writes SSM lastAuditRun; CloudTrail export (evidence/); SVG figures in analysis/figures/
- T3: **AWS MCP connection proven**: evidence/mcp-connection-verified.txt has 8 tools + server-declared read-only/destructive hints, ARN user/secondbreath-dev, real list_regions/search_documentation/run_script calls, 24 skills. CloudTrail independently shows the run_script calls (invokedBy aws-mcp.amazonaws.com) plus an AwsMcpEvent whose userAgent names claude-code/2.1.284
- T3: CloudTrail re-exported through 29 Sep 12:53Z (939 events), now covering both users; export_cloudtrail.py labels `aws-mcp` / `mcp-proxy` callers

## Audit table (analysis/audit.json, single source of truth)
| Hall | Design | Decay ACH (n) | Buildup ACH (kept) | Shortfall dec/bld |
|---|---|---|---|---|
| A | 5.8 | 0.74 (252) | 1.02 (27) | 7.8x / 5.7x |
| B | 6.0 | 1.10 (323) **uncertain** | 0.93 (31) **uncertain** | 5.5x / 6.4x |
| C | 5.9 | 0.88 (259) | 1.09 (8, thin) | 6.8x / 5.4x |

## Live state
- Site: https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/ — 200, 01:37 IST
- /health: …/health — 200, lastAuditRun present, auditStale false, 01:37 IST
- Deployed stack: secondbreath, ap-south-1, UPDATE_COMPLETE

## Broken or blocked
- **CloudFront blocked:** "Your account must be verified before you can add new CloudFront resources" (403, same verification as Bedrock). The template has the S3+OAC+CloudFront setup behind `EnableCloudFront` (default false). Human: open an AWS Support case covering CloudFront and Bedrock, then T1 deploys with `--parameter-overrides EnableCloudFront=true`. The site URL then changes to *.cloudfront.net; the API URL stays the same
- **T1's backend/ work since Phase 0 is uncommitted** (api.py, build.py, deploy_web.py, tests); the live stack runs code that isn't in git
- CloudTrail export is a snapshot; rerun `python analysis/export_cloudtrail.py` at the end
- Bedrock blocked; /explain not started
- /judges path 404s until T1 routes it (HANDOFF); the home page links to #judges, which works

## Next 3 actions
1. Human: commit backend/ and T3's evidence/ + analysis/export_cloudtrail.py; open the Support case (CloudFront + Bedrock)
2. T1: enable CloudFront once verified; /explain or template sentences after the evening of 30 Sep
3. T2: deploy web/ with backend/deploy_web.py once reviewed; T3: Zenodo 5062837 / 18195710, README attribution

## Decisions taken
- T2: audit + figures are inlined by web/.sync_audit.py (figures as <img> data URIs, so SVG styles can't leak); upload results round down, so Hall A buildup shows 1.01 live vs the audit's 1.02, and the tour says so
- Fallback hosting via API Gateway + Lambda: HTTPS today, bucket stays private, no new services
- Budget, not a CloudWatch billing alarm: EstimatedCharges exists only in us-east-1
- teachingHoursOnly mirrors the audit's split (decay by start time, buildup on the filtered series), so live and audit numbers match
- T3: CloudTrail split by userAgent; IP and access key masked in the raw export
- T3: MCP runs as a separate IAM user (secondbreath-dev), so agent-via-MCP calls separate by principal, not just userAgent
