"""
SecondBreath -- core ventilation maths.

Pure Python, zero dependencies (no numpy), so `sam build` works without Docker
and the Lambda package stays tiny.

Three things live here:

  1. fit_decays()      -- inverse problem: given a CO2 time series, recover the
                          room's air-change rate (ACH) from exponential decay
                          segments. This is the "room fingerprint".
  2. predict()         -- forward problem: given a fingerprinted room and a
                          planned session, predict CO2, rebreathed fraction and
                          the maximum occupancy that stays under a threshold.
  3. rebreathed_*()    -- Rudnick & Milton (2003): the fraction of inhaled air
                          previously exhaled by someone else in the room.

Science notes
-------------
Mass balance for a well-mixed room:

    V dC/dt = N * G - Q * (C - C_out)

    V     room volume                      (m^3)
    C     indoor CO2                       (ppm)
    C_out outdoor CO2, ~420 ppm today      (ppm)
    N     occupants
    G     CO2 generation per person        (m^3/h)
    Q     outdoor air flow                 (m^3/h),  lambda = Q / V  (ACH, 1/h)

With nobody in the room (N = 0) this reduces to exponential decay:

    C(t) = C_out + (C_0 - C_out) * exp(-lambda * t)

so ln(C - C_out) is linear in t with slope -lambda. That is the standard
tracer-gas decay method for estimating air-change rates.

Rebreathed fraction (Rudnick & Milton 2003):

    f = (C - C_out) / C_exhaled,   C_exhaled ~ 38,000 ppm (physiological constant)

f is the share of each inhaled breath that has already been through someone
else's lungs. It is a ventilation/exposure metric, NOT an infection
probability -- see the caveats in README terms.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Iterable, NamedTuple, Sequence

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Typical present-day outdoor CO2 (ppm). Override per site where known.
OUTDOOR_PPM_DEFAULT = 420.0

#: CO2 volume fraction of exhaled breath (ppm). Rudnick & Milton 2003.
EXHALED_PPM = 38_000.0

#: CO2 generation per person (m^3/h) by activity. Seated, light office work
#: is ~0.005 L/s = 0.018 m^3/h per person for a typical adult.
GENERATION_M3H = {
    "seated_quiet": 0.0145,
    "seated_speaking": 0.018,
    "light_activity": 0.026,
    "moderate_activity": 0.038,
}

#: Predicted session peak (ppm) above which predict() flags its result.
#: 5,000 ppm is an exposure limit, not a statement about model validity: it is
#: OSHA's permissible exposure limit as an 8-hour time-weighted average, and
#: ACGIH's threshold limit value (TWA), which also sets a 30,000 ppm short-term
#: exposure limit. We use it as our ceiling for two reasons. Above it the
#: useful answer is "leave the room", not a number. And it is above what our
#: own data says is typical: every room's p95 during teaching hours is below
#: it (highest 3,892 ppm, School 14), and so is the lecture halls' highest
#: reading (4,957 ppm, Hall B). Five of the 40 rooms have single raw readings
#: above it, up to 7,950 ppm, all from uncleaned school sensors
#: (analysis/audit.json).
VALIDATED_MAX_PPM = 5_000.0

#: Least room volume per occupant (m^3) accepted as input. A judgment call:
#: a sanity floor chosen by us, not taken from any source. It exists only to
#: reject input that can't be real (10,000 people in 363 m^3) and is never
#: used to estimate how many people a room holds. It is deliberately 10x looser
#: than the audit's MIN_M3_PER_PERSON = 2.0 (analysis/METHOD.md 5.5), which
#: bounds how densely a seated lecture hall can be packed. This one only turns
#: away the physically impossible. Dense but possible sessions get through and
#: are then judged by VALIDATED_MAX_PPM on their peak.
MIN_INPUT_M3_PER_PERSON = 0.2


# ---------------------------------------------------------------------------
# 1. Rebreathed fraction
# ---------------------------------------------------------------------------

def rebreathed_fraction(co2_ppm: float, outdoor_ppm: float = OUTDOOR_PPM_DEFAULT) -> float:
    """Share of inhaled air previously exhaled by another occupant (0..1).

    Capped at 1.0: a breath cannot be more than entirely exhaled air, so any
    concentration above C_out + EXHALED_PPM comes from a model pushed past its
    physics, not from a real room.
    """
    return min(1.0, max(0.0, (co2_ppm - outdoor_ppm) / EXHALED_PPM))


def one_breath_in(co2_ppm: float, outdoor_ppm: float = OUTDOOR_PPM_DEFAULT) -> float:
    """Human-readable inverse: '1 breath in N'. inf when at outdoor level."""
    f = rebreathed_fraction(co2_ppm, outdoor_ppm)
    return math.inf if f <= 0 else 1.0 / f


# ---------------------------------------------------------------------------
# 2. Inverse problem: fit the room's air-change rate from a CO2 series
# ---------------------------------------------------------------------------

class DecayFit(NamedTuple):
    start: datetime
    end: datetime
    ach: float          # fitted air changes per hour (1/h)
    r2: float           # goodness of fit on ln(C - C_out)
    minutes: float
    points: int
    co2_start: float
    co2_end: float


def _linreg(xs: Sequence[float], ys: Sequence[float]) -> tuple[float, float, float]:
    """Return (slope, intercept, r2). Assumes len(xs) == len(ys) >= 2."""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return 0.0, my, 0.0
    slope = sxy / sxx
    intercept = my - slope * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, intercept, r2


def fit_decays(
    series: Iterable[tuple[datetime, float]],
    outdoor_ppm: float = OUTDOOR_PPM_DEFAULT,
    min_start_ppm: float = 700.0,
    min_points: int = 6,
    min_minutes: float = 20.0,
    max_gap_seconds: float = 600.0,
    min_headroom_ppm: float = 60.0,
    min_r2: float = 0.90,
    ach_bounds: tuple[float, float] = (0.05, 20.0),
) -> list[DecayFit]:
    """Find falling CO2 segments and fit an air-change rate to each.

    A decay segment starts once CO2 is clearly elevated (``min_start_ppm``) and
    continues while readings keep falling, stay meaningfully above outdoor
    (``min_headroom_ppm``), and arrive without a long gap.

    Only fits that are long enough, dense enough, well-described by a single
    exponential (``min_r2``) and physically plausible (``ach_bounds``) are kept.
    Everything else is discarded rather than reported with a caveat -- a bad
    fit is not weak evidence, it is no evidence.
    """
    data = sorted(series)
    fits: list[DecayFit] = []
    i, n = 0, len(data)

    while i < n - 1:
        if data[i][1] < min_start_ppm:
            i += 1
            continue

        seg = [data[i]]
        j = i
        while j + 1 < n:
            t_next, c_next = data[j + 1]
            t_cur, c_cur = data[j]
            if (t_next - t_cur).total_seconds() > max_gap_seconds:
                break
            if c_next >= c_cur - 1.0:                      # stopped falling
                break
            if c_next <= outdoor_ppm + min_headroom_ppm:   # too close to outdoor
                break
            j += 1
            seg.append(data[j])

        minutes = (seg[-1][0] - seg[0][0]).total_seconds() / 60.0 if len(seg) > 1 else 0.0
        if len(seg) >= min_points and minutes >= min_minutes:
            t0 = seg[0][0]
            xs = [(t - t0).total_seconds() / 3600.0 for t, _ in seg]
            ys = [math.log(c - outdoor_ppm) for _, c in seg]
            slope, _, r2 = _linreg(xs, ys)
            ach = -slope
            if r2 >= min_r2 and ach_bounds[0] < ach < ach_bounds[1]:
                fits.append(
                    DecayFit(
                        start=seg[0][0], end=seg[-1][0], ach=ach, r2=r2,
                        minutes=minutes, points=len(seg),
                        co2_start=seg[0][1], co2_end=seg[-1][1],
                    )
                )
        i = max(j + 1, i + 1)

    return fits


class Fingerprint(NamedTuple):
    ach_median: float
    ach_p25: float
    ach_p75: float
    n_fits: int
    total_minutes: float

    @property
    def confident(self) -> bool:
        """Enough independent fits, and they agree closely enough to quote."""
        if self.n_fits < 5 or self.ach_median <= 0:
            return False
        spread = (self.ach_p75 - self.ach_p25) / self.ach_median
        return spread < 0.8


def fingerprint(fits: Sequence[DecayFit]) -> Fingerprint | None:
    """Summarise many decay fits into one room fingerprint.

    Median rather than mean: a single mis-detected segment (a window thrown
    open, a sensor gap) should not move the headline number.
    """
    if not fits:
        return None
    vals = sorted(f.ach for f in fits)
    n = len(vals)

    def q(p: float) -> float:
        idx = min(n - 1, max(0, int(round(p * (n - 1)))))
        return vals[idx]

    median = (vals[n // 2] if n % 2 else 0.5 * (vals[n // 2 - 1] + vals[n // 2]))
    return Fingerprint(
        ach_median=median, ach_p25=q(0.25), ach_p75=q(0.75),
        n_fits=n, total_minutes=sum(f.minutes for f in fits),
    )


# ---------------------------------------------------------------------------
# 2b. Inverse problem, occupied phase: fit ACH *while people are in the room*
# ---------------------------------------------------------------------------
#
# Decay fits measure the room as it empties. If the air handler stops with
# occupancy, that is an infiltration rate, not delivered ventilation -- a fair
# and fatal objection to any claim about what occupants actually breathe.
#
# The buildup phase answers it. During occupancy:
#
#     C(t) = C_0 * exp(-lambda*t) + C_ss * (1 - exp(-lambda*t))
#
# Two unknowns, but they are separable: the *curvature* of the rise carries
# lambda, the *asymptote* carries the CO2 source. For any fixed lambda the
# model is linear in C_ss, so we search lambda on a log grid and solve C_ss
# in closed form at each step.
#
# lambda is only identifiable if the curve actually bends. A rise still far
# from steady state looks linear and fits almost as well at many lambdas, so
# every fit carries a profile band: the range of lambda whose sum of squared
# error is within 10% of the best. Wide band, no claim.


class BuildupFit(NamedTuple):
    start: datetime
    end: datetime
    ach: float              # fitted air changes per hour
    ach_lo: float           # profile band, lower
    ach_hi: float           # profile band, upper
    steady_state_ppm: float
    implied_occupants: float
    r2: float
    minutes: float
    points: int
    co2_start: float
    co2_end: float

    @property
    def identifiable(self) -> bool:
        """Did the curve bend enough to pin lambda down?"""
        return self.ach_lo > 0 and (self.ach_hi / self.ach_lo) < 3.0


def _fit_single_buildup(
    seg: Sequence[tuple[datetime, float]],
    volume_m3: float,
    activity: str,
    outdoor_ppm: float,
    ach_bounds: tuple[float, float],
    profile_tolerance: float = 1.10,
) -> BuildupFit | None:
    t0, c0 = seg[0]
    xs = [(t - t0).total_seconds() / 3600.0 for t, _ in seg]
    ys = [c for _, c in seg]

    best: tuple[float, float, float] | None = None   # (lambda, sse, c_ss)
    grid: list[tuple[float, float]] = []             # (lambda, sse)

    lam = ach_bounds[0]
    while lam <= ach_bounds[1]:
        num = den = 0.0
        for x, y in zip(xs, ys):
            decayed = math.exp(-lam * x)
            a = 1.0 - decayed
            num += a * (y - c0 * decayed)
            den += a * a
        if den > 1e-12:
            c_ss = num / den
            sse = 0.0
            for x, y in zip(xs, ys):
                decayed = math.exp(-lam * x)
                sse += (y - (c0 * decayed + c_ss * (1.0 - decayed))) ** 2
            grid.append((lam, sse))
            if best is None or sse < best[1]:
                best = (lam, sse, c_ss)
        lam *= 1.03

    if best is None:
        return None
    lam, sse, c_ss = best

    # A steady state above exhaled-breath concentration is not a room, it is a
    # failed fit on a curve that never bent. Reject rather than report.
    if c_ss <= outdoor_ppm or c_ss > EXHALED_PPM / 4:
        return None

    n = len(seg)
    mean_y = sum(ys) / n
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    r2 = 1.0 - sse / ss_tot if ss_tot > 0 else 0.0

    band = [l for l, s in grid if s <= sse * profile_tolerance]
    lo, hi = (min(band), max(band)) if band else (lam, lam)

    # Source strength implied by the fitted asymptote, converted to people.
    source_m3h = (c_ss - outdoor_ppm) / 1e6 * lam * volume_m3
    occupants = source_m3h / GENERATION_M3H[activity]

    return BuildupFit(
        start=seg[0][0], end=seg[-1][0], ach=lam, ach_lo=lo, ach_hi=hi,
        steady_state_ppm=c_ss, implied_occupants=occupants, r2=r2,
        minutes=(seg[-1][0] - seg[0][0]).total_seconds() / 60.0,
        points=n, co2_start=c0, co2_end=seg[-1][1],
    )


def fit_buildups(
    series: Iterable[tuple[datetime, float]],
    volume_m3: float,
    activity: str = "seated_quiet",
    outdoor_ppm: float = OUTDOOR_PPM_DEFAULT,
    min_rise_ppm: float = 250.0,
    min_points: int = 8,
    min_minutes: float = 35.0,
    max_gap_seconds: float = 600.0,
    dip_tolerance_ppm: float = 40.0,
    min_r2: float = 0.95,
    ach_bounds: tuple[float, float] = (0.05, 15.0),
) -> list[BuildupFit]:
    """Fit ventilation from rising (occupied) CO2 segments.

    Small dips are tolerated (``dip_tolerance_ppm``) because real sensor traces
    are noisy and a door opening briefly should not end a segment.
    """
    data = sorted(series)
    out: list[BuildupFit] = []
    i, n = 0, len(data)

    while i < n - 1:
        seg = [data[i]]
        j = i
        while j + 1 < n:
            (t_cur, c_cur), (t_next, c_next) = data[j], data[j + 1]
            if (t_next - t_cur).total_seconds() > max_gap_seconds:
                break
            if c_next < c_cur - dip_tolerance_ppm:
                break
            j += 1
            seg.append(data[j])

        minutes = (seg[-1][0] - seg[0][0]).total_seconds() / 60.0 if len(seg) > 1 else 0.0
        if (
            len(seg) >= min_points
            and minutes >= min_minutes
            and seg[-1][1] - seg[0][1] >= min_rise_ppm
        ):
            fit = _fit_single_buildup(seg, volume_m3, activity, outdoor_ppm, ach_bounds)
            if fit and fit.r2 >= min_r2:
                out.append(fit)
        i = max(j + 1, i + 1)

    return out


# ---------------------------------------------------------------------------
# 3. Forward problem: predict a planned session
# ---------------------------------------------------------------------------

class Sample(NamedTuple):
    minute: float
    co2_ppm: float
    rebreathed_fraction: float


class Prediction(NamedTuple):
    curve: list[Sample]
    peak_ppm: float
    peak_one_in: float
    mean_rebreathed_fraction: float
    minutes_above_1000: float
    steady_state_ppm: float
    # False when peak_ppm > VALIDATED_MAX_PPM. On the peak, not the asymptote:
    # the peak is the number a user sees, and a short session that never gets
    # near its steady state shouldn't be flagged for it.
    within_validated_range: bool


def predict(
    volume_m3: float,
    ach: float,
    occupants: int,
    minutes: float,
    activity: str = "seated_speaking",
    start_ppm: float | None = None,
    outdoor_ppm: float = OUTDOOR_PPM_DEFAULT,
    step_minutes: float = 1.0,
) -> Prediction:
    """Predict the CO2 curve for a planned session in a fingerprinted room.

    Closed-form solution of the mass balance with constant occupancy:

        C(t) = C_ss + (C_0 - C_ss) * exp(-lambda * t)
        C_ss = C_out + (N * G) / (lambda * V)   [in ppm]
    """
    if volume_m3 <= 0 or ach <= 0:
        raise ValueError("volume_m3 and ach must be positive")

    g = GENERATION_M3H.get(activity)
    if g is None:
        raise ValueError(f"unknown activity {activity!r}; try {sorted(GENERATION_M3H)}")

    c0 = outdoor_ppm if start_ppm is None else start_ppm
    # N*G is m^3/h of pure CO2; divide by air flow (ach*V) and convert to ppm.
    rise = (occupants * g) / (ach * volume_m3) * 1e6
    c_ss = outdoor_ppm + rise

    curve: list[Sample] = []
    t = 0.0
    above_1000 = 0.0
    while t <= minutes + 1e-9:
        c = c_ss + (c0 - c_ss) * math.exp(-ach * (t / 60.0))
        curve.append(Sample(t, c, rebreathed_fraction(c, outdoor_ppm)))
        if c > 1000.0:
            above_1000 += step_minutes
        t += step_minutes

    peak = max(s.co2_ppm for s in curve)
    mean_f = sum(s.rebreathed_fraction for s in curve) / len(curve)
    return Prediction(
        curve=curve,
        peak_ppm=peak,
        peak_one_in=one_breath_in(peak, outdoor_ppm),
        mean_rebreathed_fraction=mean_f,
        minutes_above_1000=min(above_1000, minutes),
        steady_state_ppm=c_ss,
        within_validated_range=peak <= VALIDATED_MAX_PPM,
    )


def max_occupancy(
    volume_m3: float,
    ach: float,
    minutes: float,
    limit_ppm: float = 1000.0,
    activity: str = "seated_speaking",
    outdoor_ppm: float = OUTDOOR_PPM_DEFAULT,
    cap: int = 500,
) -> int:
    """Largest occupancy whose predicted peak stays at or under ``limit_ppm``."""
    best = 0
    for n in range(1, cap + 1):
        p = predict(volume_m3, ach, n, minutes, activity, None, outdoor_ppm)
        if p.peak_ppm > limit_ppm:
            break
        best = n
    return best


def required_ach(
    volume_m3: float,
    occupants: int,
    limit_ppm: float = 1000.0,
    activity: str = "seated_speaking",
    outdoor_ppm: float = OUTDOOR_PPM_DEFAULT,
) -> float:
    """Steady-state air-change rate needed to hold CO2 at ``limit_ppm``."""
    g = GENERATION_M3H[activity]
    headroom = limit_ppm - outdoor_ppm
    if headroom <= 0:
        raise ValueError("limit_ppm must exceed outdoor_ppm")
    return (occupants * g * 1e6) / (headroom * volume_m3)


# ---------------------------------------------------------------------------
# Self-test: recover a known ACH from a synthetic curve
# ---------------------------------------------------------------------------

def _self_test() -> None:
    true_ach = 1.35
    start = datetime(2026, 9, 28, 14, 0, 0)
    c0, c_out = 2400.0, OUTDOOR_PPM_DEFAULT

    synthetic = [
        (start + timedelta(minutes=m),
         c_out + (c0 - c_out) * math.exp(-true_ach * (m / 60.0)))
        for m in range(0, 121, 5)
    ]

    fits = fit_decays(synthetic)
    assert len(fits) == 1, f"expected one decay segment, got {len(fits)}"
    got = fits[0].ach
    assert abs(got - true_ach) < 0.01, f"recovered {got:.4f}, expected {true_ach}"
    assert fits[0].r2 > 0.999

    fp = fingerprint(fits)
    assert fp is not None and abs(fp.ach_median - true_ach) < 0.01

    # Rebreathed fraction sanity: 1400 ppm is roughly 1 breath in 39.
    assert 38 < one_breath_in(1400.0) < 40
    # ...and never more than the whole breath, however high the input.
    assert rebreathed_fraction(OUTDOOR_PPM_DEFAULT + EXHALED_PPM) == 1.0
    assert rebreathed_fraction(1e6) == 1.0 and one_breath_in(1e6) == 1.0

    # Forward model: the flag follows the session peak. An ordinary class is in
    # range; a packed room over 90 minutes is not, and its fractions stay <= 1;
    # the same crowd for 5 minutes peaks under the ceiling and is not flagged
    # even though its steady state is far above it.
    assert predict(363.0, 0.74, 60, 90, "seated_quiet").within_validated_range
    huge = predict(363.0, 0.74, 1500, 90)
    assert not huge.within_validated_range
    assert all(s.rebreathed_fraction <= 1.0 for s in huge.curve)
    brief = predict(363.0, 0.74, 1000, 5)
    assert brief.peak_ppm <= VALIDATED_MAX_PPM < brief.steady_state_ppm
    assert brief.within_validated_range

    # Forward model: steady state must match the closed form.
    p = predict(volume_m3=100.0, ach=1.0, occupants=5, minutes=600)
    expected_ss = OUTDOOR_PPM_DEFAULT + (5 * GENERATION_M3H["seated_speaking"]) / (1.0 * 100.0) * 1e6
    assert abs(p.steady_state_ppm - expected_ss) < 1e-6
    assert abs(p.curve[-1].co2_ppm - expected_ss) < 1.0

    # Round trip: required_ach should hold a full room at the limit.
    n = 20
    need = required_ach(volume_m3=200.0, occupants=n, limit_ppm=1000.0)
    long_run = predict(200.0, need, n, minutes=1200)
    assert abs(long_run.steady_state_ppm - 1000.0) < 1.0

    # max_occupancy must be monotone in the limit.
    assert max_occupancy(200.0, 2.0, 60, 1400.0) >= max_occupancy(200.0, 2.0, 60, 1000.0)

    # --- buildup round trip: simulate a known room, recover its parameters ---
    true_ach, true_people, vol = 0.80, 30, 363.0
    sim = predict(vol, true_ach, true_people, minutes=150, activity="seated_quiet",
                  start_ppm=900.0)
    rising = [
        (start + timedelta(minutes=int(s.minute)), s.co2_ppm)
        for s in sim.curve
        if int(s.minute) % 5 == 0
    ]
    bfits = fit_buildups(rising, volume_m3=vol, activity="seated_quiet")
    assert len(bfits) == 1, f"expected one buildup segment, got {len(bfits)}"
    b = bfits[0]
    assert b.identifiable, f"band too wide: {b.ach_lo:.2f}-{b.ach_hi:.2f}"
    assert abs(b.ach - true_ach) / true_ach < 0.06, f"recovered ACH {b.ach:.3f}"
    assert abs(b.implied_occupants - true_people) / true_people < 0.10, (
        f"recovered occupancy {b.implied_occupants:.1f}"
    )
    assert b.ach_lo <= b.ach <= b.ach_hi

    # A short, still-linear rise must NOT be reported as identifiable.
    short = [(t, c) for t, c in rising if (t - start).total_seconds() / 60 <= 40]
    sfits = fit_buildups(short, volume_m3=vol, activity="seated_quiet",
                         min_minutes=35, min_rise_ppm=100)
    if sfits:
        assert not sfits[0].identifiable or sfits[0].ach_hi / sfits[0].ach_lo < 3.0

    print("all self-tests passed")


if __name__ == "__main__":
    _self_test()