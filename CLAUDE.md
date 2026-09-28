# SecondBreath

How much of the air you are breathing came out of someone else's lungs.

A serverless AWS app that fingerprints a room's real ventilation rate from a CO2
CSV, then predicts what any planned meeting or class will do to the air in it.

Built for the AWS Builder Center "Zero to Shipped" hackathon.
Category: `#social-good` (Health) · Lane: `#community`
**Hard deadline: 2 Oct 2026, 23:59 PT (3 Oct, 12:29 IST).**

---

## What this is, in one paragraph

Indoor CO2 is a marker for how much of the air in a room has already passed
through somebody's lungs. Rudnick & Milton (2003) showed that the rebreathed
fraction is simply `(C_indoor - C_outdoor) / 38,000 ppm`. At 2,000 ppm, one
breath in 24 is second-hand. Nobody can see or smell this, so nobody acts on it.

The hard part is not the formula. It is that a room's ventilation rate is
unknown, and inferring it is an inverse problem. We solve it twice, two
different ways, and check the answers against each other.

---

## The two methods, and why there are two

**Decay fit** (`fit_decays`). After people leave, CO2 falls exponentially and
the slope of `ln(C - C_outdoor)` gives air changes per hour. Simple and very
precise, but it measures the room *while it is emptying*.

**Buildup fit** (`fit_buildups`). While people are in the room, CO2 rises
toward a steady state. Two unknowns — the ventilation rate and the number of
occupants — but they separate: the curvature of the rise carries the rate, the
asymptote carries the CO2 source. For any fixed rate the model is linear in the
steady state, so we search the rate on a log grid and solve the rest in closed
form.

**Why both.** The obvious objection to the decay method is that if the air
handler shuts off when the room empties, the fitted number is the building's
leak rate, not the air people actually breathe. The buildup fit runs during
occupancy and answers that objection directly. Report both, always. Two methods
that could have disagreed and did not is the strongest evidence this project
has.

Not every buildup segment can pin the rate down: a rise still far from steady
state looks almost linear and fits nearly as well at many rates. Every buildup
fit therefore carries a profile band, and `BuildupFit.identifiable` is False
when that band is too wide. **Discard unidentifiable fits. Never quote them.**

---

## The finding that anchors the submission

Three university lecture halls, each specified at 100% fresh air and roughly
6 air changes per hour.

| Hall | Design | Decay fit | Buildup fit (occupied) |
| --- | --- | --- | --- |
| A | 5.8 | 0.74 (252 fits) | 0.72 |
| B | 6.0 | 1.10 — wide spread, see below | 0.78 |
| C | 5.9 | 0.88 (259 fits) | 1.09 |

**How to state this correctly, everywhere:**

> Halls A and C fit cleanly at 0.74 and 0.88 air changes per hour. Hall B's
> decay fits scatter (interquartile range 0.47 to 1.70) and it is reported as
> uncertain, not averaged into the headline.

Peak reading 4,957 ppm in Hall B, which is one breath in eight already exhaled
by somebody else in the room.

Never round these figures up, never drop the fit counts, and never present
Hall B as if it were as certain as A and C.

---

## Non-negotiable constraints

1. **The live URL must never break.** It is a pass/fail ship gate and judging
   runs into the week of 19 Oct. Any change that risks the deployed site gets
   tested locally first. Never leave `main` in a broken deployed state.
2. **No login, no paywall, no CAPTCHA, no bot-blocking.** An automated scorer
   must be able to load the page and see real output with zero interaction.
3. **Deterministic core, LLM only at the edges.** The model never computes a
   ventilation rate, a CO2 value or a risk number. It parses free text into
   parameters and writes explanations of numbers the solver already produced.
   If you find yourself asking a model for a number, stop.
4. **Pure Python, no numpy, in Lambda.** `sam build` must work without Docker.
   Implement the maths by hand. This is deliberate, not an oversight.
5. **Serverless only.** Lambda, API Gateway HTTP API, DynamoDB on-demand, S3,
   CloudFront or Amplify, Bedrock. No EC2, no ECS, no NAT Gateway, no
   OpenSearch, no provisioned databases. The whole thing must idle at ~zero
   cost through late October.
6. **Every number shown to a user must be traceable** to either a committed
   dataset or a function in `ventilation.py`. No illustrative figures, no
   invented constants, no placeholder text, no `TODO` left in anything
   user-visible or published.
7. **Honesty beats polish.** If a fit is uncertain, say so in the UI. The
   `Fingerprint.confident` and `BuildupFit.identifiable` flags exist for this.
   A discarded bad fit is better than a quoted bad fit.

---

## Repository layout and terminal ownership

Three Claude Code sessions run in parallel. **Stay inside your own directory.**
If you need something outside it, write the request into `docs/HANDOFF.md`
rather than editing another terminal's files.

```
backend/      T1 only   Lambda handlers, SAM template, backend tests
web/          T2 only   single-page frontend, charts, styling
analysis/     T3 only   dataset download, audit pipeline, evidence generation
data/         T3 only   downloaded CSVs (gitignored)
docs/         T3 owns; T1 owns docs/API.md
evidence/     T3 only   CloudTrail export, agent-connection proof
ventilation.py          shared core maths at the repo ROOT.
                        CHANGES REQUIRE ALL THREE TO AGREE.
```

