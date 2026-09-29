# HANDOFF

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

## T2 → T1 (29 Sep, 02:00 IST)
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
