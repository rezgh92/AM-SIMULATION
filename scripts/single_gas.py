"""Single-gas programmes compared with the two-furnace plan, plus validation of the comparison.

Debinding in one gas only (N2, or air) and sintering in one gas only (N2, H2, premixed 5 % H2, or
air) against the recommended mixed-gas programmes D2, S1 and S2 of scripts/two_furnace.py. Every
single-gas sintering programme uses the same temperatures and times as S2, so only the gas differs.
Each pairing is also run with 3 % and 8 % char and 2 mm and 8 mm walls.

Validation:
  - numerics: the best pairing of each family again with 12 nodes and with rtol 1e-5;
  - literature: the published copper processes the model can be held against (CEA-LITEN, Fraunhofer
    IFAM with and without solvent debinding, Roumanie compact oxidation and argon char).

    python scripts/single_gas.py <out.json> [workers]
    python scripts/single_gas.py --phases <out.json>      (self-heating per furnace, published vs yours)
"""
import json, sys, time, itertools
from multiprocessing import Pool
import numpy as np

from cupola.cycle import Cycle, Segment
from cupola.params import scenario as make_scenario
from cupola.simulate import simulate, verdict
from cupola.materials import Setup
from cupola import validation as V

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import two_furnace as TF                                      # noqa: E402

AIR = TF.AIR
seg = TF.seg

# ------------------------------------------------------------------ one gas per furnace
DEBIND = {
    "N2": dict(name="N2 only", gas="N2",
               segs=[seg(470, 1.0, 1.0, note="binder pyrolysis, N2"), seg(25, 3.0, 0.0, note="cool, N2")]),
    "AIR": dict(name="Air only", gas="air",
                segs=[seg(150, 1.0, 0.5, O2=AIR, note="solvent out, air"),
                      seg(380, 0.5, 2.0, O2=AIR, note="burnout, air"),
                      seg(25, 3.0, 0.0, O2=AIR, note="cool, air")]),
    "AIR-SLOW": dict(name="Air only, slow (IFAM schedule)", gas="air",
                     segs=[seg(120, 1.0, 24.0, O2=AIR, note="air"),
                           seg(250, 1.0, 63.0, O2=AIR, note="oxidative debind, air"),
                           seg(25, 3.0, 0.0, O2=AIR, note="cool, air")]),
    "D2": dict(name="Recommended: N2, then 1 % O2", gas="N2; 5 % air in N2", segs=TF.DEBIND["D2"]["segs"]),
}


def sinter_single(O2=0.0, H2=0.0, label=""):
    """Same temperatures and times as S2, one gas throughout."""
    return [seg(700, 5.0, 4.0, O2=O2, H2=H2, note=f"700 C hold, {label}"),
            seg(1050, 5.0, 4.0, O2=O2, H2=H2, note=f"sinter, {label}"),
            seg(600, 5.0, 0.0, O2=O2, H2=H2, note=f"cool, {label}"),
            seg(25, 5.0, 0.0, O2=O2, H2=H2, note=f"cool, {label}")]


SINTER = {
    "N2": dict(name="N2 only", gas="N2", segs=sinter_single(label="N2")),
    "H2": dict(name="H2 only", gas="100 % H2", segs=sinter_single(H2=1.0, label="100 % H2")),
    "FG": dict(name="Forming gas only", gas="5 % H2 in N2 (premixed)", segs=sinter_single(H2=TF.FG, label="5 % H2")),
    "AIR": dict(name="Air only", gas="air", segs=sinter_single(O2=AIR, label="air")),
    "S1": dict(name="Recommended S1: N2, 1 % H2, 5 % H2", gas="N2; 1 % H2; 5 % H2", segs=TF.SINTER["S1"]["segs"]),
    "S2": dict(name="Recommended S2: N2, 1 % H2, 100 % H2", gas="N2; 1 % H2; 100 % H2", segs=TF.SINTER["S2"]["segs"]),
}


def num(b):
    if isinstance(b, (bool, np.bool_)):
        return bool(b)
    if isinstance(b, (int, float, np.floating, np.integer)):
        return float(b) if np.isfinite(b) else None
    return b


def run_custom(job):
    """job = (tag, segments, scenario dict, N, rtol)"""
    tag, segs, sc, N, rtol = job
    t0 = time.time()
    r = simulate(sc, Cycle(list(segs)), N=N, rtol=rtol)
    k = r.kpi
    v = verdict(k, Setup(sc))
    return dict(tag=list(tag), ok=bool(r.ok), wall_s=time.time() - t0,
                n_fail=sum(0 if x["ok"] else 1 for x in v.values()), failed=[a for a, b in v.items() if not b["ok"]],
                kpi={a: num(b) for a, b in k.items() if a != "verdict"})


