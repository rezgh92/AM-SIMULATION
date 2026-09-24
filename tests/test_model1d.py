"""Verification of the 1-D digital coupon against closed forms and conservation laws.

These are *verification* tests (is the code solving its equations correctly?), kept
separate from validation against published processes (tests/test_validation.py).
"""
import math

import numpy as np
import pytest

from cupola.constants import T0C, M_C, R, P_ATM
from cupola.cycle import Cycle, Segment
from cupola.integrate import ode23s
from cupola.materials import Setup
from cupola.model1d import Slab, Controls, NV, IT, IB1, IB2, IB3, IC, IX, IY, ILV, IG, INT, GTF, GO2, GH2
from cupola.params import scenario
from cupola.simulate import simulate


def _slab(**kw):
    su = Setup(scenario(**kw))
    return su, Slab(su)


def test_rhs_batched_equals_single():
    su, sl = _slab()
    Y = sl.y0(500.0, (0.01, 0.0, 0.001))
    ctl = Controls(0, 1e4, 500.0, 700.0, 0.01, 0.0, 0.001)
    rng = np.random.default_rng(0)
    batch = Y[None, :] * (1 + 1e-3 * rng.standard_normal((5, Y.size)))
    Fb = sl.evaluate(10.0, batch, ctl)
    for k in range(5):
        np.testing.assert_allclose(Fb[k], sl.evaluate(10.0, batch[k], ctl), rtol=1e-12, atol=1e-300)


def test_ode23s_against_exact_linear_stiff_system():
    lam = np.array([-1.0, -1e4])
    f = lambda t, y: y * lam
    ts, ys, n, _ = ode23s(f, 0.0, 2.0, np.array([1.0, 1.0]), atol=1e-10, rtol=1e-7)
    assert ys[-1][0] == pytest.approx(math.exp(-2.0), rel=2e-5)
    assert abs(ys[-1][1]) < 1e-8


def test_tga_peak_reproduced_in_inert_slab():
    """A thin coupon heated at 10 K/min in N2 must show its network DTG peak at Tp_network."""
    su, sl = _slab(half_thickness_mm=0.25, solvent_frac=0.0, w_backbone=0.1, h_conv=150.0)
    beta = 10.0 / 60.0
    t1 = (650 - 25) / beta
    ctl = Controls(0.0, t1, 25 + T0C, 650 + T0C, 0.0, 0.0, 1e-6)
    Y0 = sl.y0(25 + T0C)
    ts, ys, *_ = ode23s(lambda t, y: sl.evaluate(t, y, ctl), 0.0, t1, Y0, sl.atol, rtol=1e-5,
                        scale=sl.scale, h_max=5.0)
    ts, ys = np.array(ts), np.array(ys)
    node, glob = sl.split(ys)
    net = (node[:, IB2, :] * sl.wt).sum(-1)
    T = (node[:, IT, :] * sl.wt).sum(-1)
    rate = -np.gradient(net, ts)
    Tpk = T[np.argmax(rate)] - T0C
    # thin part tracks the furnace; the backbone tail shifts the combined peak by a few K at most
    assert Tpk == pytest.approx(su.s["Tp_network_C"], abs=6.0)


def test_free_sintering_matches_closed_form():
    """Olevsky/SOVS free sintering with fixed T and G: theta(t) = theta0 exp(-9 gamma t / (4 r eta)).

    Compare the model's densification rate at t=0 with the closed form (grain growth frozen,
    binder-free, carbon-free).
    """
    su, sl = _slab(kG_mult=0.1)
    Y = sl.y0(1273.15)
    node, glob = sl.split(Y)
    node[IB1:IB3 + 1] = 0.0
    glob[GTF] = 1273.15
    Y = np.concatenate([node.ravel(), glob])
    ctl = Controls(0, 1, 1273.15, 1273.15, 0.0, 0.04, 1e-5)
    F = sl.evaluate(0.0, Y, ctl)
    dnode, _ = sl.split(F)
    theta0 = 1 - su.inorganic_volume(su.X0)
    eta = su.eta0(1273.15, su.G0)
    # d lnV/dt = e_dot = -P_L/(2 eta psi) = -(9 gamma/(4 r eta)) * theta/(1-theta)
    expected = -(9 * su.gamma / (4 * su.r_s * eta)) * theta0 / (1 - theta0)
    assert dnode[ILV, 0] == pytest.approx(expected, rel=1e-3)


def test_closed_form_free_sintering_trajectory():
    """Integrate densification alone and check theta(t) against the exponential solution."""
    su, sl = _slab()
    eta, r, g = 2e9, su.r_s, su.gamma
    k = 9 * g / (4 * r * eta)
    theta0 = 0.45
    ts, ys, *_ = ode23s(lambda t, y: (1 - y) * (-(k) * y / (1 - y)), 0.0, 4 / k, np.array([theta0]),
                        atol=1e-12, rtol=1e-8)
    assert ys[-1][0] == pytest.approx(theta0 * math.exp(-4.0), rel=1e-5)


