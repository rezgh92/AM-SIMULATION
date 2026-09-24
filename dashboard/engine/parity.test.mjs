// Parity test: the JS engine must reproduce the Python reference (scripts/export_parity.py).
import { createRequire } from "module";
import fs from "fs";
const require = createRequire(import.meta.url);
const C = require("./cupola.js");
const ref = JSON.parse(fs.readFileSync(new URL("./parity_ref.json", import.meta.url)));
let fail = 0;
// ---- 1. right-hand side on identical states (round-off agreement expected)
{
  const su = new C.Setup(ref.scenario), sl = new C.Slab(su);
  const out = new Float64Array(sl.n);
  let worst = 0, worstAt = "", nTot = 0, nTight = 0;
  // scale-aware: compare each component against the largest magnitude of the same state variable
  // across all cases (derivatives of O2 are differences of large nearly-cancelling terms)
  const blk = (i) => (i < 10 * sl.N ? Math.floor(i / sl.N) : 100 + i);
  const scaleOf = {};
  for (const cs of ref.rhs) cs.dY.forEach((v, i) => { const b = blk(i); scaleOf[b] = Math.max(scaleOf[b] || 0, Math.abs(v)); });
  for (const cs of ref.rhs) {
    const [t0, t1, Ta, Tb, a, b, c] = cs.ctl;
    const ctl = new C.Controls(t0, t1, Ta, Tb, a, b, c);
    const Y = Float64Array.from(cs.Y);
    const d = sl.evaluate(cs.t, Y, ctl, out, true);
    for (let i = 0; i < sl.n; i++) {
      const p = cs.dY[i], j = out[i];
      const e = Math.abs(p - j) / (Math.abs(p) + 1e-6 * scaleOf[blk(i)] + 1e-300);
      nTot++; if (e <= 1e-9) nTight++;
      if (e > worst) { worst = e; worstAt = `t=${cs.t.toFixed(0)} i=${i} py=${p} js=${j}`; }
    }
    for (const [k, v] of [["Pi_gas", d.Pi_gas], ["exo", d.exo], ["melt", d.melt]]) {
      const e = Math.abs(cs[k] - v) / (Math.abs(cs[k]) + 1e-9);
      if (e > 1e-9 && Math.abs(cs[k] - v) > 1e-12) { console.log(`  diag ${k} mismatch py=${cs[k]} js=${v}`); fail++; }
    }
  }
  // A formula difference shows as O(1) disagreement across many components; floating-point
  // differences (numpy vs V8 exp/pow) amplified by nearly cancelling fluxes stay tiny and rare.
  const frac = nTight / nTot;
  const ok = frac >= 0.999 && worst < 1e-4;
  console.log(`RHS parity over ${ref.rhs.length} states x ${nTot / ref.rhs.length} components: ` +
              `${(100 * frac).toFixed(3)} % agree to 1e-9, worst ${worst.toExponential(2)} ${ok ? "PASS" : "FAIL " + worstAt}`);
  if (!ok) fail++;
}
// ---- 2. full simulations (same algorithm; adaptive steps may differ at round-off level)
for (const run of ref.runs) {
  const t = Date.now();
  const r = C.simulate(run.scenario, run.cycle, { rtol: 1e-3 });
  const ms = Date.now() - t;
  const rows = [];
  for (const k of ["rho_final", "shrink_xy_pct", "shrink_z_pct", "C_peak_ppm", "O_peak_ppm", "Pi_gas_max",
                   "exo_max_K", "grain_final_um", "duration_h"]) {
    const p = run.kpi[k], j = r.kpi[k];
    const e = Math.abs(p - j) / (Math.abs(p) + 1e-6);
    const tol = 0.01;
    rows.push(`${k}=${j.toFixed(4)} (py ${p.toFixed(4)}) ${e < tol ? "ok" : "MISMATCH"}`);
    if (!(e < tol)) fail++;
  }
  console.log(`run ${run.name}: ok=${r.ok} steps=${r.nstep} ${ms} ms\n   ` + rows.join("\n   "));
}
console.log(fail ? `\n${fail} FAILURES` : "\nALL PARITY CHECKS PASS");
process.exit(fail ? 1 : 0);
