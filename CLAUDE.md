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
unknown, and inferring it is an inverse problem: fit the exponential decay of
CO2 after occupancy ends and the slope gives you air changes per hour. Once a
room is fingerprinted, the forward model predicts any future session.

**The finding that anchors the submission:** three university lecture halls,
each specified at 100% fresh air and ~6 ACH, deliver 0.74, 1.10 and 0.88 ACH
measured across 834 clean decay fits over a full academic year. Five to eight
times below design. Peak 4,957 ppm, which is one breath in eight.

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
   placeholder text, no `TODO` left in anything user-visible or published.
7. **Honesty beats polish.** If a fit is uncertain, say so in the UI. The
   `Fingerprint.confident` flag exists for this. A discarded bad fit is
   better than a quoted bad fit.

---

## Repository layout and terminal ownership

Three Claude Code sessions run in parallel. **Stay inside your own directory.**
If you need something outside it, write the request into `docs/HANDOFF.md`
rather than editing another terminal's files.

```
backend/      T1 only   Lambda handlers, SAM template, backend tests
web/          T2 only   single-page frontend, charts, styling
analysis/     T3 only   dataset download, audit pipeline, evidence generation
data/         T3 only   downloaded CSVs (gitignored if large)
docs/         T3 owns; T1 owns docs/API.md
evidence/     T3 only   CloudTrail export, agent-connection proof
ventilation.py          shared core maths. CHANGES REQUIRE ALL THREE TO AGREE.
```

`docs/API.md` is the contract between backend and frontend. T1 writes it, T2
reads it and never edits it. If the shape must change, T1 updates it and notes
the change in `docs/STATUS.md`.

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
  needs a test that would fail if the physics were wrong. The strongest test
  we have is recovering a known air-change rate from a synthetic decay curve.
- **No new runtime dependencies** without a stated reason. Zero is the target
  and currently the reality.
- **Comment the why, not the what.** "Median not mean: one mis-detected
  segment should not move the headline" is useful. "Calculate the median" is
  not.
- **Small commits with real messages.** The commit log is part of the
  submission story.

---

## AWS specifics that will bite you

- **Bedrock model IDs:** bare IDs fail for on-demand invocation. Use an
  inference profile ID (prefixed `global.`, `apac.` or `us.`). Enumerate what
  is actually available with `aws bedrock list-inference-profiles` rather than
  trusting any blog post. Use the **Converse API** so swapping models is one
  parameter.
- **Least privilege:** the `/fit` and `/predict` Lambdas need no IAM policy at
  all. The `/explain` Lambda gets `bedrock:InvokeModel` and nothing else.
- **Cost guardrails:** CloudWatch log retention set to 7 days on every log
  group, DynamoDB on-demand with TTL on any per-session data, and a billing
  alarm at $20.
- **CORS** on the HTTP API, or the frontend silently fails.
- **Health endpoint** returns 200 plus the timestamp of the last audit run.
  Stale data is reported in the body, not as a non-200: degraded is not down.

---

## Data and attribution

Primary dataset: *Indoor Environmental Quality Measurements of University
Lecture Halls*, Zenodo record 18385830, **CC BY 4.0**. Three halls in Limassol,
Cyprus, full academic year, with a characteristics file giving each hall's
volume and designed ventilation.

Secondary: Zenodo 5062837 (Spanish primary classrooms, CC BY 4.0) and Zenodo
18195710 (ENSENSIA schools, CC BY 4.0).

**CC BY 4.0 requires attribution.** Cite every dataset with its DOI in the
README and in the app footer. This is a licence obligation, not a courtesy.

---

## What this project is not

State these plainly in the UI and the write-up:

- Not medical advice, and not an absolute infection probability. Rebreathed
  fraction is an exposure metric.
- The decay method measures the room while it is emptying. If the air handler
  stops with occupancy, the fitted rate reflects infiltration rather than
  delivered ventilation. The teaching-hours vs off-hours comparison tests this
  and must be reported either way.
- Single-point sensors assume a well-mixed room. Local exposure near a source
  can be higher than the room average.
- Occupancy is unknown in the public datasets, so no per-person airflow figure
  is claimed.
- Low-cost sensors drift. Readings below outdoor level are dropped, not
  clamped, and the drop count is reported.
- Evidence that elevated CO2 directly impairs cognition is contested: Harvard's
  COGfx study found large effects at 1,400 ppm, a Danish study found none at
  5,000 ppm. Lead with rebreathed air, mention cognition as debated.
