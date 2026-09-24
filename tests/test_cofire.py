"""Co-firing model: glass-ceramic viscous sintering, crystallisation kinetics and bilayer mechanics."""
import numpy as np
import pytest

from cupola.cofire.glass import GlassSetup, dsc_peak, calibrate_kp, myega_log10_eta
from cupola.cofire.run import cofire_scenario, glass_view
from cupola.cycle import Cycle, Segment
from cupola.constants import T0C
from cupola.simulate import simulate


def test_myega_passes_through_tg():
    assert myega_log10_eta(1053.15, 1053.15, 45.0) == pytest.approx(12.0)
    # fragility is the slope d log10(eta) / d (Tg/T) at Tg
    x = np.array([0.999, 1.001])
    y = myega_log10_eta(1053.15 / x, 1053.15, 45.0)
    assert (y[1] - y[0]) / (x[1] - x[0]) == pytest.approx(45.0, rel=1e-3)


@pytest.mark.parametrize("n", [1.0, 2.0, 3.0])
def test_dsc_peak_lands_on_parameter(n):
    Tp, E = 960.0 + T0C, 450e3
    assert dsc_peak(calibrate_kp(Tp, E, n), Tp, E, n) == pytest.approx(Tp, abs=0.05)


def test_isothermal_glass_densification_matches_closed_form():
    """Open-porosity SOVS with a Newtonian matrix: d theta/dt = -9 gamma theta / (4 r eta)."""
    s = glass_view(cofire_scenario(char_yield=0.0, gc_Tp_cryst_C=1100.0, gc_E_cryst=700.0))
    T_h = 830.0
    cyc = Cycle([Segment(500.0, 5.0, 0.5, note="burn off"), Segment(T_h, 10.0, 3.0, note="hold")])
    r = simulate(s, cyc, N=6, rtol=1e-5, setup_cls=GlassSetup)
    su = GlassSetup(s)
    t = r.t_h * 3600.0
    hold0 = t[np.argmax(r.series["Tset"] >= T_h - 1e-6)] + 1200.0            # let the slab equilibrate
    th = 1.0 - r.series["rho_mean"]
    i0 = np.searchsorted(t, hold0)
    sel = (t >= hold0) & (r.series["rho_mean"] < 0.85)
    assert sel.sum() > 10
    Tm = 0.5 * (r.series["T_center"] + r.series["T_surface"]) + T0C
    rate = 9.0 * su.gamma / (4.0 * su.r_s * su.eta0(Tm, np.full_like(Tm, 1e-9)))
    ts, rs = t[sel], rate[sel]
    I = np.concatenate([[0.0], np.cumsum(0.5 * (rs[1:] + rs[:-1]) * np.diff(ts))])
    th_ref = th[i0] * np.exp(-I)
    assert np.max(np.abs(th[sel] - th_ref)) < 2e-3
    assert th[sel][-1] < th[i0] - 0.1                                        # it did densify


def test_bilayer_curvature_rate_matches_timoshenko():
    import importlib.util, pathlib
    spec = importlib.util.spec_from_file_location(
        "vb", pathlib.Path(__file__).resolve().parents[1] / "scripts" / "paper3" / "verify_bilayer.py")
    vb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vb)
    r = vb.case(0.3)
    assert abs(r["rel_err"]) < 0.02
