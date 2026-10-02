"""Debinding and sintering cycles for a two-furnace line, ranked by the predicted part.

Furnace 1 (debinding) has air and nitrogen; furnace 2 (sintering) has nitrogen, hydrogen and air.
No humidifier is assumed, so every gas is dry, and lean mixtures (air in N2, H2 in N2) are blended
from the cylinders with two flowmeters. A debinding programme ends with the part cooled to room
temperature in its furnace; the part is then moved and the sintering programme starts from 25 C. The
model runs the two programmes back to back as one cycle, so the brown part carries its carbon, oxide and
porosity from the first furnace into the second.

Without steam, char left by pyrolysis can only leave as CO or CO2: burnt by oxygen, or taken by the
oxygen of copper oxide (Cu2O + C -> 2 Cu + CO). The candidates explore both.

    python scripts/two_furnace.py <out.json> [N] [workers]
    python scripts/two_furnace.py --finish <out.json>     (carbon ledger, range-cell programmes, notes)
"""
import json, sys, time, itertools
from multiprocessing import Pool
import numpy as np

from cupola.cycle import Cycle, Segment
from cupola.params import defaults, FURNACE_PRESETS
from cupola.simulate import simulate, verdict
from cupola.materials import Setup

AIR = 0.2095
FG = 0.05              # 5 % H2 in N2 (non-flammable forming gas)


def seg(T, ramp, hold=0.0, O2=0.0, H2=0.0, note=""):
    return Segment(T, ramp, hold, O2, H2, -60.0, note)


# ------------------------------------------------------------------ furnace 1: debinding (air, N2)
PYRO = [seg(470, 1.0, 1.0, note="binder pyrolysis, N2")]


def debind_graded(T_ox=250.0, air_h=1.0):
    """Pyrolyse in N2, then oxidise the copper under oxygen that is raised in steps."""
    return PYRO + [seg(150, 3.0, 0.5, note="cool and settle, N2"),
                   seg(T_ox, 0.5, 0.0, O2=0.005, note="0.5 % O2 (2.5 % air in N2)"),
                   seg(T_ox, 1.0, 1.0, O2=0.02, note="2 % O2 (10 % air in N2)"),
                   seg(T_ox, 1.0, air_h, O2=AIR, note="air"),
                   seg(25, 3.0, 0.0, note="cool, N2")]


def debind_lean(T_ox=280.0, O2=0.01, h=2.0):
    """Pyrolyse in N2, then oxidise under one lean air/N2 mixture while heating from 150 C and holding."""
    return PYRO + [seg(150, 3.0, 0.5, note="cool and settle, N2"),
                   seg(T_ox, 0.5, h, O2=O2, note=f"{O2 * 100:g} % O2 ({O2 / AIR * 100:.0f} % air in N2)"),
                   seg(25, 3.0, 0.0, note="cool, N2")]


DEBIND = {
    "D1": dict(name="N2 pyrolysis, then graded oxidation to air",
               gas="N2; then 2.5 % and 10 % air in N2; then air",
               idea="Remove the binder in N2, then oxidise part of the copper on purpose. The oxide carries the "
                    "oxygen that takes the char away later, in the sintering furnace. The oxygen is raised in steps "
                    "so a thin oxide forms first and slows the reaction before air is let in.",
               pros=["Lowest self-heating of the oxidising routes", "Air only touches copper that already has an oxide skin",
                     "Clears the carbon in furnace 2 as well as D2"],
               cons=["Overheats walls thicker than about 5 mm when the air goes in",
                     "Needs air blended into N2 at two ratios"],
               segs=debind_graded()),
    "D2": dict(name="N2 pyrolysis, then lean-air oxidation",
               gas="N2; then 5 % air in N2",
               idea="Remove the binder in N2, then oxidise part of the copper under one lean mixture, 1 % O2, while "
                    "heating from 150 to 280 C and for 2 h at 280 C. The oxide carries the oxygen that takes the char "
                    "away in the sintering furnace. Low oxygen keeps the heat of oxidation small without ever "
                    "switching to full air.",
               pros=["The only oxidising debind that also passes with 8 mm walls, and with 3 % or 8 % char",
                     "One lean mixture, never full air", "Same final part as D1"],
               cons=["Self-heating about 19 K, close to the 20 K limit", "Needs a flowmeter to blend 5 % air into N2",
                     "Brown part carries about 5 % O by mass as oxide until furnace 2"],
               segs=debind_lean()),
    "D3": dict(name="N2 pyrolysis only",
               gas="N2",
               idea="Decompose the binder without oxygen. Copper stays metallic, but about 0.4 % carbon stays "
                    "behind as char, and the sintering furnace then has to remove it (S3).",
               pros=["Shortest and simplest debind", "No oxide, no swelling, no exotherm"],
               cons=["Leaves ~4400 ppm char that dry H2 cannot remove", "Works only with an oxidation step in "
                     "furnace 2 (S3)"],
               segs=PYRO + [seg(25, 3.0, 0.0, note="cool, N2")]),
    "D4": dict(name="Air burnout",
               gas="air",
               idea="Burn binder and char in air, as for ceramics. Carbon goes, but fresh copper oxidises "
                    "fast in air and the heat of oxidation and of the burning binder overheats the part.",
               pros=["Removes carbon in one furnace", "No gas blending needed"],
               cons=["Self-heating over 100 K: risk of cracks and of a runaway", "Copper oxidises almost "
                     "completely"],
               segs=[seg(150, 1.0, 0.5, O2=AIR, note="solvent out, air"),
                     seg(380, 0.5, 2.0, O2=AIR, note="burnout, air"),
                     seg(25, 3.0, 0.0, note="cool, N2")]),
}