def test_carbon_and_oxygen_mass_balance_closes():
    """All carbon leaving the solid must appear as CO/CO2 fluxes; checked over a gasification hold."""
    su, sl = _slab(half_thickness_mm=0.5, load_cm3=1.0)
    Y = sl.y0(1073.15, (0.0, 0.04, 0.0231))
    node, glob = sl.split(Y)
    node[IB1:IB3 + 1] = 0.0
    node[IC] = 5.0                  # kg/m^3 char
    node[IX] = 0.02
    glob[GTF] = 1073.15
    Y = np.concatenate([node.ravel(), glob])
    ctl = Controls(0, 3600, 1073.15, 1073.15, 0.0, 0.04, 0.0231)
    ts, ys, *_ = ode23s(lambda t, y: sl.evaluate(t, y, ctl), 0.0, 3600.0, Y, sl.atol, rtol=1e-6,
                        scale=sl.scale)
    ts, ys = np.array(ts), np.array(ys)
    node, glob = sl.split(ys)
    C_solid = (node[:, IC, :] * sl.wt).sum(-1) / M_C * su.V_load          # mol C in the load
    # outflow of CO + CO2 from the retort, integrated
    F_out = su.F_in                                                        # to first order
    xCO, xCO2 = glob[:, 4], glob[:, 5]
    N_r = P_ATM * su.V_r / (R * 1073.15)
    out = np.trapezoid(F_out * (xCO + xCO2), ts) + N_r * (xCO[-1] + xCO2[-1])
    removed = C_solid[0] - C_solid[-1]
    assert removed > 0
    assert out == pytest.approx(removed, rel=0.02)


def test_energy_balance_inert_heating():
    """Binder-free slab, no reactions: stored enthalpy equals integrated surface heat flow."""
    su, sl = _slab(half_thickness_mm=2.0)
    Y = sl.y0(400.0)
    node, glob = sl.split(Y)
    node[IB1:IB3 + 1] = 0.0
    node[IX] = 0.0
    glob[GTF] = 400.0
    Y = np.concatenate([node.ravel(), glob])
    ctl = Controls(0, 3000, 400.0, 600.0, 0.0, 0.0, 1e-8)
    ts, ys, *_ = ode23s(lambda t, y: sl.evaluate(t, y, ctl), 0.0, 3000.0, Y, sl.atol, rtol=1e-7,
                        scale=sl.scale)
    ys = np.array(ys)
    node, _ = sl.split(ys)
    from cupola.materials import cp_cu
    # enthalpy of Cu per reference volume, integrated cp dT
    def H(T):
        return su.mCu * (360.0 * T + 0.5 * 0.0870 * T ** 2)
    stored = ((H(node[-1, IT]) - H(node[0, IT])) * sl.wt).sum() * su.L0
    # recompute surface flux along the trajectory
    q_in = []
    for t, y in zip(ts, ys):
        _, d = sl.evaluate(t, y, ctl, diag=True)
        Ts = d["T"][-1]
        Tf = d["Tf"]
        k = su.k_eff(Ts, d["w_b"][-1], d["rho"][-1])
        Rs = 1.0 / d["h_tot"] + 0.5 * sl.w[-1] / k
        q_in.append((Tf - Ts) / Rs)
    supplied = np.trapezoid(q_in, ts)
    assert stored == pytest.approx(supplied, rel=0.02)


def test_ellingham_gate_blocks_oxidation_in_forming_gas():
    """With 4 % H2 and a bubbler, Cu must not oxidise even with a trace of O2 in the feed."""
    r = simulate(scenario(half_thickness_mm=0.5),
                 Cycle([Segment(900, 10.0, 1.0, 5e-6, 0.04, 20.0), Segment(25, 10.0, 0, 0, 0.04, 20.0)]),
                 rtol=1e-3)
    assert r.ok
    assert r.kpi["O_peak_ppm"] <= r.series["O_ppm_mean"][0] * 1.05


def test_graded_mesh_convergence():
    """Doubling the node count changes the headline KPIs by less than 2 % on a short cycle."""
    cyc = Cycle([Segment(450, 2.0, 1.0, 0.002, 0.0, -60), Segment(1000, 5.0, 1.0, 0.0, 0.04, 20.0),
                 Segment(25, 10.0, 0.0, 0.0, 0.04, -60)])
    a = simulate(scenario(n_nodes=10), cyc, rtol=1e-4).kpi
    b = simulate(scenario(n_nodes=20), cyc, rtol=1e-4).kpi
    for key in ("rho_final", "shrink_xy_pct"):
        assert a[key] == pytest.approx(b[key], rel=0.02), key
    assert a["C_peak_ppm"] == pytest.approx(b["C_peak_ppm"], rel=0.05)