`docs/API.md` is the contract between backend and frontend. T1 writes it, T2
reads it and never edits it. If the shape must change, T1 updates it and notes
the change in `docs/STATUS.md`.

**How Lambda gets `ventilation.py`.** A Lambda function can only import files
inside its own `CodeUri` folder, so the root file cannot be imported directly.
The build copies it into each function folder before `sam build`. Those copies
are gitignored, and a test asserts each copy's checksum matches the root file
so they can never silently drift apart. The root file is the only one anybody
edits.

---

## Status protocol (important)

At the end of every work block, update `docs/STATUS.md`. Keep it under 50
lines. Overwrite the previous contents; git history keeps the old ones.

```markdown
# STATUS — <date, time IST>

## Phase
<current phase number and name>

## Done since last update
- <one line each, only things that actually work>

## Live state
- Site: <url> — <http status, last checked>
- /health: <url> — <status>
- Deployed stack: <name, region>

## Broken or blocked
- <what, the exact error, what you tried>

## Next 3 actions
1.
2.
3.

## Decisions taken
- <decision> — <one-line reason>
```

The human pastes this file into a planning conversation. Write it for a reader
who cannot see your terminal.

---

## Coding rules

- **Plan before writing.** For anything over ~30 lines, state the approach and
  the smallest next change, then implement. Do not scaffold a feature nobody
  asked for.
- **Test the maths, not the framework.** Every function in `ventilation.py`
  needs a test that would fail if the physics were wrong. The strongest tests
  we have recover a known air-change rate from a synthetic decay curve, and
  recover both a known rate and a known occupancy from a synthetic rise.
- **No new runtime dependencies** without a stated reason. Zero is the target
  and currently the reality.
- **Comment the why, not the what.** "Median not mean: one mis-detected
  segment should not move the headline" is useful. "Calculate the median" is
  not.
- **Small commits with real messages.** The commit log is part of the
  submission story.

---

## AWS specifics that will bite you

- **Region is `ap-south-1` (Mumbai).** One region for the whole stack. No
  cross-region calls.
- **Bedrock model IDs:** bare IDs fail. Verified profiles in this region are
  prefixed `apac.` (Asia-Pacific processing) or `in.` (India-only processing).
  Be precise about which is in use: `apac.` is **not** an in-India guarantee
  and must not be described as one. Keep the model ID as a SAM **parameter**,
  never hardcoded. Use the **Converse API** so swapping models is one change.
- **Bedrock is currently blocked** by new-account verification
  (`AccessDeniedException: Your account is currently being verified`). Build
  everything else first. If it has not cleared by the evening of 30 Sep, drop
  `/explain` and generate explanations from deterministic sentence templates
  built on solver output. The app is model-optional by design and the write-up
  should say so.
- **Least privilege:** `/fit` and `/predict` get no IAM policy at all.
  `/explain` gets `bedrock:InvokeModel` and nothing else.
- **Cost guardrails:** CloudWatch log retention 7 days on every log group,
  DynamoDB on-demand with TTL on any per-session data, billing alarm at $20.
- **CORS** on the HTTP API, or the frontend silently fails.
- **Health endpoint** returns 200 plus the timestamp of the last audit run.
  Stale data is reported in the body, not as a non-200: degraded is not down.
- **Windows PowerShell writes a byte-order mark** with
  `Out-File -Encoding utf8`, and the AWS CLI rejects those files. Use
  `[IO.File]::WriteAllText(...)` for any JSON handed to the CLI.

---

## Data and attribution

Primary dataset: *Indoor Environmental Quality Measurements of University
Lecture Halls*, Zenodo record 18385830, **CC BY 4.0**. Three halls in Limassol,
Cyprus, full academic year, with a characteristics file giving each hall's
volume (A 363, B 283, C 1520 m3) and designed ventilation.

Secondary: Zenodo 5062837 (Spanish primary classrooms, CC BY 4.0) and Zenodo
18195710 (ENSENSIA schools, CC BY 4.0).

**CC BY 4.0 requires attribution.** Cite every dataset with its DOI in the
README and in the app footer. This is a licence obligation, not a courtesy.

---

## What this project is not

State these plainly in the UI and the write-up:

- Not medical advice, and not an absolute infection probability. Rebreathed
  fraction is an exposure metric.
- The decay method measures the room while it is emptying, so on its own it
  could be reporting infiltration rather than delivered ventilation. The
  buildup fit is the test of that, and both results are reported either way.
- Single-point sensors assume a well-mixed room. Local exposure near a source
  can be higher than the room average.
- Occupancy is not recorded in these datasets. The buildup fit *infers* an
  implied occupancy from the fitted source strength; that is an output of the
  model, not a measurement, and must be labelled as such.
- Low-cost sensors drift. Readings below outdoor level are dropped, not
  clamped, and the drop count is reported.
- Evidence that elevated CO2 directly impairs cognition is contested: Harvard's
  COGfx study found large effects at 1,400 ppm, a Danish study found none at
  5,000 ppm. Lead with rebreathed air, mention cognition as debated.
- No figure derived from an assumption that is not in the data may be shown to
  a user. Estimating seat counts by dividing room volume by a made-up number
  is the exact thing this rule forbids.