# ------------------------------------------------------------------ furnace 2: sintering (N2, H2, air)
def sinter_cth(T_c=700.0, t_c=2.0, T_s=1050.0, t_s=4.0, H2=FG):
    """N2 hold for the carbothermic reaction, lean-H2 reduction of the rest of the oxide, then sinter."""
    return [seg(T_c, 5.0, t_c, note="Cu2O + C -> Cu + CO, N2"),
            seg(T_c, 1.0, 2.0, H2=0.01, note="reduce the rest of the oxide, 1 % H2"),
            seg(T_s, 5.0, t_s, H2=H2, note=f"sinter, {H2 * 100:.0f} % H2"),
            seg(600, 5.0, 0.0, H2=H2, note=f"cool, {H2 * 100:.0f} % H2"),
            seg(25, 5.0, 0.0, note="cool, N2")]


SINTER = {
    "S1": dict(name="N2 carbon-oxide hold, lean-H2 reduction, sinter in forming gas",
               gas="N2; then 1 % H2 in N2; then 5 % H2 in N2",
               idea="Heat the oxidised part in N2 to 700 C, where the oxide and the char react and leave as CO. "
                    "Only then add hydrogen, at 1 % to reduce the rest of the oxide gently, and sinter for 4 h at "
                    "1050 C in 5 % H2.",
               pros=["Uses the oxide made in furnace 1 to remove the char", "Non-flammable gases only",
                     "Gentle reduction: self-heating below 8 K"],
               cons=["Must start in N2: hydrogen before the 700 C hold removes the oxide the char needs",
                     "Slightly lower density than pure H2"],
               segs=sinter_cth()),
    "S2": dict(name="As S1, sintered in pure H2",
               gas="N2; then 1 % H2 in N2; then 100 % H2",
               idea="The same route with pure hydrogen from the end of the 700 C reduction, if the furnace is rated "
                    "for it. Hydrogen carries heat about seven times better than N2, so the part follows the furnace "
                    "more closely and spends longer at the sintering temperature.",
               pros=["Highest density and conductivity of all routes", "Same carbon and oxygen removal as S1"],
               cons=["Needs a hydrogen-rated furnace and safety case", "Gain over 5 % H2 is small, about 0.5 % density",
                     "Must still start in N2, as S1"],
               segs=sinter_cth(H2=1.0)),
    "S3": dict(name="Oxidise in the sintering furnace, then as S1",
               gas="N2; 2.5 %, 10 % air in N2, air; N2; 1 % and 5 % H2 in N2",
               idea="For parts debound in N2 only (D3): the graded oxidation of D1 is done here, at the start "
                    "of the sintering programme, followed by an N2 purge and the rest of S1.",
               pros=["Lets the debinding furnace stay N2-only", "Same properties as D1 + S1"],
               cons=["Longest sintering run", "Air and H2 in the same retort: purge well between them"],
               segs=[seg(150, 5.0, 0.5, note="heat, N2"),
                     seg(250, 0.5, 0.0, O2=0.005, note="0.5 % O2 (2.5 % air in N2)"),
                     seg(250, 1.0, 1.0, O2=0.02, note="2 % O2 (10 % air in N2)"),
                     seg(250, 1.0, 1.0, O2=AIR, note="air"),
                     seg(250, 1.0, 0.5, note="purge, N2")] + sinter_cth()),
    "S4": dict(name="Conventional: reduce in forming gas, sinter",
               gas="5 % H2 in N2",
               idea="Reduce at 400 C and sinter for 4 h at 1050 C in forming gas. Good for clean powder; with "
                    "char in the part the hydrogen removes the oxide before it can react with the carbon.",
               pros=["Simplest programme", "Works if the debind left no char"],
               cons=["Traps the char: carbon holds the copper at low density"],
               segs=[seg(400, 5.0, 2.0, H2=FG, note="reduce oxide, 5 % H2"),
                     seg(1050, 5.0, 4.0, H2=FG, note="sinter, 5 % H2"),
                     seg(600, 5.0, 0.0, H2=FG, note="cool, 5 % H2"),
                     seg(25, 5.0, 0.0, note="cool, N2")]),
}

