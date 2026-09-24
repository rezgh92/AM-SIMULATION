"""Co-firing figures of merit computed from a pair of slab runs (glass-ceramic body, copper conductor)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import numpy as np

from ..constants import T0C
from .glass import GlassSetup, FilledCopperSetup
from .mechanics import porous_viscosities, integrate_camber, warpage_from_curvature
from .run import glass_view


@dataclass
class Geometry:
    """Reference co-fired stack: a copper plane on a glass-ceramic layer (package warpage), and a
    thin embedded line (constrained-film stress)."""
    h_cu_mm: float = 0.10
    h_gc_mm: float = 1.00
    span_mm: float = 20.0


def _common_time(r_a, r_b, n=4000):
    t_end = min(r_a.t_h[-1], r_b.t_h[-1]) * 3600.0
    return np.linspace(0.0, t_end, n)


def _interp(r, key, t):
    return np.interp(t, r.t_h * 3600.0, r.series[key])


def biaxial_viscosity_series(r, su, t):
    T = 0.5 * (_interp(r, "T_center", t) + _interp(r, "T_surface", t)) + T0C
    G = _interp(r, "G_um", t) * 1e-6
    C = _interp(r, "C_ppm_mean", t)
    wb = np.clip(_interp(r, "binder_left", t), 0.0, 1.0)
    theta = 1.0 - _interp(r, "rho_mean", t)
    eta = su.eta0(T, G) * su.carbon_factor(C) * (1.0 + 1e4 * wb)
    _, _, _, _, B = porous_viscosities(eta, theta)
    return B, T


from .props import GC_E as GC_E_DENSE, CU_E as CU_E_DENSE


def elastic_modulus(su, r, t, E_dense):
    """Biaxial elastic modulus of the porous body: binder-carried when green, neck-controlled when brown."""
    T = 0.5 * (_interp(r, "T_center", t) + _interp(r, "T_surface", t)) + T0C
    wb = np.clip(_interp(r, "binder_left", t), 0.0, 1.0)
    rho = _interp(r, "rho_mean", t)
    neck = np.clip((rho - su.phi) / (1.0 - su.phi), 0.0, 1.0)
    E = su.E_green(T, np.clip(1.0 - wb, 0.0, 1.0)) + E_dense * (0.002 + neck ** 1.5)
    return E / (1.0 - 0.25)


def maxwell_series(t, rate_mis, E1, B1, E2, B2):
    """Stress in two Maxwell elements in series forced by a misfit strain rate (implicit Euler).

    d_eps/dt = sigma_dot (1/E1 + 1/E2) + sigma (1/B1 + 1/B2): each layer relaxes viscously and
    responds elastically, so the stress stays bounded when either material is effectively solid.
    """
    sig = np.zeros_like(t)
    for k in range(1, len(t)):
        dt = t[k] - t[k - 1]
        C = 1.0 / E1[k] + 1.0 / E2[k]
        D = 1.0 / B1[k] + 1.0 / B2[k]
        sig[k] = (C * sig[k - 1] + dt * rate_mis[k]) / (C + dt * D)
    return sig


def cofire_metrics(r_gc, r_cu, s: dict, geo: Geometry = Geometry()) -> Dict[str, float]:
    su_gc = GlassSetup(glass_view(s))
    su_cu = FilledCopperSetup(s)
    t = _common_time(r_gc, r_cu)
    eps_gc = np.log(np.clip(1.0 - _interp(r_gc, "shrink_xy", t), 1e-6, None))
    eps_cu = np.log(np.clip(1.0 - _interp(r_cu, "shrink_xy", t), 1e-6, None))
    B_gc, T = biaxial_viscosity_series(r_gc, su_gc, t)
    B_cu, _ = biaxial_viscosity_series(r_cu, su_cu, t)
    kappa, s_cu, s_gc = integrate_camber(t, eps_cu, eps_gc, B_cu, B_gc, geo.h_cu_mm * 1e-3, geo.h_gc_mm * 1e-3)
    d_eps = eps_cu - eps_gc
    # embedded conductor: the misfit strain rate is shared between line and body in proportion to
    # their compliances (series coupling, Eshelby factor of order one): a soft line follows the body
    # and carries B_cu x misfit; a stiff line forces the body to flow round it and the stress is set
    # by B_gc. Positive = copper in tension (it wants to shrink more than the body lets it).
    rate_mis = np.gradient(eps_gc - eps_cu, t)
    E_cu = elastic_modulus(su_cu, r_cu, t, CU_E_DENSE)
    E_gc = elastic_modulus(su_gc, r_gc, t, GC_E_DENSE)
    sig_line = maxwell_series(t, rate_mis, E_cu, B_cu, E_gc, B_gc)
    rho_cu = _interp(r_cu, "rho_mean", t)
    rho_gc_t = _interp(r_gc, "rho_mean", t)
    str_cu = su_cu.sigma_brown(rho_cu) + su_cu.sigma_green(T, np.clip(1.0 - _interp(r_cu, "binder_left", t), 0, 1))
    str_gc = su_gc.sigma_brown(rho_gc_t) + su_gc.sigma_green(T, np.clip(1.0 - _interp(r_gc, "binder_left", t), 0, 1))
    Pi_cu = np.maximum(sig_line, 0.0) / str_cu        # copper line pulled apart: voids, open circuits
    Pi_gc = np.maximum(-sig_line, 0.0) / str_gc       # body shrinking onto a stiff line: radial cracks
    Pi_line = np.maximum(Pi_cu, Pi_gc)
    X = su_gc.crystal_fraction(r_gc.series["G_um"])
    k_gc, k_cu = r_gc.kpi, r_cu.kpi
    warp = warpage_from_curvature(kappa, geo.span_mm * 1e-3) * 1e6      # um
    i_end = -1
    out = dict(
        duration_h=float(r_gc.kpi["duration_h"]),
        gc_rho=float(k_gc["rho_final"]), gc_X=float(X[-1]), gc_shrink_pct=float(k_gc["shrink_xy_pct"]),
        gc_C_close_ppm=float(k_gc["C_at_close_ppm"] if k_gc["closed"] else k_gc["C_final_ppm"]),
        gc_bloat=float(max(k_gc["Pi_bloat_max"], 0.0)), gc_Pi_gas=float(k_gc["Pi_gas_max"]),
        gc_Pi_th=float(k_gc["Pi_th_max"]),
        cu_rho=float(k_cu["rho_final"]), cu_iacs=float(k_cu["iacs"]), cu_shrink_pct=float(k_cu["shrink_xy_pct"]),
        cu_C_close_ppm=float(k_cu["C_at_close_ppm"] if k_cu["closed"] else k_cu["C_final_ppm"]),
        cu_O_close_ppm=float(k_cu["O_at_close_ppm"] if k_cu["closed"] else k_cu["O_final_ppm"]),
        cu_Pi_gas=float(k_cu["Pi_gas_max"]), cu_melt_margin=float(k_cu["melt_margin_min_K"]),
        mismatch_final_pct=float(100 * d_eps[i_end]), mismatch_max_pct=float(100 * np.max(np.abs(d_eps))),
        warp_final_um=float(warp[i_end]), warp_max_um=float(np.max(np.abs(warp))),
        line_stress_max_MPa=float(np.max(np.abs(sig_line)) / 1e6), Pi_cu_max=float(np.max(Pi_cu)),
        Pi_gc_max=float(np.max(Pi_gc)), line_Pi_max=float(np.max(Pi_line)),
        kappa_final=float(kappa[i_end]), kappa_max=float(np.max(np.abs(kappa))),
        ok=bool(r_gc.ok and r_cu.ok),
    )
    series = dict(t_h=t / 3600.0, T_C=T - T0C, eps_gc=eps_gc, eps_cu=eps_cu, d_eps=d_eps, kappa=kappa, warp_um=warp,
                  B_gc=B_gc, B_cu=B_cu, sig_line=sig_line, Pi_line=Pi_line, Pi_cu=Pi_cu, Pi_gc=Pi_gc,
                  rho_gc=_interp(r_gc, "rho_mean", t), rho_cu=rho_cu,
                  X_gc=np.interp(t, r_gc.t_h * 3600.0, X),
                  C_gc=_interp(r_gc, "C_ppm_mean", t), C_cu=_interp(r_cu, "C_ppm_mean", t))
    return out, series
