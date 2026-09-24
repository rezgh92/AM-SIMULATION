"""Voxel geometries for the 3-D model. Units: mm; z is the build (and gravity) direction.

Voxel meshes are exactly what an LCM printer builds (layers of pixels), so a hex mesh on the
voxel grid is a faithful representation of the green part, and it is trivially robust.
"""
from __future__ import annotations

import numpy as np
from skfem import MeshHex


def mesh_from_mask(mask: np.ndarray, h: float) -> MeshHex:
    """Hex mesh of the True voxels of a (nx, ny, nz) boolean mask with voxel size h (mm -> m)."""
    nx, ny, nz = mask.shape
    x = np.arange(nx + 1) * h * 1e-3
    y = np.arange(ny + 1) * h * 1e-3
    z = np.arange(nz + 1) * h * 1e-3
    m = MeshHex.init_tensor(x, y, z)
    c = m.p[:, m.t].mean(axis=1) / (h * 1e-3)
    ix = np.floor(c[0]).astype(int)
    iy = np.floor(c[1]).astype(int)
    iz = np.floor(c[2]).astype(int)
    keep = mask[ix, iy, iz]
    return m.remove_elements(np.where(~keep)[0])


def cantilever(h=0.5):
    """Column 6 x 6 x 8 mm with an 18 mm arm (2 mm thick) at the top: the gravity-slump probe.

    The tip deflection is the deviatoric measurement that separates the shear viscosity from the
    sintering-stress/bulk-viscosity ratio, which free dilatometry cannot.
    """
    L, W, H, arm, t = 24.0, 6.0, 10.0, 18.0, 2.0
    nx, ny, nz = int(round(L / h)), int(round(W / h)), int(round(H / h))
    m = np.zeros((nx, ny, nz), bool)
    col = int(round(6.0 / h))
    m[:col, :, :] = True
    m[:, :, nz - int(round(t / h)):] = True
    return mesh_from_mask(m, h), dict(name="cantilever", L=L, W=W, H=H, arm=arm, t=t, h=h)


def heat_sink(h=0.75):
    """24 x 24 mm base (3 mm) with five 1.5 mm fins 10 mm tall: a typical copper thermal part."""
    B, tb, Hf, tf, nf = 24.0, 3.0, 10.0, 1.5, 5
    n = int(round(B / h))
    nzb, nzf = int(round(tb / h)), int(round(Hf / h))
    m = np.zeros((n, n, nzb + nzf), bool)
    m[:, :, :nzb] = True
    pitch = B / nf
    xs = np.arange(n) * h + h / 2
    for k in range(nf):
        x0 = k * pitch + (pitch - tf) / 2
        sel = (xs >= x0) & (xs < x0 + tf)
        m[sel, :, nzb:] = True
    return mesh_from_mask(m, h), dict(name="heat_sink", B=B, tb=tb, Hf=Hf, tf=tf, nf=nf, h=h)


def ring(h=0.6):
    """Hollow cylinder, 20 mm OD, 12 mm ID, 12 mm tall (waveguide / RF cavity-like)."""
    Ro, Ri, H = 10.0, 6.0, 12.0
    n = int(round(2 * Ro / h))
    nz = int(round(H / h))
    xs = (np.arange(n) + 0.5) * h - Ro
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    r = np.hypot(X, Y)
    ann = (r <= Ro) & (r >= Ri)
    m = np.repeat(ann[:, :, None], nz, axis=2)
    return mesh_from_mask(m, h), dict(name="ring", Ro=Ro, Ri=Ri, H=H, h=h)


def cube(size=6.0, h=1.0):
    n = int(round(size / h))
    return mesh_from_mask(np.ones((n, n, n), bool), h), dict(name="cube", size=size, h=h)


GEOMETRIES = {"cantilever": cantilever, "heat_sink": heat_sink, "ring": ring, "cube": cube}