def literature_jobs():
    """Published copper processes, as (tag, segments, scenario, N, rtol)."""
    cea = dict(make_scenario(d50_um=22.0, span=1.5, phi=0.60, h2_max=1.0, dp_max_C=20.0))
    ifam = dict(d50_um=16.0, span=1.0, phi=0.52, solvent_frac=0.15, h2_max=1.0, dp_max_C=20.0,
                h_conv=40.0, half_thickness_mm=2.0)
    ifam_s = dict(make_scenario(**ifam, pre_extracted_frac=0.4))
    ifam_a = dict(make_scenario(**ifam))
    from cupola.cycle import cea_reference, ifam_reference
    ar = [Segment(400, 1.0, 4.0, 0.0, 0.0, -60, "Ar debind"), Segment(25, 5.0, 0.0, 0.0, 0.0, -60, "cool")]
    return [(("lit", "cea"), cea_reference().segments, cea, None, 1e-3),
            (("lit", "ifam_solvent"), ifam_reference().segments, ifam_s, None, 1e-3),
            (("lit", "ifam_air_only"), ifam_reference().segments, ifam_a, None, 1e-3),
            (("lit", "roumanie_ar_char"), ar, cea, None, 1e-3)]


LITERATURE = {
    "cea": dict(what="CEA-LITEN DLP copper: 400 C / 4 h air, then 1050 C / 4 h H2", measured="90-94 % density",
                lo=0.90, hi=0.94, metric="rho_final", role="calibration point for the sintering rate"),
    "ifam_solvent": dict(what="Fraunhofer IFAM LMM copper: acetone, air 120 C / 24 h + 250 C / 63 h, 1050 C / 2 h H2",
                         measured="95.3 % density", lo=0.953, hi=0.953, metric="rho_final", role="independent"),
    "ifam_air_only": dict(what="Fraunhofer IFAM, same without the acetone step (air only, then H2 only)",
                          measured="about 92 % density", lo=0.92, hi=0.92, metric="rho_final", role="independent"),
    "roumanie_ar_char": dict(what="Roumanie (CEA): 400 C / 4 h in argon", measured="0.394 wt% carbon",
                             lo=3940, hi=3940, metric="C_final_ppm", role="calibration point for the char yield"),
}


def _phase_job(name):
    from cupola.cycle import cea_reference, ifam_reference
    ifam = dict(d50_um=16.0, span=1.0, phi=0.52, solvent_frac=0.15, h2_max=1.0, dp_max_C=20.0, h_conv=40.0,
                half_thickness_mm=2.0)
    cases = {
        "CEA (published, intact parts)": (make_scenario(d50_um=22.0, span=1.5, phi=0.60, h2_max=1.0, dp_max_C=20.0),
                                          cea_reference().segments, 2),
        "IFAM with acetone (published, intact parts)": (make_scenario(**ifam, pre_extracted_frac=0.4),
                                                        ifam_reference().segments, 3),
        "IFAM air only (published, intact parts)": (make_scenario(**ifam), ifam_reference().segments, 3),
        "Yours: air only (slow) + S1": (TF.scenario(), DEBIND["AIR-SLOW"]["segs"] + SINTER["S1"]["segs"], 3),
        "Yours: air only (slow) + H2 only": (TF.scenario(), DEBIND["AIR-SLOW"]["segs"] + SINTER["H2"]["segs"], 3),
        "Yours: recommended D2 + S2": (TF.scenario(), DEBIND["D2"]["segs"] + SINTER["S2"]["segs"],
                                       len(DEBIND["D2"]["segs"])),
    }
    sc, segs, nd = cases[name]
    cyc = Cycle(list(segs))
    r = simulate(sc, cyc, N=8, rtol=1e-3)
    S, t = r.series, r.t_h
    tb = sum(b - a for (a, b, sg, *_) in cyc.boundaries() if any(sg is x for x in segs[:nd])) / 3600
    heat = S["Tset"] >= S["Tf"] - 0.5
    deb, sin = heat & (t <= tb), heat & (t > tb)
    return dict(case=name, debind_exo_K=float(np.max(np.where(deb, S["exo_gen"], 0.0))),
                sinter_exo_K=float(np.max(np.where(sin, S["exo_gen"], 0.0))),
                O_after_debind_ppm=float(S["O_ppm_mean"][min(np.searchsorted(t, tb), len(t) - 1)]),
                rho_final=float(r.kpi["rho_final"]))


def phases(path, W=4):
    """Self-heating in each furnace, for published processes that made intact parts and for yours."""
    names = ["CEA (published, intact parts)", "IFAM with acetone (published, intact parts)",
             "IFAM air only (published, intact parts)", "Yours: air only (slow) + S1",
             "Yours: air only (slow) + H2 only", "Yours: recommended D2 + S2"]
    with Pool(W) as p:
        rows = p.map(_phase_job, names)
    data = json.load(open(path))
    data["selfheat"] = rows
    json.dump(TF.clean(data), open(path, "w"), indent=1, allow_nan=False)
    for r in rows:
        print(r)


if __name__ == "__main__" and sys.argv[1] == "--phases":
    phases(sys.argv[2])
