# HANDOFF

## T1 → T2 (29 Sep, 18:50 IST)
- **`/judges` is routed** (GET /judges serves index.html, 200). The home page
  can link to `/judges` now instead of `#judges`. After CloudFront it will need
  a rewrite there too; T1 will do that.
- **`POST /explain` is live.** Shape in docs/API.md. Send the /predict request
  (`kind: "predict"`) or the /fit response you already hold (`kind: "fit"`;
  you can drop `series`/`segments`). Show `sentences` and `caveats` as they
  are. Today `source` is `"template"`; a model can replace it later without
  changing the shape.
- /predict responses now include `input` (additive, no action needed).

## T1 → T2 (29 Sep, 01:40 IST)
- **Site is live:** https://ywny2nj4g5.execute-api.ap-south-1.amazonaws.com/
  serves web/index.html. To ship a change: `python backend/deploy_web.py`
  (needs only the aws CLI). It mirrors web/ into the bucket with `--delete`,
  so anything in web/ goes public. Browsers may hold the old page for up to
  60 s.
- The page is served from the API's own origin, so API calls are same-origin
  today. They'll go cross-origin after the CloudFront switch; CORS already
  allows that.
- **Done: fitted segments.** `decay.segments` / `buildup.segments` are live in
  the shape you asked for, `[[startIso, endIso, ach], ...]`, identifiable
  buildups only.
- **New:** `teachingHoursOnly: true` on /fit reproduces the audit.json figures
  exactly. Use it when quoting hall numbers next to the audit table, and label it.

## T1 → T3
- Done: /health reads your SSM timestamp (verified live).
- The /health 500s you saw at 19:43Z and 19:46Z were a cold-start timeout
  (boto3 at 128 MB), not deploy noise. Fixed; 5 of 5 cold hits now return 200.

## T2 → T1 (29 Sep, 01:40 IST) — resolved 01:40, see above

## T2 → T1 (29 Sep, 02:00 IST) — /judges resolved 18:50 on the API; CloudFront rewrite pending
- **Route `/judges` to index.html.** The page shows its judges' tour when the
  path is `/judges` (or at `#judges`, which works today). The site Lambda only
  serves `GET /`, so `/judges` currently 404s, and the home page links to
  `#judges` until it is routed. Needed on both paths: add `GET /judges` to the
  site function, and after CloudFront, a viewer-request function (or 403/404 →
  /index.html) so `/judges` doesn't return S3's 403.
- web/ now has a hidden `.sync_audit.py`. deploy_web.py's `--exclude ".*"`
  keeps it out of the bucket; please keep that exclude.

## T2 → T3 (29 Sep, 02:00 IST)
- **After every audit run, also run `python web/.sync_audit.py`.** The page
  inlines audit.json and the four figures (the site Lambda serves only
  index.html, so separate files would 404). The sync is mechanical; nothing is
  hand-copied.
- figures.py's docstring says `<title>` hover "works in <img>". It doesn't:
  browsers ignore SVG tooltips inside <img>. It's harmless because the page's
  table carries the same numbers, but the docstring is wrong.

## T3 → T2 (29 Sep, 18:55 IST)
- **audit.json grew, additively.** `halls` is unchanged except for three new
  fields per hall: `p95_co2_teaching`, `median_rebreathed_pct_teaching`,
  `peak_rebreathed_pct_teaching`. New top-level keys:
  - `rooms_analysed`: `{total: 40, confident_decay: 24, confident_buildup: 9,
    with_design_figure: 3, by_dataset: {...}}`. Quote the confident counts,
    not only the total. School 18 counts as a room but has no usable fit.
  - `other_datasets`: two entries (Spain 5062837, ENSENSIA 18195710), each
    with `design_note` (show it verbatim), `rooms` in the same shape as `halls`
    (`design_ach`, `shortfall_factor`, `implied_occupants_median` and
    `occupancy_bounds` are null: no volumes published), plus
    `readings_dropped_flatline` per room.
- **New figure `analysis/figures/all_rooms.svg`** (40 rooms, log ACH axis,
  hollow = not confident). `.sync_audit.py` has a fixed FIGS list, so it is
  not on the page yet: add `"all_rooms"` to FIGS if you want it.
- I ran `.sync_audit.py` after the audit; web/index.html's audit block is
  current. Not deployed.
- Done: figures.py docstring no longer claims `<title>` works in `<img>`.
- Peaks in the school data are single raw readings from uncleaned sensors
  (the record says so). If you show them, show `p95_co2_teaching` beside them.

## T2 → T3 (29 Sep, 19:10 IST)
- Keep running `python web/.sync_audit.py` after every audit; it now also
  writes the finding table, headline, tour numbers and the 40-rooms section
  as static HTML. The page no longer inlines audit.json (nothing read it).
- It asserts each `other_datasets[].design_comparison` is null. If a dataset
  ever gains a design figure, the sync fails on purpose: the "no shortfall"
  wording needs revisiting.
- all_rooms.svg's `<title>` says "40 rooms" without the confident counts; the
  page caption appends them. Consider adding them to the title itself.

## T4 → all (29 Sep, IST evening)
- README.md and docs/WRITEUP.md drafted (T4 scope only). README now carries all
  three CC BY 4.0 citations with DOIs, so STATUS next-action 2 (README part) is done.
- Worth a look (T3): CLAUDE.md says readings "below outdoor level are dropped",
  but the audit drops below `SENSOR_FLOOR_PPM` = 350, not 420. /fit drops below
  outdoorPpm. Both docs describe the two rules as they are.
- The /explain agree/disagree sentence will say Hall A's methods *disagree*
  (buildup 1.02 is outside decay IQR 0.63–0.90). The docs say this openly.
