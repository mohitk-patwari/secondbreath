# SecondBreath

SecondBreath works out a room's real ventilation rate from its CO2 log, then tells you how much of the air in that room has already been breathed out by someone else.

**Live:** https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/ (no login needed; the judges' tour is at [`/judges`](https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/judges))

```bash
curl https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/health
# {"ok": true, "service": "secondbreath", "lastAuditRun": "<UTC time of the last audit run>", "auditStale": false}
```

`/health` returns 200 even when the audit is stale. In that case `auditStale` is true: the service is degraded, not down.

---

## The finding

Three university lecture halls in Limassol, Cyprus, were measured for a full academic year (Sept 2023 to Aug 2024). Each one was designed for 100% fresh air at about six air changes per hour (ACH).

| Hall | Design ACH | Decay fit (room emptying) | Buildup fit (room occupied) | Peak CO2 |
|---|---|---|---|---|
| A | 5.79 | **0.74** (252 fits, IQR 0.63–0.90) | **1.02** (27 kept, 6 discarded, IQR 0.52–1.18) | 3,171 ppm |
| B | 6.01 | 1.10 **uncertain** (323 fits, IQR 0.47–1.70) | 0.93 **uncertain** (31 kept, 8 discarded, IQR 0.64–1.50) | 4,957 ppm |
| C | 5.92 | **0.88** (259 fits, IQR 0.58–1.26) | **1.09** **thin** (8 kept, 2 discarded, IQR 0.80–1.25) | 2,241 ppm |

These are teaching hours only (Mon–Fri, 08:00–17:59). Every number is copied from [`analysis/audit.json`](analysis/audit.json).

- **Halls A and C** fit cleanly: 0.74 and 0.88 ACH by decay, and 1.02 and 1.09 by buildup. That is 5.4 to 7.8 times below their design on either method.
- **Hall B** is uncertain on both methods. Its decay fits scatter across an interquartile range of 0.47 to 1.70 and its buildup fits across 0.64 to 1.50. The medians (1.10 and 0.93) are not the room's rate and should not be quoted as if they were. Hall B is left out of the headline, not averaged into it.
- **Hall C's buildup** rests on only 8 fits. It is thin, and it is labelled that way.

Hall B's peak reading was 4,957 ppm. At that point about 12% of the air in the room, **one breath in eight**, had already been breathed out by someone else.

### 40 rooms, and how many of them are confident

The same fits, with the same parameters, ran over **40 rooms from three open datasets**. Of those, **24 have a confident decay fit, 9 have a confident buildup fit, and 3 have a published design figure**. A room without a confident fit is counted as analysed, but its rate is never quoted.

| Dataset | Rooms | Confident decay | Confident buildup | Design figure |
|---|---|---|---|---|
| Lecture halls, Cyprus (Zenodo 18385830) | 3 | 2 | 2 | 3 |
| Primary classrooms, Castellón, Spain, 2021 (Zenodo 5062837) | 12 | 8 | 0 | 0 |
| ENSENSIA schools, Patras, Greece, 2023–25 (Zenodo 18195710) | 25 | 14 | 7 | 0 |

The two school datasets publish no room volumes and no design airflow. That means no shortfall against design can be claimed for any of their rooms, and none is. Their confident decay rates are there for context only. The Spanish classrooms, measured with Covid-19 ventilation measures in force, range from 0.68 to 3.65 ACH (median 2.32). The Greek schools range from 0.24 to 1.75 ACH (median 1.40). The halls' 0.74 and 0.88 sit inside the range of ordinary schools, even though the halls were designed for six.

## Two methods, and why both

**Decay fit** (`ventilation.fit_decays`). When people leave a room, CO2 falls exponentially towards the outdoor level. The slope of `ln(C − C_outdoor)` gives the air-change rate.

**Buildup fit** (`ventilation.fit_buildups`). While people are in the room, CO2 rises towards a steady state. The curvature of that rise gives the air-change rate, and the level it is heading for gives the CO2 source strength.

The obvious objection to the decay method is that the air handler may switch off when a lecture ends. If it does, a decay fit measures the building's leakage (infiltration), not the ventilation people actually breathe during class. The buildup fit is the test of that objection, because it reads the same room while it is full. If the halls were getting their design airflow during lectures, buildup would come out near six. It comes out at 1.02 and 1.09.

The two methods do not agree to the decimal. Buildup reads higher in both clean halls, and Hall A's buildup median (1.02) sits just above its decay interquartile range (0.63–0.90). But the two methods could have disagreed by a factor of six, and they do not.

Some buildup fits cannot pin the rate down. A rise that is still far from steady state looks almost linear, so many different rates fit it about equally well. Every buildup fit therefore carries a profile band: the range of rates whose squared error is within 10% of the best fit. If the top of that band is 3 or more times its bottom, the fit is **discarded and never quoted**.

## Reproduce it

You need Python 3.11 or newer. There are no packages to install for the maths or the audit.

```bash
git clone https://github.com/mohitk-patwari/secondbreath.git
cd secondbreath

python ventilation.py                            # self-test: recovers a known ACH from a synthetic decay,
                                                 # and a known ACH and occupancy from a synthetic rise
python analysis/test_loaders.py                  # school-dataset loaders, flatline rule
python analysis/audit_lecture_halls.py --json    # downloads the three Zenodo records into data/ (once),
                                                 # writes analysis/audit.json and analysis/figures/*.svg
```

At the end of a run, the audit script tries to write the run time to SSM for `/health`. Without AWS credentials this step only prints a warning, and every number the audit produces is still valid.

Backend (needs the AWS SAM CLI, but not Docker):

```bash
cd backend
python build.py                                  # copies the root ventilation.py into src/, then sam build
python -m unittest discover tests                # includes a checksum test: src/ventilation.py == root copy
sam deploy --parameter-overrides AlertEmail=<your email>
python deploy_web.py                             # ships web/index.html
```

## Architecture

- **API Gateway HTTP API** in front of six Python 3.13 arm64 Lambdas: `/fit`, `/predict`, `/explain`, `/health`, the site itself (`/` and `/judges`), and an uptime checker. The page is a single `index.html` stored in a private S3 bucket.
- **Zero runtime dependencies.** `ventilation.py` is written in plain Python with no numpy, so `sam build` runs without Docker.
- **Least privilege.** `/fit`, `/predict` and `/explain` have no IAM policy at all. `/health` can read one SSM parameter, and the site function can read one S3 object.
- **Cost guardrails.** Every log group keeps logs for 7 days. There is an account-wide $20/month AWS Budget with actual and forecast alerts. Nothing is provisioned, so the stack costs close to nothing when idle.
- **Uptime.** A scheduled Lambda requests `/` and `/health` every 5 minutes. The CloudWatch alarm `secondbreath-down` fires on 2 failures in 10 minutes, and it also fires if the checker itself stops running.
- **Serverless throughout.** There is no EC2, no containers, no NAT gateway and no database. Everything runs in `ap-south-1` apart from the Budget, which AWS only offers globally. CloudFront is written into the template but switched off: it stays off until AWS finishes verifying this new account.

The API contract is in [`docs/API.md`](docs/API.md), and the evidence of how the stack was built is in [`evidence/`](evidence/README.md).

`/explain` writes its sentences from **deterministic templates**, not a language model. Every number in its output is a number the solver already produced, rounded in whichever direction does not flatter the room. No model computes any rate, CO2 value or risk figure anywhere in this project.

## What it doesn't know

- **This is not medical advice, and not an infection probability.** Rebreathed fraction is a measure of exposure.
- **The decay method measures the room while it empties.** On its own it could be reporting infiltration rather than delivered ventilation. The buildup fit is the test of that, and both results are reported either way.
- **One sensor assumes the air is well mixed.** Exposure close to a person can be higher than the room average.
- **None of these datasets records occupancy.** The buildup fit infers an implied occupancy from the source strength it fits. That is an output of the model, not a measurement, and the site does not show it. For the school datasets it cannot be computed at all, because no room volumes are published.
- **Low-cost sensors drift.** Low readings are dropped, never clamped, and the drop is counted. The audit drops readings below 350 ppm and records the count per room in `audit.json`. The live `/fit` endpoint drops readings below the outdoor level you set and returns that count. The school loaders also drop dead-sensor stretches, where one value repeats unchanged for 13 or more readings over at least 2 hours.
- **The evidence that CO2 itself impairs thinking is contested.** Harvard's COGfx study found large effects at 1,400 ppm. A Danish study found none at 5,000 ppm. This project leads with rebreathed air instead.
- **No figure rests on an assumption that is not in the data.** Seat counts are never estimated by dividing room volume by an invented number.
- **The school rooms have no design comparison.** Their datasets publish neither volume nor design airflow.

## Data and attribution

All three datasets are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The same citations appear in the site footer.

- Kakoulli, C., Michaelides, M. and Kyriacou, A. (2026). *Indoor Environmental Quality Measurements of University Lecture Halls*. Zenodo record 18385830. [doi:10.5281/zenodo.18385830](https://doi.org/10.5281/zenodo.18385830). CC BY 4.0.
- Trilles, S. (2021). *Co2 concentration, temperature and humidity in primary classrooms during the Covid-19 Safety Measures in Spain*. Zenodo record 5062837. [doi:10.5281/zenodo.5062837](https://doi.org/10.5281/zenodo.5062837). CC BY 4.0.
- Apostolopoulos, J., Fouskas, G. and Pandis, S. (2026). *Indoor Air Pollutants (Raw)* (ENSENSIA). Zenodo record 18195710. [doi:10.5281/zenodo.18195710](https://doi.org/10.5281/zenodo.18195710). CC BY 4.0.

The rebreathed-fraction formula `(C_indoor − C_outdoor) / 38,000 ppm` comes from Rudnick, S. N. and Milton, D. K. (2003), *Risk of indoor airborne infection transmission estimated from carbon dioxide concentration*, Indoor Air 13(3).

Built for the AWS Builder Center "Zero to Shipped" hackathon (`#social-good`, `#community`).