elif __name__ == "__main__":
    out = sys.argv[1]
    W = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    N = 8
    base = TF.scenario()
    jobs = []
    for d, s in itertools.product(DEBIND, SINTER):
        jobs.append((("grid", d, s, "nominal"), DEBIND[d]["segs"] + SINTER[s]["segs"], base, N, 1e-4))
        for vn, vx in TF.VARIANTS.items():
            jobs.append((("grid", d, s, vn), DEBIND[d]["segs"] + SINTER[s]["segs"], TF.scenario(vx), N, 1e-4))
    jobs += literature_jobs()
    t0 = time.time()
    res = []
    with Pool(W) as p:
        for r in p.imap_unordered(run_custom, jobs):
            res.append(r)
            k = r["kpi"]
            print(f"[{len(res):3d}/{len(jobs)}] {'/'.join(map(str, r['tag'][1:])):34s} fail {r['n_fail']} "
                  f"{','.join(r['failed']):42s} rho {k.get('rho_final') or 0:.3f} C {k.get('C_final_ppm') or 0:7.0f} "
                  f"O {k.get('O_final_ppm') or 0:7.0f} exo {k.get('exo_max_K') or 0:6.1f} ({time.time() - t0:.0f} s)",
                  flush=True)

    grid = {}
    for r in res:
        if r["tag"][0] == "grid":
            _, d, s, v = r["tag"]
            grid.setdefault((d, s), {})[v] = r
    table = []
    for (d, s), vs in grid.items():
        nom = dict(vs["nominal"], debind=d, sinter=s)
        nom["robust"] = {vn: dict(n_fail=vs[vn]["n_fail"], failed=vs[vn]["failed"]) for vn in TF.VARIANTS}
        nom["n_robust"] = sum(1 for vn in TF.VARIANTS if vs[vn]["n_fail"] == 0)
        nom["t_total_h"] = Cycle(list(DEBIND[d]["segs"]) + list(SINTER[s]["segs"])).duration_h()
        table.append(nom)
    table.sort(key=TF.rank_key)
    for i, r in enumerate(table):
        r["rank"] = i + 1

    # numerical check: the best pairing of each debinding family, finer mesh and tighter tolerance
    best = {}
    for r in table:
        best.setdefault(r["debind"], r)
    chk_jobs = []
    for d, r in best.items():
        segs = DEBIND[d]["segs"] + SINTER[r["sinter"]]["segs"]
        chk_jobs.append((("num", d, r["sinter"], "N12"), segs, base, 12, 1e-4))
        chk_jobs.append((("num", d, r["sinter"], "rtol1e-5"), segs, base, 8, 1e-5))
    with Pool(W) as p:
        chk = p.map(run_custom, chk_jobs)
    numerics = []
    for c in chk:
        _, d, s, how = c["tag"]
        ref = next(r for r in table if r["debind"] == d and r["sinter"] == s)
        numerics.append(dict(debind=d, sinter=s, how=how, n_fail=c["n_fail"], n_fail_ref=ref["n_fail"],
                             rho=c["kpi"]["rho_final"], rho_ref=ref["kpi"]["rho_final"],
                             C=c["kpi"]["C_final_ppm"], C_ref=ref["kpi"]["C_final_ppm"],
                             exo=c["kpi"]["exo_max_K"], exo_ref=ref["kpi"]["exo_max_K"]))
        print("numerics", d, s, how, numerics[-1])

    lit = []
    for r in res:
        if r["tag"][0] == "lit":
            L = dict(LITERATURE[r["tag"][1]])
            L.update(key=r["tag"][1], predicted=r["kpi"][L["metric"]], exo=r["kpi"]["exo_max_K"],
                     C_final_ppm=r["kpi"]["C_final_ppm"], rho_final=r["kpi"]["rho_final"])
            lit.append(L)
    for T, meas in V.ROUMANIE_OX:
        lit.append(dict(key=f"roumanie_ox_{T:.0f}", what=f"Roumanie (CEA): Cu compact in air, 1 K/min to {T:.0f} C + 4 h",
                        measured=f"{meas} wt% mass gain", lo=meas, hi=meas, metric="mass_gain_wt",
                        role="independent", predicted=float(V.cu_compact_oxidation(T))))
    for L in lit:
        print("literature", L["key"], L["measured"], L["predicted"])

    json.dump(TF.clean(dict(generated=time.strftime("%Y-%m-%d"), N=N, variants=list(TF.VARIANTS),
                            debind={k: dict(name=v["name"], gas=v["gas"], segments=TF.seg_dicts(v["segs"]),
                                            duration_h=Cycle(list(v["segs"])).duration_h()) for k, v in DEBIND.items()},
                            sinter={k: dict(name=v["name"], gas=v["gas"], segments=TF.seg_dicts(v["segs"]),
                                            duration_h=Cycle(list(v["segs"])).duration_h()) for k, v in SINTER.items()},
                            grid=table, numerics=numerics, literature=lit)),
              open(out, "w"), indent=1, allow_nan=False)
    print("ranking:", [(r["debind"], r["sinter"], r["n_fail"]) for r in table[:8]])
