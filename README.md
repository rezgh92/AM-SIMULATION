# AM-SIMULATION

Simulation of thermal debinding and sintering for the Lithoz R&D copper photopolymer slurry
printed on a CeraFab Multi 2M30 — and derivation of an optimum thermal cycle.

**Status: working model, cycle optimiser and dashboard. Awaiting the first furnace runs to calibrate.**

## Use it

- **Dashboard:** open `dashboard/dist/cupola-studio.html` in a browser (one self-contained file).
  Move any uncertain input, pick or edit a cycle, run the optimiser, read the ten-check verdict,
  and scrub the 3-D shrinkage of three test parts.
- **Python package** (`pip install -e .`, package `cupola`):

  | Module | What it does |
  |---|---|
  | `thermo` | Cu-O-C-H thermochemistry: Ellingham lines, dew points, carbothermic onset, Cu-O solidus |
  | `params` | all 64 inputs with range, unit and provenance tag (DERIVED / ANALOGUE / GUESS); powder and furnace presets |
  | `model1d`, `simulate` | 1-D coupon through the critical wall: heat, binder pyrolysis and burn, pore gas, oxidation and reduction, char gasification, viscous sintering, trapped gas; KPIs and the ten-check verdict |
  | `synth` | cycle optimiser: fastest cycle that keeps every risk index under 80 % of its limit |
  | `fem3d` | 3-D voxel FEM of sintering with gravity and setter friction |
  | `calibrate` | fits the sintering viscosity factor to interrupted-run coupons, no dilatometer needed |

- **Scripts:** `run_3d.py` (3-D run of a geometry through a cycle), `calibrate_sintering.py`
  (fit f_eta from caliper or Archimedes data; `--demo` shows the workflow),
  `build_dashboard.py` (rebuild the dashboard after `node dashboard/build/precompute.mjs`),
  `export_params.py`, `export_parity.py`, `fit_cu_oxidation.py`, `fit_sintering_cea.py`.
- **Tests:** `python -m pytest` (Python) and `node dashboard/engine/parity.test.mjs` (browser engine
  against the Python reference).

## What the model says with today's best assumptions

For a 5 mm wall of 12 µm copper at 55 vol% in a lab retort with N₂, 4 % forming gas and a
room-temperature bubbler, the optimiser finds a **12.8 h** cycle that passes all ten checks
(95.3 % density, 15.4 % x-y and 19.4 % z shrinkage), against 146 h for the conservative v0
envelope: pyrolyse in dry N₂ at the 1 K/min guard ramp, gasify char in wet forming gas at 1000 °C,
densify dry just under the Cu-O solidus. The char gasification rate, the powder D50 and the
sintering viscosity factor are the unknowns that move the outcome most; each has a stated
measurement in the dashboard.

## Background

- **[`docs/PROPOSAL.md`](docs/PROPOSAL.md)** — the architecture proposal, the baseline cycle
  that can go in a furnace next week, the experimental campaign, risks, and the decisions
  needed before anything is built.
- [`docs/research/`](docs/research/) — the evidence base: 27 verbatim research and design-review
  reports from a multi-agent literature and data sweep. Preserved as produced, errors included;
  where they disagree with the proposal, the proposal is the corrected version.

## The problem in one paragraph

The slurry comes from Lithoz's internal R&D programme, so there is no datasheet, no published
thermal cycle, and the binder chemistry and content are proprietary and unknown. Copper is the
hard case: it oxidises readily, forms no carbide so residual carbon can only be gasified, is prone
to hydrogen embrittlement if oxide and H₂ coexist, and sinters just below its 1084.6 °C melting
point — with a Cu–Cu₂O eutectic 18.6 K below that.

## The three findings that shape the approach

1. **You mostly do not need to know the binder.** Oxidative debinding of a metal-filled
   photopolymer is heat-removal and oxygen-flux limited, not kinetics limited, so the binder's
   pre-exponential factor has no leverage on the part-scale cycle. Minimum debinding time follows
   a parameter-free law that reproduces two published industrial cycles with zero fitted parameters.
2. **The real problem is ordering, not temperature.** Carbon and oxygen must be below spec
   *before* porosity closes at ~92 % relative density, after which both are sealed in permanently.
3. **`Cu₂O + C → 2Cu + CO` is spontaneous above 76 °C** and was missing from every independent
   design. It is both the real carbon sink and the real blistering source.
