"""T0 thermochemistry, parameter registry and material constants."""
import math

import numpy as np
import pytest

from cupola import thermo, params
from cupola.constants import T0C
from cupola.materials import Setup, kp_from_Tpeak, lognormal_sigma_from_span


# ------------------------------------------------------------------ thermochemistry
def test_cu2o_equilibrium_pO2_1000C():
    # ~5e-7 atm: 5.0-grade Ar/N2 (1-5 ppm O2) is OXIDISING to Cu at 1000 C
    p = thermo.pO2_eq_Cu_Cu2O(1000 + T0C)
    assert 3e-7 < p < 8e-7


def test_ibm_785C_setpoint_margin():
    # IBM's co-fired-Cu burnout setpoint H2O/H2 = 1e4 sits ~5.8x on the reducing side
    m = thermo.reducing_margin(1e4, 785 + T0C)
    assert 5.0 < m < 6.5


def test_boundary_values_match_research_table():
    assert thermo.h2o_h2_boundary_Cu(1000 + T0C) == pytest.approx(1.26e4, rel=0.02)
    assert thermo.h2o_h2_boundary_Cu(700 + T0C) == pytest.approx(1.28e5, rel=0.02)


def test_carbothermic_onset_76C():
    assert thermo.T_carbothermic_onset() - T0C == pytest.approx(75.6, abs=0.5)
    assert thermo.dG_carbothermic(400 + T0C) < 0


def test_steam_gasification_K_crosses_one_near_673C():
    assert thermo.K_steam_gasification(660 + T0C) < 1 < thermo.K_steam_gasification(690 + T0C)


def test_dewpoint_roundtrip():
    for td in (-40.0, -10.0, 0.5, 20.0, 60.0):
        x = thermo.x_h2o_from_dewpoint(td)
        assert thermo.dewpoint_from_x_h2o(x) == pytest.approx(td, abs=0.02)
    assert thermo.x_h2o_from_dewpoint(20.0) == pytest.approx(0.02308, rel=0.01)


def test_forming_gas_bubbler_is_strongly_reducing_everywhere():
    # 4 % H2, dew point +20 C: the Ellingham constraint is slack by >1e4 up to 1066 C
    r = thermo.x_h2o_from_dewpoint(20.0) / 0.04
    for tc in (300, 500, 800, 1066):
        assert thermo.reducing_margin(r, tc + T0C) > 1e4


def test_solidus_uses_solubility_not_eutectic_composition():
    assert thermo.T_solidus_Cu_O(0) - T0C == pytest.approx(1084.62, abs=0.01)
    assert thermo.T_solidus_Cu_O(80) - T0C == pytest.approx(1066.2, abs=0.01)
    # 500 ppm is far below the 0.39 wt% eutectic composition yet melts at 1066 C
    assert thermo.T_solidus_Cu_O(500) - T0C == pytest.approx(1066.2, abs=0.01)


# ------------------------------------------------------------------ registry
def test_registry_defaults_inside_ranges():
    for p in params.REGISTRY.values():
        assert p.lo <= p.value <= p.hi, p.key
        assert p.tag in {"MEASURED", "ANALOGUE", "DERIVED", "GUESS"}
        assert p.group in params.GROUPS


def test_scenario_validation_rejects_out_of_range():
    with pytest.raises(ValueError):
        params.scenario(d50_um=100.0)
    with pytest.raises(KeyError):
        params.scenario(not_a_param=1.0)


def test_presets_are_valid():
    for name in params.POWDER_PRESETS:
        s = params.apply_preset(params.defaults(), powder=name)
        params.scenario(**s)
    for name in params.FURNACE_PRESETS:
        s = params.apply_preset(params.defaults(), furnace=name)
        params.scenario(**s)


# ------------------------------------------------------------------ materials
def test_span_to_sigma():
    sig = lognormal_sigma_from_span(1.0)
    assert 2 * math.sinh(1.2815516 * sig) == pytest.approx(1.0)


def test_binder_inventory_matches_research_table():
    # binder wt% of green body vs phi (rho_b = 1.13): 11.2 % at 0.50, 9.4 % at 0.55
    for phi, wt in ((0.50, 11.2), (0.55, 9.4), (0.60, 7.8)):
        su = Setup(params.scenario(phi=phi))
        frac = su.mb0 / (su.mb0 + su.mCu)
        assert 100 * frac == pytest.approx(wt, abs=0.15)


def test_native_oxide_scales_inverse_with_size():
    o_fine = Setup(params.scenario(d50_um=3.0)).O_ppm(Setup(params.scenario(d50_um=3.0)).X0)
    s12 = Setup(params.scenario(d50_um=12.0))
    o_std = s12.O_ppm(s12.X0)
    assert 80 < o_std < 300           # gas-atomised ~12 um Cu, 4 nm film
    assert o_fine == pytest.approx(4 * o_std, rel=0.05)


def test_first_order_peak_condition():
    # k(Tp) = E beta / (R Tp^2) puts the DTG peak exactly at Tp for a linear ramp
    from scipy.integrate import solve_ivp
    Tp, E, beta = 673.15, 190e3, 10 / 60
    kp = kp_from_Tpeak(Tp, E)
    T0 = 400.0
    f = lambda t, y: [-kp * math.exp(-(E / 8.314462618) * (1 / (T0 + beta * t) - 1 / Tp)) * y[0]]
    ts = np.linspace(0, (800 - T0) / beta, 20001)
    sol = solve_ivp(f, (ts[0], ts[-1]), [1.0], t_eval=ts, rtol=1e-10, atol=1e-12)
    rate = -np.gradient(sol.y[0], ts)
    assert T0 + beta * ts[np.argmax(rate)] == pytest.approx(Tp, abs=0.2)


def test_oxide_volume_expansion():
    su = Setup(params.defaults())
    ratio = su.inorganic_volume(0.5) / su.inorganic_volume(0.0)
    assert ratio == pytest.approx(1.68, abs=0.01)   # Pilling-Bedworth Cu2O


def test_sintering_viscosity_order_of_magnitude():
    su = Setup(params.defaults())
    eta = su.eta0(1000 + T0C, 4.8e-6)
    assert 3e8 < eta < 1e10


def test_iacs_phosphorus_penalty():
    su = Setup(params.scenario(P_ppm=100.0, P_dissolved_frac=1.0))
    assert su.iacs(1.0) == pytest.approx(101 - 7.3, abs=0.01)
