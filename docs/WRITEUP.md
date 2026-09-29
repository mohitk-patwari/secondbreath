# SecondBreath: how much of the air you're breathing came out of someone else's lungs

Live: https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/judges
Code: https://github.com/mohitk-patwari/secondbreath
`#social-good` (Health) · `#community`

---

## 1. The problem

It's the last lecture of the afternoon, in a hall with no windows that open. The room was full at two o'clock and it's now ten to four. The lecturer has slowed down, and half the room has too. Someone near the back props the door open for a minute, the corridor air feels cold and sharp, and then the door swings shut again.

Nobody in that room can see what they are breathing. Every breath out carries about 38,000 ppm of CO2, so the amount of CO2 above the outdoor level is a direct measure of how much of the room's air has already been through somebody's lungs. The building's documents say the hall gets six complete changes of fresh air an hour. Nobody present can check that. The facilities team can't easily check it either: working out a room's real ventilation rate from a sensor log is a small inverse problem, and nobody's job includes solving it.

## 2. What it does

The page needs no login, no sign-up, no cookies and no clicks. By the time it has loaded, it has already run a live fit and a live prediction. The same click path is on the page itself, at `/judges`.

The expected values come from two sources:

- **Steps 3 and 4** show audit figures, copied from `analysis/audit.json`.
- **Steps 5 to 8** show live-demo output: what the deployed API returned for the demo file and the prefilled form when the tour was written. These are not audit figures, and the demo covers only 2 to 27 October 2023, which is why its rates differ from the full-year audit. Step 8 re-runs the full-year file and should reproduce the audit's fit counts.

1. **Open https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/judges.** A seven-step tour opens at the top of the page.
2. **Hero: drag the CO2 slider to the far right (5,000 ppm).**
   Expect: "1 breath in 8 has already been through someone else's lungs." The highest reading in the lecture-hall data was 4,957 ppm.
3. **The finding: read the table.**
   Expect: Hall A was designed for 5.79 ACH and measures 0.74 by decay (252 fits) and 1.02 by buildup (27 fits). Hall B is marked *Uncertain* on both methods. Hall C's buildup is marked *Thin* (8 fits). Below the table: a figure comparing design with measured rates, and one week of CO2 for each hall with the fitted stretches highlighted.
4. **Are the halls unusual?**
   Expect: 40 rooms in 3 datasets, of which 24 have a confident decay fit, 9 a confident buildup fit and 3 a design figure. A log-scale figure plots every room, and rooms without a confident fit are drawn hollow.
5. **Fingerprint your own room: no click needed.** The demo (Hall A, 2–27 Oct 2023) was sent to `POST /fit` on load.
   Expect (live demo output): decay 0.75 ACH from 34 fits. Buildup 0.61 ACH, struck through and badged *Uncertain* (4 identifiable fits, 1 discarded). The chart is a grey CO2 trace with the decay stretches in blue and the buildup stretches in orange. There is a gap from 14 to 25 Oct, where the sensor recorded nothing.
6. **Predict a session: already filled in** (60 people, 90 minutes, seated and quiet, 363 m³, 0.75 ACH).
   Expect (live demo output): peak 2,579 ppm, 1 breath in 17. Max safe occupancy is 16 people for a 1,000 ppm limit and 27 for 1,400 ppm. Change occupants to 16 and press **Predict**: the peak drops to 996 ppm.
7. **Back in Fingerprint, tick "Teaching hours only".**
   Expect (live demo output): the demo refits using weekday 08:00–17:59 data only. Decay becomes 0.76 ACH from 30 fits. Buildup has 11 identifiable fits and is still uncertain.
