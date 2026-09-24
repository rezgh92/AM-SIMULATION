(() => {
"use strict";

// ============================================================ data + helpers
const D = window.CUPOLA_DATA;
const C = window.Cupola;
const PR = D.params;
const REG = PR.registry;
const BYKEY = Object.fromEntries(REG.map((p) => [p.key, p]));
const DEF = Object.fromEntries(REG.map((p) => [p.key, p.value]));
const PRE = D.pre || {};
const STORE_KEY = "cupola.studio.v1";

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
function el(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  if (attrs) for (const [k, v] of Object.entries(attrs)) {
    if (v == null || v === false) continue;
    if (k === "class") e.className = v;
    else if (k === "html") e.innerHTML = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v === true ? "" : v);
  }
  for (const k of kids.flat()) if (k != null && k !== false) e.append(k.nodeType ? k : document.createTextNode(String(k)));
  return e;
}
const SVGNS = "http://www.w3.org/2000/svg";
function sv(tag, attrs) {
  const e = document.createElementNS(SVGNS, tag);
  if (attrs) for (const [k, v] of Object.entries(attrs)) if (v != null) e.setAttribute(k, v);
  return e;
}
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function fmt(v, d = 3) {
  if (v == null || !Number.isFinite(v)) return "–";
  const a = Math.abs(v);
  if (a === 0) return "0";
  if (a >= 1e5 || a < 1e-3) return v.toExponential(1).replace("e+", "e");
  if (a >= 100) return v.toFixed(0);
  if (a >= 10) return v.toFixed(Math.max(0, d - 2));
  if (a >= 1) return v.toFixed(Math.max(0, d - 1));
  return v.toPrecision(d);
}
const UNIT = { um: "µm", C: "°C", "kg/m3": "kg/m³", "W/m2/K": "W/m²K", cm3: "cm³", "J/m2": "J/m²", "-": "", "W/m/K": "W/m·K" };
const unit = (u) => (u in UNIT ? UNIT[u] : u);

const ICON = {
  good: '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="7" fill="currentColor"/><path d="M4.6 8.3l2.2 2.2 4.6-4.8" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  warn: '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.3l7 12.6H1z" fill="currentColor"/><path d="M8 6v3.6" stroke="#15181B" stroke-width="1.7" stroke-linecap="round"/><circle cx="8" cy="11.7" r="1" fill="#15181B"/></svg>',
  crit: '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="7" fill="currentColor"/><path d="M5.3 5.3l5.4 5.4M10.7 5.3l-5.4 5.4" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/></svg>',
  info: '<svg width="14" height="14" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M8 7.2v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="8" cy="4.9" r=".95" fill="currentColor"/></svg>',
  undo: '<svg width="14" height="14" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 6.5h6a3.5 3.5 0 010 7H6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M6 3.8L3.3 6.5 6 9.2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  del: '<svg width="14" height="14" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
};
const statusLabel = { good: "Pass", warn: "At limit", crit: "Fail" };

// ============================================================ state
const state = {
  values: { ...DEF },
  showAdvanced: false,
  source: "opt",
  cycles: { opt: clone(PRE.default_cycle || C.baselineV0()), v0: C.baselineV0(), ifam: C.ifamReference(), cea: C.ceaReference(), custom: null },
  N: 8,
  live: true,
  result: null,
  prevKpi: null,
  synth: PRE.synth || null,
  sens: PRE.sensitivity || null,
  sensMetric: "rho_final",
  sensAll: false,
};
function clone(x) { return x == null ? x : JSON.parse(JSON.stringify(x)); }
const curCycle = () => state.cycles[state.source] || state.cycles.opt;

function saveState() {
  try {
    localStorage.setItem(STORE_KEY, JSON.stringify({
      values: state.values, showAdvanced: state.showAdvanced, source: state.source, N: state.N, live: state.live,
      custom: state.cycles.custom, opt: state.cycles.opt, synth: state.synth,
    }));
  } catch (e) { /* storage unavailable: nothing to remember */ }
}
function loadState() {
  let s = null;
  try { s = JSON.parse(localStorage.getItem(STORE_KEY) || "null"); } catch (e) { s = null; }
  if (!s) return;
  for (const [k, v] of Object.entries(s.values || {})) if (k in DEF && Number.isFinite(v)) state.values[k] = v;
  state.showAdvanced = !!s.showAdvanced;
  if (s.custom && Array.isArray(s.custom.segments)) state.cycles.custom = s.custom;
  if (s.opt && Array.isArray(s.opt.segments)) state.cycles.opt = s.opt;
  if (s.synth && Array.isArray(s.synth.candidates)) state.synth = s.synth;
  if (["opt", "v0", "ifam", "cea", "custom"].includes(s.source) && state.cycles[s.source]) state.source = s.source;
  if (s.N === 8 || s.N === 12) state.N = s.N;
  if (typeof s.live === "boolean") state.live = s.live;
}
const isDefault = () => REG.every((p) => state.values[p.key] === DEF[p.key]);
const sameCycle = (a, b) => JSON.stringify(a && a.segments) === JSON.stringify(b && b.segments);

// ============================================================ worker jobs
const ENGINE_SRC = $("#cupola-engine").textContent;
const WORKER_SRC = `
const post = (m, tr) => self.postMessage(m, tr || []);
function pack(r) {
  const tr = [r.t_h.buffer];
  for (const k in r.series) tr.push(r.series[k].buffer);
  return [{ t_h: r.t_h, series: r.series, kpi: r.kpi, ok: r.ok, message: r.message, nstep: r.nstep, cycle: r.cycle }, tr];
}
function summary(r, metrics) {
  const k = r.kpi, o = { ok: r.ok };
  for (const m of metrics) o[m] = k[m];
  o.n_fail = Object.values(k.verdict).filter((v) => !v.ok).length;
  if (!k.closed) o.C_at_close_ppm = k.C_final_ppm;
  return o;
}
self.onmessage = async (e) => {
  const m = e.data;
  try {
    if (m.cmd === "simulate") {
      const r = await Cupola.simulateAsync(m.scenario, m.cycle, { N: m.N, progress: (f) => post({ type: "progress", frac: f }) });
      const [o, tr] = pack(r);
      post({ type: "done", result: o }, tr);
    } else if (m.cmd === "synthesize") {
      const out = await Cupola.synthesize(m.scenario, { N: m.N, progress: (p) => post({ type: "progress", frac: p.frac || 0, stage: p.stage }) });
      const cands = out.candidates.map((c) => ({ topology: c.topology, T_B_C: c.T_B_C, feasible: c.feasible, duration_h: c.duration_h, note: c.note, cycle: c.cycle }));
      let res = null, tr = [];
      if (out.best && out.best.result) [res, tr] = pack(out.best.result);
      post({ type: "done", candidates: cands, best: out.best ? out.best.cycle.name : null, result: res }, tr);
    } else if (m.cmd === "sensitivity") {
      const metrics = m.metrics;
      const base = summary(Cupola.simulate(m.scenario, m.cycle, { N: m.N }), metrics);
      const rows = [];
      for (let i = 0; i < m.params.length; i++) {
        const p = m.params[i];
        const row = { key: p.key, label: p.label, tag: p.tag, unit: p.unit, group: p.group, base: m.scenario[p.key], lo: p.lo, hi: p.hi };
        for (const side of ["lo", "hi"]) {
          const s = Object.assign({}, m.scenario, { [p.key]: p[side] });
          try { row["out_" + side] = summary(Cupola.simulate(s, m.cycle, { N: m.N }), metrics); }
          catch (err) { row["out_" + side] = { ok: false, error: String(err) }; }
        }
        rows.push(row);
        post({ type: "progress", frac: (i + 1) / m.params.length, stage: p.label });
        await new Promise((r) => setTimeout(r, 0));
      }
      post({ type: "done", sens: { base, rows } });
    }
  } catch (err) { post({ type: "error", message: String((err && err.message) || err) }); }
};`;
let workerURL = null;
try { workerURL = URL.createObjectURL(new Blob([ENGINE_SRC, "\n;\n", WORKER_SRC], { type: "text/javascript" })); } catch (e) { workerURL = null; }

class Cancelled extends Error {}
class Job {
  constructor() { this.w = null; this.pend = null; }
  run(msg, onProgress) {
    this.cancel();
    return new Promise((resolve, reject) => {
      let w = null;
      try { w = workerURL ? new Worker(workerURL) : null; } catch (e) { w = null; }
      if (!w) { mainThread(msg, onProgress).then(resolve, reject); return; }
      this.w = w;
      this.pend = { reject };
      w.onmessage = (e) => {
        const m = e.data;
        if (m.type === "progress") { if (onProgress) onProgress(m); return; }
        this.w = null; this.pend = null; w.terminate();
        if (m.type === "done") resolve(m); else reject(new Error(m.message));
      };
      w.onerror = (e) => { this.w = null; this.pend = null; w.terminate(); reject(new Error(e.message || "worker error")); };
      w.postMessage(msg);
    });
  }
  cancel() {
    if (this.w) { this.w.terminate(); this.w = null; }
    if (this.pend) { this.pend.reject(new Cancelled("cancelled")); this.pend = null; }
  }
  get busy() { return !!this.w; }
}
// Used only when the browser refuses a Worker: the same engine on the page thread.
async function mainThread(msg, onProgress) {
  if (msg.cmd === "simulate") {
    const r = await C.simulateAsync(msg.scenario, msg.cycle, { N: msg.N, progress: (f) => onProgress && onProgress({ frac: f }) });
    return { result: r };
  }
  if (msg.cmd === "synthesize") {
    const out = await C.synthesize(msg.scenario, { N: msg.N, progress: (p) => onProgress && onProgress(p) });
    return { candidates: out.candidates, best: out.best ? out.best.cycle.name : null, result: out.best ? out.best.result : null };
  }
  throw new Error("This browser blocked the background worker; the sensitivity sweep needs it.");
}
const runJob = new Job(), optJob = new Job(), sensJob = new Job();

// ============================================================ run status
function setRun(kind, text) {
  $("#runDot").className = "dot " + (kind || "");
  $("#runText").textContent = text;
}

// ============================================================ inputs rail
const PRESET_LABEL = {
  ultrafine_3um: ["3 µm", "ultrafine"], fine_6um: ["6 µm", "fine"], standard_12um: ["12 µm", "default"],
  ifam_16um: ["16 µm", "IFAM"], cea_22um: ["22 µm", "CEA"], coarse_30um: ["30 µm", "coarse"],
};
const FURNACE_LABEL = { basic_tube: "Basic tube", standard_retort: "Standard retort", advanced_h2: "Advanced H₂" };
const POWDER_DOC = {
  ultrafine_3um: "Finest powder a 35 µm pixel would ever see. Fast sintering, most native oxide per gram, tightest pores for pyrolysis gas.",
  fine_6um: "Fine gas-atomised Cu. Sinters well below the solidus; oxide and gas escape become the harder part.",
  standard_12um: "Default assumption for a 2M30 copper slurry: d90 under ~25 µm for 25 µm layers.",
  ifam_16um: "Powder of the published IFAM/Incus copper LMM work.",
  cea_22um: "Powder of the CEA-LITEN DLP copper study that calibrates the sintering model.",
  coarse_30um: "Coarse end. Easy debinding, slow densification; expect lower density at a safe peak.",
};

function sliderPos(p, v) {
  if (p.log) return 1000 * Math.log(v / p.lo) / Math.log(p.hi / p.lo);
  return 1000 * (v - p.lo) / (p.hi - p.lo);
}
function sliderVal(p, x) {
  let v = p.log ? p.lo * Math.pow(p.hi / p.lo, x / 1000) : p.lo + (p.hi - p.lo) * x / 1000;
  if (p.kind === "int") return Math.round(v);
  const mag = Math.pow(10, Math.floor(Math.log10(Math.max(Math.abs(v), 1e-12))) - 2);
  return Math.round(v / mag) * mag;
}
function numStep(p) {
  if (p.kind === "int") return 1;
  const span = p.hi - p.lo;
  return span >= 500 ? 10 : span >= 50 ? 1 : span >= 5 ? 0.1 : span >= 0.5 ? 0.01 : 0.001;
}

function buildRail() {
  const pc = $("#powderChips");
  for (const [k, v] of Object.entries(PR.powder_presets)) {
    const [a, b] = PRESET_LABEL[k] || [k, ""];
    pc.append(el("button", { class: "chip", "data-preset": k, "aria-pressed": "false", title: POWDER_DOC[k] || "", onclick: () => applyPreset(PR.powder_presets[k]) },
      a, el("span", { class: "k" }, b)));
  }
  const fc = $("#furnaceChips");
  for (const k of Object.keys(PR.furnace_presets)) {
    fc.append(el("button", { class: "chip", "data-furnace": k, "aria-pressed": "false", onclick: () => applyPreset(PR.furnace_presets[k]) }, FURNACE_LABEL[k] || k));
  }
  const groups = $("#groups");
  for (const [g, gl] of Object.entries(PR.groups)) {
    const ps = REG.filter((p) => p.group === g);
    const det = el("details", { class: "grp", "data-group": g, open: g === "powder" || g === "furnace" ? true : null },
      el("summary", null, gl, el("span", { class: "cnt" }, String(ps.length)), el("span", { class: "mod" })));
    for (const p of ps) det.append(paramRow(p));
    groups.append(det);
  }
  $("#advCount").textContent = "(" + REG.filter((p) => p.advanced).length + " more)";
  $("#advToggle").checked = state.showAdvanced;
  $("#advToggle").addEventListener("change", (e) => { state.showAdvanced = e.target.checked; syncRail(); saveState(); });
  $("#resetAll").addEventListener("click", () => { state.values = { ...DEF }; syncRail(); inputsChanged(); });
  $("#railBtn").addEventListener("click", () => {
    const r = $("#rail"); const c = r.dataset.collapsed !== "false";
    r.dataset.collapsed = c ? "false" : "true"; $("#railBtn").setAttribute("aria-expanded", c ? "true" : "false");
  });
}

function paramRow(p) {
  const id = "in-" + p.key;
  const row = el("div", { class: "prm" + (p.kind === "bool" ? " bool" : ""), "data-key": p.key });
  const info = el("button", { class: "iconbtn", "aria-expanded": "false", "aria-label": "About " + p.label, html: ICON.info });
  const doc = el("p", { class: "doc", hidden: true }, (p.doc || "No further notes.") + "  Range " + fmt(p.lo) + "–" + fmt(p.hi) + " " + unit(p.unit) + ".");
  info.addEventListener("click", () => { const o = doc.hidden; doc.hidden = !o; info.setAttribute("aria-expanded", o ? "true" : "false"); });
  const undo = el("button", { class: "iconbtn", title: "Back to default", "aria-label": "Reset " + p.label, html: ICON.undo,
    onclick: () => setParam(p.key, DEF[p.key]) });
  row.append(el("div", { class: "prm-top" }, el("label", { for: id }, p.label), el("span", { class: "tag tag-" + p.tag, title: p.tag }, p.tag), info));
  if (p.kind === "bool") {
    const cb = el("input", { type: "checkbox", id });
    cb.addEventListener("change", () => setParam(p.key, cb.checked ? 1 : 0));
    row.append(el("div", { class: "prm-ctl" }, cb, el("span", { class: "unit" }, "available"), undo));
  } else {
    const rg = el("input", { type: "range", min: 0, max: 1000, step: 1, id: "rg-" + p.key, "aria-label": p.label + " slider" });
    const nb = el("input", { type: "number", id, min: p.lo, max: p.hi, step: numStep(p) });
    rg.addEventListener("input", () => { const v = sliderVal(p, +rg.value); nb.value = v; setParam(p.key, v, true); });
    nb.addEventListener("change", () => { let v = parseFloat(nb.value); if (!Number.isFinite(v)) v = DEF[p.key]; setParam(p.key, clamp(v, p.lo, p.hi)); });
    row.append(el("div", { class: "prm-ctl" }, rg, nb, el("span", { class: "unit" }, unit(p.unit)), undo));
  }
  row.append(doc);
  return row;
}

function setParam(key, v, fromSlider) {
  state.values[key] = v;
  syncRail(fromSlider ? key : null);
  inputsChanged();
}
function applyPreset(pv) { Object.assign(state.values, pv); syncRail(); inputsChanged(); }

function syncRail(skipKey) {
  for (const p of REG) {
    const row = $(`.prm[data-key="${p.key}"]`);
    if (!row) continue;
    const v = state.values[p.key];
    const changed = v !== DEF[p.key];
    row.classList.toggle("changed", changed);
    row.hidden = p.advanced && !state.showAdvanced && !changed;
    $(".iconbtn[title]", row).style.visibility = changed ? "visible" : "hidden";
    if (p.kind === "bool") { $("input", row).checked = v >= 0.5; continue; }
    if (p.key !== skipKey) $("#rg-" + p.key).value = sliderPos(p, v);
    $("#in-" + p.key).value = +v.toPrecision(4);
  }
  for (const det of $$("details.grp")) {
    const n = REG.filter((p) => p.group === det.dataset.group && state.values[p.key] !== DEF[p.key]).length;
    $(".mod", det).textContent = n ? n + " changed" : "";
  }
  let pdoc = "Powder does not match a preset: your own mix.";
  for (const b of $$("[data-preset]")) {
    const pv = PR.powder_presets[b.dataset.preset];
    const on = Object.entries(pv).every(([k, v]) => state.values[k] === v);
    b.setAttribute("aria-pressed", on ? "true" : "false");
    if (on) pdoc = POWDER_DOC[b.dataset.preset] || "";
  }
  $("#powderDoc").textContent = pdoc;
  let fdoc = "Furnace does not match a preset: your own settings.";
  for (const b of $$("[data-furnace]")) {
    const pv = PR.furnace_presets[b.dataset.furnace];
    const on = Object.entries(pv).every(([k, v]) => state.values[k] === v);
    b.setAttribute("aria-pressed", on ? "true" : "false");
    if (on) fdoc = (PR.preset_docs[b.dataset.furnace] || "").replace(/^DEFAULT\.\s*/, "");
  }
  $("#furnaceDoc").textContent = fdoc;
}

let runTimer = null;
function inputsChanged() {
  saveState();
  renderProgram();
  if (state.live) { clearTimeout(runTimer); runTimer = setTimeout(runNow, 450); }
  else setRun("", "inputs changed · press Run");
}

// ============================================================ running
async function runNow() {
  clearTimeout(runTimer);
  const cyc = curCycle();
  const t0 = performance.now();
  setRun("busy", "solving 0 %");
  $("#runBtn").disabled = false;
  try {
    const m = await runJob.run({ cmd: "simulate", scenario: { ...state.values }, cycle: cyc, N: state.N },
      (p) => setRun("busy", "solving " + Math.round(100 * p.frac) + " %"));
    showResult(m.result);
    const dt = (performance.now() - t0) / 1000;
    setRun(m.result.ok ? "ok" : "err", m.result.ok ? `solved in ${dt.toFixed(1)} s · ${m.result.t_h.length} steps` : "solver stopped early");
  } catch (e) {
    if (e instanceof Cancelled) return;
    setRun("err", "error: " + e.message);
  }
}

function showResult(r) {
  if (state.result) state.prevKpi = state.result.kpi;
  state.result = r;
  renderVerdict();
  renderKpis();
  renderMeta();
  for (const ch of CHARTS) ch.update(r);
}

// ============================================================ verdict + KPIs
const VERDICT_HELP = {
  gas_pressure: "Pyrolysis-gas pressure in the pores vs green/brown strength, with safety factor",
  thermal_stress: "Through-thickness temperature gradient stress vs strength",
  self_heating: "Part temperature above the furnace from binder burn or oxidation",
  binder_removed: "Binder fraction still in the part at the end",
  carbon_at_closure: "Carbon in the core when pores seal (it is trapped after that)",
  oxygen_at_closure: "Oxide oxygen in the core when pores seal",
  melting: "Peak temperature below the Cu–O solidus, beyond your safety margin",
  bloating: "Gas trapped in closed pores vs the sintering stress",
  density: "Final mean relative density vs your target",
  debind_guard: "Fastest ramp while more than 1 % binder remains vs the guard ramp",
};
function vStatus(v) { return !v.ok ? "crit" : v.index >= 0.9 ? "warn" : "good"; }

function renderVerdict() {
  const vd = state.result.kpi.verdict;
  const items = Object.entries(vd);
  const nFail = items.filter(([, v]) => !v.ok).length;
  const active = items.filter(([, v]) => v.ok && v.index >= 0.9).map(([, v]) => v.label);
  const head = $("#verdictHead");
  const st = nFail ? "crit" : "good";
  head.innerHTML = "";
  head.append(el("span", { class: "pill " + st, html: `<span class="st-${st}">${ICON[st]}</span>` + (nFail ? `${nFail} of 10 checks fail` : "All 10 checks pass") }));
  head.append(el("span", { class: "why" }, nFail ? "Change the cycle or run the optimiser." :
    active.length ? "At the limit, so these set the cycle time: " + active.slice(0, 3).join(" · ") : "No check is near its limit."));
  const list = $("#verdict");
  list.innerHTML = "";
  for (const [k, v] of items) {
    const s = vStatus(v);
    const idx = Number.isFinite(v.index) ? v.index : 0;
    const w = clamp(idx / 1.25, 0, 1) * 100;
    let val = (Math.abs(v.value) < 0.01 && v.unit !== "-" ? "< 0.01" : fmt(v.value)) + (v.unit && v.unit !== "-" ? " " + v.unit : "");
    if (k === "density") val = (100 * v.value).toFixed(1) + " %";
    if (k === "binder_removed") val = (100 * Math.max(v.value, 0)).toFixed(2) + " %";
    if (k === "melting") val = fmt(v.value) + " K";
    list.append(el("div", { class: "vrow", title: statusLabel[s] + " · index " + fmt(idx) },
      el("span", { class: "st-" + s, html: ICON[s], "aria-label": statusLabel[s] }),
      el("div", { class: "lbl" }, v.label, el("small", null, VERDICT_HELP[k] || "")),
      el("div", { class: "bullet", "aria-hidden": "true" }, el("i", { class: "fill-" + s, style: `width:${w}%` }), el("b", { style: "left:80%" })),
      el("div", { class: "val" }, val)));
  }
}

const KPIS = [
  { k: "duration_h", l: "Cycle time", u: "h", f: (x) => x.toFixed(1), hero: true, lowerBetter: true },
  { k: "rho_final", l: "Final density", u: "% TD", f: (x) => (100 * x).toFixed(1), scale: 100 },
  { k: "shrink_xy_pct", l: "Shrinkage x-y", u: "%", f: (x) => x.toFixed(1) },
  { k: "shrink_z_pct", l: "Shrinkage z (build)", u: "%", f: (x) => x.toFixed(1) },
  { k: "C_at_close_ppm", l: "Carbon at pore closure", u: "ppm", f: (x) => (x < 0.1 ? "< 0.1" : fmt(x, 2)), lowerBetter: true },
  { k: "O_at_close_ppm", l: "Oxygen at pore closure", u: "ppm", f: (x) => (x < 0.1 ? "< 0.1" : fmt(x, 2)), lowerBetter: true },
  { k: "grain_final_um", l: "Final grain size", u: "µm", f: (x) => x.toFixed(0) },
  { k: "iacs", l: "Conductivity estimate", u: "% IACS", f: (x) => x.toFixed(0) },
];
function renderKpis() {
  const k = state.result.kpi, p = state.prevKpi;
  const box = $("#kpis");
  box.innerHTML = "";
  for (const d of KPIS) {
    let v = k[d.k];
    if (d.k === "C_at_close_ppm" && !k.closed) v = k.C_final_ppm;
    if (d.k === "O_at_close_ppm" && !k.closed) v = k.O_final_ppm;
    let delta = "";
    if (p && Number.isFinite(p[d.k]) && Number.isFinite(v)) {
      const dv = (v - p[d.k]) * (d.scale || 1);
      if (Math.abs(dv) > 1e-9 * Math.max(1, Math.abs(v))) delta = (dv > 0 ? "▲ +" : "▼ ") + fmt(dv, 2) + " vs previous run";
    }
    box.append(el("div", { class: "kpi" + (d.hero ? " hero" : "") },
      el("span", { class: "k" }, d.l + (d.k.includes("close") && !k.closed ? " (pores stay open)" : "")),
      el("span", { class: "v", html: `${Number.isFinite(v) ? d.f(v) : "–"}<small>${d.u}</small>` }),
      el("span", { class: "d" }, delta)));
  }
}

function renderMeta() {
  const cyc = curCycle();
  const segs = cyc.segments || [];
  const peak = Math.max(...segs.map((s) => s.T_end_C));
  const meta = $("#cycleMeta");
  meta.innerHTML = "";
  meta.append(el("span", null, el("b", null, cyc.name || "Custom cycle")),
    el("span", null, C.cycleDurationH(cyc).toFixed(1) + " h"), el("span", null, segs.length + " segments"),
    el("span", null, "peak " + peak.toFixed(0) + " °C"),
    el("span", null, "wall " + state.values.half_thickness_mm * 2 + " mm, " + state.values.d50_um + " µm powder"));
}

// ============================================================ atmosphere
function atmOf(sg) {
  const s = state.values;
  const o2 = s.has_air_bleed >= 0.5 ? Math.min(sg.O2 || 0, 0.2095) : 0;
  const h2 = Math.min(sg.H2 || 0, s.h2_max);
  const dp = Math.min(sg.dp_C, s.dp_max_C);
  const pc = (x) => (x * 100 >= 1 ? (x * 100).toFixed(0) : (x * 100).toFixed(1)) + " %";
  if (o2 > 0) return { k: "ox", label: o2 >= 0.2 ? "Air" : "N₂ + " + pc(o2) + " O₂" };
  if (h2 > 0) return dp > -20 ? { k: "wet", label: pc(h2) + " H₂ wet" } : { k: "dry", label: pc(h2) + " H₂ dry" };
  return { k: "inert", label: "N₂" };
}
const ATM_KEY = [["inert", "N₂ (inert)"], ["ox", "N₂ + O₂ / air"], ["wet", "Forming gas, wet"], ["dry", "Forming gas, dry"]];

// ============================================================ charts
let hoverT = null;
const CHARTS = [];
function niceStep(span, n) {
  const raw = span / Math.max(n, 1);
  const p = Math.pow(10, Math.floor(Math.log10(raw)));
  const m = raw / p;
  return (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p;
}
function ticksLin(a, b, n) {
  const st = niceStep(b - a, n);
  const out = [];
  for (let v = Math.ceil(a / st - 1e-9) * st; v <= b + st * 1e-9; v += st) out.push(+v.toPrecision(12));
  return out;
}
const decFor = (st) => Math.max(0, -Math.floor(Math.log10(st) + 1e-9));
const tickFmt = (st) => (v) => v.toFixed(decFor(st));
function bsearch(a, x) {
  let lo = 0, hi = a.length - 1;
  while (hi - lo > 1) { const m = (lo + hi) >> 1; if (a[m] <= x) lo = m; else hi = m; }
  return x - a[lo] <= a[hi] - x ? lo : hi;
}
function lineSwatch(color, dash) {
  const s = sv("svg", { width: 18, height: 8, "aria-hidden": "true" });
  s.append(sv("line", { x1: 1, y1: 4, x2: 17, y2: 4, style: `stroke:${color};stroke-width:2;stroke-linecap:round`, "stroke-dasharray": dash || null }));
  return s;
}

class LineChart {
  constructor(id, cfg) {
    this.fig = document.getElementById(id);
    this.cfg = cfg;
    this.fig.innerHTML = "";
    this.tblBtn = el("button", { class: "btn ghost small", "aria-expanded": "false" }, "Table");
    this.fig.append(el("div", { class: "chart-head" }, el("h3", null, cfg.title), el("span", { class: "cap" }, cfg.cap || ""), this.tblBtn));
    this.legend = el("div", { class: "legend" });
    this.fig.append(this.legend);
    this.plot = el("div", { class: "plot" });
    this.fig.append(this.plot);
    this.tip = el("div", { class: "tip", hidden: true });
    this.plot.append(this.tip);
    this.tbl = el("div", { class: "tblwrap", hidden: true });
    this.fig.append(this.tbl);
    this.tblBtn.addEventListener("click", () => {
      const o = this.tbl.hidden; this.tbl.hidden = !o; this.tblBtn.setAttribute("aria-expanded", o ? "true" : "false");
      if (o) this.renderTable();
    });
    this.r = null;
    CHARTS.push(this);
    new ResizeObserver(() => { if (this.r && this.plot.clientWidth !== this.w) this.draw(); }).observe(this.plot);
  }
  update(r) { this.r = r; this.draw(); if (!this.tbl.hidden) this.renderTable(); }
  series() {
    const r = this.r;
    return this.cfg.series.map((s) => ({ ...s, y: s.get(r.series, r.kpi, state.values) })).filter((s) => s.y);
  }
  draw() {
    const r = this.r, cfg = this.cfg;
    if (!r) return;
    const W = this.plot.clientWidth || 600;
    this.w = W;
    const narrow = W < 460;
    const direct = cfg.direct === true && !narrow;
    const H = cfg.height || 190;
    const band = !!cfg.band;
    const M = { l: 46, r: direct ? 92 : 12, t: cfg.segNos ? 16 : 8, b: band ? 42 : 24 };
    const pw = W - M.l - M.r, ph = H - M.t - M.b;
    const t = r.t_h, n = t.length, tmax = t[n - 1] || 1;
    const S = this.series();
    // y domain
    let lo = Infinity, hi = -Infinity;
    for (const s of S) for (let i = 0; i < n; i++) { const v = s.y[i]; if (Number.isFinite(v)) { if (v < lo) lo = v; if (v > hi) hi = v; } }
    const refs = cfg.refs ? cfg.refs(r.kpi, state.values).filter((x) => Number.isFinite(x.y)) : [];
    if (cfg.refsInDomain !== false) for (const x of refs) { lo = Math.min(lo, x.y); hi = Math.max(hi, x.y); }
    if (!Number.isFinite(lo) || !Number.isFinite(hi)) { lo = cfg.y === "log" ? 1 : 0; hi = cfg.y === "log" ? 10 : 1; }
    const log = cfg.y === "log";
    if (log) {
      const fl = cfg.floor || 0.1;
      lo = Math.max(lo, fl); hi = Math.max(hi, lo * 10);
      lo = Math.pow(10, Math.floor(Math.log10(lo))); hi = Math.pow(10, Math.ceil(Math.log10(hi)));
    } else {
      if (cfg.min != null) lo = cfg.min; if (cfg.max != null) hi = cfg.max;
      if (cfg.minMax != null) hi = Math.max(hi, cfg.minMax);
      if (cfg.clampLo != null) lo = Math.max(lo, cfg.clampLo);
      if (cfg.clampHi != null) hi = Math.min(hi, cfg.clampHi);
      if (!(hi > lo)) { hi = lo + 1; }
      const st = niceStep(hi - lo, 4);
      lo = Math.floor(lo / st) * st; hi = Math.ceil(hi / st - 1e-9) * st;
    }
    const X = (v) => M.l + (v / tmax) * pw;
    const Y = log ? (v) => M.t + ph * (1 - (Math.log10(Math.max(v, lo)) - Math.log10(lo)) / (Math.log10(hi) - Math.log10(lo)))
                  : (v) => M.t + ph * (1 - (clamp(v, lo, hi) - lo) / (hi - lo));
    this.X = X; this.Y = Y; this.M = M; this.pw = pw; this.ph = ph; this.tmax = tmax; this.S = S;
    const svg = sv("svg", { viewBox: `0 0 ${W} ${H}`, height: H, role: "img", "aria-label": cfg.title });
    // grid + y ticks
    const yt = log ? (() => { const a = []; for (let e = Math.log10(lo); e <= Math.log10(hi) + 1e-9; e++) a.push(Math.pow(10, e)); return a; })() : ticksLin(lo, hi, 4);
    const yf = cfg.yfmt || (log ? (v) => (v >= 1 ? v.toFixed(0) : String(+v.toPrecision(1))) : tickFmt(niceStep(hi - lo, 4)));
    for (const v of yt) {
      const y = Y(v);
      svg.append(sv("line", { class: "gl", x1: M.l, x2: M.l + pw, y1: y, y2: y }));
      const tx = sv("text", { x: M.l - 6, y: y + 3.5, "text-anchor": "end" });
      tx.textContent = yf(v);
      svg.append(tx);
    }
    // segment boundaries
    const bounds = C.cycleBoundaries(r.cycle || curCycle());
    if (cfg.segNos || band) {
      const segs = (r.cycle || curCycle()).segments;
      let segStart = new Map();
      for (const b of bounds) { const k = segs.indexOf(b[2]); if (!segStart.has(k)) segStart.set(k, [b[0] / 3600, b[1] / 3600]); else segStart.get(k)[1] = b[1] / 3600; }
      if (cfg.segNos) for (const [k, [a, b]] of segStart) {
        if (a > 0) svg.append(sv("line", { class: "segl", x1: X(a), x2: X(a), y1: M.t, y2: M.t + ph }));
        if (X(b) - X(a) > 14) { const tx = sv("text", { class: "segno", x: (X(a) + X(b)) / 2, y: M.t - 5, "text-anchor": "middle" }); tx.textContent = k + 1; svg.append(tx); }
      }
      if (band) {
        const by = M.t + ph + 4;
        for (const b of bounds) {
          const a = atmOf(b[2]);
          const x0 = X(b[0] / 3600), x1 = X(b[1] / 3600);
          svg.append(sv("rect", { class: "band-" + a.k, x: x0, y: by, width: Math.max(x1 - x0 - 1, 0.5), height: 13 }));
        }
        // merge equal neighbours for labels
        let cur = null;
        const runs = [];
        for (const b of bounds) { const a = atmOf(b[2]); if (cur && cur.label === a.label) cur.t1 = b[1]; else { cur = { label: a.label, t0: b[0], t1: b[1] }; runs.push(cur); } }
        for (const u of runs) {
          const x0 = X(u.t0 / 3600), x1 = X(u.t1 / 3600);
          if (x1 - x0 > u.label.length * 5.8 + 8) { const tx = sv("text", { class: "bandt", x: (x0 + x1) / 2, y: by + 10, "text-anchor": "middle" }); tx.textContent = u.label; svg.append(tx); }
        }
      }
    }
    // x axis
    svg.append(sv("line", { class: "ax", x1: M.l, x2: M.l + pw, y1: M.t + ph, y2: M.t + ph }));
    const xtY = M.t + ph + (band ? 32 : 15);
    const xf = tickFmt(niceStep(tmax, narrow ? 4 : 7));
    for (const v of ticksLin(0, tmax, narrow ? 4 : 7)) {
      const tx = sv("text", { x: X(v), y: xtY, "text-anchor": "middle" }); tx.textContent = xf(v); svg.append(tx);
    }
    const xl = sv("text", { x: M.l + pw, y: xtY + (band ? 0 : 0), "text-anchor": "start", dx: 4 }); xl.textContent = "h"; svg.append(xl);
    // vertical markers
    const vms = cfg.vmarks ? cfg.vmarks(r.kpi).filter((m) => Number.isFinite(m.t)) : [];
    for (const m of vms) {
      svg.append(sv("line", { class: "vm", x1: X(m.t), x2: X(m.t), y1: M.t, y2: M.t + ph }));
      const tx = sv("text", { class: "vmt", x: X(m.t) + 4, y: M.t + 10 }); tx.textContent = m.label; svg.append(tx);
    }
    // refs
    for (const x of refs) {
      if (x.y < lo || x.y > hi) continue;
      svg.append(sv("line", { class: "ref" + (x.crit ? " ref-crit" : ""), x1: M.l, x2: M.l + pw, y1: Y(x.y), y2: Y(x.y) }));
      const tx = sv("text", { class: "reft", x: M.l + 4, y: Y(x.y) - 4 }); tx.textContent = x.label; svg.append(tx);
    }
    // lines (min/max decimation per pixel column keeps peaks)
    const ends = [];
    for (const s of S) {
      let d = "";
      const cols = Math.max(50, Math.floor(pw));
      if (n > cols * 3) {
        let lastCol = -1, mn = null, mx = null, first = true;
        const flush = () => {
          if (mn == null) return;
          const xx = X(t[mn[0]]).toFixed(1);
          const pts = mn[0] < mx[0] ? [mn, mx] : [mx, mn];
          for (const q of pts) { d += (first ? "M" : "L") + X(t[q[0]]).toFixed(1) + " " + Y(q[1]).toFixed(1); first = false; }
        };
        for (let i = 0; i < n; i++) {
          const v = s.y[i]; if (!Number.isFinite(v)) continue;
          const c = Math.floor((t[i] / tmax) * cols);
          if (c !== lastCol) { flush(); lastCol = c; mn = [i, v]; mx = [i, v]; }
          else { if (v < mn[1]) mn = [i, v]; if (v > mx[1]) mx = [i, v]; }
        }
        flush();
      } else {
        let first = true;
        for (let i = 0; i < n; i++) { const v = s.y[i]; if (!Number.isFinite(v)) { first = true; continue; } d += (first ? "M" : "L") + X(t[i]).toFixed(1) + " " + Y(v).toFixed(1); first = false; }
      }
      svg.append(sv("path", { class: "ln", d, style: `stroke:${s.color}`, "stroke-dasharray": s.dash || null }));
      let li = n - 1; while (li > 0 && !Number.isFinite(s.y[li])) li--;
      ends.push({ y: Y(s.y[li]), label: s.short || s.label });
    }
    if (direct) {
      ends.sort((a, b) => a.y - b.y);
      for (let i = 1; i < ends.length; i++) if (ends[i].y - ends[i - 1].y < 12) ends[i].y = ends[i - 1].y + 12;
      const over = ends.length ? ends[ends.length - 1].y - (M.t + ph + 4) : 0;
      if (over > 0) for (const e of ends) e.y -= over;
      for (const e of ends) { const tx = sv("text", { class: "dl", x: M.l + pw + 6, y: e.y + 3.5 }); tx.textContent = e.label; svg.append(tx); }
    }
    this.xh = sv("line", { class: "xh", x1: 0, x2: 0, y1: M.t, y2: M.t + ph, visibility: "hidden" });
    svg.append(this.xh);
    this.dots = S.map((s) => { const c = sv("circle", { r: 4, style: `fill:${s.color};stroke:var(--surface);stroke-width:2`, visibility: "hidden" }); svg.append(c); return c; });
    const hit = sv("rect", { x: M.l, y: 0, width: pw, height: H, fill: "transparent" });
    hit.addEventListener("pointermove", (e) => { const b = svg.getBoundingClientRect(); const x = (e.clientX - b.left) * (W / b.width); setHover(((x - M.l) / pw) * tmax, this); });
    hit.addEventListener("pointerleave", () => setHover(null, null));
    svg.append(hit);
    const old = $("svg", this.plot); if (old) old.remove();
    this.plot.insertBefore(svg, this.tip);
    // legend
    this.legend.innerHTML = "";
    for (const s of S) this.legend.append(el("span", null, lineSwatch(s.color, s.dash), s.label));
    if (band) for (const [k, l] of ATM_KEY) this.legend.append(el("span", null, el("i", { class: "swatch sw-" + k }), l));
    this.setHover(hoverT, null);
  }
  setHover(tq, src) {
    if (!this.r || !this.xh) return;
    if (tq == null || tq < 0 || tq > this.tmax) {
      this.xh.setAttribute("visibility", "hidden"); for (const d of this.dots) d.setAttribute("visibility", "hidden"); this.tip.hidden = true; return;
    }
    const i = bsearch(this.r.t_h, tq);
    const x = this.X(this.r.t_h[i]);
    this.xh.setAttribute("x1", x); this.xh.setAttribute("x2", x); this.xh.setAttribute("visibility", "visible");
    this.S.forEach((s, k) => {
      const v = s.y[i]; const d = this.dots[k];
      if (Number.isFinite(v)) { d.setAttribute("cx", x); d.setAttribute("cy", this.Y(v)); d.setAttribute("visibility", "visible"); } else d.setAttribute("visibility", "hidden");
    });
    if (src !== this) { this.tip.hidden = true; return; }
    const Ts = this.r.series.Tset[i];
    this.tip.innerHTML = `<div class="th">t ${this.r.t_h[i].toFixed(2)} h · set ${Ts.toFixed(0)} °C</div>` + this.S.map((s) =>
      `<div class="tr"><i style="background:${s.color}"></i><span>${esc(s.label)}</span><b>${(this.cfg.tfmt || fmt)(s.y[i])}${this.cfg.unit ? " " + this.cfg.unit : ""}</b></div>`).join("");
    this.tip.hidden = false;
    const pwp = this.plot.clientWidth, sc = pwp / this.w;
    const tw = this.tip.offsetWidth;
    let left = x * sc + 12; if (left + tw > pwp) left = x * sc - tw - 12;
    this.tip.style.left = Math.max(0, left) + "px"; this.tip.style.top = (this.M.t + 4) + "px";
  }
  renderTable() {
    const r = this.r; if (!r) return;
    const S = this.series(), t = r.t_h, n = t.length, tmax = t[n - 1];
    const rows = 48;
    let h = `<table class="data"><thead><tr><th>t (h)</th><th>Setpoint °C</th>${S.map((s) => `<th>${esc(s.label)}${this.cfg.unit ? " (" + esc(this.cfg.unit) + ")" : ""}</th>`).join("")}</tr></thead><tbody>`;
    let last = -1;
    for (let k = 0; k <= rows; k++) {
      const i = bsearch(t, (k / rows) * tmax); if (i === last) continue; last = i;
      h += `<tr><td>${t[i].toFixed(2)}</td><td>${r.series.Tset[i].toFixed(0)}</td>${S.map((s) => `<td>${(this.cfg.tfmt || fmt)(s.y[i])}</td>`).join("")}</tr>`;
    }
    this.tbl.innerHTML = h + "</tbody></table>";
  }
}
function setHover(t, src) { hoverT = t; for (const c of CHARTS) c.setHover(t, src); }

const col = (i) => `var(--s${i})`;
const REF = "var(--sref)";
const scaled = (a, f) => Float64Array.from(a, (x) => x * f);
function makeCharts() {
  new LineChart("ch-temp", {
    title: "Temperature and atmosphere", cap: "Numbers above the plot are furnace program rows; the strip below is the gas.",
    height: 290, band: true, segNos: true, unit: "°C", tfmt: (v) => v.toFixed(0), min: 0,
    series: [
      { label: "Furnace setpoint", short: "setpoint", color: REF, dash: "5 4", get: (S) => S.Tset },
      { label: "Furnace gas", short: "gas", color: col(1), get: (S) => S.Tf },
      { label: "Part core", short: "core", color: col(2), get: (S) => S.T_center },
      { label: "Part surface", short: "surface", color: col(3), get: (S) => S.T_surface },
    ],
  });
  const closeMark = (k) => [{ t: k.t_close_h, label: "pores close" }];
  new LineChart("ch-binder", {
    title: "Binder left", cap: "% of the printed binder", unit: "%", min: 0, max: 100, tfmt: (v) => fmt(v, 3), direct: false,
    series: [{ label: "Binder remaining", color: col(1), get: (S) => scaled(S.binder_left, 100) }],
  });
  new LineChart("ch-carbon", {
    title: "Carbon", cap: "ppm by mass, log scale", unit: "ppm", y: "log", floor: 0.1, vmarks: closeMark,
    refs: (k, s) => [{ y: s.C_spec_ppm, label: "limit at closure", crit: true }],
    series: [{ label: "Core", color: col(1), get: (S) => S.C_ppm_center }, { label: "Mean", color: col(2), get: (S) => S.C_ppm_mean }],
  });
  new LineChart("ch-oxygen", {
    title: "Oxide oxygen", cap: "ppm by mass, log scale", unit: "ppm", y: "log", floor: 0.1, vmarks: closeMark,
    refs: (k, s) => [{ y: s.O_spec_ppm, label: "limit at closure", crit: true }],
    series: [{ label: "Core", color: col(1), get: (S) => S.O_ppm_center }, { label: "Mean", color: col(2), get: (S) => S.O_ppm_mean }],
  });
  new LineChart("ch-rho", {
    title: "Relative density", cap: "of the metal skeleton", unit: "", tfmt: (v) => (100 * v).toFixed(1) + " %", yfmt: (v) => (100 * v).toFixed(0) + "%",
    refs: (k, s) => [{ y: s.rho_target, label: "target" }], vmarks: closeMark,
    series: [{ label: "Mean", color: col(1), get: (S) => S.rho_mean }, { label: "Core", color: col(2), get: (S) => S.rho_center }, { label: "Surface", color: col(3), get: (S) => S.rho_surface }],
  });
  new LineChart("ch-shrink", {
    title: "Linear shrinkage", cap: "scale the CAD by 1/(1 − shrinkage)", unit: "%", min: 0, tfmt: (v) => v.toFixed(2), direct: true,
    series: [{ label: "x-y (in layer)", short: "x-y", color: col(1), get: (S) => scaled(S.shrink_xy, 100) }, { label: "z (build)", short: "z", color: col(2), get: (S) => scaled(S.shrink_z, 100) }],
  });
  new LineChart("ch-grain", {
    title: "Mean grain size", cap: "µm", unit: "µm", min: 0, direct: false, tfmt: (v) => v.toFixed(1),
    series: [{ label: "Grain size", color: col(1), get: (S) => S.G_um }],
  });
  new LineChart("ch-risk", {
    title: "Risk indices", cap: "each divided by its limit: above 1 fails", unit: "", min: 0, minMax: 1.2, tfmt: (v) => fmt(v, 3), height: 220,
    refs: () => [{ y: 1, label: "limit", crit: true }],
    series: [
      { label: "Debinding gas pressure", short: "gas pressure", color: col(1), get: (S) => S.Pi_gas },
      { label: "Thermal stress", short: "thermal", color: col(2), get: (S) => S.Pi_th },
      { label: "Trapped gas", short: "trapped gas", color: col(3), get: (S) => Float64Array.from(S.Pi_bloat, (x) => Math.max(x, 0)) },
      { label: "Self-heating", short: "self-heating", color: col(4), get: (S, k, s) => Float64Array.from(S.exo_gen, (x) => Math.max(x, 0) / s.dT_exo_max) },
    ],
  });
  new LineChart("ch-melt", {
    title: "Margin to melting", cap: "K below the Cu–O solidus after your safety margin; shown above 700 °C", unit: "K", clampHi: 150, clampLo: -30, height: 220, direct: false, tfmt: (v) => v.toFixed(1),
    refs: () => [{ y: 0, label: "no margin left", crit: true }],
    series: [{ label: "Margin", color: col(1), get: (S) => Float64Array.from(S.melt_margin, (x, i) => (S.Tset[i] > 700 ? x : NaN)) }],
  });
  new LineChart("ch-dew", {
    title: "Outlet dew point", cap: "°C at the retort exhaust", unit: "°C", direct: false, tfmt: (v) => v.toFixed(1),
    series: [{ label: "Dew point", color: col(1), get: (S) => S.dewpoint_out }],
  });
  new LineChart("ch-gas", {
    title: "Outlet gas", cap: "ppm by volume, log scale", unit: "ppm", y: "log", floor: 0.1,
    series: [
      { label: "O₂", color: col(1), get: (S) => scaled(S.xO2, 1e6) },
      { label: "CO", color: col(2), get: (S) => scaled(S.xCO, 1e6) },
      { label: "CO₂", color: col(3), get: (S) => scaled(S.xCO2, 1e6) },
      { label: "Hydrocarbons", color: col(4), get: (S) => scaled(S.x_hc, 1e6) },
    ],
  });
}

// ============================================================ program table
const COLS = [
  { k: "T_end_C", f: (v) => v, p: (v) => v, step: 5 },
  { k: "ramp_Kmin", f: (v) => v, p: (v) => Math.max(v, 0.01), step: 0.1 },
  { k: "hold_h", f: (v) => v, p: (v) => Math.max(v, 0), step: 0.25 },
  { k: "O2", f: (v) => +(v * 100).toFixed(3), p: (v) => clamp(v / 100, 0, 0.2095), step: 0.1 },
  { k: "H2", f: (v) => +(v * 100).toFixed(2), p: (v) => clamp(v / 100, 0, 1), step: 1 },
  { k: "dp_C", f: (v) => v, p: (v) => clamp(v, -60, 80), step: 5 },
];
function segHours(cyc) {
  const out = [];
  let T = cyc.T_start_C == null ? 25 : cyc.T_start_C;
  for (const s of cyc.segments) { out.push(Math.abs(s.T_end_C - T) / Math.max(s.ramp_Kmin, 1e-9) / 60 + s.hold_h); T = s.T_end_C; }
  return out;
}
function segIssues(cyc) {
  const s = state.values, out = [];
  cyc.segments.forEach((g, i) => {
    const n = i + 1;
    if ((g.H2 || 0) > s.h2_max + 1e-9) out.push([i, "H2", `Row ${n}: ${(g.H2 * 100).toFixed(0)} % H₂ asked, furnace max ${(s.h2_max * 100).toFixed(0)} %. Runs at ${(s.h2_max * 100).toFixed(0)} %.`]);
    if ((g.O2 || 0) > 0 && s.has_air_bleed < 0.5) out.push([i, "O2", `Row ${n}: O₂ asked but the furnace has no air bleed. Runs as N₂.`]);
    if (g.dp_C > s.dp_max_C + 1e-9) out.push([i, "dp_C", `Row ${n}: dew point ${g.dp_C} °C asked, humidifier max ${s.dp_max_C} °C. Runs at ${s.dp_max_C} °C.`]);
    if (g.ramp_Kmin > s.max_ramp_Kmin + 1e-9) out.push([i, "ramp_Kmin", `Row ${n}: ramp ${g.ramp_Kmin} K/min is above the furnace's ${s.max_ramp_Kmin} K/min; the furnace lag will stretch it.`]);
    if (g.T_end_C > s.T_furnace_max_C) out.push([i, "T_end_C", `Row ${n}: ${g.T_end_C} °C is above the furnace maximum of ${s.T_furnace_max_C} °C.`]);
  });
  return out;
}
function renderProgram() {
  const cyc = curCycle();
  const tb = $("#progTable tbody");
  tb.innerHTML = "";
  const hrs = segHours(cyc);
  const iss = segIssues(cyc);
  cyc.segments.forEach((g, i) => {
    const tr = el("tr");
    tr.append(el("td", { class: "n" }, String(i + 1)));
    for (const c of COLS) {
      const inp = el("input", { type: "number", step: c.step, value: c.f(g[c.k]), "aria-label": `Row ${i + 1} ${c.k}`, id: `pg-${i}-${c.k}` });
      if (iss.some(([j, k]) => j === i && k === c.k)) inp.classList.add("flag");
      inp.addEventListener("change", () => { const v = parseFloat(inp.value); if (Number.isFinite(v)) editSeg(i, c.k, c.p(v)); });
      tr.append(el("td", null, inp));
    }
    const a = atmOf(g);
    tr.append(el("td", { class: "atm" }, el("span", { class: "status" }, el("i", { class: "swatch sw-" + a.k }), a.label)));
    const note = el("input", { class: "note", value: g.note || "", "aria-label": `Row ${i + 1} note`, id: `pg-${i}-note` });
    note.addEventListener("change", () => editSeg(i, "note", note.value));
    tr.append(el("td", { style: "text-align:left" }, note));
    tr.append(el("td", { class: "dur" }, hrs[i].toFixed(2)));
    tr.append(el("td", null, el("button", { class: "iconbtn", "aria-label": `Delete row ${i + 1}`, html: ICON.del, onclick: () => delSeg(i) })));
    tb.append(tr);
  });
  $("#progTotal").textContent = C.cycleDurationH(cyc).toFixed(1);
  const box = $("#progIssues");
  box.innerHTML = "";
  for (const [, , msg] of iss) box.append(el("div", null, el("span", { class: "st-warn", html: ICON.warn }), el("span", null, msg)));
}
function toCustom() {
  if (state.source !== "custom") {
    const c = clone(curCycle());
    c.name = "Custom (from " + (curCycle().name || state.source) + ")";
    state.cycles.custom = c;
    state.source = "custom";
    syncSource();
  }
  return state.cycles.custom;
}
function editSeg(i, k, v) { const c = toCustom(); c.segments[i][k] = v; cycleChanged(); }
function delSeg(i) { const c = toCustom(); if (c.segments.length > 1) c.segments.splice(i, 1); cycleChanged(); }
function addSeg() {
  const c = toCustom();
  const last = c.segments[c.segments.length - 1] || { T_end_C: 25, O2: 0, H2: 0, dp_C: -60 };
  c.segments.push({ T_end_C: last.T_end_C, ramp_Kmin: 5, hold_h: 1, O2: last.O2 || 0, H2: last.H2 || 0, dp_C: last.dp_C, note: "new" });
  cycleChanged();
}
function cycleChanged() { saveState(); renderProgram(); renderMeta(); if (state.live) { clearTimeout(runTimer); runTimer = setTimeout(runNow, 300); } }

function copyText(txt) {
  const box = $("#copyBox");
  const fallback = () => { box.hidden = false; box.value = txt; box.focus(); box.select(); setRun("", "select the text below and copy it"); };
  try {
    navigator.clipboard.writeText(txt).then(() => { box.hidden = true; setRun("ok", "copied to clipboard"); }, fallback);
  } catch (e) { fallback(); }
}
function cycleTsv() {
  const cyc = curCycle();
  const rows = [["#", "Target C", "Ramp K/min", "Hold h", "O2 %", "H2 %", "Dew point C", "Note"]];
  cyc.segments.forEach((g, i) => rows.push([i + 1, g.T_end_C, +g.ramp_Kmin.toFixed(3), g.hold_h, +(g.O2 * 100).toFixed(3), +(g.H2 * 100).toFixed(2), g.dp_C, g.note || ""]));
  return rows.map((r) => r.join("\t")).join("\n");
}

// ============================================================ source switch
function syncSource() {
  for (const b of $$("#srcSeg button")) {
    b.setAttribute("aria-pressed", b.dataset.src === state.source ? "true" : "false");
    b.disabled = b.dataset.src === "custom" && !state.cycles.custom;
  }
}
function setSource(src) {
  if (!state.cycles[src]) return;
  state.source = src; syncSource(); saveState(); renderProgram(); renderMeta(); runNow();
}

// ============================================================ optimiser
function renderCands() {
  const tb = $("#candTable tbody");
  tb.innerHTML = "";
  const sy = state.synth;
  if (!sy) { $("#candNote").textContent = "No optimiser run yet."; return; }
  const maxH = Math.max(...sy.candidates.map((c) => c.duration_h));
  for (const c of sy.candidates) {
    const best = c.cycle && c.cycle.name === sy.best;
    const s = c.feasible ? "good" : "crit";
    tb.append(el("tr", { class: best ? "best" : null },
      el("td", null, c.topology),
      el("td", { class: "num" }, c.T_B_C.toFixed(0) + " °C"),
      el("td", null, el("span", { class: "status" }, el("span", { class: "st-" + s, html: ICON[s] }), c.feasible ? (best ? "Shortest passing" : "Passes") : "Breaks a limit")),
      el("td", null, el("span", { class: "hrs" }, el("i", { class: c.feasible ? "" : "bad", style: `width:${Math.max(4, 120 * c.duration_h / maxH)}px` }), c.duration_h.toFixed(1) + " h")),
      el("td", null, c.cycle ? el("button", { class: "btn small", onclick: () => loadCandidate(c) }, "Load") : "")));
  }
  $("#candNote").textContent = `${sy.candidates.filter((c) => c.feasible).length} of ${sy.candidates.length} candidates pass. ` +
    "Strategies that burn binder with more O₂ reach the same end time but break the self-heating or gas limits on the way. " +
    (sy.at ? "Optimised " + new Date(sy.at).toLocaleString() + " for the inputs at that time." : "Shown for the default inputs.");
}
function loadCandidate(c) {
  state.cycles.opt = clone(c.cycle);
  setSource("opt");
  document.getElementById("results").scrollIntoView({ behavior: "smooth" });
}
async function optimise() {
  $("#optBtn").disabled = true; $("#optCancel").hidden = false; $("#optProg").hidden = false;
  const bar = $("#optProg i"), st = $("#optStage");
  const t0 = performance.now();
  bar.style.width = "0%"; st.textContent = "starting";
  const tick = setInterval(() => { st.dataset.el = ((performance.now() - t0) / 1000).toFixed(0); }, 1000);
  try {
    const m = await optJob.run({ cmd: "synthesize", scenario: { ...state.values }, N: 8 },
      (p) => { bar.style.width = (100 * (p.frac || 0)).toFixed(0) + "%"; st.textContent = (p.stage || "") + " · " + ((performance.now() - t0) / 1000).toFixed(0) + " s"; });
    state.synth = { candidates: m.candidates, best: m.best, at: Date.now() };
    renderCands();
    if (m.best) {
      const b = m.candidates.find((c) => c.cycle && c.cycle.name === m.best);
      state.cycles.opt = clone(b.cycle);
      state.source = "opt"; syncSource(); renderProgram();
      if (m.result) { m.result.cycle = state.cycles.opt; showResult(m.result); setRun("ok", "optimised cycle loaded"); } else runNow();
      st.textContent = `done in ${((performance.now() - t0) / 1000).toFixed(0)} s · shortest passing cycle ${b.duration_h.toFixed(1)} h`;
    } else st.textContent = "no candidate passes every check with these inputs; see the table";
    saveState();
  } catch (e) {
    st.textContent = e instanceof Cancelled ? "cancelled" : "error: " + e.message;
  } finally {
    clearInterval(tick);
    $("#optBtn").disabled = false; $("#optCancel").hidden = true; $("#optProg").hidden = true;
  }
}

// ============================================================ 3-D
const GEO = {
  cantilever: { name: "Cantilever", why: "An 18 mm arm, 2 mm thick, off a 6 mm column. Gravity sag of the arm is the distortion copper parts show when they sinter hot and soft." },
  heat_sink: { name: "Heat sink", why: "24 mm base with five 1.5 mm fins. Thin fins and a thick base densify at different rates." },
  ring: { name: "Ring", why: "20 mm OD, 12 mm ID, 12 mm tall. Setter friction holds the bottom back and makes an elephant foot." },
};
const three = { ok: false };
function densColor(r) {
  const stops = [[0.55, [246, 227, 211]], [0.7, [228, 167, 122]], [0.85, [191, 106, 51]], [1.0, [107, 46, 14]]];
  r = clamp(r, 0.55, 1.0);
  for (let i = 1; i < stops.length; i++) if (r <= stops[i][0]) {
    const [a, ca] = stops[i - 1], [b, cb] = stops[i]; const f = (r - a) / (b - a);
    return ca.map((x, k) => (x + (cb[k] - x) * f) / 255);
  }
  return stops[3][1].map((x) => x / 255);
}
function init3D() {
  const geos = D.geo3d || {};
  const names = Object.keys(GEO).filter((k) => geos[k]);
  $("#cbarGrad").style.background = "linear-gradient(90deg,rgb(246,227,211),rgb(228,167,122) 33%,rgb(191,106,51) 67%,rgb(107,46,14))";
  const seg = $("#geoSeg");
  for (const k of names) seg.append(el("button", { "data-geo": k, "aria-pressed": "false", onclick: () => showGeo(k) }, GEO[k].name));
  if (!names.length || !window.THREE) {
    $("#viewer").append(el("div", { class: "nogl" }, !names.length ? "3-D results are not bundled in this build." : "The 3-D library did not load; check that cdnjs is reachable."));
    return;
  }
  const canvas = $("#glc");
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true }); } catch (e) {
    $("#viewer").append(el("div", { class: "nogl" }, "WebGL is not available in this browser."));
    return;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  const scene = new THREE.Scene();
  const cam = new THREE.PerspectiveCamera(35, 1, 0.1, 1000);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8f94, 0.85));
  const dl = new THREE.DirectionalLight(0xffffff, 0.75); dl.position.set(30, -40, 60); scene.add(dl);
  const dl2 = new THREE.DirectionalLight(0xffffff, 0.3); dl2.position.set(-40, 30, 20); scene.add(dl2);
  let controls = null;
  if (THREE.OrbitControls) { controls = new THREE.OrbitControls(cam, canvas); controls.enableDamping = true; controls.dampingFactor = 0.12; }
  Object.assign(three, { ok: true, renderer, scene, cam, controls, canvas, frame: 0, playing: false, geo: null });
  const resize = () => {
    const w = canvas.parentElement.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); three.dirty = true;
  };
  new ResizeObserver(resize).observe(canvas);
  if (controls) controls.addEventListener("change", () => { three.dirty = true; });
  let visible = true;
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(canvas);
  let lastPlay = 0;
  const loop = (ts) => {
    requestAnimationFrame(loop);
    if (!visible) return;
    if (three.playing && ts - lastPlay > 140) {
      lastPlay = ts;
      const n = three.geo.data.frames.length;
      setFrame(three.frame + 1 >= n ? 0 : three.frame + 1);
      if (three.frame === n - 1) { three.playing = false; $("#playBtn").textContent = "Play"; }
    }
    const moved = controls ? controls.update() : false;
    if (three.dirty || moved) { renderer.render(scene, cam); three.dirty = false; }
  };
  requestAnimationFrame(loop);
  $("#frameRange").addEventListener("input", (e) => setFrame(+e.target.value));
  $("#playBtn").addEventListener("click", () => {
    three.playing = !three.playing; $("#playBtn").textContent = three.playing ? "Pause" : "Play";
    if (three.playing && three.frame >= three.geo.data.frames.length - 1) setFrame(0);
  });
  $("#ghostToggle").addEventListener("change", (e) => { if (three.geo) { three.geo.ghost.visible = e.target.checked; three.dirty = true; } });
  showGeo(names[0]);
  resize();
}
function showGeo(k) {
  if (!three.ok) return;
  for (const b of $$("#geoSeg button")) b.setAttribute("aria-pressed", b.dataset.geo === k ? "true" : "false");
  if (three.geo) { three.scene.remove(three.geo.mesh, three.geo.ghost, three.geo.grid); three.geo.mesh.geometry.dispose(); }
  const d = D.geo3d[k];
  const nv = d.n_vert;
  const geom = new THREE.BufferGeometry();
  const pos = new Float32Array(nv * 3), colr = new Float32Array(nv * 3);
  geom.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geom.setAttribute("color", new THREE.BufferAttribute(colr, 3));
  geom.setIndex(d.tris);
  const mat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.55, metalness: 0.15, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(geom, mat);
  // green ghost: frame 0 as faint edges
  const g0 = new THREE.BufferGeometry();
  g0.setAttribute("position", new THREE.BufferAttribute(Float32Array.from(d.frames[0].p, (x) => x / 1000), 3));
  g0.setIndex(d.tris);
  const ghost = new THREE.LineSegments(new THREE.EdgesGeometry(g0, 30), new THREE.LineBasicMaterial({ color: 0x8a949b, transparent: true, opacity: 0.35 }));
  ghost.visible = $("#ghostToggle").checked;
  const p0 = d.frames[0].p;
  let zmin = Infinity, span = 0;
  for (let i = 0; i < nv; i++) { zmin = Math.min(zmin, p0[3 * i + 2] / 1000); }
  for (let i = 0; i < p0.length; i++) span = Math.max(span, Math.abs(p0[i] / 1000));
  const grid = new THREE.GridHelper(span * 3, 12, 0x9aa3a9, 0xc9d0d4);
  grid.rotation.x = Math.PI / 2; grid.position.z = zmin - 0.02;
  grid.material.transparent = true; grid.material.opacity = 0.5;
  three.scene.add(mesh, ghost, grid);
  three.geo = { key: k, data: d, mesh, ghost, grid, pos, colr };
  const r = span * 3.6;
  three.cam.up.set(0, 0, 1);
  three.cam.position.set(r * 0.9, -r * 1.1, r * 0.75);
  three.cam.lookAt(0, 0, 0);
  if (three.controls) { three.controls.target.set(0, 0, 0); three.controls.update(); }
  $("#frameRange").max = d.frames.length - 1;
  setFrame(d.frames.length - 1);
  renderFacts(k);
}
function setFrame(i) {
  const g = three.geo; if (!g) return;
  three.frame = i;
  const f = g.data.frames[i];
  const p = f.p, rho = f.rho;
  for (let j = 0; j < p.length; j++) g.pos[j] = p[j] / 1000;
  for (let v = 0; v < rho.length; v++) { const c = densColor(rho[v] / 1000); g.colr[3 * v] = c[0]; g.colr[3 * v + 1] = c[1]; g.colr[3 * v + 2] = c[2]; }
  g.mesh.geometry.attributes.position.needsUpdate = true;
  g.mesh.geometry.attributes.color.needsUpdate = true;
  g.mesh.geometry.computeVertexNormals();
  g.mesh.geometry.computeBoundingSphere();
  $("#frameRange").value = i;
  $("#frameInfo").textContent = `${f.t_h.toFixed(2)} h · ${f.T_C.toFixed(0)} °C · ${(100 * f.rho_mean).toFixed(1)} % dense`;
  $("#hud").textContent = `${GEO[g.key].name} · frame ${i + 1}/${g.data.frames.length}`;
  three.dirty = true;
}
function renderFacts(k) {
  const d = D.geo3d[k], s = d.summary;
  const box = $("#facts");
  box.innerHTML = "";
  const fact = (label, v, u) => el("div", { class: "fact" }, el("div", { class: "k" }, label), el("div", { class: "v", html: `${v}<small> ${u}</small>` }));
  box.append(el("p", { class: "note" }, GEO[k].why));
  const sh = s.shrink_bbox_pct;
  box.append(fact("Bounding-box shrinkage x / y / z", sh.map((x) => x.toFixed(1)).join(" / "), "%"));
  box.append(fact("1-D coupon prediction x-y / z", `${s.shrink_1d_xy.toFixed(1)} / ${s.shrink_1d_z.toFixed(1)}`, "%"));
  box.append(fact("Mean density, min–max", `${(100 * s.rho_mean).toFixed(1)}`, `% (${(100 * s.rho_min).toFixed(1)}–${(100 * s.rho_max).toFixed(1)})`));
  if (s.tip_sag_mm != null) box.append(fact("Arm tip sag from gravity", s.tip_sag_mm.toFixed(2), "mm"));
  if (s.OD_bottom_mm != null) box.append(fact("Outer diameter bottom / top", `${s.OD_bottom_mm.toFixed(2)} / ${s.OD_top_mm.toFixed(2)}`, "mm"));
  if (s.height_mm != null) box.append(fact("Sintered height", s.height_mm.toFixed(2), "mm"));
  box.append(el("p", { class: "note" }, `Precomputed with the Python FEM (${d.info.h} mm voxels) on the default optimised cycle (${s.duration_h.toFixed(1)} h) and default inputs. It does not follow the sliders; rerun scripts/run_3d.py for a new case.`));
}

