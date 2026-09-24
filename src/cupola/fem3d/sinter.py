"""3-D Skorohod-Olevsky viscous sintering on a voxel hex mesh (updated Lagrangian, velocity form).

Constitutive law (Olevsky 1998), per element:
    sigma = 2 eta [ phi(theta) e' + psi(theta) tr(e) I ] + P_L(theta) I + P_aniso
    phi = (1-theta)^2,  psi = (2/3)(1-theta)^3/theta,  P_L = (3 gamma / r) (1-theta)^2
    P_aniso = P_L a (theta/theta0) diag(-1/3, -1/3, 2/3)   (extra build-direction shrinkage)
Equilibrium  div sigma + rho_bulk g = 0, with
    bottom face on the setter:  v_z = 0  and Coulomb friction t = -mu p_n v_t/|v_t| (regularised, lagged)
State update per element: d theta/dt = (1 - theta) tr(e),  grain growth as in the 1-D model.

eta(T, G, C) is the same function the 1-D model uses (Frost & Ashby diffusional creep x f_eta x
carbon inhibition), so a free cube must reproduce the 1-D densification exactly (tests/test_fem3d.py).
Volumetric terms use one-point quadrature (selective reduced integration) to avoid locking as
theta -> 0, where the bulk/shear viscosity ratio 2 psi/phi grows without bound.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional

import numpy as np
from scipy.sparse.linalg import spsolve
from skfem import (MeshHex, ElementHex1, ElementVector, Basis, FacetBasis, BilinearForm, LinearForm,
                   asm, condense)
from skfem.helpers import sym_grad, ddot, trace

from ..constants import G_ACC, RHO_CU
from ..materials import Setup, THETA_PIN

try:
    import pyamg
except ImportError:     # pragma: no cover
    pyamg = None

ELEM = ElementVector(ElementHex1())
CENTRE = (np.array([[0.5], [0.5], [0.5]]), np.array([1.0]))


@BilinearForm
def _dev(u, v, w):
    Eu, Ev = sym_grad(u), sym_grad(v)
    return w["kd"] * (ddot(Eu, Ev) - trace(Eu) * trace(Ev) / 3.0)


@BilinearForm
def _bulk(u, v, w):
    return w["kb"] * trace(sym_grad(u)) * trace(sym_grad(v))


@BilinearForm
def _friction(u, v, w):
    return w["cf"] * (u[0] * v[0] + u[1] * v[1])


@LinearForm
def _sinter_rhs(v, w):
    return -w["pl"] * trace(sym_grad(v))


@LinearForm
def _aniso_rhs(v, w):
    E = sym_grad(v)
    # P_aniso = pa * diag(-1/3, -1/3, 2/3)
    return -w["pa"] * (-E[0, 0] / 3.0 - E[1, 1] / 3.0 + 2.0 * E[2, 2] / 3.0)


@LinearForm
def _gravity(v, w):
    return -w["rg"] * v[2]


@dataclass
class Frame:
    t_h: float
    T_C: float
    p: np.ndarray            # node coordinates (3, nnodes), m
    theta: np.ndarray        # element porosity
    G_um: np.ndarray         # element grain size


class Sinter3D:
    def __init__(self, mesh: MeshHex, su: Setup, theta0: float, G0_m: float, mu_f: float = 0.6,
                 gravity: bool = True, aniso: Optional[float] = None, v_reg: float = 1e-8):
        self.t_conn = mesh.t.copy()
        self.p = mesh.p.copy()
        self.p0 = mesh.p.copy()
        self.su = su
        ne = mesh.nelements
        self.theta = np.full(ne, float(theta0))
        self.theta0 = float(theta0)
        self.G = np.full(ne, float(G0_m))
        self.mu_f = mu_f
        self.gravity = gravity
        self.aniso = su.aniso if aniso is None else aniso
        self.v_reg = v_reg
        z = self.p[2]
        self.bottom_nodes = np.where(np.isclose(z, z.min()))[0]
        self.v = np.zeros(3 * mesh.nvertices)
        self.frames: List[Frame] = []
        self.t = 0.0
        self.nodal_dofs = Basis(mesh, ELEM, intorder=2).nodal_dofs

    def mesh(self):
        return MeshHex(self.p, self.t_conn)

    # ------------------------------------------------------------------ one velocity solve
    def solve(self, T: float, C_ppm: float, picard: int = 8, tol: float = 0.03):
        """Velocity solve with Picard iterations on the regularised Coulomb friction law.

        The material operator and load are assembled once per step; each friction iteration only
        re-assembles the small boundary term and re-solves with a warm start.
        """
        m = self.mesh()
        b8 = Basis(m, ELEM, intorder=2)
        b1 = Basis(m, ELEM, quadrature=CENTRE)
        A0, rhs = self._material(T, C_ppm, b8, b1)
        fac = m.facets_satisfying(lambda x: np.isclose(x[2], self.p[2].min()))
        fb = FacetBasis(m, ELEM, facets=fac, intorder=2) if len(fac) else None
        D = b8.nodal_dofs[2, self.bottom_nodes]
        v_prev = None
        for it in range(picard):
            A = A0 + (self._friction(fb, b1) if fb is not None else 0 * A0)
            v = self._linsolve(A, rhs, D, m)
            self.v = v
            vb = self._vel_nodes(v)[:2, self.bottom_nodes]
            if v_prev is not None:
                dvn = np.linalg.norm(vb - v_prev) / max(np.linalg.norm(vb), 1e-30)
                if dvn < tol:
                    break
            v_prev = vb
        dv = b1.interpolate(v)
        edot = trace(sym_grad(dv))[:, 0]
        return v, edot

    def _rigid_modes(self, m, I):
        nd = self.nodal_dofs
        x, y, z = m.p
        n = 3 * m.nvertices
        B = np.zeros((n, 6))
        for k in range(3):
            B[nd[k], k] = 1.0
        B[nd[0], 3], B[nd[1], 3] = -y, x
        B[nd[1], 4], B[nd[2], 4] = -z, y
        B[nd[0], 5], B[nd[2], 5] = z, -x
        return B[I]

    def _linsolve(self, A, rhs, D, m):
        Ac, bc, xc, I = condense(A, rhs, D=D)
        Ac = Ac.tocsr()
        x0 = self.v[I] if np.any(self.v) else None
        if pyamg is not None and Ac.shape[0] > 3000:
            # rebuild the AMG hierarchy every few steps; in between it preconditions CG on a matrix that
            # has changed only slightly (small strain per step)
            if getattr(self, "_ml", None) is None or self._ml_age >= 6 or self._ml_n != Ac.shape[0]:
                self._ml = pyamg.smoothed_aggregation_solver(Ac, B=self._rigid_modes(m, I), symmetry="symmetric",
                                                             max_coarse=500)
                self._ml_age, self._ml_n = 0, Ac.shape[0]
            self._ml_age += 1
            from scipy.sparse.linalg import cg
            x, info = cg(Ac, bc, x0=x0, rtol=1e-9, maxiter=500, M=self._ml.aspreconditioner(cycle="V"))
            if info != 0:          # fall back to a fresh hierarchy
                self._ml = pyamg.smoothed_aggregation_solver(Ac, B=self._rigid_modes(m, I), symmetry="symmetric")
                x = self._ml.solve(bc, x0=x0, tol=1e-9, accel="cg", maxiter=800)
        else:
            x = spsolve(Ac.tocsc(), bc)
        v = np.zeros(A.shape[0])
        v[I] = x
        return v

    def _friction(self, fb, b1):
        th = np.clip(self.theta, 1e-4, 0.999)
        weight = float(np.sum((RHO_CU * (1.0 - th)) * b1.dx[:, 0])) * G_ACC
        area = float(np.sum(fb.dx))
        p_n = weight / max(area, 1e-12)
        vt = fb.interpolate(self.v)
        speed = np.sqrt(vt[0] ** 2 + vt[1] ** 2)
        if not np.any(self.v):
            speed = np.full_like(speed, 1e-3)      # start sliding; Picard settles stick/slip
        cf = self.mu_f * p_n / np.maximum(speed, self.v_reg)
        return asm(_friction, fb, cf=cf)

    def _material(self, T: float, C_ppm: float, b8, b1):
        su = self.su
        th = np.clip(self.theta, 1e-4, 0.999)
        eta = su.eta0(T, self.G) * (1.0 + (C_ppm / su.C_inh) ** 2)
        phi = (1.0 - th) ** 2
        psi = (2.0 / 3.0) * (1.0 - th) ** 3 / th
        PL = 3.0 * su.gamma / su.r_s * (1.0 - th) ** 2
        pa = PL * self.aniso * (th / self.theta0)
        q8 = b8.X.shape[1]
        kd = np.repeat((2.0 * eta * phi)[:, None], q8, axis=1)
        kb = (2.0 * eta * psi)[:, None]
        A = asm(_dev, b8, kd=kd) + asm(_bulk, b1, kb=kb)
        rhs = asm(_sinter_rhs, b1, pl=PL[:, None]) + asm(_aniso_rhs, b8, pa=np.repeat(pa[:, None], q8, axis=1))
        if self.gravity:
            rho_b = RHO_CU * (1.0 - th)
            rhs = rhs + asm(_gravity, b8, rg=np.repeat((rho_b * G_ACC)[:, None], q8, axis=1))
        return A, rhs

    @staticmethod
    def _elem_volumes(m):
        b = Basis(m, ElementHex1(), quadrature=CENTRE)
        return b.dx[:, 0]

    # ------------------------------------------------------------------ time integration
    def run(self, t_s: np.ndarray, T_K: np.ndarray, C_ppm: np.ndarray, max_strain=0.01, n_frames=40,
            progress: Optional[Callable] = None):
        """Integrate over the given temperature/carbon history (piecewise-linear in time)."""
        t_end = float(t_s[-1])
        t = float(t_s[0])
        frame_times = np.linspace(t, t_end, n_frames)
        k_frame = 0
        dt = 60.0
        T_peak_t = float(t_s[int(np.argmax(T_K))])
        while t < t_end - 1e-9:
            T = float(np.interp(t, t_s, T_K))
            if t > T_peak_t and T < 973.15:        # cooled below 700 C: deformation is frozen
                break
            C = float(np.interp(t, t_s, C_ppm))
            v, edot = self.solve(T, C)
            # step limits: element strain increment <= max_strain, and relative porosity change <= 5 %
            # (the porosity equation stiffens as theta -> 0 even though the strain rate falls)
            rate = max(np.max(np.abs(edot)), 1e-12)
            rel = max(np.max(np.abs(edot) * (1.0 - self.theta) / np.maximum(self.theta, 1e-4)), 1e-12)
            dt = min(max_strain / rate, 0.05 / rel, 3600.0, t_end - t)
            # temperature budget: at most 10 K change per step (eta is strongly T-dependent)
            dTdt = abs(float(np.interp(t + 60.0, t_s, T_K)) - T) / 60.0
            if dTdt > 0:
                dt = min(dt, max(10.0 / dTdt, 30.0))
            while k_frame < n_frames and frame_times[k_frame] <= t + 1e-9:
                self.frames.append(Frame(t / 3600.0, T - 273.15, self.p.copy(), self.theta.copy(), self.G.copy() * 1e6))
                k_frame += 1
            self.p = self.p + dt * self._vel_nodes(v)
            # exact for constant edot and mass-conserving: relative density scales as 1/volume
            self.theta = np.clip(1.0 - (1.0 - self.theta) * np.exp(-edot * dt), 1e-4, 0.999)
            pin = THETA_PIN / (self.theta + THETA_PIN)
            self.G = self.G + dt * self.su.kG_rate(T) / (3.0 * self.G ** 2) * pin ** 2
            t += dt
            self.t = t
            if progress:
                progress(t, T, float(np.mean(1.0 - self.theta)))
        T = float(np.interp(t, t_s, T_K))
        self.frames.append(Frame(t / 3600.0, T - 273.15, self.p.copy(), self.theta.copy(), self.G.copy() * 1e6))
        return self.frames

    def _vel_nodes(self, v):
        nd = self.nodal_dofs
        return np.vstack([v[nd[0]], v[nd[1]], v[nd[2]]])


def history_from_1d(result, t_start_h: Optional[float] = None):
    """Extract (t_s, T_K, C_ppm, theta0, G0) for the 3-D run from a 1-D simulation Result.

    The 3-D run starts when the binder is gone (nothing sinters before that) or at t_start_h.
    """
    S = result.series
    t_h = result.t_h
    if t_start_h is None:
        # start once the binder is gone AND the part is hot enough for copper to sinter (below ~600 C
        # the 1-D densification is < 0.1 %, and 3-D steps there are pure cost)
        idx = np.where((S["binder_left"] < 1e-3) & (0.5 * (S["T_center"] + S["T_surface"]) > 600.0))[0]
        i0 = int(idx[0]) if idx.size else 0
    else:
        i0 = int(np.searchsorted(t_h, t_start_h))
    t_s = (t_h[i0:] - t_h[i0]) * 3600.0
    T_K = 0.5 * (S["T_center"][i0:] + S["T_surface"][i0:]) + 273.15
    C = S["C_ppm_mean"][i0:]
    # the 3-D model is oxide-free copper: start from the metal-equivalent density, not the skeleton
    # density (which includes the volume of any oxide grown during an oxidising debind)
    theta0 = 1.0 - float(S["rho_m_mean"][i0])
    G0 = float(S["G_um"][i0]) * 1e-6
    return t_s, T_K, C, theta0, G0, float(t_h[i0])
