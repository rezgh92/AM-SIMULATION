"""T1 - the digital coupon: a 1-D symmetric slab through the critical section.

Per node (cell-centred finite volumes in green/reference coordinates):
    T      temperature, K
    b1..b3 binder pseudo-components (solvent, network, char-forming backbone), fraction of initial binder
    c      char carbon, kg per m^3 of green part
    X      oxygen bound as oxide, mol O per mol Cu (0.5 = all Cu2O, 1 = all CuO)
    y      O2 mole fraction in the pore gas
    lnV    log of envelope volume relative to green (sintering shrinkage < 0)
    G      grain size, um
    ntr    insoluble gas trapped in closed pores, mol per m^3 of green part
Global:
    Tf     furnace (retort) temperature, K
    xO2, xH2, xH2O, xCO, xCO2   retort gas mole fractions (well-mixed CSTR)
    ez     accumulated deviatoric z-strain (anisotropic shrinkage)

Physics, in one line each (details in the docstrings of the helpers below):
  * heat: conduction with k_eff(binder, density, T); convective + radiative surface loss;
    sources = oxidative exotherms (binder, char, Cu), pyrolysis/vaporisation endotherms, reduction/gasification.
  * binder: 3 parallel first-order pyrolysis channels (TGA-peak parameterised) + an oxidative
    channel first-order in pore O2; char yield from the network channels.
  * O2: diffusion (molecular + Knudsen) through the open pore network with outward "blowing" by
    pyrolysis gas, and a gas-film resistance tied to h (Chilton-Colburn); consumed by binder, char, Cu.
  * copper: oxidation law fitted to powder data; H2 reduction (TPR-parameterised, Langmuir in H2,
    thermodynamically gated); carbothermic Cu2O + C -> 2Cu + CO; steam gasification of char.
  * sintering: Skorohod-Olevsky viscous sintering, eta from Frost & Ashby Cu diffusion, carbon
    inhibition, pore-gas back-pressure of insoluble gas trapped at closure (and generated after it).
  * retort: CSTR balances with gas-phase H2/O2 recombination and volatile combustion.
"""
from __future__ import annotations

import math
import numpy as np

from .constants import (R, SIGMA_SB, P_ATM, M_C, M_O2, RHO_CHAR, V_CU, V_CU_IN_CU2O, V_CU_IN_CUO, T0C)
from . import thermo
from .materials import (Setup, cp_cu, mu_gas, D_O2_N2, smoothstep, sigmoid,
                        CUOX_M, CUOX_X0, NU_O2_BINDER, N_CO2_BINDER, N_H2O_BINDER,
                        DH_CU_OX, DH_RED_H2, DH_CARBOTHERMIC, DH_GASIF, DH_CHAR_OX,
                        CP_BINDER, CP_CHAR, THETA_PIN)

NV = 10
IT, IB1, IB2, IB3, IC, IX, IY, ILV, IG, INT = range(NV)
NG = 7
GTF, GO2, GH2, GH2O, GCO, GCO2, GEZ = range(NG)
NODE_NAMES = ["T", "b1", "b2", "b3", "c", "X", "y", "lnV", "G", "ntr"]
GLOB_NAMES = ["Tf", "xO2", "xH2", "xH2O", "xCO", "xCO2", "ez"]

Y_SMALL = 1e-4          # O2 level below which oxidation becomes first order in O2
X_SWITCH = 1e-3         # oxide level at which carbothermic/reduction rates switch off
EPS_ACC = 0.02          # open porosity at which gas access is half established
MESH_GRADE = 1.35       # geometric growth of cell width from surface to centre
D_POLY_O2 = 1e-10       # O2 permeation through rubbery binder, as a gas-phase-equivalent diffusivity (m^2/s)


def pos(z, w):
    """Smooth max(z, 0) with transition width w. Keeps the Jacobian continuous at thermodynamic
    equilibria and at exhausted reactants, where a hard clip stalls a Rosenbrock error estimator."""
    return 0.5 * (z + np.sqrt(z * z + w * w))