# both furnaces together: air in both, H2 up to 100 % in the second, dry gas only
LINE_PRESET = "two_furnace"
VARIANTS = {"char_yield=0.03": dict(char_yield=0.03), "char_yield=0.08": dict(char_yield=0.08),
            "half_thickness_mm=1.0": dict(half_thickness_mm=1.0),
            "half_thickness_mm=4.0": dict(half_thickness_mm=4.0)}


# ranges around the best pairing (D2 + S2)
SWEEPS = {
    "sinter": dict(title="Sintering temperature and hold", x="Sinter", y="Hold",
                   xs=[1040.0, 1050.0, 1060.0], ys=[2.0, 3.0, 4.0], xu="C", yu="h",
                   note="Every cell passes. 1060 C uses most of the melting margin; 1050 C for 4 h is the default."),
    "carbothermic": dict(title="N2 carbon-oxide hold", x="Hold at", y="Time",
                         xs=[600.0, 650.0, 700.0], ys=[1.0, 2.0, 3.0], xu="C", yu="h",
                         note="At 600 C the oxide and the char barely react and the carbon stays. The onset "
                              "temperature is an estimate, so 700 C keeps a margin."),
    "oxidation": dict(title="Lean-air oxidation in furnace 1", x="Up to", y="O2",
                      xs=[250.0, 280.0, 310.0], ys=[0.5, 1.0, 2.0], xu="C", yu="% O2",
                      note="The oxygen level, not the temperature, sets the heat. 0.5 % runs coolest but leaves "
                           "char in the centre of 8 mm walls; 1 % is the default."),
}


def sweep_cycle(name, x, y):
    if name == "oxidation":
        return debind_lean(T_ox=x, O2=y / 100.0), sinter_cth(H2=1.0)
    if name == "sinter":
        return debind_lean(), sinter_cth(T_s=x, t_s=y, H2=1.0)
    return debind_lean(), sinter_cth(T_c=x, t_c=y, H2=1.0)


def scenario(extra=None):
    sc = dict(defaults()); sc.update(FURNACE_PRESETS[LINE_PRESET])
    if extra:
        sc.update(extra)
    return sc


def run(job):
    """job = (tag, debind segments, sinter segments, scenario overrides, N)"""
    tag, dsegs, ssegs, extra, N = job
    sc = scenario(extra)
    cyc = Cycle(list(dsegs) + list(ssegs), name="+".join(str(x) for x in tag))
    t0 = time.time()
    r = simulate(sc, cyc, N=N)
    k = r.kpi
    v = verdict(k, Setup(sc))
    n_fail = sum(0 if x["ok"] else 1 for x in v.values())
    worst = max(v.items(), key=lambda kv: kv[1]["index"])
    t_deb = Cycle(list(dsegs)).duration_h()
    num = lambda b: float(b) if isinstance(b, (int, float, np.floating, np.integer, bool)) else b
    return dict(tag=list(tag), ok=bool(r.ok), wall_s=time.time() - t0, n_fail=n_fail,
                failed=[a for a, b in v.items() if not b["ok"]],
                worst=worst[0], worst_index=float(worst[1]["index"]),
                t_debind_h=t_deb, t_sinter_h=cyc.duration_h() - t_deb, t_total_h=cyc.duration_h(),
                kpi={a: num(b) for a, b in k.items() if a != "verdict"},
                verdict={a: dict(index=float(b["index"]), ok=bool(b["ok"]), value=float(b["value"])) for a, b in v.items()})


