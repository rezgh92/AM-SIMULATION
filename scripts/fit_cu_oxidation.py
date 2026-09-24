"""Reproduce the Cu oxidation law used in cupola.materials (CUOX_K350, CUOX_M).

Law:  dX/dt = K(T) (10 um / d50)^2 (1 - X) / (X + X0)^m,  X = mol O / mol Cu, in air.
E is fixed at 100 kJ/mol (mid-literature Cu2O growth); K(350 C) and m are fitted to the
two intrinsic powder points of Ott (Diss. Univ. des Saarlandes 2022, Fig. 5.2):
12.7 um OFHC powder at 350 C in synthetic air: +7-8 wt% after 60 min, +9.75-10.16 wt% after 300 min.

Roumanie et al. compact data (400/600/800 C) are NOT used here; they are an out-of-sample
check in cupola.validation (the 1-D model adds pore filling by oxide, which a fit cannot).
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

R = 8.314462618
WT = 15.999 / 63.546
X0 = 2e-3
E = 100e3
DATA = [(12.7, 350.0, 3600.0, 0.0750 / WT), (12.7, 350.0, 18000.0, 0.0995 / WT)]


def sim(lnK, m, d, Tc, t_end):
    T = Tc + 273.15
    k = np.exp(lnK) * np.exp(-(E / R) * (1 / T - 1 / 623.15)) * (10.0 / d) ** 2
    f = lambda t, y: [k * max(1 - y[0], 0) / (max(y[0], 0) + X0) ** m]
    return solve_ivp(f, (0, t_end), [X0], method="LSODA", rtol=1e-9, atol=1e-12).y[0, -1]


def main():
    res = least_squares(lambda p: [np.log(sim(p[0], p[1], *d[:3]) / d[3]) for d in DATA],
                        [np.log(1e-6), 3.0], bounds=([-40, 0], [5, 12]))
    lnK, m = res.x
    print(f"K(350 C) = {np.exp(lnK):.4e} 1/s   m = {m:.3f}   (cost {res.cost:.2e})")
    for d, T, t, Xm in DATA:
        print(f"  {d} um {T} C {t/60:.0f} min: measured {Xm*WT*100:.2f} wt%, fit {sim(lnK, m, d, T, t)*WT*100:.2f} wt%")


if __name__ == "__main__":
    main()