class Controls:
    """Setpoint and inlet gas for one segment (ramp or hold)."""

    def __init__(self, t0, t1, Ta_K, Tb_K, xO2_in, xH2_in, xH2O_in):
        self.t0, self.t1, self.Ta, self.Tb = t0, t1, Ta_K, Tb_K
        self.xO2_in, self.xH2_in, self.xH2O_in = xO2_in, xH2_in, xH2O_in

    def Tset(self, t):
        if self.t1 <= self.t0:
            return self.Tb
        f = min(max((t - self.t0) / (self.t1 - self.t0), 0.0), 1.0)
        return self.Ta + f * (self.Tb - self.Ta)


class Slab:
    def __init__(self, setup: Setup, N: int | None = None):
        self.su = setup
        self.N = int(N or setup.s["n_nodes"])
        self.n = NV * self.N + NG
        # geometrically graded cells, thinnest at the surface: oxidation, O2 ingress and heat exchange
        # start in a skin a few um thick, which a uniform 0.2 mm cell cannot resolve
        w = MESH_GRADE ** np.arange(self.N - 1, -1, -1, dtype=float)
        self.w = w / w.sum() * setup.L0            # reference cell widths, centre (i=0) -> surface
        self.dface = 0.5 * (self.w[:-1] + self.w[1:])
        self.wt = self.w / setup.L0                # volume weights for averages
        self.xc = np.cumsum(self.w) - 0.5 * self.w # cell-centre positions from the mid-plane
        # pores within ~1-3 particle diameters of the free surface vent to it and cannot trap gas
        depth = setup.L0 - self.xc
        self.trap_depth = smoothstep((depth - setup.d50) / (2.0 * setup.d50))
        self.Vb0 = setup.mb0 / setup.rho_b
        self.b_net0 = float(setup.b0[1] + setup.b0[2]) / setup.mb0
        self.theta0 = 1.0 - setup.phi
        # scales for finite-difference Jacobians and error control
        sc_node = np.array([300.0, 1.0, 1.0, 1.0, 1.0, 0.01, 0.01, 0.01, 10.0, 1.0])
        sc_glob = np.array([300.0, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        self.scale = np.concatenate([np.repeat(sc_node, self.N), sc_glob])
        at_node = np.array([1e-3, 1e-7, 1e-7, 1e-7, 1e-6, 1e-8, 1e-9, 1e-8, 1e-5, 1e-7])
        at_glob = np.array([1e-3, 1e-9, 1e-9, 1e-9, 1e-9, 1e-9, 1e-8])
        self.atol = np.concatenate([np.repeat(at_node, self.N), at_glob])

    # ------------------------------------------------------------------ state helpers
    def y0(self, T0_K=298.15, x_in=(0.0, 0.0, 0.0)):
        su, N = self.su, self.N
        node = np.zeros((NV, N))
        node[IT] = T0_K
        b = su.b0.copy()
        rem = su.s.get("pre_extracted_frac", 0.0) * su.mb0      # solvent debind before the thermal cycle
        for k in range(3):
            take = min(b[k], rem)
            b[k] -= take
            rem -= take
        node[IB1:IB3 + 1] = (b / su.mb0)[:, None]
        node[IC] = 0.0
        node[IX] = su.X0
        node[IY] = 0.2095 * 0 + x_in[0]
        node[ILV] = 0.0
        node[IG] = su.G0 * 1e6
        node[INT] = 0.0
        glob = np.array([T0_K, x_in[0], x_in[1], x_in[2], 0.0, 0.0, 0.0])
        return np.concatenate([node.ravel(), glob])

    def split(self, Y):
        node = Y[..., :NV * self.N].reshape(Y.shape[:-1] + (NV, self.N))
        glob = Y[..., NV * self.N:]
        return node, glob

    # ------------------------------------------------------------------ core evaluation
    def evaluate(self, t, Y, ctl: Controls, diag=False):
        """Return dY/dt (same shape as Y). With diag=True also a dict of derived quantities."""
        su, N = self.su, self.N
        w, dface, wt = self.w, self.dface, self.wt
        node, glob = self.split(Y)
        T = node[..., IT, :]
        bf = node[..., IB1:IB3 + 1, :]
        B = pos(bf, 1e-12) * su.mb0                                        # kg/m^3, (...,3,N)
        c = pos(node[..., IC, :], 1e-9)
        X = np.minimum(pos(node[..., IX, :], 1e-9), 1.0)
        y = np.minimum(pos(node[..., IY, :], 1e-12), 1.0)
        lnV = node[..., ILV, :]
        V = np.exp(lnV)
        G = np.maximum(node[..., IG, :], 1e-3) * 1e-6
        ntr = np.maximum(node[..., INT, :], 0.0)

        Tf = glob[..., GTF]
        xO2r = pos(glob[..., GO2], 1e-12)
        xH2r = pos(glob[..., GH2], 1e-12)
        xH2Or = pos(glob[..., GH2O], 1e-12)
        xCOr = pos(glob[..., GCO], 1e-12)
        xCO2r = pos(glob[..., GCO2], 1e-12)
        ex = lambda a: a[..., None]                                          # broadcast globals to nodes

        # ---------------- composition & microstructure
        Vsol = su.inorganic_volume(X)
        Vb = B.sum(axis=-2) / su.rho_b
        Vc = c / RHO_CHAR
        eps = np.clip(1.0 - (Vsol + Vb + Vc) / V, 0.0, 1.0)
        rho_s = np.clip(Vsol / V, 1e-3, 0.99999)
        theta = 1.0 - rho_s
        # Pore closure is a sintering event: judge it on the metal-equivalent density. Oxide growing
        # into pores (+68 % volume) also chokes gas access, but through eps (porosity) not closure,
        # and it reverses on reduction.
        rho_m = np.clip(su.nCu * V_CU / V, 1e-3, 0.99999)
        u_cl = (rho_m - (su.rho_close - 0.03)) / 0.06
        f_cl = smoothstep(u_cl)
        eps_open = eps * (1.0 - f_cl)
        w_b = np.clip(Vb / self.Vb0, 0.0, 1.0)
        a_net = 1.0 - (bf[..., 1, :] + bf[..., 2, :]) / self.b_net0
        acc = eps_open / (eps_open + EPS_ACC)
        m_inorg = su.inorganic_mass(X)
        C_ppm = 1e6 * c / m_inorg

        # ---------------- binder
        Tb3 = T[..., None, :]
        k_p = su.kp[:, None] * np.exp(-(su.E[:, None] / R) * (1.0 / Tb3 - 1.0 / su.Tp[:, None]))
        r_p = k_p * B                                                          # kg/m^3/s
        k_o = su.kp_ox[1:, None] * np.exp(-(su.E_ox[1:, None] / R) * (1.0 / Tb3 - 1.0 / su.Tp_ox[1:, None]))
        r_o = k_o * B[..., 1:, :] * (y[..., None, :] / 0.21)                   # oxidative, network only
        chi = su.chi[:, None] * (1.0 - 0.36 * ex(xH2r))[..., None, :]
        char_form = (chi * r_p).sum(axis=-2)
        r_co = su.k_char_ox(T) * c * (y / 0.21) * (1.0 - f_cl)                # kg C/m^3/s, open pores only

        # ---------------- copper oxide and carbon chemistry
        yO2 = y
        pO2eq = thermo.pO2_eq_Cu_Cu2O(T)
        th_ox = pos(1.0 - np.sqrt(pO2eq / np.maximum(yO2, 1e-30)), 0.01)
        fy = (yO2 / 0.21) ** (1.0 / 7.0) * yO2 / (yO2 + Y_SMALL)
        dX_ox = su.k_cu_ox(T) * fy * th_ox * pos(1.0 - X, 1e-6) / (X + CUOX_X0) ** CUOX_M
        dX_ox = dX_ox * (1.0 - f_cl)          # closed pores see no O2 (open-pore O2 access is in y)

        ratio = ex(xH2Or) / np.maximum(ex(xH2r), 1e-12)
        th_red = pos(1.0 - ratio / thermo.h2o_h2_boundary_Cu(T), 0.01)
        fH2 = 2.0 * ex(xH2r) / (ex(xH2r) + 0.04)
        hot = sigmoid((T - 600.0) / 20.0)
        k_rX = su.k_red(T) * X * fH2 * th_red
        # open pores: H2 from the gas, H2O vents. Closed pores: H2 arrives by lattice diffusion through
        # Cu, but the H2O it makes is insoluble and stays (hydrogen disease / steam blistering).
        rX_open = acc * (1.0 - f_cl) * k_rX
        rX_closed = f_cl * hot * k_rX
        rX_red = rX_open + rX_closed                                           # 1/s

        Kst = thermo.K_steam_gasification(T)
        Qst = ex(xCOr) * ex(xH2r) / np.maximum(ex(xH2Or), 1e-12)
        th_g = pos(1.0 - Qst / Kst, 0.01)
        inh = (1.0 + su.K_inh * 0.04) / (1.0 + su.K_inh * ex(xH2r))
        # steam cannot reach char sealed in closed pores: it stays, inert, and inhibits sintering
        r_g = acc * (1.0 - f_cl) * su.k_gasif(T) * (c / M_C) * np.sqrt(ex(xH2Or) / su.x_h2o_ref) * inh * th_g
        r_cth = su.k_carbothermic(T) * (c / M_C) * X / (X + X_SWITCH)                          # mol C/m^3/s

        dXdt = dX_ox - rX_red - r_cth / su.nCu
        dcdt = char_form - r_co - M_C * (r_g + r_cth)
        dBdt = -r_p
        dBdt = dBdt - np.concatenate([np.zeros_like(r_o[..., :1, :]), r_o], axis=-2)

        # ---------------- gas generation (net moles into pore gas, mol/m^3/s) and O2 demand
        n_vol = (r_p * (1.0 - chi) / su.Mgas[:, None]).sum(axis=-2)
        n_ox_net = (N_CO2_BINDER + N_H2O_BINDER - NU_O2_BINDER) * r_o.sum(axis=-2)
        n_red = su.nCu * rX_red                                                # H2O made = H2 used
        n_red_open = su.nCu * rX_open
        n_red_closed = su.nCu * rX_closed
        ndot = n_vol + n_ox_net - 0.5 * su.nCu * dX_ox + r_g + r_cth
        R_O2 = NU_O2_BINDER * r_o.sum(axis=-2) + r_co / M_C + 0.5 * su.nCu * dX_ox

        # ---------------- heat
        q = (-0.4e6 * r_p[..., 0, :] - su.dHpyr * r_p[..., 1:, :].sum(axis=-2)
             + su.dHc * r_o.sum(axis=-2) + DH_CHAR_OX * r_co / M_C + DH_CU_OX * su.nCu * dX_ox
             + DH_RED_H2 * n_red - DH_CARBOTHERMIC * r_cth - DH_GASIF * r_g)
        Ccap = m_inorg * cp_cu(T) + B.sum(axis=-2) * CP_BINDER + c * CP_CHAR
        s = np.exp(lnV / 3.0)
        kk = su.k_eff(T, w_b, rho_s)
        kf = 2.0 * kk[..., :-1] * kk[..., 1:] / (kk[..., :-1] + kk[..., 1:])
        sf = 0.5 * (s[..., :-1] + s[..., 1:])
        dist = dface * sf
        Qf = sf ** 2 * kf * (T[..., 1:] - T[..., :-1]) / dist                  # into cell i from i+1
        w_dark = np.maximum(w_b, np.maximum(np.clip(C_ppm / 300.0, 0, 1), np.clip(X / 0.02, 0, 1)))
        epsr = su.emissivity(w_dark[..., -1], theta[..., -1])
        Ts = T[..., -1]
        h_rad = epsr * SIGMA_SB * (Tf ** 2 + Ts ** 2) * (Tf + Ts)
        # H2 conducts heat ~7x better than N2/Ar, so the convective film coefficient rises with H2
        # content (h ~ k_gas^0.7). This is what keeps pure-H2 reduction of oxidised Cu from running away.
        h_cv = su.h_conv * (1.0 + 6.0 * xH2r) ** 0.7
        h_tot = h_cv + h_rad
        Rs = 1.0 / h_tot + 0.5 * w[-1] * s[..., -1] / kk[..., -1]
        Qs = s[..., -1] ** 2 * (Tf - Ts) / Rs
        div_T = np.zeros_like(T)
        div_T[..., :-1] += Qf
        div_T[..., 1:] -= Qf
        div_T[..., -1] += Qs
        dTdt = (div_T / w + q) / Ccap

        # ---------------- O2 transport in pores
        ctot = P_ATM / (R * T)
        d_pore = np.maximum((2.0 / 3.0) * eps_open / np.maximum(1.0 - eps_open, 1e-3) * su.d32, 1e-9)
        DKn = d_pore / 3.0 * np.sqrt(8.0 * R * T / (math.pi * M_O2))
        Dm = 1.0 / (1.0 / D_O2_N2(T) + 1.0 / DKn)
        Deff = eps_open ** 1.5 * Dm + D_POLY_O2 * w_b
        Df = 2.0 * Deff[..., :-1] * Deff[..., 1:] / (Deff[..., :-1] + Deff[..., 1:])
        cf = 0.5 * (ctot[..., :-1] + ctot[..., 1:])
        Ndiff = sf ** 2 * Df * cf * (y[..., 1:] - y[..., :-1]) / dist          # into i from i+1
        J = np.cumsum(ndot * w, axis=-1)                                       # outward gas flow per ref area at faces
        Jf = J[..., :-1]
        Nadv = -np.maximum(Jf, 0.0) * y[..., :-1] + np.maximum(-Jf, 0.0) * y[..., 1:]
        Nface = Ndiff + Nadv                                                   # net O2 flow into cell i from face i+1/2
        ctg = P_ATM / (R * Tf)
        k_m = h_cv / (ctg * 29.1)                                               # Chilton-Colburn, m/s
        Rsm = 1.0 / (k_m * ctg) + 0.5 * w[-1] * s[..., -1] / (Deff[..., -1] * ctot[..., -1])
        Js = J[..., -1]
        Ns = s[..., -1] ** 2 * (xO2r - y[..., -1]) / Rsm \
            - np.maximum(Js, 0.0) * y[..., -1] + np.maximum(-Js, 0.0) * xO2r
        div_y = np.zeros_like(y)
        div_y[..., :-1] += Nface
        div_y[..., 1:] -= Nface
        div_y[..., -1] += Ns
        Cg = (eps_open + 0.01) * ctot * V
        dydt = (div_y / w - R_O2) / Cg

        # ---------------- sintering (SOVS) with carbon inhibition and pore-gas back-pressure
        th = np.clip(theta, 1e-4, 0.999)
        psi = (2.0 / 3.0) * (1.0 - th) ** 3 / th
        phi_s = (1.0 - th) ** 2
        PL = 3.0 * su.gamma / su.r_s * (1.0 - th) ** 2
        # closed-pore gas pressure; the floor keeps p_g bounded when the closed fraction is ~0
        # (the release term below guarantees ntr -> 0 there, so the floor never sets physics)
        Vcl = f_cl * eps * V + 1e-4 * pos(eps, 1e-6) * V + 1e-9
        p_g = ntr * R * T / Vcl
        # Overpressure beyond a few times the sintering stress ruptures the pore wall and vents (a
        # blister); saturate it so the swelling rate stays bounded. Pi_bloat reports the raw value.
        dP_raw = f_cl * (p_g - P_ATM)
        dP = 3.0 * PL * np.tanh(dP_raw / (3.0 * PL))
        eta = su.eta0(T, G) * (1.0 + (C_ppm / su.C_inh) ** 2) * (1.0 + 1e4 * w_b)
        e_dot = -(PL - dP) / (2.0 * eta * psi)
        dvdX = np.where(X < 0.5, (V_CU_IN_CU2O - V_CU) / 0.5, (V_CU_IN_CUO - V_CU_IN_CU2O) / 0.5) * su.nCu
        swell = smoothstep((0.04 - eps) / 0.04) * dvdX * dXdt / V
        dlnVdt = e_dot + swell
        dGdt = 1e6 * su.kG_rate(T) / (3.0 * G ** 2) * (THETA_PIN / (th + THETA_PIN)) ** 2

        # closure can come from sintering OR from oxide filling the pores (+68 % volume); both are
        # reversible (reduction reopens oxide-filled pores), so gas is trapped on closing and
        # released in proportion to the closed fraction that reopens.
        drho = -rho_m * dlnVdt
        uc = np.clip(u_cl, 0.0, 1.0)
        dfcl = 6.0 * uc * (1.0 - uc) / 0.06 * drho
        x_insol = 1.0 - ex(xH2r)
        dep = self.trap_depth
        trap = dep * (P_ATM / (R * T)) * x_insol * eps * V * pos(dfcl, 1e-12)
        gen_cl = dep * (n_red_closed + f_cl * r_cth)                           # insoluble gas made inside closed pores
        release = ntr * pos(-dfcl, 1e-12) / np.maximum(f_cl, 1e-3) \
            + ntr * (1.0 - smoothstep(f_cl / 0.01)) * 1e-3
        dntr = trap + gen_cl - release

        a = su.aniso
        dez_node = -PL * a * (th / self.theta0) * (2.0 / 3.0) / (2.0 * eta * phi_s)

        # ---------------- furnace and retort
        Tset = ctl.Tset(t)
        dTf = su.ramp_max * np.tanh((Tset - Tf) / (su.tau_f * su.ramp_max))
        Nr = P_ATM * su.V_r / (R * Tf)
        vol = su.V_load
        mean = lambda a_: (a_ * wt).sum(axis=-1)
        esc = 1.0 - f_cl
        S_O2 = -vol * Ns / su.L0
        S_H2O = vol * mean(n_red_open + N_H2O_BINDER * r_o.sum(axis=-2) - r_g)
        S_H2 = vol * mean(-n_red + r_g)
        S_CO = vol * mean(r_g + esc * r_cth)
        S_CO2 = vol * mean(N_CO2_BINDER * r_o.sum(axis=-2) + r_co / M_C)
        S_HC = vol * mean(n_vol)
        # gas-phase: volatile combustion above ignition, H2/O2 recombination
        nu_hc = NU_O2_BINDER * su.s["M_vol"]
        f_gc = sigmoid((Tf - (350.0 + T0C)) / 15.0)
        r_gc = f_gc * nu_hc * S_HC * xO2r / (xO2r + 1e-3)                      # mol O2/s
        burnt = r_gc / nu_hc
        r_rec = 50.0 * sigmoid((Tf - 473.15) / 20.0) * Nr * xH2r * xO2r        # mol H2/s
        S_O2 = S_O2 - r_gc - 0.5 * r_rec
        S_H2 = S_H2 - r_rec
        S_H2O = S_H2O + r_rec + N_H2O_BINDER * su.s["M_vol"] * burnt
        S_CO2 = S_CO2 + N_CO2_BINDER * su.s["M_vol"] * burnt
        S_HC = S_HC - burnt
        S_tot = S_O2 + S_H2 + S_H2O + S_CO + S_CO2 + S_HC
        Fin = su.F_in
        xO2_in = ctl.xO2_in
        dxO2 = (Fin * (xO2_in - xO2r) + S_O2 - xO2r * S_tot) / Nr
        dxH2 = (Fin * (ctl.xH2_in - xH2r) + S_H2 - xH2r * S_tot) / Nr
        dxH2O = (Fin * (ctl.xH2O_in - xH2Or) + S_H2O - xH2Or * S_tot) / Nr
        dxCO = (Fin * (0.0 - xCOr) + S_CO - xCOr * S_tot) / Nr
        dxCO2 = (Fin * (0.0 - xCO2r) + S_CO2 - xCO2r * S_tot) / Nr
        dez = mean(dez_node)

        # ---------------- assemble
        dnode = np.empty(node.shape)
        dnode[..., IT, :] = dTdt
        dnode[..., IB1:IB3 + 1, :] = dBdt / su.mb0
        dnode[..., IC, :] = dcdt
        dnode[..., IX, :] = dXdt
        dnode[..., IY, :] = dydt
        dnode[..., ILV, :] = dlnVdt
        dnode[..., IG, :] = dGdt
        dnode[..., INT, :] = dntr
        dglob = np.stack([dTf + 0 * Tf, dxO2, dxH2, dxH2O, dxCO, dxCO2, dez], axis=-1)
        dY = np.concatenate([dnode.reshape(dnode.shape[:-2] + (NV * N,)), dglob], axis=-1)
        if not diag:
            return dY

        # ---------------- diagnostics (debinding gas pressure, strengths, risk indices)
        mu = mu_gas(T)
        dK = np.maximum((2.0 / 3.0) * eps / np.maximum(1.0 - eps, 1e-3) * su.d32, 1e-9)
        K_kc = eps ** 3 * su.d32 ** 2 / (180.0 * np.maximum(1.0 - eps, 1e-3) ** 2)
        # Knudsen (slip) flow expressed as an equivalent permeability: (eps/tau) D_Kn mu / p, tau = eps^-0.5
        K_kn = eps ** 1.5 * dK / 3.0 * np.sqrt(8.0 * R * T / (math.pi * su.s["M_vol"])) * mu / P_ATM
        perc = sigmoid((eps_open - su.eps_c) / 0.005)
        K_poly = su.perm_poly * mu * R * T / P_ATM
        K_app = perc * (K_kc + K_kn) + K_poly
        # quasi-steady compressible Darcy in the slab: d(p^2)/dx = -2 mu R T J(x) / K
        g_face = 2.0 * mu * R * T * np.maximum(J, 0.0) / K_app                  # at cell outer faces, Pa^2/m
        # integrate from surface inward: Phi_i = P^2 + sum_{j>=i} g_j w_j (face-based)
        Phi = P_ATM ** 2 + np.flip(np.cumsum(np.flip(g_face * w * s, -1), axis=-1), -1)
        dPhi = Phi - P_ATM ** 2
        dp_gas = dPhi / (np.sqrt(Phi) + P_ATM)                               # sqrt(P^2+d)-P without cancellation
        sig_t = su.sigma_green(T, a_net) + su.sigma_brown(rho_s)
        sig_t_z = su.f_int * su.sigma_green(T, a_net) + su.sigma_brown(rho_s)
        Pi_gas = su.sf_gas * dp_gas / sig_t_z
        dT_int = T.max(axis=-1) - T.min(axis=-1)
        Eg = su.E_green(T, a_net)
        sig_th = Eg * 30e-6 * (2.0 / 3.0) * ex(dT_int) / 0.7
        Pi_th = (sig_th / sig_t).max(axis=-1)
        exo = T.max(axis=-1) - Tf
        # self-heating = hotter than the furnace BECAUSE reactions release heat; a clean Cu part that
        # merely lags the furnace on cooling (emissivity ~0.1) must not count
        exo_gen = np.where(q.max(axis=-1) > 1e3, exo, -np.inf)
        O_ppm = su.O_ppm(X)
        T_sol = thermo.T_solidus_Cu_O(O_ppm)
        melt_margin = (T_sol - su.T_margin) - T                                  # >0 is safe
        # only where closed pores dominate is "gas pressure vs sintering stress" meaningful
        Pi_bloat = np.where(f_cl >= 0.5, (p_g - P_ATM) / PL, 0.0)
        d = dict(
            T=T, Tf=Tf, Tset=np.full(Tf.shape, Tset), b=bf, c=c, C_ppm=C_ppm, X=X, O_ppm=O_ppm, y=y,
            eps=eps, eps_open=eps_open, rho=rho_s, rho_m=rho_m, f_cl=f_cl, G_um=G * 1e6, p_g=p_g, e_dot=e_dot,
            dp_gas=dp_gas, sig_t=sig_t, Pi_gas=Pi_gas.max(axis=-1), Pi_gas_node=Pi_gas, Pi_th=Pi_th,
            exo=exo, exo_gen=exo_gen, dT_int=dT_int, melt_margin=melt_margin.min(axis=-1), Pi_bloat=Pi_bloat.max(axis=-1),
            w_b=w_b, a_net=a_net, xO2=xO2r, xH2=xH2r, xH2O=xH2Or, xCO=xCOr, xCO2=xCO2r,
            x_hc=np.maximum(S_HC, 0.0) / (Fin + np.maximum(S_tot, 0.0)),
            q=q, R_O2=R_O2, eta=eta, PL=PL, eps_rad=epsr, h_tot=h_tot,
        )
        return dY, d