// ============================================================ unknowns (tornado)
const METRIC_FMT = {
  rho_final: (v) => (100 * v).toFixed(1) + " %", shrink_xy_pct: (v) => v.toFixed(1) + " %", C_at_close_ppm: (v) => fmt(v, 2) + " ppm",
  Pi_gas_max: (v) => fmt(v, 2), Pi_bloat_max: (v) => fmt(v, 2), n_fail: (v) => String(v),
};
const METRIC_AXIS = {
  rho_final: (v) => (100 * v).toFixed(0) + "%", shrink_xy_pct: (v) => v.toFixed(0) + "%", C_at_close_ppm: (v) => fmt(v, 2),
  Pi_gas_max: (v) => fmt(v, 2), Pi_bloat_max: (v) => fmt(v, 2), n_fail: (v) => String(Math.round(v)),
};
const MATERIAL_GROUPS = ["powder", "feedstock", "chemistry", "sinter"];
const METRIC_SHORT = { rho_final: "Density", shrink_xy_pct: "Shrinkage", C_at_close_ppm: "Carbon", Pi_gas_max: "Debind gas", Pi_bloat_max: "Trapped gas", n_fail: "Checks failed" };
function initSens() {
  const seg = $("#metricSeg");
  for (const m of Object.keys(METRIC_SHORT)) seg.append(el("button", { "data-m": m, "aria-pressed": m === state.sensMetric ? "true" : "false", onclick: () => { state.sensMetric = m; renderSens(); } }, METRIC_SHORT[m]));
  $("#sensLegend").append(el("span", null, el("i", { class: "swatch", style: "background:var(--s1)" }), "Input at slider minimum"),
    el("span", null, el("i", { class: "swatch", style: "background:var(--s2)" }), "Input at slider maximum"));
  $("#sensBtn").addEventListener("click", recomputeSens);
  $("#sensAll").addEventListener("change", (e) => { state.sensAll = e.target.checked; renderSens(); });
}
function renderSens() {
  for (const b of $$("#metricSeg button")) b.setAttribute("aria-pressed", b.dataset.m === state.sensMetric ? "true" : "false");
  const sd = state.sens, box = $("#tornado");
  box.innerHTML = "";
  if (!sd) { $("#sensNote").textContent = "No sensitivity data."; return; }
  const m = state.sensMetric, f = METRIC_FMT[m];
  const base = sd.base[m];
  const rows = sd.rows.filter((r) => state.sensAll || MATERIAL_GROUPS.includes(r.group)).map((r) => {
    const a = r.out_lo && r.out_lo.ok !== false ? r.out_lo[m] : NaN, b = r.out_hi && r.out_hi.ok !== false ? r.out_hi[m] : NaN;
    const sw = Math.max(Math.abs((a ?? base) - base) || 0, Math.abs((b ?? base) - base) || 0);
    return { ...r, a, b, sw };
  }).sort((x, y) => y.sw - x.sw);
  const show = rows.slice(0, 14);
  let lo = base, hi = base;
  for (const r of show) for (const v of [r.a, r.b]) if (Number.isFinite(v)) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
  if (hi - lo < 1e-12) { hi = base + 1; lo = base - 1; }
  const pad = (hi - lo) * 0.04; lo -= pad; hi += pad;
  const X = (v) => (100 * (v - lo)) / (hi - lo);
  box.append(el("div", { class: "hd" }, "Input (range)"),
    (() => { const ax = el("div", { class: "hd axisrow" }); for (const v of ticksLin(lo, hi, 4)) if (X(v) > 3 && X(v) < 97) ax.append(el("span", { style: `left:${X(v)}%` }, METRIC_AXIS[m](v))); return ax; })(),
    el("div", { class: "hd v", style: "text-align:right" }, "min → max"));
  for (const r of show) {
    const rb = el("div", { class: "rb" });
    rb.append(el("b", { style: `left:${X(base)}%` }));
    for (const [side, v] of [["lo", r.a], ["hi", r.b]]) {
      if (!Number.isFinite(v) || Math.abs(v - base) < 1e-12) continue;
      const x0 = Math.min(X(v), X(base)), x1 = Math.max(X(v), X(base));
      rb.append(el("i", { class: side + (v > base ? (side === "lo" ? " r" : "") : (side === "hi" ? " l" : "")), style: `left:${x0}%;width:${Math.max(x1 - x0, 0.4)}%` }));
    }
    const failed = [r.out_lo, r.out_hi].some((o) => o && o.ok === false);
    const title = `${r.label}: ${fmt(r.lo)} → ${fmt(r.hi)} ${unit(r.unit)} gives ${Number.isFinite(r.a) ? f(r.a) : "–"} → ${Number.isFinite(r.b) ? f(r.b) : "–"} (now ${f(base)})` + (failed ? " · one run stopped early" : "");
    box.append(el("div", { class: "row", title },
      el("div", { class: "rl" }, el("span", null, r.label), el("span", { class: "tag tag-" + r.tag }, r.tag)),
      rb,
      el("div", { class: "rv" }, `${Number.isFinite(r.a) ? f(r.a) : "–"} → ${Number.isFinite(r.b) ? f(r.b) : "–"}`)));
  }
  $("#sensNote").textContent = `Current value ${f(base)} (vertical line). Top ${show.length} of ${rows.length} ${state.sensAll ? "inputs" : "material unknowns"} by swing. ` +
    (sd.at ? "Recomputed " + new Date(sd.at).toLocaleString() + "." : "Computed for the default inputs and the default optimised cycle.");
  renderMeasure(rows);
}
function measureText(doc) {
  const m = doc.match(/(Measure|Calibrate)[^.]*(\.[^A-Z][^.]*)*\.?/);
  return m ? m[0] : "";
}
function renderMeasure() {
  const sd = state.sens; if (!sd) return;
  // rank by the sum of swings normalised across the physical outcomes
  const ms = ["rho_final", "C_at_close_ppm", "Pi_gas_max", "Pi_bloat_max", "shrink_xy_pct"];
  const score = new Map();
  for (const m of ms) {
    const base = sd.base[m];
    const sws = sd.rows.map((r) => Math.max(...[r.out_lo, r.out_hi].map((o) => (o && Number.isFinite(o[m]) ? Math.abs(o[m] - base) : 0))));
    const mx = Math.max(...sws, 1e-12);
    sd.rows.forEach((r, i) => score.set(r.key, (score.get(r.key) || 0) + sws[i] / mx));
  }
  const list = sd.rows.filter((r) => BYKEY[r.key] && MATERIAL_GROUPS.includes(BYKEY[r.key].group))
    .sort((a, b) => score.get(b.key) - score.get(a.key)).slice(0, 6);
  const ol = $("#measure");
  ol.innerHTML = "";
  list.forEach((r, i) => {
    const how = measureText(BYKEY[r.key].doc || "") || "No direct test listed; bracket it with the slider.";
    ol.append(el("li", null, el("span", { class: "rank" }, String(i + 1)), el("div", null, el("b", null, r.label), " ", el("span", { class: "tag tag-" + r.tag }, r.tag), el("p", null, how))));
  });
}
async function recomputeSens() {
  const btn = $("#sensBtn"), pr = $("#sensProg");
  btn.disabled = true; pr.hidden = false;
  const bar = $("i", pr);
  const params = REG.filter((p) => !p.advanced && p.group !== "limits" && p.kind !== "int").map((p) => ({ key: p.key, label: p.label, tag: p.tag, unit: p.unit, group: p.group, lo: p.lo, hi: p.hi }));
  try {
    const m = await sensJob.run({ cmd: "sensitivity", scenario: { ...state.values }, cycle: curCycle(), N: 8, params, metrics: Object.keys(METRIC_SHORT).filter((x) => x !== "n_fail") },
      (p) => { bar.style.width = (100 * p.frac).toFixed(0) + "%"; btn.textContent = "Sweeping " + p.stage; });
    state.sens = { ...m.sens, at: Date.now() };
    renderSens();
  } catch (e) {
    $("#sensNote").textContent = e instanceof Cancelled ? "Cancelled." : "Error: " + e.message;
  } finally { btn.disabled = false; btn.textContent = "Recompute for current inputs"; pr.hidden = true; }
}

