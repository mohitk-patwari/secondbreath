# SecondBreath API

Base URL: `https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com`

JSON in, JSON out. CORS allows any origin, methods `GET, POST, OPTIONS`,
header `content-type`. Errors: `400`/`413` with `{"error": "<human message>"}`.
Show `error` to the user as is.

Numbers come back at full precision. Rounding is the frontend's job, and it
should not round in a direction that flatters the room. `null` in a number
field means "no value", for example `peakOneBreathIn` when the peak is at
outdoor level.

## GET /

Serves `web/index.html` (`text/html; charset=utf-8`, `max-age=60`), gzipped
when the request sends `Accept-Encoding: gzip`. `HEAD` works on `/`,
`/judges` and `/health`: the same status and headers, with no body. This is
the public site until CloudFront is enabled; see docs/STATUS.md. Ship changes
with `python backend/deploy_web.py`.

## GET /judges

The same `index.html` as `GET /`. The page opens its judges' tour when the path
is `/judges`.

## GET /health

```json
200 {"ok": true, "service": "secondbreath", "lastAuditRun": "2026-09-28T19:05:00Z", "auditStale": false}
```
`lastAuditRun` is read from SSM parameter `/secondbreath/lastAuditRun`. It is
`null` if the parameter doesn't exist. `auditStale` is true when the value is
missing or more than 7 days old. Always 200: stale means degraded, not down.

## POST /fit

Fingerprints a room from a CO2 time series using both methods.

Request:
```json
{
  "csv": "recorded;CO2 ppm\n2023-09-01T09:15:20;503.00\n...",
  "volumeM3": 363,
  "outdoorPpm": 420,
  "columns": {"timestamp": "recorded", "co2": "CO2 ppm", "delimiter": ";"},
  "teachingHoursOnly": false
}
```
- `volumeM3` is required, 1 to 1,000,000.
- `teachingHoursOnly` is optional, boolean, default `false`. When true it
  restricts fitting to Mon–Fri 08:00–17:59 in the CSV's own wall-clock time,
  the same rule as analysis/audit_lecture_halls.py. Decay fits are kept by
  start time. Buildups are fitted on the filtered series. On the full Hall A
  year this reproduces audit.json exactly: decay 0.744 (252 fits), buildup
  1.019 (27 identifiable, 6 discarded). The flag only affects `decay` and
  `buildup`. `readings`, `peak*` and `series` always cover the whole upload.
- `outdoorPpm` is optional, 300 to 600, default 420.
- `columns` and each of its keys are optional. By default the delimiter is
  whichever of `;` `,` or tab appears most often in the header. The timestamp
  column is the first header containing `time`, `date` or `recorded`. The CO2
  column is the first header containing `co2`, case-insensitive.
- Timestamps can be ISO 8601 (with or without an offset) or epoch seconds.
- Rows with an empty CO2 cell are skipped silently; interleaved multi-sensor
  exports do this. Rows that fail to parse are counted in `rowsUnparseable`.
  Readings below `outdoorPpm` are dropped, not clamped, and counted.
- **Size limit:** the request body must be at most 6,000,000 bytes, or you get
  413 with a message. Over about 6.2 MB, API Gateway returns its own 413
  `{"message": "Request Entity Too Large"}`. **Check file size in the browser
  before upload.** Sending only the timestamp and CO2 columns shrinks a full
  year of one hall to about 2.2 MB, and that takes about 4.3 s to process.

Response (real output for Hall A, full year, `teachingHoursOnly: true`,
trimmed `segments` and `series`):
```json
{
  "readings": 81450,
  "readingsDroppedBelowOutdoor": 970,
  "rowsUnparseable": 0,
  "span": ["2023-09-01T09:15:20", "2024-08-31T23:59:20"],
  "outdoorPpm": 420.0,
  "volumeM3": 363.0,
  "teachingHoursOnly": true,
  "peakPpm": 3171.0,
  "peakRebreathedFraction": 0.07239473684210526,
  "peakOneBreathIn": 13.81315885132679,
  "decay": {
    "fingerprint": {"achMedian": 0.7438054612350747, "achP25": 0.6307635952420085,
                    "achP75": 0.9006306106047278, "nFits": 252,
                    "totalMinutes": 16105.316666666668, "confident": true},
    "fits": 252,
    "segments": [["2023-09-04T09:09:26", "2023-09-04T10:34:30", 0.8082988700761499],
                 ["2023-09-04T11:09:26", "2023-09-04T11:59:26", 0.6678398051324023]]
  },
  "buildup": {
    "fingerprint": {"achMedian": 1.0194523334245216, "achP25": 0.5165480852636026,
                    "achP75": 1.1818246601236873, "nFits": 27,
                    "totalMinutes": 2565.35, "confident": true},
    "identifiable": 27,
    "discarded": 6,
    "segments": [["2023-09-04T08:04:30", "2023-09-04T09:09:26", 1.4534952630007525],
                 ["2023-09-07T08:04:31", "2023-09-07T09:29:27", 1.2537977819252197]]
  },
  "series": [["2023-09-01T09:15:20", 503.0], ["2023-09-01T16:14:28", 491.0]]
}
```
- `segments` lists `[startIso, endIso, ach]` per fit, the same stretches the
  fingerprint was built from. `buildup.segments` holds identifiable fits only;
  discarded fits are never returned. The full-year response has 252 decay
  segments, about 20 KB.
- `decay.fingerprint` and `buildup.fingerprint` are `null` when there are no fits.
- `confident: false` means the frontend must show the number as uncertain,
  not as a headline.
- `buildup.fingerprint` is built only from identifiable fits. `discarded`
  fits are never quoted anywhere.
