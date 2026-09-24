"""3-D sintering FEM against the closed-form free-body solution and mass conservation."""
import numpy as np
import pytest
from scipy.integrate import solve_ivp

from cupola.fem3d.geometry import cube
from cupola.fem3d.sinter import Sinter3D
from cupola.materials import Setup, THETA_PIN
from cupola.params import defaults

T_K = 1050.0 + 273.15
THETA0, G0 = 0.40, 5e-6


def closed_form(su, t_end):
    """Stress-free body: 2 eta psi tr(e) + P_L = 0, so d theta/dt = -(1 - theta) P_L / (2 eta psi)."""
    def rhs(t, y):
        th, G = y
        eta = su.eta0(T_K, G)
        psi = (2.0 / 3.0) * (1.0 - th) ** 3 / th
        PL = 3.0 * su.gamma / su.r_s * (1.0 - th) ** 2
        pin = THETA_PIN / (th + THETA_PIN)
        return [-(1.0 - th) * PL / (2.0 * eta * psi), su.kG_rate(T_K) / (3.0 * G ** 2) * pin ** 2]
    sol = solve_ivp(rhs, (0.0, t_end), [THETA0, G0], method="LSODA", rtol=1e-9, atol=1e-12)
    return sol.y[0, -1]


@pytest.fixture(scope="module")
def free_cube():
    su = Setup(defaults())
    mesh, _ = cube(size=2.0, h=0.5)
    # no gravity, no anisotropy, near-frictionless setter: the body should shrink homogeneously
    s3 = Sinter3D(mesh, su, THETA0, G0, mu_f=1e-3, gravity=False, aniso=0.0)
    vol0 = Sinter3D._elem_volumes(s3.mesh())
    s3.run(np.array([0.0, 3600.0]), np.array([T_K, T_K]), np.array([0.0, 0.0]), n_frames=2)
    return su, s3, vol0


def test_free_cube_matches_closed_form(free_cube):
    su, s3, _ = free_cube
    rho_ref = 1.0 - closed_form(su, 3600.0)
    rho = 1.0 - s3.theta
    assert rho_ref > 1.0 - THETA0 + 0.05                  # the hold densifies measurably
    assert np.mean(rho) == pytest.approx(rho_ref, rel=5e-3)
    assert np.ptp(rho) < 2e-3                              # homogeneous
    shrink = 1.0 - np.ptp(s3.p, axis=1) / np.ptp(s3.p0, axis=1)
    assert np.ptp(shrink) < 2e-3                           # isotropic
    # linear shrinkage consistent with the density change: (1 - s)^3 = rho0 / rho
    assert np.mean(shrink) == pytest.approx(1.0 - ((1.0 - THETA0) / np.mean(rho)) ** (1.0 / 3.0), rel=1e-2)


def test_free_cube_conserves_mass(free_cube):
    _, s3, vol0 = free_cube
    m0 = np.sum((1.0 - THETA0) * vol0)
    m1 = np.sum((1.0 - s3.theta) * Sinter3D._elem_volumes(s3.mesh()))
    assert m1 == pytest.approx(m0, rel=2e-3)
