"""Thermal-mismatch stress and warpage on cooling a co-fired Cu / glass-ceramic stack.

Copper is elastic-perfectly plastic with a temperature-dependent yield stress; the glass-ceramic is
elastic. Stresses start at the stress-free temperature T_sf, below which the residual glass can no
longer relax them. Output: copper stress, glass-ceramic stress and bow over a 20 mm span versus
temperature, for several copper-to-body thickness ratios, plus the purely elastic reference.
"""
import json, sys
import numpy as np
from cupola.cofire.mechanics import ThermoMech, cooling_bilayer, warpage_from_curvature
from cupola.cofire import props

if __name__ == "__main__":
    out = sys.argv[1]
    cu = ThermoMech(E=props.CU_E, nu=props.CU_NU, alpha=props.cu_alpha, yield_=props.cu_yield)
    cu_el = ThermoMech(E=props.CU_E, nu=props.CU_NU, alpha=props.cu_alpha, yield_=None)
    gc = ThermoMech(E=props.GC_E, nu=props.GC_NU, alpha=props.gc_alpha)
    res = dict(T_sf=props.GC_T_SF, cases=[])
    h_gc = 1.0e-3
    for h_cu_um in (10.0, 20.0, 50.0, 100.0, 200.0):
        h_cu = h_cu_um * 1e-6
        for label, m1 in (("plastic", cu), ("elastic", cu_el)):
            T, kap, s1, s2, ep = cooling_bilayer(props.GC_T_SF, 25.0, h_cu, h_gc, m1, gc)
            res["cases"].append(dict(h_cu_um=h_cu_um, model=label, T=T.tolist(), kappa=kap.tolist(),
                                     s_cu_MPa=(s1 / 1e6).tolist(), s_gc_MPa=(s2 / 1e6).tolist(), eps_p=ep.tolist(),
                                     bow_um_20mm=(warpage_from_curvature(kap, 20e-3) * 1e6).tolist()))
            print(f"h_cu {h_cu_um:5.0f} um {label:8s} Cu stress {s1[-1]/1e6:7.1f} MPa  GC {s2[-1]/1e6:6.1f} MPa  "
                  f"bow {warpage_from_curvature(kap[-1], 20e-3)*1e6:7.1f} um")
    # stress-free temperature sensitivity at 50 um copper
    for Tsf in (500.0, 600.0, 700.0, 800.0):
        T, kap, s1, s2, ep = cooling_bilayer(Tsf, 25.0, 50e-6, h_gc, cu, gc)
        res.setdefault("Tsf_scan", []).append(dict(T_sf=Tsf, s_cu_MPa=float(s1[-1] / 1e6),
                                                   bow_um_20mm=float(warpage_from_curvature(kap[-1], 20e-3) * 1e6)))
    json.dump(res, open(out, "w"))
