"""Checks for the school-dataset loaders: python analysis/test_loaders.py"""
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_lecture_halls import _drop_flatlines, load_spain  # noqa: E402

t0 = datetime(2024, 1, 8, 9)
step = timedelta(minutes=10)

# 13 identical readings over 2 h is a dead sensor; 11 over 110 min is not.
dead = [(t0 + i * step, 658.0) for i in range(13)]
alive = [(t0 + i * step, 700.0) for i in range(11)]
assert _drop_flatlines(dead) == ([], 13)
assert _drop_flatlines(alive) == (alive, 0)
# Two equal readings either side of a 3 h gap are not a flatline.
pair = [(t0, 500.0), (t0 + timedelta(hours=3), 500.0)]
assert _drop_flatlines(pair) == (pair, 0)

# Sant Miquel's quoted-line layout, UTC in, Madrid local (CEST, +2) out;
# the sub-floor reading is dropped and counted.
raw = ('"published_at,""date_time"",""co2"",""sensor_id"""\n'
       '"2021-05-03T07:00:05.241Z,""2021-05-03T07:00:05"",820,"" CO2_06"""\n'
       '"2021-05-03T07:05:05.348Z,""2021-05-03T07:05:05"",301,"" CO2_06"""\n')
with tempfile.TemporaryDirectory() as d:
    f = Path(d) / "CEIP_SantMiquel_Vilafames.csv"
    f.write_text(raw, encoding="utf-8")
    rooms = load_spain(f, ZoneInfo("Europe/Madrid"))
assert rooms == {"Vilafames CO2_06": ([(datetime(2021, 5, 3, 9, 0, 5, 241000), 820.0)], 1, 0)}, rooms

print("loaders ok")
