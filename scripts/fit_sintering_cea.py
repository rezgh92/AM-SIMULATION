"""Reproduce the default sintering viscosity factor f_eta = 0.28 from the CEA-LITEN anchor.

CEA-LITEN DLP copper: 22 um air-atomised powder, 60 vol%, 400 C / 4 h air debind, 1050 C / 4 h
H2 sinter -> 90-94 % relative density (Roumanie et al.). Air debinding at 400 C leaves little
carbon, so the final density isolates the sintering kinetics.
"""
import numpy as np
from multiprocessing import Pool
from cupola.validation import cea_case


def run(fe):
    return fe, cea_case(f_eta=fe).kpi["rho_final"]


def main():
    fes = [0.15, 0.2, 0.3, 0.45]
    with Pool(4) as p:
        res = p.map(run, fes)
    fe = np.array([r[0] for r in res]); rho = np.array([r[1] for r in res])
    o = np.argsort(rho)
    for tgt in (0.90, 0.92, 0.94):
        print(f"rho = {tgt}: f_eta = {np.exp(np.interp(tgt, rho[o], np.log(fe[o]))):.3f}")


if __name__ == "__main__":
    main()
