"""Run from backend/: python -m unittest discover tests  (after python build.py)."""
import hashlib
import json
import math
import re
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
ROOT_VENT = BACKEND.parent / "ventilation.py"
sys.path.insert(0, str(BACKEND / "src"))

import api  # noqa: E402


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def call(handler, body):
    raw = body if isinstance(body, str) else json.dumps(body)
    r = handler({"body": raw, "isBase64Encoded": False}, None)
    return r["statusCode"], json.loads(r["body"])


class CopiesMatchRoot(unittest.TestCase):
    def test_every_codeuri_copy_matches_root(self):
        template = (BACKEND / "template.yaml").read_text()
        uris = set(re.findall(r"CodeUri:\s*(\S+)", template))
        self.assertTrue(uris)
        # The built artifacts are what actually deploy, so check those too.
        copies = [BACKEND / u / "ventilation.py" for u in uris]
        copies += list((BACKEND / ".aws-sam" / "build").glob("*/ventilation.py"))
        for c in copies:
            self.assertTrue(c.exists(), f"{c} missing; run python build.py")
            self.assertEqual(sha(c), sha(ROOT_VENT), f"{c} drifted from root ventilation.py")


class Fit(unittest.TestCase):
    def test_recovers_known_decay_rate_from_csv(self):
        true_ach, c0, out = 1.35, 2400.0, 420.0
        t0 = datetime(2026, 9, 28, 14)
        rows = ["recorded;CO2 ppm"] + [
            f"{(t0 + timedelta(minutes=m)).isoformat()};{out + (c0 - out) * math.exp(-true_ach * m / 60):.2f}"
            for m in range(0, 121, 5)
        ] + [f"{(t0 + timedelta(minutes=125)).isoformat()};300"]  # drifted reading
        status, r = call(api.fit, {"csv": "\n".join(rows), "volumeM3": 363})
        self.assertEqual(status, 200, r)
        self.assertAlmostEqual(r["decay"]["fingerprint"]["achMedian"], true_ach, delta=0.01)
        self.assertEqual(r["decay"]["fits"], 1)
        self.assertEqual(r["readingsDroppedBelowOutdoor"], 1)
        self.assertEqual(r["peakPpm"], 2400.0)

    def test_segments_and_teaching_hours_filter(self):
        def decay_csv(t0):
            return "\n".join(["recorded;CO2 ppm"] + [
                f"{(t0 + timedelta(minutes=m)).isoformat()};{420 + 1980 * math.exp(-1.35 * m / 60):.2f}"
                for m in range(0, 121, 5)])
        weekday, saturday = datetime(2026, 9, 28, 14), datetime(2026, 10, 3, 14)
        for t0, teaching, expected in ((weekday, True, 1), (saturday, False, 1), (saturday, True, 0)):
            status, r = call(api.fit, {"csv": decay_csv(t0), "volumeM3": 363,
                                       "teachingHoursOnly": teaching})
            self.assertEqual(status, 200, r)
            self.assertEqual(len(r["decay"]["segments"]), expected, (t0, teaching))
        start, end, ach = call(api.fit, {"csv": decay_csv(weekday), "volumeM3": 363})[1]["decay"]["segments"][0]
        self.assertEqual(start, weekday.isoformat())
        self.assertAlmostEqual(ach, 1.35, delta=0.01)

    def test_oversize_rejected_with_413(self):
        status, r = call(api.fit, "x" * (api.MAX_BODY_BYTES + 1))
        self.assertEqual(status, 413)
        self.assertIn("limit", r["error"])

    def test_missing_co2_column_is_400(self):
        status, r = call(api.fit, {"csv": "time,temp\n2026-01-01T00:00,20", "volumeM3": 100})
        self.assertEqual(status, 400)
        self.assertIn("co2", r["error"])


class Predict(unittest.TestCase):
    def test_matches_closed_form_and_occupancy_is_monotone(self):
        status, r = call(api.predict, {"volumeM3": 100, "ach": 1, "occupants": 5, "minutes": 600})
        self.assertEqual(status, 200, r)
        expected_ss = 420 + 5 * 0.018 / 100 * 1e6
        self.assertAlmostEqual(r["steadyStatePpm"], expected_ss, places=6)
        self.assertAlmostEqual(r["peakOneBreathIn"], 38000 / (r["peakPpm"] - 420), places=6)
        self.assertLessEqual(r["maxOccupancy"]["1000"], r["maxOccupancy"]["1400"])

    def test_rejects_bad_values(self):
        for body in ({"volumeM3": 100, "ach": 0, "occupants": 5, "minutes": 60},
                     {"volumeM3": 100, "ach": 1, "occupants": True, "minutes": 60},
                     {"volumeM3": 100, "ach": 1, "occupants": 5, "minutes": 60, "activity": "x"}):
            self.assertEqual(call(api.predict, body)[0], 400, body)


class Explain(unittest.TestCase):
    def test_predict_sentences_carry_solver_numbers_rounded_unflatteringly(self):
        req = {"volumeM3": 363, "ach": 0.74, "occupants": 60, "minutes": 90, "activity": "seated_quiet"}
        status, r = call(api.explain, {"kind": "predict", "request": req})
        self.assertEqual(status, 200, r)
        p = call(api.predict, req)[1]
        text = " ".join(r["sentences"])
        self.assertEqual(r["facts"]["peakPpm"], p["peakPpm"])
        self.assertIn(f"{math.ceil(p['peakPpm']):,} ppm", text)            # ppm rounds up
        self.assertIn(f"one breath in {math.floor(p['peakOneBreathIn'])}", text)  # N rounds down
        self.assertIn(f"at most {p['maxOccupancy']['1000']} people", text)

    def test_fit_uncertain_is_said_and_unconfident_rates_never_headline(self):
        fp = lambda med, p25, p75, n, ok: {"achMedian": med, "achP25": p25, "achP75": p75,
                                           "nFits": n, "confident": ok}
        result = {"outdoorPpm": 420, "peakPpm": 4957, "readingsDroppedBelowOutdoor": 3,
                  "decay": {"fingerprint": fp(1.10, 0.47, 1.70, 323, False)},
                  "buildup": {"fingerprint": None, "discarded": 2}}
        status, r = call(api.explain, {"kind": "fit", "result": result})
        self.assertEqual(status, 200, r)
        text = " ".join(r["sentences"])
        self.assertIn("uncertain", text)
        self.assertIn("0.47 to 1.70", text)
        self.assertIn("one breath in 8", text)   # CLAUDE.md: Hall B peak
        self.assertIn("discarded", text)
        self.assertIn("leak rate", text)         # decay alone is flagged

    def test_rejects_unknown_kind_and_bad_numbers(self):
        self.assertEqual(call(api.explain, {"kind": "x"})[0], 400)
        self.assertEqual(call(api.explain, {"kind": "fit", "result": {"outdoorPpm": 420, "peakPpm": "big"}})[0], 400)


if __name__ == "__main__":
    unittest.main()
