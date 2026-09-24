import json
from pathlib import Path

import pytest

from cupola.calibrate import fit_f_eta, interrupted_cycle, synthetic_coupons
from cupola.cycle import Cycle
from cupola.params import defaults

BASE = Cycle.from_dict(json.loads((Path(__file__).resolve().parents[1] / "dashboard" / "data" /
                                   "synth_default_cycle.json").read_text()))


def test_interrupted_cycle_cuts_base_at_peak():
    c = interrupted_cycle(BASE, 950.0, 0.5)
    assert max(sg.T_end_C for sg in c.segments) == 950.0
    peak = [sg for sg in c.segments if sg.T_end_C == 950.0][0]
    assert peak.hold_h == 0.5 and peak.H2 > 0 and peak.dp_C > 0          # still in wet forming gas (phase B)
    assert c.segments[-1].T_end_C == 25.0
    hot = interrupted_cycle(BASE, 1080.0, 1.0)                             # above the base peak: extra ramp
    assert max(sg.T_end_C for sg in hot.segments) == 1080.0
    assert hot.duration_h() > BASE.duration_h() - 1.0


def test_fit_recovers_f_eta_from_noiseless_coupons():
    s = defaults()
    plan = [(1030.0, 0.5, "shrink_xy"), (1060.0, 2.0, "rho")]
    coupons = synthetic_coupons(s, BASE, 0.6, plan=plan, N=6)
    fit = fit_f_eta(s, BASE, coupons, N=6, xatol=0.03)
    assert fit["f_eta"] == pytest.approx(0.6, rel=0.05)
    assert fit["f_eta_lo"] < fit["f_eta"] < fit["f_eta_hi"]
