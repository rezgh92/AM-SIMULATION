"""Fit the sintering viscosity factor f_eta to interrupted-sinter coupons (no dilatometer needed).

    python scripts/calibrate_sintering.py coupons.csv [--base CYCLE.json] [--set key=value ...] [--N 8]
    python scripts/calibrate_sintering.py --demo          # synthetic coupons at f_eta = 0.6, then refit

coupons.csv columns: peak_C, hold_h, kind, value[, sigma]
    kind = rho        value = relative density (0-1), e.g. from Archimedes
    kind = shrink_xy  value = linear shrinkage in the layer plane, %, from calipers
    kind = shrink_z   value = linear shrinkage along the build direction, %
scripts/example_coupons.csv holds synthetic values (the model at f_eta = 0.6 plus noise); replace them
with your measurements. Enter measured powder data with --set first (d50_um, span, phi):
f_eta and D50 trade off against each other.
"""
import argparse
import csv
import json
from pathlib import Path

from cupola.calibrate import Coupon, fit_f_eta, interrupted_cycle, synthetic_coupons
from cupola.cycle import Cycle
from cupola.params import scenario

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = ROOT / "dashboard" / "data" / "synth_default_cycle.json"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="?")
    ap.add_argument("--base", default=str(DEFAULT_BASE), help="cycle JSON whose debind + clean phases the coupons saw")
    ap.add_argument("--set", nargs="*", default=[], metavar="key=value", help="scenario overrides, e.g. d50_um=16")
    ap.add_argument("--N", type=int, default=8)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()

    over = {k: float(v) for k, v in (kv.split("=", 1) for kv in a.set)}
    s = scenario(**over)
    base = Cycle.from_dict(json.loads(Path(a.base).read_text()))
    if a.demo:
        coupons = synthetic_coupons(s, base, 0.6, N=a.N, noise=1.0, seed=1)
        print("demo: synthetic coupons generated at f_eta = 0.60 with 1-sigma measurement noise")
    else:
        if not a.csv:
            ap.error("give a coupons CSV or --demo")
        with open(a.csv, newline="") as fh:
            coupons = [Coupon(float(r["peak_C"]), float(r["hold_h"]), float(r["value"]), r.get("kind", "rho").strip(),
                              float(r["sigma"]) if r.get("sigma") else None) for r in csv.DictReader(fh)]
    for c in coupons:
        cyc = interrupted_cycle(base, c.peak_C, c.hold_h)
        print(f"  {c.peak_C:6.0f} C  {c.hold_h:4.1f} h  {c.kind:9s} {c.value:8.4f}   ({cyc.duration_h():.1f} h cycle)")
    fit = fit_f_eta(s, base, coupons, N=a.N)
    print(f"\nf_eta = {fit['f_eta']:.3f}  (1-sigma {fit['f_eta_lo']:.3f} - {fit['f_eta_hi']:.3f}), "
          f"chi2 = {fit['chi2']:.2f} for {fit['dof']} dof, {fit['n_sim']} simulations")
    for c, p in zip(coupons, fit["predicted"]):
        print(f"  {c.peak_C:6.0f} C {c.hold_h:4.1f} h {c.kind:9s} measured {c.value:8.4f}  model {p:8.4f}")
    print("\nSet 'Sintering viscosity factor' to this value in the dashboard, then re-optimise the cycle.")


if __name__ == "__main__":
    main()
