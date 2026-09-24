"""Stiff integration: Shampine & Reichelt (1997) Rosenbrock 2(3) pair ("ode23s").

L-stable, one Jacobian and one LU per step, a third-order error estimate, and FSAL.
Chosen because it is short enough to implement identically in the JavaScript
dashboard, so both implementations run the same algorithm and can be compared to
round-off. The Jacobian is a forward-difference one evaluated in a single batched
call of the vectorised right-hand side.
"""
from __future__ import annotations

import math
import numpy as np
from scipy.linalg import lu_factor, lu_solve

D_ROS = 1.0 / (2.0 + math.sqrt(2.0))
E32 = 6.0 + math.sqrt(2.0)


class StepFailure(RuntimeError):
    pass


def fd_jacobian(f, t, y, f0, scale):
    n = y.size
    dy = 1e-7 * np.maximum(np.abs(y), scale)
    Yp = np.repeat(y[None, :], n, axis=0)
    Yp[np.arange(n), np.arange(n)] += dy
    Fp = f(t, Yp)
    return ((Fp - f0[None, :]) / dy[:, None]).T


def ode23s(f, t0, t1, y0, atol, rtol=1e-4, h0=None, scale=None, h_max=np.inf, callback=None,
           max_steps=200_000, jac_every=1):
    """Integrate y' = f(t, y) from t0 to t1. f must accept batched y of shape (B, n).

    ``jac_every``: refresh the Jacobian every k accepted steps (and always after a rejection).
    The underlying Wolfbrandt formula is a W-method, so the second-order solution keeps its order
    with an approximate Jacobian; k=1 reproduces the classic ode23s exactly.

    Returns (ts, ys, n_steps, n_rejected). ``callback(t, y)`` may return True to stop early.
    """
    y = np.array(y0, dtype=float)
    n = y.size
    scale = np.ones(n) if scale is None else scale
    atol = np.broadcast_to(atol, (n,)).astype(float)
    t = float(t0)
    span = t1 - t0
    if span <= 0:
        return [t], [y.copy()], 0, 0
    F0 = f(t, y)
    if h0 is None:
        d0 = np.linalg.norm(y / (atol + rtol * np.abs(y))) / math.sqrt(n)
        d1 = np.linalg.norm(F0 / (atol + rtol * np.abs(y))) / math.sqrt(n)
        h = 0.01 * d0 / d1 if (d0 > 1e-5 and d1 > 1e-5) else 1e-3
        h = min(max(h, 1e-6), 0.1 * span)
    else:
        h = min(h0, span)
    ts, ys = [t], [y.copy()]
    nstep = nrej = 0
    I = np.eye(n)
    J = None
    since_jac = 0
    while t < t1:
        if nstep > max_steps:
            raise StepFailure(f"too many steps at t={t:.1f}")
        h = min(h, h_max, t1 - t)
        if t + 1.01 * h >= t1:
            h = t1 - t
        if J is None or since_jac >= jac_every:
            J = fd_jacobian(f, t, y, F0, scale)
            dt_fd = 1e-7 * max(abs(t), 1.0)
            Ft = (f(t + dt_fd, y) - F0) / dt_fd
            since_jac = 0
        fresh = since_jac == 0
        while True:
            W = I - h * D_ROS * J
            try:
                lu = lu_factor(W, check_finite=False)
            except Exception as exc:          # pragma: no cover
                raise StepFailure(str(exc))
            k1 = lu_solve(lu, F0 + h * D_ROS * Ft)
            F1 = f(t + 0.5 * h, y + 0.5 * h * k1)
            k2 = lu_solve(lu, F1 - k1) + k1
            ynew = y + h * k2
            F2 = f(t + h, ynew)
            k3 = lu_solve(lu, F2 - E32 * (k2 - F1) - 2.0 * (k1 - F0) + h * D_ROS * Ft)
            err_vec = (h / 6.0) * (k1 - 2.0 * k2 + k3)
            sc = atol + rtol * np.maximum(np.abs(y), np.abs(ynew))
            err = np.max(np.abs(err_vec) / sc)
            if not np.all(np.isfinite(ynew)) or not np.isfinite(err):
                err = 1e10
            if err <= 1.0:
                break
            nrej += 1
            if not fresh:                       # stale Jacobian: refresh before shrinking the step
                J = fd_jacobian(f, t, y, F0, scale)
                dt_fd = 1e-7 * max(abs(t), 1.0)
                Ft = (f(t + dt_fd, y) - F0) / dt_fd
                since_jac = 0
                fresh = True
                continue
            h = h * max(0.1, 0.8 * err ** (-1.0 / 3.0))
            # floor at floating-point resolution of t: fast gas transients after a segment switch
            # (ms time constants) must be resolvable even hundreds of hours into a cycle
            if h < 64.0 * np.finfo(float).eps * max(1.0, abs(t)):
                raise StepFailure(f"step size underflow at t={t:.3f}")
        t = t + h
        y = ynew
        F0 = F2
        nstep += 1
        since_jac += 1
        ts.append(t)
        ys.append(y.copy())
        if callback is not None and callback(t, y):
            break
        fac = min(5.0, max(0.2, 0.8 * max(err, 1e-10) ** (-1.0 / 3.0)))
        h = h * fac
    return ts, ys, nstep, nrej
