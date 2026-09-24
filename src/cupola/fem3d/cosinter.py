"""Two-material 3-D co-sintering: copper conductors embedded in a glass-ceramic body.

Every element carries its own material (index into ``setups``), porosity and microstructure state:
grain size for copper, the JMAK crystallisation integral for the glass-ceramic (stored, like the
slab model does, as xi x 1e-6 so that ``Setup.eta0(T, G)`` and ``Setup.dG_dt`` apply unchanged).
Both materials use the Skorohod-Olevsky law, so the mismatch stresses, the constrained densification
of each phase and the part distortion come out of one velocity solve per step.

Boundary conditions: ``bc="setter"`` (bottom face on a setter plate: v_z = 0, Coulomb friction,
gravity) or ``bc="free"`` (3-2-1 support, no gravity, for free camber and verification).
"""
from __future__ import annotations

from typing import Callable, List, Optional, Sequence

import numpy as np
from skfem import MeshHex, Basis, FacetBasis, asm
from skfem.helpers import sym_grad, trace

from ..constants import G_ACC, RHO_CU
from .sinter import (Sinter3D, Frame, ELEM, CENTRE, _dev, _bulk, _sinter_rhs, _gravity)


class CoSinter3D(Sinter3D):
    def __init__(self, mesh: MeshHex, mat: np.ndarray, setups: Sequence, theta0: Sequence[float],
                 micro0: Sequence[float], rho_solid: Sequence[float], mu_f: float = 0.6,
                 gravity: bool = True, bc: str = "setter", v_reg: float = 1e-8):
        super().__init__(mesh, setups[0], float(theta0[0]), float(micro0[0]), mu_f=mu_f, gravity=gravity,
                         aniso=0.0, v_reg=v_reg)
        self.mat = np.asarray(mat, dtype=int)
        self.setups = list(setups)
        self.theta = np.array([theta0[k] for k in self.mat], dtype=float)
        self.G = np.array([micro0[k] for k in self.mat], dtype=float)
        self.rho_s = np.array([rho_solid[k] for k in self.mat], dtype=float)
        self.bc = bc
        if bc == "free":
            self.gravity = False
            self.mu_f = 0.0
            self._free_dofs = self._three_two_one(mesh)

    # ------------------------------------------------------------------ supports
    def _three_two_one(self, mesh):
        """Remove the six rigid-body modes of a free body without restraining its deformation."""
        p = mesh.p
        nd = self.nodal_dofs
        c = p.mean(axis=1)
        z0 = p[2].min()
        bot = np.where(np.isclose(p[2], z0))[0]
        a = bot[np.argmin(np.hypot(p[0, bot] - c[0], p[1, bot] - c[1]))]          # centre of the bottom
        xr = bot[np.argmax(p[0, bot] - p[0, a] - 1e3 * np.abs(p[1, bot] - p[1, a]))] # along +x from a
        yr = bot[np.argmax(p[1, bot] - p[1, a] - 1e3 * np.abs(p[0, bot] - p[0, a]))] # along +y from a
        return np.array([nd[0, a], nd[1, a], nd[2, a], nd[1, xr], nd[2, xr], nd[2, yr]])

    # ------------------------------------------------------------------ constitutive fields
    def _fields(self, T, C_ppm):
        ne = len(self.mat)
        eta = np.empty(ne)
        PL = np.empty(ne)
        th = np.clip(self.theta, 1e-4, 0.999)
        for k, su in enumerate(self.setups):
            sel = self.mat == k
            if not np.any(sel):
                continue
            eta[sel] = su.eta0(T, self.G[sel]) * su.carbon_factor(C_ppm[k])
            PL[sel] = 3.0 * su.gamma / su.r_s * (1.0 - th[sel]) ** 2
        return eta, PL, th

    def _material(self, T: float, C_ppm, b8, b1):
        eta, PL, th = self._fields(T, C_ppm)
        phi = (1.0 - th) ** 2
        psi = (2.0 / 3.0) * (1.0 - th) ** 3 / th
        q8 = b8.X.shape[1]
        kd = np.repeat((2.0 * eta * phi)[:, None], q8, axis=1)
        kb = (2.0 * eta * psi)[:, None]
        A = asm(_dev, b8, kd=kd) + asm(_bulk, b1, kb=kb)
        rhs = asm(_sinter_rhs, b1, pl=PL[:, None])
        if self.gravity:
            rho_b = self.rho_s * (1.0 - th)
            rhs = rhs + asm(_gravity, b8, rg=np.repeat((rho_b * G_ACC)[:, None], q8, axis=1))
        return A, rhs

    def _friction(self, fb, b1):
        th = np.clip(self.theta, 1e-4, 0.999)
        weight = float(np.sum((self.rho_s * (1.0 - th)) * b1.dx[:, 0])) * G_ACC
        area = float(np.sum(fb.dx))
        p_n = weight / max(area, 1e-12)
        vt = fb.interpolate(self.v)
        speed = np.sqrt(vt[0] ** 2 + vt[1] ** 2)
        if not np.any(self.v):
            speed = np.full_like(speed, 1e-3)
        from .sinter import _friction as _fr
        cf = self.mu_f * p_n / np.maximum(speed, self.v_reg)
        return asm(_fr, fb, cf=cf)

    # ------------------------------------------------------------------ one velocity solve
    def solve(self, T: float, C_ppm, picard: int = 8, tol: float = 0.03):
        if self.bc != "free":
            return super().solve(T, C_ppm, picard, tol)
        m = self.mesh()
        b8 = Basis(m, ELEM, intorder=2)
        b1 = Basis(m, ELEM, quadrature=CENTRE)
        A, rhs = self._material(T, C_ppm, b8, b1)
        v = self._linsolve(A, rhs, self._free_dofs, m)
        self.v = v
        edot = trace(sym_grad(b1.interpolate(v)))[:, 0]
        return v, edot

    # ------------------------------------------------------------------ time integration
    def run(self, t_s: np.ndarray, T_K: np.ndarray, C_ppm: Sequence[np.ndarray], max_strain=0.01,
            n_frames=40, progress: Optional[Callable] = None, t_stop: Optional[float] = None):
        """Integrate over a common temperature history and per-material carbon histories."""
        t_end = float(t_s[-1]) if t_stop is None else float(t_stop)
        t = float(t_s[0])
        frame_times = np.linspace(t, t_end, n_frames)
        k_frame = 0
        T_peak_t = float(t_s[int(np.argmax(T_K))])
        while t < t_end - 1e-9:
            T = float(np.interp(t, t_s, T_K))
            if t > T_peak_t and T < 973.15:
                break
            C = [float(np.interp(t, t_s, c)) for c in C_ppm]
            v, edot = self.solve(T, C)
            rate = max(np.max(np.abs(edot)), 1e-12)
            rel = max(np.max(np.abs(edot) * (1.0 - self.theta) / np.maximum(self.theta, 1e-4)), 1e-12)
            dt = min(max_strain / rate, 0.05 / rel, 1800.0, t_end - t)
            dTdt = abs(float(np.interp(t + 60.0, t_s, T_K)) - T) / 60.0
            if dTdt > 0:
                dt = min(dt, max(5.0 / dTdt, 20.0))
            while k_frame < n_frames and frame_times[k_frame] <= t + 1e-9:
                self.frames.append(Frame(t / 3600.0, T - 273.15, self.p.copy(), self.theta.copy(), self.G.copy() * 1e6))
                k_frame += 1
            self.p = self.p + dt * self._vel_nodes(v)
            self.theta = np.clip(1.0 - (1.0 - self.theta) * np.exp(-edot * dt), 1e-4, 0.999)
            for k, su in enumerate(self.setups):
                sel = self.mat == k
                if np.any(sel):
                    self.G[sel] = self.G[sel] + dt * 1e-6 * su.dG_dt(T, self.G[sel], self.theta[sel])
            t += dt
            self.t = t
            if progress:
                progress(t, T, self)
        T = float(np.interp(t, t_s, T_K))
        self.frames.append(Frame(t / 3600.0, T - 273.15, self.p.copy(), self.theta.copy(), self.G.copy() * 1e6))
        return self.frames