// ============================================================ powders
function renderPowders() {
  const rows = (PRE.powder || []).slice().sort((a, b) => a.d50_um - b.d50_um);
  const tb = $("#powTable tbody");
  tb.innerHTML = "";
  for (const r of rows) {
    const s = r.synth;
    tb.append(el("tr", null,
      el("td", null, (PRESET_LABEL[r.preset] || [r.preset, ""])[1] || r.preset),
      el("td", { class: "num" }, r.d50_um + " µm"), el("td", { class: "num" }, r.span.toFixed(1)), el("td", { class: "num" }, r.native_oxide_nm + " nm"),
      el("td", null, s ? el("span", { class: "status", title: s.passes === false ? "Best effort: " + (s.fails || []).join("; ") : "Passes all 10 checks" },
        el("span", { class: "st-" + (s.passes === false ? "warn" : "good"), html: ICON[s.passes === false ? "warn" : "good"] }),
        el("span", { class: "num" }, s.duration_h.toFixed(1) + " h"), s.passes === false ? "best effort" : "") : "–"),
      el("td", { class: "num" }, s ? s.T_peak_C.toFixed(0) + " °C" : "–"),
      el("td", { class: "num" }, s ? (100 * s.rho_final).toFixed(1) + " %" : "–"),
      el("td", { class: "num" }, s ? s.shrink_xy_pct.toFixed(1) + " %" : "–"),
      el("td", null, el("button", { class: "btn small", onclick: () => {
        applyPresetQuiet(PR.powder_presets[r.preset]);
        if (s) { state.cycles.opt = clone(s.cycle); state.source = "opt"; syncSource(); }
        renderProgram(); saveState(); runNow();
        document.getElementById("results").scrollIntoView({ behavior: "smooth" });
      } }, "Load"))));
  }
  if (!rows.length) return;
  const d50 = rows.map((r) => r.d50_um);
  const hollow = rows.map((r) => !!(r.synth && r.synth.passes === false));
  pointChart("ch-pow-h", "Own optimised cycle", "hours; open markers pass everything except the density target", d50,
    [{ label: "Cycle time", color: col(1), y: rows.map((r) => (r.synth ? r.synth.duration_h : NaN)), hollow }], (v) => v.toFixed(1) + " h", { min: 0 });
  pointChart("ch-pow-rho", "Final density", "% of theoretical", d50,
    [{ label: "Own optimised cycle", color: col(1), y: rows.map((r) => (r.synth ? 100 * r.synth.rho_final : NaN)), hollow },
     { label: "Default optimised cycle", color: col(2), y: rows.map((r) => 100 * r.fixed.rho_final) }],
    (v) => v.toFixed(1) + " %", { ref: 100 * DEF.rho_target, refLabel: "target" });
}
function applyPresetQuiet(pv) { Object.assign(state.values, pv); syncRail(); }
function pointChart(id, title, cap, xs, series, f, opt) {
  const fig = document.getElementById(id);
  fig.innerHTML = "";
  fig.append(el("div", { class: "chart-head" }, el("h3", null, title), el("span", { class: "cap" }, cap)));
  const lg = el("div", { class: "legend" });
  for (const s of series) lg.append(el("span", null, lineSwatch(s.color), s.label));
  fig.append(lg);
  const plot = el("div", { class: "plot" });
  fig.append(plot);
  const tip = el("div", { class: "tip", hidden: true });
  plot.append(tip);
  const draw = () => {
    const W = plot.clientWidth || 500, H = 210, M = { l: 46, r: 16, t: 10, b: 30 };
    const pw = W - M.l - M.r, ph = H - M.t - M.b;
    let lo = Infinity, hi = -Infinity;
    for (const s of series) for (const v of s.y) if (Number.isFinite(v)) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
    if (opt.ref != null) { lo = Math.min(lo, opt.ref); hi = Math.max(hi, opt.ref); }
    if (opt.min != null) lo = opt.min;
    const st = niceStep(hi - lo || 1, 4); lo = Math.floor(lo / st) * st; hi = Math.ceil(hi / st) * st;
    const x0 = 0, x1 = Math.ceil(Math.max(...xs) / 10) * 10;
    const X = (v) => M.l + ((v - x0) / (x1 - x0)) * pw, Y = (v) => M.t + ph * (1 - (v - lo) / (hi - lo));
    const svg = sv("svg", { viewBox: `0 0 ${W} ${H}`, height: H, role: "img", "aria-label": title });
    for (const v of ticksLin(lo, hi, 4)) { svg.append(sv("line", { class: "gl", x1: M.l, x2: M.l + pw, y1: Y(v), y2: Y(v) })); const t = sv("text", { x: M.l - 6, y: Y(v) + 3.5, "text-anchor": "end" }); t.textContent = fmt(v, 3); svg.append(t); }
    svg.append(sv("line", { class: "ax", x1: M.l, x2: M.l + pw, y1: M.t + ph, y2: M.t + ph }));
    for (const v of ticksLin(x0, x1, 6)) { const t = sv("text", { x: X(v), y: M.t + ph + 15, "text-anchor": "middle" }); t.textContent = v; svg.append(t); }
    const xl = sv("text", { x: M.l + pw, y: M.t + ph + 27, "text-anchor": "end" }); xl.textContent = "powder D50 (µm)"; svg.append(xl);
    if (opt.ref != null) { svg.append(sv("line", { class: "ref", x1: M.l, x2: M.l + pw, y1: Y(opt.ref), y2: Y(opt.ref) })); const t = sv("text", { class: "reft", x: M.l + 4, y: Y(opt.ref) - 4 }); t.textContent = opt.refLabel; svg.append(t); }
    for (const s of series) {
      let d = "", first = true;
      xs.forEach((x, i) => { if (!Number.isFinite(s.y[i])) { first = true; return; } d += (first ? "M" : "L") + X(x).toFixed(1) + " " + Y(s.y[i]).toFixed(1); first = false; });
      svg.append(sv("path", { class: "ln", d, style: `stroke:${s.color}` }));
      xs.forEach((x, i) => {
        if (!Number.isFinite(s.y[i])) return;
        const open = s.hollow && s.hollow[i];
        const c = sv("circle", { cx: X(x), cy: Y(s.y[i]), r: open ? 4 : 4.5, style: open ? `fill:var(--surface);stroke:${s.color};stroke-width:2` : `fill:${s.color};stroke:var(--surface);stroke-width:2` });
        const hit = sv("circle", { cx: X(x), cy: Y(s.y[i]), r: 12, fill: "transparent" });
        hit.addEventListener("pointerenter", () => {
          tip.innerHTML = `<div class="th">D50 ${x} µm${open ? " · best effort" : ""}</div><div class="tr"><i style="background:${s.color}"></i><span>${esc(s.label)}</span><b>${f(s.y[i])}</b></div>`;
          tip.hidden = false; const sc = plot.clientWidth / W; let left = X(x) * sc + 10; if (left + tip.offsetWidth > plot.clientWidth) left = X(x) * sc - tip.offsetWidth - 10;
          tip.style.left = left + "px"; tip.style.top = Math.max(0, Y(s.y[i]) * sc - 20) + "px";
        });
        hit.addEventListener("pointerleave", () => { tip.hidden = true; });
        svg.append(c, hit);
      });
    }
    const old = $("svg", plot); if (old) old.remove();
    plot.insertBefore(svg, tip);
  };
  draw();
  let w = plot.clientWidth;
  new ResizeObserver(() => { if (plot.clientWidth !== w) { w = plot.clientWidth; draw(); } }).observe(plot);
  const tbl = el("div", { class: "tblwrap", hidden: true });
  const btn = el("button", { class: "btn ghost small", "aria-expanded": "false" }, "Table");
  $(".chart-head", fig).append(btn);
  fig.append(tbl);
  tbl.innerHTML = `<table class="data"><thead><tr><th>D50 (µm)</th>${series.map((s) => `<th>${esc(s.label)}</th>`).join("")}</tr></thead><tbody>` +
    xs.map((x, i) => `<tr><td>${x}</td>${series.map((s) => `<td>${Number.isFinite(s.y[i]) ? f(s.y[i]) : "–"}</td>`).join("")}</tr>`).join("") + "</tbody></table>";
  btn.addEventListener("click", () => { const o = tbl.hidden; tbl.hidden = !o; btn.setAttribute("aria-expanded", o ? "true" : "false"); });
}

