"""Mechanics of co-firing: porous viscous moduli, shrinkage mismatch, bilayer camber, cooling warpage.

Constitutive law (Skorohod-Olevsky, the same one the 1-D and 3-D models use):
    sigma = 2 eta [ phi(theta) e' + psi(theta) tr(e) I ] + P_L(theta) I
so the porous body is an isotropic linear viscous solid with
    shear viscosity  G_v = eta phi,     bulk viscosity  K_v = 2 eta psi,
    uniaxial viscosity E_v = 9 K_v G_v / (3 K_v + G_v),  viscous Poisson ratio
    nu_v = (3 K_v - 2 G_v) / (2 (3 K_v + G_v)),  biaxial viscosity E_v / (1 - nu_v).

By the elastic-viscous correspondence principle, a bilayer of two linear viscous layers whose
free in-plane strain RATES differ bends at a curvature RATE given by Timoshenko's bimetal formula
with the elastic moduli replaced by biaxial viscosities and the thermal strain by the free
sintering strain-rate difference (Cai, Green & Messing 1997 used this for laminates).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np


# ----------------------------------------------------------------------------- porous moduli
def sovs_functions(theta):
    th = np.clip(theta, 1e-4, 0.999)
    phi = (1.0 - th) ** 2
    psi = (2.0 / 3.0) * (1.0 - th) ** 3 / th
    return phi, psi


def porous_viscosities(eta, theta):
    """(G_v, K_v, E_v, nu_v, B_v) of a porous SOVS body with matrix viscosity eta (Pa s)."""
    phi, psi = sovs_functions(theta)
    G = eta * phi
    K = 2.0 * eta * psi
    E = 9.0 * K * G / (3.0 * K + G)
    nu = (3.0 * K - 2.0 * G) / (2.0 * (3.0 * K + G))
    return G, K, E, nu, E / (1.0 - nu)


def free_strain_rate(PL, eta, theta):
    """Free linear sintering strain rate (1/s, negative = shrinkage): tr(e)/3 with tr(e) = -P_L/(2 eta psi)."""
    _, psi = sovs_functions(theta)
    return -PL / (2.0 * eta * psi) / 3.0


# ----------------------------------------------------------------------------- Timoshenko bilayer
def timoshenko_factor(h1, h2, B1, B2):
    """kappa = F * (eps2 - eps1) for a bilayer with biaxial moduli B1, B2 (layer 1 on top).

    Positive kappa: concave towards layer 1, i.e. layer 1 has contracted more. Timoshenko (1925):
        kappa = 6 (1+m)^2 d_eps / [ h (3 (1+m)^2 + (1 + m n)(m^2 + 1/(m n))) ],  m = h1/h2, n = B1/B2.
    """
    m = h1 / h2
    n = B1 / B2
    h = h1 + h2
    return 6.0 * (1.0 + m) ** 2 / (h * (3.0 * (1.0 + m) ** 2 + (1.0 + m * n) * (m * m + 1.0 / (m * n))))


def layer_mean_stresses(h1, h2, B1, B2, d_eps):
    """Mean in-plane stress in each layer from a misfit d_eps = eps2 - eps1 (force balance plus the
    bending relief of Timoshenko's solution). Positive = tension."""
    F = timoshenko_factor(h1, h2, B1, B2)
    kap = F * d_eps
    h = h1 + h2
    # neutral-axis bookkeeping: axial force P in layer 1 (tension +), -P in layer 2
    # P = kappa (B1 I1 + B2 I2) / (h/2), with I_i = h_i^3/12 per unit width
    P = kap * (B1 * h1 ** 3 / 12.0 + B2 * h2 ** 3 / 12.0) / (h / 2.0)
    return P / h1, -P / h2, kap


def integrate_camber(t, eps1, eps2, B1, B2, h1_0, h2_0, ez1=None, ez2=None):
    """Integrate the curvature of a sintering bilayer from free-strain histories.

    t (s), eps_i free linear in-plane strains (ln, negative = shrinkage), B_i biaxial viscosities
    (Pa s) along t. Layer thicknesses follow their own free strains through-thickness (ez_i).
    Returns kappa(t) (1/m) and the mean layer stresses (Pa).
    """
    ez1 = eps1 if ez1 is None else ez1
    ez2 = eps2 if ez2 is None else ez2
    d_rate = np.gradient(eps2 - eps1, t)
    h1 = h1_0 * np.exp(ez1)
    h2 = h2_0 * np.exp(ez2)
    F = timoshenko_factor(h1, h2, B1, B2)
    kdot = F * d_rate
    kappa = np.concatenate([[0.0], np.cumsum(0.5 * (kdot[1:] + kdot[:-1]) * np.diff(t))])
    s1, s2, _ = layer_mean_stresses(h1, h2, B1, B2, d_rate)
    # viscous stresses: stress = viscosity x strain-rate misfit (instantaneous, not accumulated)
    return kappa, s1, s2


# ----------------------------------------------------------------------------- cooling (elastic-plastic)
@dataclass
class ThermoMech:
    E: float            # Pa
    nu: float
    alpha: Callable     # 1/K as function of T (C)
    yield_: Optional[Callable] = None     # Pa as function of T (C); None = elastic


def cooling_bilayer(T_sf, T_end, h1, h2, m1: ThermoMech, m2: ThermoMech, n=400):
    """Cool a bonded bilayer from its stress-free temperature T_sf (C) to T_end.

    Layer 1 (copper) is elastic-perfectly plastic with a temperature-dependent yield stress; the
    layer carries a uniform plastic strain that caps its mean stress (thin-layer approximation).
    Returns T, kappa (1/m), mean stress in layer 1 and 2 (Pa), plastic strain in layer 1.
    """
    T = np.linspace(T_sf, T_end, n)
    B1 = m1.E / (1.0 - m1.nu)
    B2 = m2.E / (1.0 - m2.nu)
    F = timoshenko_factor(h1, h2, B1, B2)
    # stress in layer 1 per unit misfit (d_eps = eps2 - eps1 > 0 puts layer 1 in tension)
    s1_per, _, _ = layer_mean_stresses(h1, h2, B1, B2, 1.0)
    mis = 0.0
    ep = 0.0
    kap, s1, s2, eps_p = [], [], [], []
    for k in range(n):
        if k:
            dT = T[k] - T[k - 1]
            a1 = m1.alpha(0.5 * (T[k] + T[k - 1]))
            a2 = m2.alpha(0.5 * (T[k] + T[k - 1]))
            mis += (a2 - a1) * dT       # layer 1 shrinks more on cooling (alpha1 > alpha2) -> mis > 0
        el = mis - ep
        sig = s1_per * el
        if m1.yield_ is not None:
            sy = m1.yield_(T[k])
            if abs(sig) > sy:
                ep = mis - np.sign(sig) * sy / s1_per
                el = mis - ep
                sig = s1_per * el
        kap.append(F * el)
        s1.append(sig)
        s2.append(-sig * h1 / h2)
        eps_p.append(ep)
    return T, np.array(kap), np.array(s1), np.array(s2), np.array(eps_p)


def warpage_from_curvature(kappa, span):
    """Bow of a plate of length ``span`` bent to curvature kappa (sagitta), m."""
    return kappa * span ** 2 / 8.0
