// Precompute the dashboard's at-rest data with the JavaScript engine.
//
//   node dashboard/build/precompute.mjs [default] [synth] [sens] [powder]
//
// Each part merges into dashboard/data/precomputed.json, so parts can be rerun on their own.
import { createRequire } from "module";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const require = createRequire(import.meta.url);
const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const C = require(join(ROOT, "engine", "cupola.js"));
const P = require(join(ROOT, "engine", "params.json"));
const OUT = join(ROOT, "data", "precomputed.json");
const CYCLE = JSON.parse(fs.readFileSync(join(ROOT, "data", "synth_default_cycle.json"), "utf8"));

const N_PREVIEW = 8;
const base = {};
for (const p of P.registry) base[p.key] = p.value;

// KPIs the sensitivity and powder studies report
const METRICS = {
  rho_final: "Final relative density",
  shrink_xy_pct: "Linear shrinkage x-y (%)",
  C_at_close_ppm: "Carbon at pore closure (ppm)",
  Pi_gas_max: "Debinding gas index",
  Pi_bloat_max: "Trapped-gas index",
  n_fail: "Constraints failed",
};

const sig = (x, n = 5) => (Number.isFinite(x) ? Number(x.toPrecision(n)) : null);

function kpiSummary(r) {
  const k = r.kpi;
  const out = {};
  for (const m of Object.keys(METRICS)) out[m] = m === "n_fail" ? 0 : sig(k[m]);
  out.n_fail = Object.values(k.verdict).filter((v) => !v.ok).length;
  if (!k.closed) out.C_at_close_ppm = sig(k.C_final_ppm);
  out.ok = r.ok;
  return out;
}

function packResult(r) {
  const series = {};
  for (const [k, a] of Object.entries(r.series)) series[k] = Array.from(a, (x) => sig(x));
  const kpi = {};
  for (const [k, v] of Object.entries(r.kpi)) {
    if (k === "verdict") continue;
    kpi[k] = typeof v === "number" ? sig(v, 6) : v;
  }
  const verdict = {};
  for (const [k, v] of Object.entries(r.kpi.verdict)) verdict[k] = { ...v, value: sig(v.value), index: sig(v.index) };
  kpi.verdict = verdict;
  return { t_h: Array.from(r.t_h, (x) => sig(x, 6)), series, kpi, ok: r.ok, message: r.message };
}

const stripCand = (c) => ({ topology: c.topology, T_B_C: c.T_B_C, feasible: c.feasible, duration_h: sig(c.duration_h, 4),
                            note: c.note, cycle: c.cycle });

function load() {
  try { return JSON.parse(fs.readFileSync(OUT, "utf8")); } catch { return {}; }
}
function save(d) {
  d.generated = new Date().toISOString();
  fs.writeFileSync(OUT, JSON.stringify(d));
  console.log("wrote", OUT, (fs.statSync(OUT).size / 1024).toFixed(0), "kB");
}

const parts = process.argv.slice(2);
const want = (p) => parts.length === 0 || parts.includes(p);
const data = load();
const t0 = Date.now();
const el = () => ((Date.now() - t0) / 1000).toFixed(0) + " s";

if (want("default")) {
  const r = C.simulate(base, CYCLE, { N: N_PREVIEW });
  data.default_cycle = CYCLE;
  data.default_result = packResult(r);
  data.default_N = N_PREVIEW;
  console.log("default run", el(), r.kpi.rho_final.toFixed(4));
  save(data);
}

if (want("synth")) {
  let last = 0;
  const out = await C.synthesize(base, { N: N_PREVIEW, progress: (p) => {
    if (Date.now() - last > 5000) { last = Date.now(); console.log("  synth", el(), p.stage); } } });
  data.synth = { candidates: out.candidates.map(stripCand), best: out.best ? out.best.cycle.name : null };
  console.log("synthesis", el(), data.synth.best);
  save(data);
}

if (want("sens")) {
  const baseK = kpiSummary(C.simulate(base, CYCLE, { N: N_PREVIEW }));
  const rows = [];
  const keys = P.registry.filter((p) => !p.advanced && p.group !== "limits" && p.kind !== "int");
  for (const p of keys) {
    const row = { key: p.key, label: p.label, tag: p.tag, unit: p.unit, group: p.group, base: p.value, lo: p.lo, hi: p.hi };
    for (const side of ["lo", "hi"]) {
      const s = { ...base, [p.key]: p[side] };
      let k;
      try { k = kpiSummary(C.simulate(s, CYCLE, { N: N_PREVIEW })); } catch (e) { k = { ok: false, error: String(e) }; }
      row["out_" + side] = k;
    }
    rows.push(row);
    console.log("  sens", el(), p.key);
  }
  data.sensitivity = { metrics: METRICS, base: baseK, rows, cycle: CYCLE.name };
  save(data);
}

if (want("powder")) {
  const rows = [];
  for (const [name, pv] of Object.entries(P.powder_presets)) {
    const s = { ...base, ...pv };
    const fixed = kpiSummary(C.simulate(s, CYCLE, { N: N_PREVIEW }));
    const out = await C.synthesize(s, { N: N_PREVIEW });
    // no candidate kept the 20 % margin everywhere: report the best effort (fewest failed checks, then shortest)
    let b = out.best, passes = !!b;
    if (!b) {
      for (const c of out.candidates) {
        if (!c.cycle) continue;
        c.result = C.simulate(s, c.cycle, { N: N_PREVIEW });
        c.n_fail = Object.values(c.result.kpi.verdict).filter((v) => !v.ok).length;
        if (!b || c.n_fail < b.n_fail || (c.n_fail === b.n_fail && c.duration_h < b.duration_h)) b = c;
      }
    }
    const fails = b ? Object.values(b.result.kpi.verdict).filter((v) => !v.ok).map((v) => v.label) : [];
    rows.push({ preset: name, ...pv, fixed,
                synth: b ? { name: b.cycle.name, duration_h: sig(b.duration_h, 4), rho_final: sig(b.result.kpi.rho_final),
                             shrink_xy_pct: sig(b.result.kpi.shrink_xy_pct), n_fail: fails.length, fails, passes,
                             note: b.note || "", T_peak_C: Math.max(...b.cycle.segments.map((g) => g.T_end_C)), cycle: b.cycle }
                   : null,
                n_feasible: out.candidates.filter((c) => c.feasible).length });
    console.log("  powder", el(), name, b ? b.duration_h.toFixed(1) + " h" + (passes ? "" : " best effort: " + (b.note || fails.join("; "))) : "no cycle");
  }
  data.powder = rows;
  save(data);
}