8. **Optional, about a minute:** download `Lecture Hall A_raw_data.csv` (8 MB) from [Zenodo 18385830](https://zenodo.org/records/18385830), drop it on the upload box, enter volume 363, keep "Teaching hours only" ticked, and press **Fingerprint**.
   Expect (live demo output): decay 0.74 ACH (252 fits) and buildup 1.01 ACH (27 identifiable, 6 discarded). These are the same fit counts as the committed audit. The solver returns 1.0195: the audit rounds that to 1.02, but the page always rounds down, so it shows 1.01.
9. **What this project is not, and the footer.**
   Expect: the limits, stated plainly, and all three datasets cited with DOI and CC BY 4.0.
   `curl https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/health` returns 200 with the time of the last audit run.

## 3. Why this is not a wrapper

The rebreathed-fraction formula is one line: `(C_indoor − C_outdoor) / 38,000` (Rudnick & Milton, 2003). Nothing hard happens there. What makes the problem hard is that you almost never know a room's air-change rate. Design documents state what a ventilation system should deliver, not what it does deliver. A CO2 log is a curve, and the rate has to be recovered from the shape of that curve. That is an inverse problem, and SecondBreath solves it twice, in two independent ways.

**Decay.** When people leave, CO2 falls exponentially towards the outdoor level. `fit_decays` finds each falling stretch that starts above 700 ppm and lasts at least 20 minutes, then fits a straight line to `ln(C − C_outdoor)` over that stretch. The slope is the air-change rate, and a fit is kept only if R² ≥ 0.9. Individual fits are reduced to a fingerprint: the median and interquartile range. A fingerprint counts as *confident* only when there are at least 5 fits and the interquartile range is under 0.8 times the median. The median, not the mean, is used so that one badly detected segment cannot move the headline.

**Buildup.** While people are in the room, CO2 rises towards a steady state. That leaves two unknowns: the ventilation rate and the CO2 source strength. They can be separated because the curvature of the rise depends on the rate, while the level the curve is heading for depends on the source. For any fixed rate, the model is linear in the steady-state level. So `fit_buildups` searches the rate on a logarithmic grid and solves for everything else in closed form at each grid point.

**The profile band.** A rise that is still far from steady state looks nearly linear, and nearly linear data fits many rates about equally well. So every buildup fit keeps its whole error profile. The band is every grid rate whose squared error is within 10% of the best rate's. When the top of the band is 3 or more times its bottom, the rate is not identifiable from that stretch of data, and the fit is **discarded**. Discarded fits never reach a median, never appear in an API response and are never quoted. In the halls, 6 of 33 buildup fits were discarded in Hall A, 8 of 39 in Hall B and 2 of 10 in Hall C.

**The tests check the physics.** `python ventilation.py` builds a synthetic room with a known answer and checks that the solver recovers it. From a clean decay it must recover 1.35 ACH to within 0.01. From a simulated occupied room (363 m³, 0.80 ACH, 30 people) it must recover the rate to within 6% and the occupancy to within 10%. The same file checks that the forward model's steady state matches the closed-form result. If the physics were wrong, these tests would fail.

**The language model is kept out.** `POST /explain` turns solver output into plain sentences, and today it does that with **deterministic templates, not a model**. This is a design decision, not a placeholder. Every number in `sentences` also appears in `facts`, and a backend test enforces that. Rounding always goes against the room: ACH and "one breath in N" round down, and ppm and percentages round up. A fit marked uncertain is described with its interquartile range and is never stated as the room's rate. A model could later replace the templates behind the same response shape, but it would still only phrase numbers the solver had already produced. No model computes any rate, CO2 value or risk figure anywhere in this project.

## 4. The finding

Three lecture halls in Limassol, Cyprus, were recorded for a full academic year. Each is specified at 100% fresh air and about six air changes per hour. Results are for teaching hours only (Mon–Fri, 08:00–17:59).

| Hall | Design ACH | Decay ACH (room emptying) | Buildup ACH (room occupied) | Below design, decay / buildup |
|---|---|---|---|---|
| A (363 m³) | 5.79 | **0.74** · 252 fits · IQR 0.63–0.90 | **1.02** · 27 kept · IQR 0.52–1.18 | 7.8× / 5.7× |
| B (283 m³) | 6.01 | 1.10 · 323 fits · IQR 0.47–1.70 · **uncertain** | 0.93 · 31 kept · IQR 0.64–1.50 · **uncertain** | not claimed |
| C (1,520 m³) | 5.92 | **0.88** · 259 fits · IQR 0.58–1.26 | **1.09** · 8 kept · IQR 0.80–1.25 · **thin** | 6.8× / 5.4× |

Halls A and C fit cleanly at 0.74 and 0.88 air changes per hour. **That statement is fully true only if the halls' timestamps are local time.** The dataset's `recorded` column carries no timezone. The audit treats it as Cyprus local time, but the timestamps run straight through both 2023–24 clock changes without a gap or a repeated hour, so the column is really UTC or a fixed offset, and the data cannot tell which. With the timestamps read as UTC (same code, same parameters), the results change like this:

- **Hall A holds.** Decay 0.75 (181 fits) and buildup 0.85 (10 fits), both confident.
- **Hall C does not.** Its decay stays at 0.87 (244 fits), but the spread (IQR divided by median) becomes 0.83. That is just over the 0.8 limit, so the fit reads as *uncertain*. Its buildup falls to 0.50 (10 fits), also uncertain.
- **Hall B stays uncertain** on both methods (decay 1.17, buildup 0.96).

What does not change is the shortfall. **Every hall stays at or below 1.17 air changes per hour against a design of about six, on both methods and under both timestamp readings.** The timezone question decides whether Hall C's rate can be quoted with confidence, not whether the halls fall short. The UTC figures come from a one-off check recorded in `analysis/METHOD.md` (section 7, item 6); `audit.json` and the table above use the local-time reading.

Hall B's decay fits scatter (interquartile range 0.47 to 1.70), and it is reported as uncertain rather than averaged into the headline. Its buildup fits scatter too (0.64 to 1.50). The audit file does compute shortfall factors for Hall B (5.5× and 6.4×), but they are divisions by medians that should not be quoted, so they are left out of the table above.

The two methods do not agree to the decimal. Buildup reads higher in both clean halls, and Hall A's buildup median sits just outside its decay interquartile range. But they could have disagreed by a factor of six, and they don't. If the air handlers delivered their design airflow during lectures and shut off afterwards, the occupied-room fit would read near six. It reads 1.02 and 1.09.

Hall B peaked at **4,957 ppm**. At that moment 11.94% of the air, about **one breath in eight**, had already been exhaled by someone else in the room. Across teaching hours, Hall B was above 1,000 ppm 19.6% of the time and above 2,000 ppm 4.4% of the time.

**Are the halls unusual?** The same code, with the same fit parameters (nothing tuned per dataset), ran over two school datasets. In total that is **40 rooms, of which 24 have a confident decay fit, 9 a confident buildup fit and 3 a published design figure**.

- **12 primary classrooms in Castellón, Spain (spring 2021, Covid-19 ventilation measures in force).** 8 have a confident decay fit, ranging from 0.68 to 3.65 ACH (median 2.32). None has a confident buildup fit.
- **25 ENSENSIA schools, one sensor each, mostly in Patras, Greece (2023–25).** 14 have a confident decay fit, from 0.24 to 1.75 ACH (median 1.40). 7 have a confident buildup fit, from 0.40 to 1.05 ACH (median 0.72).

So the halls' 0.74 and 0.88 fall within the ordinary-classroom range, even though the halls were designed for six.

**The honesty machinery.** Each of these rules either removed a number or labelled one as weak. None of them made a result look better.

- **Hall B is uncertain on both methods.** Its median is shown struck through and is never used as the room's rate.
- **Hall C's buildup is thin.** Eight fits is enough for the result to count as confident, but it is labelled *Thin* wherever it appears. Hall C's confidence also depends on the timezone reading described above.
- **One sensor was stuck at exactly 658 ppm.** ENSENSIA School 18 reported exactly 658 ppm for 46,826 consecutive readings, about 90% of its record, while its temperature and humidity readings kept changing. This turned out to be a device fill value, not air. The rule that now removes it: any value repeated unchanged for 13 or more readings spanning at least 2 hours is treated as a dead sensor and dropped, and the drop is counted per room in `audit.json`. It fired in 8 of the 25 ENSENSIA rooms (School 19 lost 25,445 readings, School 21 lost 22,927) and in none of the halls, so the halls' numbers did not change. School 18 is still counted among the 40 rooms, but it has no usable fit.
- **Readings below 350 ppm are dropped.** Clean outdoor air is about 420 ppm, so a reading well below that is sensor drift (low-cost sensors re-baseline themselves automatically). Such readings are dropped, never clamped up, and the count is reported. The halls lost none. One Spanish classroom lost 186. ENSENSIA School 19 lost 10,198.
- **The school rooms get no design comparison.** Neither school dataset publishes room volumes or design airflow, so no shortfall is claimed and no implied occupancy is computed for any of those 37 rooms. `audit.json` says this in a `design_note` for each dataset, and the page shows that note word for word. Air-change rates can still be fitted without a volume, because volume only scales the occupancy estimate, not the rate.
- **Peaks in the school data are single raw readings from uncleaned sensors.** ENSENSIA School 14 peaked at 7,950 ppm, but its 95th percentile is 3,892 ppm, and the two are always quoted together.

## 5. Architecture and implementation

```
browser ─► API Gateway HTTP API (ap-south-1)
             ├─ GET  /, /judges  → site Lambda  → S3 (private; one object: index.html)
             ├─ GET  /health     → health Lambda → SSM /secondbreath/lastAuditRun
             ├─ POST /fit        → fit Lambda      ┐
             ├─ POST /predict    → predict Lambda  ├─ ventilation.py, pure Python
             └─ POST /explain    → explain Lambda  ┘
EventBridge (5 min) → uptime Lambda → CloudWatch alarm "secondbreath-down" → SNS email
```

- **Zero runtime dependencies.** All the maths is hand-written in `ventilation.py`: least squares, exponential fits, the profile search and the forward model. There is no numpy anywhere. Because nothing needs compiling, `sam build` runs without Docker, and the Lambdas run on arm64. `ventilation.py` lives at the root of the repository. `backend/build.py` copies it into the Lambda code folder before building, and a test fails if that copy ever differs from the root file.
- **Least privilege.** `/fit`, `/predict` and `/explain` have **no IAM policy at all**. `/health` can read one SSM parameter. The site function can read one S3 object. The bucket blocks all public access.
- **Cost guardrails.** Every Lambda log group is created by the template with a 7-day retention period, because Lambda's automatically created groups never expire. There is a **$20/month AWS Budget** with alerts on both actual and forecast spend. It is a Budget rather than a billing alarm because the `EstimatedCharges` billing metric exists only in us-east-1, and this stack stays in ap-south-1. Nothing is provisioned (no EC2, no containers, no NAT gateway, no database), so idle cost is close to zero.
- **Uptime.** A Lambda requests `/` and `/health` every 5 minutes. The alarm fires on 2 failures in 10 minutes. It also fires when no data arrives, because a checker that has stopped running must page too. We chose this over a CloudWatch Synthetics canary on cost: at one run every 5 minutes, a canary makes about 8,600 runs a month against a 100-run free tier. The Lambda, alarm and SNS topic all stay inside the free tier.
- **Degraded is not down.** `/health` always returns 200 and puts `auditStale: true` in the body when the last audit run is more than 7 days old. An automated scorer should never get a non-200 response just because data is old.
- **Input validation happens at the edge.** `/fit` rejects bodies over 6 MB with a 413 and a readable message. The page trims large CSVs to their time and CO2 columns before uploading, which is how a full year of one hall (8 MB) fits under the limit. Every numeric field has bounds, and an out-of-range value gets a 400 that says what was wrong.
- **Backend tests.** The tests (`python -m unittest discover tests`) cover:
  - recovering a known decay rate from a CSV
  - the teaching-hours filter
  - 413 and 400 responses
  - the closed-form steady state
  - rounding that never flatters the room
  - uncertain fits never being used as a headline
  - HEAD requests matching GET
  - the checksum match between the root `ventilation.py` and its copy

## 6. How the coding agent shipped this

Claude Code built this project from a terminal, with three sessions working in parallel (backend, frontend, analysis), each in its own directory. They coordinated through `docs/HANDOFF.md` and a short `docs/STATUS.md`, and `docs/API.md` was the contract between backend and frontend.

**The AWS Agent Toolkit.** Two parts of the toolkit were used:

- **The AWS MCP server**, connected through `mcp-proxy-for-aws`. It exposes 8 tools. Six are read-only (`list_regions`, `search_documentation`, `read_documentation`, `retrieve_skill`, `get_regional_availability`, `get_tasks`). `get_presigned_url` is neither read-only nor destructive. `run_script` is the only one marked destructive, and what it can actually do is limited by its IAM user's permissions.
- **24 AWS skills** installed in `~/.claude/skills`, which Claude Code loads when a task needs them: `aws-serverless`, `aws-iam`, `aws-cloudformation`, `amazon-bedrock`, `aws-billing-and-cost-management` and others.

The MCP server signs its requests as its own scoped IAM user, `secondbreath-dev`, not as the human's user. CloudTrail therefore separates the agent's calls from the human's by principal, not just by user agent. `evidence/mcp-connection-verified.txt` records a `run_script` call (STS `GetCallerIdentity` and CloudFormation `DescribeStacks` on the `secondbreath` stack at 2026-09-29T12:52:46–47Z). CloudTrail recorded that call independently: the user is `secondbreath-dev`, and `invokedBy`, `userAgent` and `sourceIPAddress` are all `aws-mcp.amazonaws.com`. A matching `AwsMcpEvent` in us-east-1 shows the MCP client's user agent ending in `claude-code/2.1.284`. That record links the agent to the account call without relying on anything we wrote ourselves.

The full export in `evidence/cloudtrail-timeline.md` has 1,554 management events from 2026-09-28T18:45Z through 2026-09-29T13:49Z. Of these, 1,201 came from the build user and 353 from `secondbreath-dev`, the MCP user. 133 returned an error. None of the errors is a failed deploy: 105 are CloudFormation or SAM probing S3 bucket settings that were never set, 12 are `GetFunction` calls made before the function existed, 2 are the refused Bedrock `Converse` calls and 1 is the refused CloudFront `CreateDistributionWithTags`. The per-caller breakdown shows how the stack was built:

- 983 events by CloudFormation acting for us, 96 by Lambda and 1 by API Gateway
- 232 from `aws-cli`, 163 from `sam-cli` and 21 from `Boto3`
- 41 from the agent through the MCP server (`aws-mcp`), plus 15 MCP session events (`mcp-proxy`)
- 2 from the console

CloudTrail's event history lags by up to 15 minutes, so events after about 13:42Z may be missing from the export. The errors are left in. So is the limit: before the MCP user existed, the agent and the human shared one IAM user, and for those rows only the user agent separates them.

**The obstacles, in the order we hit them.**

1. **The MCP endpoint wasn't in our region.** The stack lives in Mumbai, so the first MCP configuration pointed at a Mumbai endpoint, and the hostname failed DNS resolution. The AWS MCP server is served only from us-east-1 and us-west-2. We moved the endpoint to `https://aws-mcp.us-east-1.api.aws/mcp`. The calls it makes still target whichever region we pass, which is `ap-south-1` for everything here, as the CloudTrail records above show.
2. **Root credentials, replaced before the connection worked.** That first, DNS-failing attempt used the account's root credentials. Root was never shown to be the problem. Before the connection first worked, though, root was replaced with `secondbreath-dev`, a scoped IAM user for the agent. That change is what makes principal-level attribution in CloudTrail possible.
3. **`uvx` wasn't installed.** The proxy is launched with `uvx mcp-proxy-for-aws@latest …`, and `uv` wasn't on the Windows machine. We installed it before the MCP server would start.
4. **PowerShell's byte-order mark.** On Windows PowerShell, `Out-File -Encoding utf8` writes a UTF-8 byte-order mark, and the AWS CLI rejects JSON files that start with one. JSON handed to the CLI is now written with `[IO.File]::WriteAllText(...)`, and the rule is in the project instructions so that no session makes the same mistake twice.
5. **A cold start that would have shown a scorer a 500.** On 28 Sep at 19:43Z and 19:46Z, `/health` returned 500. It looked like deploy noise, but it was a timeout: importing boto3 at 128 MB took longer than the 5-second limit. The first request from an automated scorer is usually a cold start, so this would have been the first thing a judge saw. The health and site functions now run at 512 MB with a 10-second timeout, and five out of five forced cold starts returned 200. The uptime alarm needs two failures within 10 minutes, so one slow cold start doesn't page anyone.
6. **Bedrock and CloudFront were blocked by account verification.** This is a new AWS account, and AWS was still verifying it.
   - **Bedrock:** two model calls on 28 Sep failed with two different errors.
     - `apac.amazon.nova-lite-v1:0` returned `AccessDeniedException`: "Your account is currently being verified. Verification normally takes less than 2 hours."
     - `global.anthropic.claude-haiku-4-5-20251001-v1:0` returned `ValidationException`: "Operation not allowed".

     The CloudTrail export has two `Converse` events, at 18:56:10Z and 18:57:08Z. Both are logged as `ValidationException`, "Operation not allowed", and neither records a model ID. The Nova call's `AccessDeniedException` does not appear in the export. Its text above is what the CLI returned.

     There is a separate trap here. In ap-south-1, `list-foundation-models` shows no Anthropic or Nova models available on demand, while the `apac.` and `in.` inference profiles are all `ACTIVE`. Bare model IDs therefore fail, and only inference-profile IDs work. `apac.` means Asia-Pacific processing, not processing kept inside India.
   - **CloudFront:** CloudTrail shows CloudFormation's `CreateDistributionWithTags` failing with `AccessDenied` at 19:43:22Z. CloudFormation rolled back and deleted the origin access control it had just created.

   The design absorbed both. CloudFront sits behind a template parameter (`EnableCloudFront`, default `false`), and until it can be switched on, a small Lambda serves the page from the private bucket. `/explain` was always meant to be model-optional, so it ships with deterministic templates, and its response has a `source` field that currently reads `"template"`. When verification clears, turning on CloudFront is a parameter change, and adding a model to `/explain` is one IAM permission and one function body.

## 7. Impact

**What has been measured.** Three lecture halls, each designed for about six air changes per hour, deliver between 0.74 and 1.09 on the two clean halls (reading the timestamps as local time), and every hall is at or below 1.17 under either reading, measured two independent ways across a full academic year. Hall B is too scattered to quote. The same method ran on 37 school rooms, where it produced confident rates for 22 of them by decay and 7 by buildup. Every figure can be regenerated from open data with one command.

**What has not been measured.** Health outcomes, attendance and learning: none of that. Nothing has been validated against a tracer-gas test or the halls' own air-handler logs, so the gap between design and measurement is a strong inference from two methods, not a direct inspection. We don't know why the halls fall short. It could be the fan schedules, the dampers or the controls. The site collects no analytics, so we also can't say who has used it.

The halls' timezone is also unresolved (see section 4). Their timestamps are UTC or a fixed offset, not local time with daylight saving, and the data cannot tell which. The audit reads them as local time. If they are UTC, the halls still fall short of design by the same margin, but Hall C's decay and buildup fits both become uncertain. The dataset's authors could settle it. Details are in `analysis/METHOD.md`, section 7, item 6.

**Who it's for.** People who already own a CO2 monitor and have no way to act on its readings:

- a teacher with a classroom sensor
- a school or university facilities team with a year of building logs nobody has looked at
- a parents' association asking whether a classroom is adequately ventilated
- a student who can export a CSV

SecondBreath gives each of them a number they can take to whoever runs the building ("this room delivers about one air change an hour, not six"), along with the evidence for it and its uncertainty. The prediction panel turns that number into a practical decision: how many people this room can hold for 90 minutes before its air passes 1,000 ppm, or 1,400 ppm.

This is the Community lane, and the method is designed to be reused. Every CC BY 4.0 dataset is cited, the audit runs on anyone's machine without an AWS account, and the thresholds that decide what counts as confident are written in `audit.json` for anyone to challenge.

## 8. What I'd do next

1. **Check the finding against the building.** Send the Hall A–C results to the dataset's authors in Limassol and ask for the halls' air-handler schedules, or for one tracer-gas or door-closed test. Ask them too which clock the `recorded` column uses, since that decides whether Hall C's rate is confident. This is the direct test of the infiltration objection, and it could confirm or overturn the headline.
2. **Accept exports from consumer monitors as they come.** The halls were recorded with Airthings sensors, and the parser already handles semicolon, comma and tab delimiters, ISO and epoch timestamps, and interleaved multi-sensor rows. The next step is a tested import for the two or three monitors that teachers actually own, so that step 8 of the click path works with anyone's file.
3. **Switch on CloudFront and a model for `/explain` once verification clears, without giving up the rule.** CloudFront needs its `/judges` rewrite. For `/explain`, the model would phrase the sentences, but the existing test that every number in `sentences` appears in `facts` would stay mandatory, and the template would remain as the fallback.