- `series` is `[isoTimestamp, ppm]` pairs, downsampled by stride to at most
  about 1,000 points, for plotting only. Brief spikes can fall between points,
  so always take the peak from `peakPpm`.

## POST /predict

Forward model for a planned session.

Request:
```json
{"volumeM3": 363, "ach": 0.74, "occupants": 60, "minutes": 90,
 "activity": "seated_quiet", "startPpm": 420, "outdoorPpm": 420}
```
- Required: `volumeM3` (1 to 1e6), `ach` (0.01 to 50), `occupants` (0 to
  10,000, truncated to an integer) and `minutes` (1 to 1,440).
- **Physical density limit:** `volumeM3 / occupants` must be at least
  0.2 m³ per person (`MIN_INPUT_M3_PER_PERSON` in ventilation.py). That floor is a
  sanity check we chose, not a sourced figure, and it is used only to reject
  impossible input. Otherwise you get 400 with an `error` such as "2,000
  people cannot fit in 363 m³ ...". Show it as is.
- `activity` is optional and must be one of `seated_quiet`, `seated_speaking`
  (the default), `light_activity` or `moderate_activity`.
- `startPpm` is optional, from `outdoorPpm` to 10,000, and defaults to
  `outdoorPpm`.
- `outdoorPpm` is optional, 300 to 600, default 420.

Response (real output for the request above, trimmed `curve`):
```json
{
  "curve": [{"minute": 0.0, "ppm": 420.0, "rebreathedFraction": 0.0},
            {"minute": 1.0, "ppm": 459.69958623839193, "rebreathedFraction": 0.001044725953641893},
            {"minute": 90.0, "ppm": 2591.4083235223943, "rebreathedFraction": 0.0571423243032209}],
  "peakPpm": 2591.4083235223943,
  "peakRebreathedFraction": 0.0571423243032209,
  "peakOneBreathIn": 17.500163183660238,
  "meanRebreathedFraction": 0.03369380423566409,
  "minutesAbove1000": 75.0,
  "steadyStatePpm": 3658.7759660486936,
  "withinValidatedRange": true,
  "validatedMaxPpm": 5000.0,
  "maxOccupancy": {"1000": 16, "1400": 27},
  "input": {"volumeM3": 363.0, "ach": 0.74, "occupants": 60, "minutes": 90.0,
            "activity": "seated_quiet", "outdoorPpm": 420.0}
}
```
- `input` echoes the validated request with defaults filled in (added 29 Sep, additive).
- `curve` has one point per minute, `minutes + 1` points in total.
- `maxOccupancy` is the largest headcount whose peak stays at or under each
  ppm limit for this room, duration and activity. It is capped at 500, so
  `500` means "500 or more".
- **`withinValidatedRange: false`** means the session's `peakPpm` is above
  `validatedMaxPpm`. That is 5,000 ppm: OSHA's 8-hour PEL and ACGIH's TLV,
  both exposure limits. We use it because above it the useful answer is
  "leave the room", and it is above every room's p95 in our data. **Show a
  warning instead of the peak, the curve and the fractions.** `/explain` does
  the same. `steadyStatePpm` is the asymptote. It is not flagged: a short
  session can have a high asymptote and still peak within range.
- `rebreathedFraction` never exceeds 1.0, and `peakOneBreathIn` never drops
  below 1: a breath can't be more than entirely exhaled air.

## POST /explain

Plain-language sentences about solver output. Today they come from
deterministic templates (`"source": "template"`). A model can replace the
templates later behind this same endpoint and response shape, and `source`
will then name it. Every number in `sentences` is one of the numbers in `facts`.

Request, one of:
```json
{"kind": "predict", "request": {<a /predict request body>}}
{"kind": "fit", "result": {<a /fit response, as received>}}
```
- `predict` re-runs the solver on `request`, with the same validation and 400s
  as /predict.
- `fit` reads only `outdoorPpm`, `peakPpm`, `readingsDroppedBelowOutdoor`,
  `decay.fingerprint`, `buildup.fingerprint` and `buildup.discarded` from a
  /fit response the client already has. `series` and `segments` can be left
  out. The peak fraction is recomputed from `peakPpm`.

Response (real output, fit kind, with Hall B's audit numbers):
```json
{
  "source": "template",
  "sentences": [
    "The highest reading was 4,957 ppm: 12.0% of inhaled air had already been exhaled by someone else, one breath in 8.",
    "The decay fit is uncertain: 323 fits scatter from 0.47 to 1.70 air changes per hour (interquartile range), so its median of 1.10 should not be quoted as the room's rate.",
    "Only the decay method produced a result. It measures the room while it empties, so on its own it could be the building's leak rate rather than the ventilation people breathe."
  ],
  "caveats": ["Rebreathed fraction is an exposure measure, not an infection probability, and this is not medical advice.",
              "A single sensor assumes well-mixed air; close to a person it can be higher."],
  "facts": {"kind": "fit", "outdoorPpm": 420.0, "peakPpm": 4957.0, "peakRebreathedFraction": 0.1194,
            "peakOneBreathIn": 8.3756, "readingsDroppedBelowOutdoor": 0,
            "decay": {"achMedian": 1.1, "achP25": 0.47, "achP75": 1.7, "nFits": 323, "confident": false},
            "buildup": null, "buildupDiscarded": 0}
}
```
- Rounding never flatters the room. ACH and "one breath in N" round down; ppm
  and percentages round up.
- A fingerprint with `confident: false` is described as uncertain, with its
  interquartile range, and is never stated as the room's rate.
- When both methods are confident, one sentence says whether the buildup
  median falls inside the decay fits' interquartile range (agree or disagree).
- Show `sentences` and `caveats` as they are. `facts` is there for tracing.
