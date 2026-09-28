# SecondBreath API

Base URL: `https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com`

All bodies are JSON. CORS allows any origin, methods `GET, POST, OPTIONS`,
header `content-type`. Errors return 4xx/5xx with `{"error": "<message>"}`.

## GET /health — live

```json
200 {"ok": true, "service": "secondbreath", "lastAuditRun": null}
```

`lastAuditRun` is an ISO-8601 UTC string once the audit pipeline has run,
`null` before that. A stale audit is reported in the body, never as a non-200.

## POST /fit — planned, shape may change

Fingerprints a room's ventilation rate from a CO2 time series.

Request:
```json
{
  "csv": "timestamp,co2_ppm\n2025-10-01T09:00:00Z,812\n...",
  "outdoorPpm": 420,
  "volumeM3": 850
}
```
`outdoorPpm` and `volumeM3` are optional. Without `outdoorPpm` the solver
estimates a baseline from the data.

Response:
```json
{
  "ach": 0.88,
  "achRange": [0.71, 1.04],
  "confident": true,
  "outdoorPpm": 420,
  "segmentsFound": 41,
  "segmentsUsed": 34,
  "readingsDropped": 12,
  "peakPpm": 4957,
  "peakRebreathedFraction": 0.119,
  "notes": ["12 readings below outdoor level were dropped"]
}
```
`confident: false` means the frontend must show the number as uncertain.
`achRange` is the spread across used decay segments. `ach` is the median.

## POST /predict — planned, shape may change

Forward model for a planned session in a fingerprinted room.

Request:
```json
{
  "ach": 0.88,
  "volumeM3": 850,
  "occupants": 60,
  "durationMin": 90,
  "outdoorPpm": 420,
  "startPpm": 420
}
```

Response:
```json
{
  "series": [{"minute": 0, "ppm": 420, "rebreathedFraction": 0.0}, "..."],
  "peakPpm": 2380,
  "peakRebreathedFraction": 0.052,
  "oneBreathIn": 19
}
```
`series` is one point per minute. `oneBreathIn` is `round(1 / peakRebreathedFraction)`.