def rank_key(r):
    """Fewest failed checks, then robustness, then density (to 0.5 %), carbon (below 50 ppm counts as clean),
    conductivity (to 1 % IACS) and time."""
    k = r["kpi"]
    return (r["n_fail"], -r.get("n_robust", 0), -round(k.get("rho_final", 0.0) * 200),
            max(round(k.get("C_final_ppm", 1e9), -1), 50.0), -round(k.get("iacs", 0.0)), r["t_total_h"])


def seg_dicts(segs):
    return [dict(s.__dict__) for s in segs]


ASSUMPTIONS = [
    "All gases are dry (no humidifier). Lean mixtures are blended from the cylinders with two flowmeters: air into N2 "
    "in both furnaces, H2 into N2 in the sintering furnace.",
    "The part cools to room temperature in furnace 1 and is moved to furnace 2. A brown part with oxide on it is "
    "fragile and should be handled on its setter.",
    "Default slurry and part: 12 um copper at 55 vol%, 5 mm thickest wall, 5 % char yield, 2 slpm in a 5 L retort. "
    "Each pairing was also run with 3 % and 8 % char and with 2 mm and 8 mm walls; with 8 mm walls the step to full "
    "air in D1 overheats the part, and D2 does not.",
    "The model has no rate data for char on copper or for this binder; the carbothermic onset (600 C) and the char "
    "yield are estimates. Check the plan with LECO carbon and oxygen on coupons after each furnace.",
    "Swelling of the brown part by the oxide (4-5 % O by mass) is reversible on reduction in the model, but "
    "cracking from it is not modelled. Inspect parts after furnace 1.",
    "Sintering at 1050 C keeps 15 K of the model's melting margin (pure copper 1085 C, less 15 K margin and 5 K "
    "furnace uniformity). 1060 C adds about 0.2 % density but uses most of that margin: survey the furnace first.",
    "100 % H2 (S2) gives the best part, but only by about 0.5 % density over 5 % H2 (S1). If the sintering furnace is "
    "not rated for pure hydrogen, S1 is the choice.",
]


def ledger(dsegs, ssegs, N=8):
    """State at the end of every programme row of one pairing."""
    sc = scenario()
    segs = list(dsegs) + list(ssegs)
    cyc = Cycle(segs)
    r = simulate(sc, cyc, N=N)
    S, t = r.series, r.t_h
    rows, seen = [], set()
    for (a, b, sg, Tfrom, kind) in cyc.boundaries():
        j = next(i for i, x in enumerate(segs) if x is sg)
        m = (t >= a / 3600 - 1e-9) & (t <= b / 3600 + 1e-9)
        if not m.any():
            continue
        i = int(np.where(m)[0][-1])
        row = dict(row=j + 1, furnace=1 if j < len(dsegs) else 2, note=sg.note, T=sg.T_end_C, t_end_h=b / 3600,
                   C=float(S["C_ppm_mean"][i]), O=float(S["O_ppm_mean"][i]), rho=float(S["rho_mean"][i]),
                   binder=float(S["binder_left"][i]))
        if j in seen:
            rows[-1] = row
        else:
            rows.append(row)
        seen.add(j)
    return rows


def clean(o):
    """Non-finite numbers (e.g. carbon at closure when the pores never close) become null for JSON."""
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [clean(v) for v in o]
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return o


def finish(path, N=8):
    data = json.load(open(path))
    best = data["combos"][0]
    data["ledger"] = ledger(DEBIND[best["debind"]]["segs"], SINTER[best["sinter"]]["segs"], N)
    for name, sw in data["sweeps"].items():
        for c in sw["cells"]:
            ds, ss = sweep_cycle(name, c["x"], c["y"])
            c["segments"] = ([dict(s.__dict__, note="F1 · " + s.note) for s in ds] +
                             [dict(s.__dict__, note="F2 · " + s.note) for s in ss])
    for key, defs in (("debind", DEBIND), ("sinter", SINTER)):
        for k, o in data[key].items():
            o.update({f: defs[k][f] for f in ("name", "gas", "idea", "pros", "cons")})
    for name, sw in data["sweeps"].items():
        sw.update({f: v for f, v in SWEEPS[name].items() if f not in ("xs", "ys")})
    data["assumptions"] = ASSUMPTIONS
    json.dump(clean(data), open(path, "w"), indent=1, allow_nan=False)
    print("ledger:", [(r["note"], round(r["C"]), round(r["O"])) for r in data["ledger"]])


