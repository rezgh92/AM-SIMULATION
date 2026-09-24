"""Run a 3-D geometry through the sintering part of a 1-D simulated cycle and export it for the dashboard."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Optional

import numpy as np
from skfem import MeshHex

from ..materials import Setup
from .geometry import GEOMETRIES
from .sinter import Sinter3D, history_from_1d


def surface(mesh: MeshHex):
    """Boundary quads of a hex mesh -> (vertex ids, triangles in local numbering, element of each quad)."""
    bf = mesh.boundary_facets()
    quads = mesh.facets[:, bf].T                         # (nq, 4) node ids, ordered around the face
    f2t = mesh.f2t[0, bf]
    verts, inv = np.unique(quads.ravel(), return_inverse=True)
    q = inv.reshape(-1, 4)
    tris = np.vstack([q[:, [0, 1, 2]], q[:, [0, 2, 3]]])
    return verts, tris, f2t


def node_density(mesh: MeshHex, theta: np.ndarray):
    """Average relative density of the elements sharing each node."""
    acc = np.zeros(mesh.nvertices)
    cnt = np.zeros(mesh.nvertices)
    for k in range(mesh.t.shape[0]):
        np.add.at(acc, mesh.t[k], 1.0 - theta)
        np.add.at(cnt, mesh.t[k], 1.0)
    return acc / np.maximum(cnt, 1)


def run_geometry(name: str, result1d, su: Setup, h: Optional[float] = None, mu_f=0.6, n_frames=24,
                 verbose=True):
    gen = GEOMETRIES[name]
    mesh, info = gen() if h is None else gen(h=h)
    t_s, T_K, C, theta0, G0, t0_h = history_from_1d(result1d)
    s3 = Sinter3D(mesh, su, theta0, G0, mu_f=mu_f)
    t = time.time()
    last = [0.0]

    def prog(tt, T, rho):
        if verbose and time.time() - last[0] > 20:
            last[0] = time.time()
            print(f"   {name}: t={tt/3600:6.2f} h  T={T-273.15:6.0f} C  rho={rho:.4f}  ({time.time()-t:.0f} s)", flush=True)

    frames = s3.run(t_s, T_K, C, n_frames=n_frames, progress=prog)
    return s3, frames, info, t0_h


def summarise(s3: Sinter3D, info: dict):
    p0, p1 = s3.p0, s3.p
    bb0 = np.ptp(p0, axis=1)
    bb1 = np.ptp(p1, axis=1)
    shrink = 1.0 - bb1 / bb0
    out = dict(shrink_bbox_pct=(100 * shrink).tolist(), rho_mean=float(np.mean(1 - s3.theta)),
               rho_min=float(np.min(1 - s3.theta)), rho_max=float(np.max(1 - s3.theta)))
    if info["name"] == "cantilever":
        # tip sag relative to a uniformly shrunk arm: vertical drop of the arm tip top edge
        tip = p0[0] > p0[0].max() - 1e-9
        top = p0[2] > p0[2].max() - 1e-9
        sel = tip & top
        z_free = p0[2][sel] * (1 - shrink[2])                  # where it would be with no gravity
        out["tip_sag_mm"] = float(np.mean(z_free - p1[2][sel]) * 1e3)
    if info["name"] == "ring":
        # out-of-roundness at top vs bottom (setter friction elephant-foot)
        c = p1[:2].mean(axis=1, keepdims=True)
        r = np.hypot(*(p1[:2] - c))
        z = p1[2]
        outer = np.hypot(*(p0[:2] - p0[:2].mean(axis=1, keepdims=True))) > (info["Ro"] - 0.6 * info["h"]) * 1e-3
        bot = outer & (z < z.min() + 1e-6)
        topn = outer & (z > z.max() - 1e-6)
        out["OD_bottom_mm"] = float(2 * r[bot].mean() * 1e3)
        out["OD_top_mm"] = float(2 * r[topn].mean() * 1e3)
    if info["name"] == "heat_sink":
        z = p1[2]
        out["height_mm"] = float(np.ptp(z) * 1e3)
    return out


def export(s3: Sinter3D, frames, info: dict, summary: dict, path: Path, t0_h: float):
    m0 = MeshHex(s3.p0, s3.t_conn)
    verts, tris, _ = surface(m0)
    centre = s3.p0[:, verts].mean(axis=1, keepdims=True)
    def q(p):   # micrometres, integers, relative to the green centroid
        return np.round((p[:, verts] - centre) * 1e6).astype(int).T.ravel().tolist()
    fr = []
    for f in frames:
        mf = MeshHex(f.p, s3.t_conn)
        rho = node_density(mf, f.theta)[verts]
        fr.append(dict(t_h=round(f.t_h + t0_h, 3), T_C=round(f.T_C, 1), p=q(f.p),
                       rho=np.round(rho * 1000).astype(int).tolist(),
                       rho_mean=round(float(np.mean(1 - f.theta)), 4)))
    data = dict(name=info["name"], info=info, summary=summary, tris=tris.ravel().tolist(),
                n_vert=int(len(verts)), frames=fr, units="um, rho x1000")
    path.write_text(json.dumps(data, separators=(",", ":")))
    return data
