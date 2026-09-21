# AM-SIMULATION

Simulation of thermal debinding and sintering for the Lithoz R&D copper photopolymer slurry
printed on a CeraFab Multi 2M30 — and derivation of an optimum thermal cycle.

**Status: proposal stage. No implementation yet.**

## Start here

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