if __name__ == "__main__" and sys.argv[1] == "--finish":
    finish(sys.argv[2])
elif __name__ == "__main__":
    out = sys.argv[1]
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    W = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    jobs = []
    for d, s in itertools.product(DEBIND, SINTER):
        jobs.append((("combo", d, s, "nominal"), DEBIND[d]["segs"], SINTER[s]["segs"], None, N))
        for vn, vx in VARIANTS.items():
            jobs.append((("combo", d, s, vn), DEBIND[d]["segs"], SINTER[s]["segs"], vx, N))
    for name, sw in SWEEPS.items():
        for xv, yv in itertools.product(sw["xs"], sw["ys"]):
            ds, ss = sweep_cycle(name, xv, yv)
            jobs.append((("sweep", name, xv, yv), ds, ss, None, N))

    t0 = time.time()
    with Pool(W) as p:
        res = []
        for r in p.imap_unordered(run, jobs):
            res.append(r)
            k = r["kpi"]
            print(f"[{len(res):3d}/{len(jobs)}] {'/'.join(map(str, r['tag'][1:])):40s} fail {r['n_fail']} "
                  f"{','.join(r['failed']):40s} rho {k.get('rho_final', 0):.3f} C {k.get('C_final_ppm', 0):6.0f} "
                  f"O {k.get('O_final_ppm', 0):5.0f} exo {k.get('exo_max_K', 0):5.1f} iacs {k.get('iacs', 0):5.1f} "
                  f"t {r['t_total_h']:5.1f} h  ({time.time() - t0:.0f} s)", flush=True)

    combos = {}
    for r in res:
        if r["tag"][0] == "combo":
            _, d, s, v = r["tag"]
            combos.setdefault((d, s), {})[v] = r
    table = []
    for (d, s), vs in combos.items():
        nom = dict(vs["nominal"])
        nom["debind"], nom["sinter"] = d, s
        nom["robust"] = {vn: dict(n_fail=vs[vn]["n_fail"], failed=vs[vn]["failed"],
                                  rho=vs[vn]["kpi"].get("rho_final"), C=vs[vn]["kpi"].get("C_final_ppm"),
                                  iacs=vs[vn]["kpi"].get("iacs")) for vn in VARIANTS}
        nom["n_robust"] = sum(1 for vn in VARIANTS if vs[vn]["n_fail"] == 0)
        table.append(nom)
    table.sort(key=rank_key)
    for i, r in enumerate(table):
        r["rank"] = i + 1

    def best_for(key, val):
        return min((r for r in table if r[key] == val), key=rank_key)

    d_rank = sorted(DEBIND, key=lambda d: rank_key(best_for("debind", d)))
    s_rank = sorted(SINTER, key=lambda s: rank_key(best_for("sinter", s)))

    sweeps = {}
    for name, sw in SWEEPS.items():
        cells = [dict(x=r["tag"][2], y=r["tag"][3], n_fail=r["n_fail"], failed=r["failed"], kpi=r["kpi"],
                      t_total_h=r["t_total_h"]) for r in res if r["tag"][0] == "sweep" and r["tag"][1] == name]
        cells.sort(key=lambda c: (c["y"], c["x"]))
        sweeps[name] = dict(sw, cells=cells)

    def block(defs, order):
        o = {}
        for i, k in enumerate(order):
            v = defs[k]
            b = best_for("debind" if k.startswith("D") else "sinter", k)
            o[k] = dict(rank=i + 1, name=v["name"], gas=v["gas"], idea=v["idea"], pros=v["pros"], cons=v["cons"],
                        segments=seg_dicts(v["segs"]), duration_h=Cycle(list(v["segs"])).duration_h(),
                        best_partner=b["sinter"] if k.startswith("D") else b["debind"])
        return o

    json.dump(dict(generated=time.strftime("%Y-%m-%d"), N=N, preset=LINE_PRESET,
                   preset_values=FURNACE_PRESETS[LINE_PRESET], variants=list(VARIANTS),
                   debind=block(DEBIND, d_rank), sinter=block(SINTER, s_rank),
                   combos=table, sweeps=sweeps), open(out, "w"), indent=1)
    print(f"debind ranking: {d_rank}; sinter ranking: {s_rank}; best combo {table[0]['debind']}+{table[0]['sinter']}")
