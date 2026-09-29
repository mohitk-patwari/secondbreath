# STATUS — 30 Sep 2026, 01:25 IST (root housekeeping block)

## Phase
4 complete. Housekeeping: licence, evidence tidy, line endings

## Done since last update
- **Submission visuals**: analysis/figures/png/ (the 5 figures at 1200 px on the page's dark background), method.svg/png (one real Hall A session, 3 Nov 2023, with its buildup and decay fits; year medians 1.02 / 0.74 vs design 5.79 from audit.json), architecture.svg/png (from template.yaml; CloudFront dashed, in front of S3), docs/cover.png (live hero, 1200x675, "1 breath in 17")
- **LICENSE (MIT, 2026, Mohit Kumar Patwari)** at the root; README.md has a Licence section. MIT covers this repository's code only; the three Zenodo datasets keep their CC BY 4.0 terms. The write-up's "designed to be reused" is now true in law, not just intent
- **test-msg.json moved to evidence/** (moved, not deleted: it is the `--messages` body of both Converse calls in bedrock-cli-errors.txt). evidence/README.md says what it is. The transcript still reads `file://test-msg.json` on purpose, because it is verbatim terminal output from the repo root
- **.gitattributes `* text=auto eol=lf`**, `git add --renormalize .` run. **No committed blob changed**: all 34 text files were already LF in the index (core.autocrlf only made working copies CRLF). audit.json and the 5 SVGs are untouched, so METHOD.md's hashes need no update
- Verified: `python ventilation.py` passes; `analysis/test_loaders.py` passes; `analysis/audit_lecture_halls.py --json` re-run leaves audit.json and all 5 figures byte-identical (git sees no change), and all 6 sha256s match METHOD.md
- Earlier (29–30 Sep): T2 hero + out-of-range handling + timezone footnote deployed; T1 physical bounds on /predict deployed (peak > 5,000 ppm flagged, < 0.2 m³/person → 400); T3 final CloudTrail export, METHOD 7.6

## Audit table (halls, unchanged; analysis/audit.json is the source)
| Hall | Design | Decay ACH (n) | Buildup ACH (kept) | Shortfall dec/bld |
|---|---|---|---|---|
| A | 5.8 | 0.74 (252) | 1.02 (27) | 7.8x / 5.7x |
| B | 6.0 | 1.10 (323) **uncertain** | 0.93 (31) **uncertain** | 5.5x / 6.4x |
| C | 5.9 | 0.88 (259)* | 1.09 (8, thin)* | 6.8x / 5.4x |

\* Confident only if the timestamps are local time; see METHOD 7.6.

## Live state
- Site: https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/ — 200, 01:24 IST
- /health: 200, lastAuditRun 2026-09-29T19:51:32Z (this block's verification re-run), auditStale false
- Stack secondbreath, ap-south-1; uptime alarm OK, SNS confirmed

## Broken or blocked
- CloudFront + Bedrock blocked on account verification (unchanged; the site runs on API Gateway)
- The final CloudTrail export predates the 29 Sep 21:50 IST bounds deploy; re-export if the evidence must cover it
- Halls timestamp zone: open question (METHOD 7.6), deliberately unresolved
- Working copies of 9 files are still CRLF on this machine until next checkout (harmless; the index is LF)

## Next 3 actions
1. T4: apply the WRITEUP.md line 128/131 numbers from HANDOFF; keep the Hall C qualifier
2. Optional: re-export CloudTrail so the evidence covers the last deploy
3. Nothing else queued

## Decisions taken
- test-msg.json moved, not deleted — the evidence transcript names it, so it's part of that record
- Transcript path left as `file://test-msg.json` — rewriting verbatim terminal output would falsify it; evidence/README.md explains instead
- eol=lf for everything — METHOD.md's sha256 claim holds on any OS without relying on each reviewer's autocrlf
- 40 is never printed without 24 / 9 beside it; outputs written with LF so the reproducibility claim is checkable by sha256