// ============================================================ boot
function boot() {
  loadState();
  buildRail();
  syncRail();
  makeCharts();
  syncSource();
  $("#fidelity").value = String(state.N);
  $("#liveToggle").checked = state.live;
  $("#fidelity").addEventListener("change", (e) => { state.N = +e.target.value; saveState(); runNow(); });
  $("#liveToggle").addEventListener("change", (e) => { state.live = e.target.checked; saveState(); });
  $("#runBtn").addEventListener("click", runNow);
  for (const b of $$("#srcSeg button")) b.addEventListener("click", () => setSource(b.dataset.src));
  $("#addSeg").addEventListener("click", addSeg);
  $("#copyTsv").addEventListener("click", () => copyText(cycleTsv()));
  $("#copyJson").addEventListener("click", () => copyText(JSON.stringify(curCycle(), null, 1)));
  $("#optBtn").addEventListener("click", optimise);
  $("#optCancel").addEventListener("click", () => optJob.cancel());
  renderProgram();
  renderMeta();
  renderCands();
  initSens(); renderSens();
  renderPowders();
  $("#foot").textContent = `Engine parity with the Python reference verified · data built ${D.built || ""} · ${REG.length} inputs (${REG.filter((p) => p.tag === "GUESS").length} guesses)`;
  // at-rest result: the bundled run when nothing differs from it, otherwise solve now
  const pre = PRE.default_result;
  if (pre && isDefault() && state.source === "opt" && state.N === (PRE.default_N || 8) && sameCycle(state.cycles.opt, PRE.default_cycle)) {
    const r = { t_h: Float64Array.from(pre.t_h), series: {}, kpi: pre.kpi, ok: pre.ok, cycle: state.cycles.opt };
    for (const [k, a] of Object.entries(pre.series)) r.series[k] = Float64Array.from(a, (x) => (x == null ? NaN : x));
    r.kpi.t_close_h = r.kpi.t_close_h == null ? NaN : r.kpi.t_close_h;
    showResult(r);
    setRun("ok", "bundled result · default inputs");
  } else runNow();
  init3D();
}
boot();
})();
