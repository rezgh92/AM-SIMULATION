"""Controllable-variable registry.

Every input the model uses is declared here once, with its display unit, a
physically defensible range, a provenance tag and a one-line justification. The
dashboard, the synthesizer and the tests all read from this table, so changing a
default in one place changes it everywhere.

Provenance tags
---------------
MEASURED  taken directly from a measurement or handbook value for pure copper
ANALOGUE  measured on a closely related system (other Cu VPP feedstock, LCM ceramic)
DERIVED   computed from other quantities or fitted to published data (fit documented)
GUESS     engineering estimate; the model is known to be sensitive to it and it
          should be replaced by a measurement - the doc string names which one
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, Iterable


@dataclass(frozen=True)
class Param:
    key: str
    value: float
    unit: str
    lo: float
    hi: float
    group: str
    tag: str
    label: str
    doc: str
    log: bool = False
    advanced: bool = False
    kind: str = "float"   # float | bool | int

    def check(self, v: float) -> float:
        if self.kind == "bool":
            return 1.0 if v else 0.0
        if not (self.lo - 1e-12 <= v <= self.hi + 1e-12):
            raise ValueError(f"{self.key}={v} outside [{self.lo}, {self.hi}] {self.unit}")
        return float(v)


GROUPS = {
    "powder": "Copper powder",
    "feedstock": "Slurry & binder",
    "part": "Part & load",
    "furnace": "Furnace capability",
    "chemistry": "Gas-solid chemistry",
    "sinter": "Sintering (copper)",
    "limits": "Quality targets & limits",
}

_P = [
    # ------------------------------------------------------------------ powder
    Param("d50_um", 12.0, "um", 2.0, 45.0, "powder", "GUESS", "Powder D50",
          "Unknown for the Lithoz slurry. Published Cu VPP: 16 um (IFAM/Incus), 22 um (CEA-LITEN). "
          "35 um pixels and 25 um layers need d90 < ~25 um. Drives permeability (d^2), native oxide (1/d), "
          "oxidation/reduction rates, sintering stress (1/d) and initial grain size. Measure: laser diffraction "
          "on powder recovered by solvent washing."),
    Param("span", 1.0, "-", 0.4, 2.5, "powder", "ANALOGUE", "PSD span (d90-d10)/d50",
          "IFAM powder A: (25-9)/16 = 1.0. Sets the Sauter mean d32 used for surface-area terms."),
    Param("native_oxide_nm", 4.0, "nm", 1.0, 20.0, "powder", "ANALOGUE", "Native oxide thickness",
          "Gas-atomised Cu carries a 2-10 nm Cu2O film. Converts to initial oxygen via surface area. "
          "Measure: LECO O on recovered powder."),
    Param("grain_ratio", 0.4, "-", 0.1, 1.0, "powder", "GUESS", "Initial grain size / D50",
          "Gas-atomised particles are polycrystalline; grains ~1/3-1/2 of particle size. Measure: EBSD on powder.",
          advanced=True),

    # ------------------------------------------------------------------ feedstock
    Param("phi", 0.55, "-", 0.40, 0.62, "feedstock", "ANALOGUE", "Cu solids loading (vol)",
          "Lithoz ceramics 39-49 vol%; Cu VPP 52-60 vol%. Measure: slurry pycnometry, phi = (rho - 1.13)/7.83."),
    Param("rho_binder", 1130.0, "kg/m3", 1000.0, 1300.0, "feedstock", "DERIVED", "Binder density",
          "Back-calculated two independent ways from Lithoz LithaLox HP500 and LithaNit 720 data.", advanced=True),
    Param("solvent_frac", 0.15, "-", 0.0, 0.40, "feedstock", "GUESS", "Non-reactive solvent (of binder)",
          "Lithoz LCM organics contain a non-reactive solvent; its early evaporation opens the pore network that "
          "later pyrolysis gas escapes through. Measure: TGA mass loss below 250 C in N2."),
    Param("pre_extracted_frac", 0.0, "-", 0.0, 0.8, "feedstock", "GUESS", "Binder removed by solvent debind",
          "Fraction of binder extracted before the thermal cycle (IFAM/Incus: 24 h acetone). 0 for the Lithoz "
          "route, which has no solvent debind.", advanced=True),
    Param("Tp_solvent_C", 170.0, "C", 80.0, 300.0, "feedstock", "GUESS", "Solvent TGA peak (10 K/min)",
          "Resch reports a 70-140 C event; peak at 10 K/min placed at 170 C.", advanced=True),
    Param("Tp_network_C", 400.0, "C", 320.0, 470.0, "feedstock", "ANALOGUE", "Network pyrolysis peak (10 K/min, N2)",
          "Acrylate networks (HDDA/TMPTA/urethane acrylates) scission at 380-430 C in N2 at 10 K/min. "
          "Measure: multi-rate TGA on cured green coupons."),
    Param("Tp_backbone_C", 470.0, "C", 380.0, 560.0, "feedstock", "ANALOGUE", "Char-forming residue peak (10 K/min)",
          "Acrylate-bound Cu feedstocks lose weight to ~600 C in argon, leaving char.", advanced=True),
    Param("E_solvent", 60.0, "kJ/mol", 30.0, 120.0, "feedstock", "GUESS", "Solvent evaporation E", "", advanced=True),
    Param("E_network", 190.0, "kJ/mol", 120.0, 280.0, "feedstock", "ANALOGUE", "Network pyrolysis E",
          "Isoconversional E for acrylate networks 150-240 kJ/mol.", advanced=True),
    Param("E_backbone", 160.0, "kJ/mol", 100.0, 280.0, "feedstock", "GUESS", "Backbone pyrolysis E",
          "Low E makes this component broad, reproducing the slow tail to ~600 C.", advanced=True),
    Param("w_backbone", 0.40, "-", 0.1, 0.8, "feedstock", "GUESS", "Backbone share of network",
          "Fraction of non-solvent binder in the slow char-forming component.", advanced=True),
    Param("char_yield", 0.05, "-", 0.0, 0.15, "feedstock", "ANALOGUE", "Char yield in inert gas",
          "Roumanie (CEA): 0.394 wt% C after 400 C/4 h in Ar on a 60 vol% Cu part = ~5 % of the binder. "
          "Aromatic light-absorbing dyes (present in LCM slurries, absent from the CEA study) would raise it."),
    Param("dHc_MJkg", 25.0, "MJ/kg", 18.0, 32.0, "feedstock", "ANALOGUE", "Binder heat of combustion",
          "Acrylates 24-28 MJ/kg. Heat released in the part follows Thornton's rule (13.1 MJ per kg O2). "
          "Measure: bomb calorimetry."),
    Param("dHpyr_MJkg", 0.8, "MJ/kg", 0.0, 2.0, "feedstock", "GUESS", "Pyrolysis endotherm",
          "Depolymerisation/volatilisation is mildly endothermic.", advanced=True),
    Param("M_vol", 0.10, "kg/mol", 0.03, 0.30, "feedstock", "GUESS", "Mean molar mass of volatiles",
          "Sets moles of gas per kg of binder, hence internal pressure.", advanced=True),
    Param("ox_shift_K", 70.0, "K", 0.0, 150.0, "feedstock", "GUESS", "Oxidative degradation shift",
          "Polymers degrade oxidatively 50-100 K below their inert pyrolysis temperature in air.", advanced=True),
    Param("E_oxdeg", 110.0, "kJ/mol", 70.0, 200.0, "feedstock", "ANALOGUE", "Oxidative degradation E",
          "Thermo-oxidative degradation of acrylates has E ~80-140 kJ/mol, well below inert pyrolysis. Controls how "
          "fast a low-temperature air hold (IFAM: 63 h at 250 C) removes binder.", advanced=True),
    Param("perm_polymer_barrer", 100.0, "Barrer", 1.0, 1e4, "feedstock", "GUESS", "Gas permeability of cured binder",
          "Governs gas escape before the pore network percolates, which is where debinding cracks nucleate. "
          "Calibrate from the critical thickness in a thickness-ladder debind.", log=True),
    Param("eps_perc", 0.04, "-", 0.01, 0.12, "feedstock", "GUESS", "Pore percolation threshold",
          "Porosity at which binder removal opens a connected escape path.", advanced=True),
    Param("sigma_green_MPa", 17.0, "MPa", 5.0, 30.0, "feedstock", "ANALOGUE", "Green strength (RT)",
          "IFAM LMM Cu: 20 (X;Z), 17 (Y;Z), 13 (Z;Y) MPa."),
    Param("interlayer_factor", 0.65, "-", 0.3, 1.0, "feedstock", "ANALOGUE", "Interlayer strength factor",
          "13/20 from IFAM build-orientation data; applies to the build-direction (delamination) mode."),
    Param("Tg_C", 100.0, "C", 40.0, 180.0, "feedstock", "GUESS", "Binder glass transition", "", advanced=True),
    Param("rubbery_ratio", 0.15, "-", 0.02, 0.5, "feedstock", "GUESS", "Rubbery/glassy strength ratio",
          "Strength retained above Tg.", advanced=True),
    Param("k_green", 1.5, "W/m/K", 0.5, 20.0, "feedstock", "GUESS", "Green thermal conductivity",
          "Polymer-continuous Maxwell-Eucken gives ~0.9; a percolating Cu skeleton could give 5-20. Decides "
          "whether oxidative debinding is heat-removal limited. Measure: laser flash on a cured coupon.", log=True),
    Param("P_ppm", 30.0, "ppm", 0.0, 300.0, "feedstock", "GUESS", "Phosphorus retained",
          "At 450 nm only BAPO-class (P-bearing) or acylgermane initiators are practical. 30-180 ppm if "
          "retained. Costs conductivity, not melting: P solubility in solid Cu is ~1.7 wt% at 714 C. "
          "Measure: ICP-OES on digested green body."),
    Param("P_dissolved_frac", 0.5, "-", 0.0, 1.0, "feedstock", "GUESS", "P fraction in solid solution",
          "Phosphate residues can stay as oxide unless strongly reduced.", advanced=True),

    # ------------------------------------------------------------------ part
    Param("half_thickness_mm", 2.5, "mm", 0.25, 15.0, "part", "GUESS", "Critical half-thickness",
          "Half of the thickest section (a 5 mm wall has 2.5 mm)."),
    Param("anisotropy", 0.08, "-", 0.0, 0.3, "part", "GUESS", "Build-direction shrinkage anisotropy",
          "Extra shrinkage in z from layered green structure (LCM ceramics: z 1-3 %% larger)."),
    Param("load_cm3", 5.0, "cm3", 0.1, 500.0, "part", "GUESS", "Total green volume in retort",
          "Sets how much the load depletes or enriches the furnace gas.", log=True),
    Param("n_nodes", 12, "-", 6, 40, "part", "DERIVED", "Through-thickness nodes", "", advanced=True, kind="int"),

    # ------------------------------------------------------------------ furnace
    Param("h_conv", 15.0, "W/m2/K", 3.0, 150.0, "furnace", "ANALOGUE", "Convective h at the part",
          "Retort with modest flow 5-20; a baffle and forced flow reach 50-150. Radiation is added separately.",
          log=True),
    Param("max_ramp_Kmin", 10.0, "K/min", 1.0, 30.0, "furnace", "ANALOGUE", "Max furnace ramp rate", ""),
    Param("furnace_lag_min", 5.0, "min", 0.5, 30.0, "furnace", "GUESS", "Furnace thermal lag", "", advanced=True),
    Param("T_furnace_max_C", 1100.0, "C", 900.0, 1400.0, "furnace", "ANALOGUE", "Furnace max temperature", ""),
    Param("flow_slpm", 2.0, "slpm", 0.2, 20.0, "furnace", "ANALOGUE", "Gas flow", "", log=True),
    Param("retort_L", 5.0, "L", 0.5, 100.0, "furnace", "GUESS", "Retort free volume", "", log=True),
    Param("has_air_bleed", 1.0, "-", 0.0, 1.0, "furnace", "GUESS", "Air bleed into N2 available",
          "A needle valve or MFC adding air to the N2 stream.", kind="bool"),
    Param("h2_max", 0.04, "-", 0.0, 1.0, "furnace", "GUESS", "Max H2 fraction",
          "0.04 = non-flammable forming gas (no hydrogen safety case). 1.0 = pure-H2 furnace."),
    Param("dp_max_C", 20.0, "C", -40.0, 60.0, "furnace", "GUESS", "Max dew point",
          "-40 = no humidifier; +20 = room-temperature bubbler; +60 = heated humidifier with heated line."),
    Param("o2_impurity_ppm", 5.0, "ppm", 0.1, 100.0, "furnace", "ANALOGUE", "O2 in 'inert' gas",
          "5.0-grade N2/Ar ~ 1-5 ppm; leaks add more.", log=True, advanced=True),
    Param("T_uniformity_K", 5.0, "K", 1.0, 25.0, "furnace", "GUESS", "Load temperature uniformity (+/-)",
          "Added to the melting margin. Measure by thermocouple survey.", advanced=True),

    # ------------------------------------------------------------------ chemistry
    Param("t_half_gasif_h", 2.0, "h", 0.2, 20.0, "chemistry", "GUESS", "Char gasification half-life",
          "At 800 C, dew point +20 C, 4 % H2. No rate constant exists for char on Cu in the literature. "
          "Measure: interrupted-quench LECO C series.", log=True),
    Param("E_gasif", 200.0, "kJ/mol", 120.0, 280.0, "chemistry", "ANALOGUE", "Gasification E",
          "Carbon-steam gasification 170-250 kJ/mol.", advanced=True),
    Param("T_carbothermic_C", 600.0, "C", 400.0, 800.0, "chemistry", "GUESS", "Carbothermic reduction onset",
          "Temperature at which Cu2O + C -> 2Cu + CO reaches 1e-4 1/s. Thermodynamically allowed above 76 C; "
          "kinetics unknown. A CO spike in the exhaust under inert gas identifies it.", advanced=True),
    Param("Tp_reduction_C", 330.0, "C", 250.0, 450.0, "chemistry", "ANALOGUE", "Cu2O reduction peak (TPR, 10 K/min, 4 % H2)",
          "Consistent with native oxide reducing in minutes at 350 C (Ott).", advanced=True),
    Param("E_reduction", 114.6, "kJ/mol", 60.0, 180.0, "chemistry", "ANALOGUE", "Cu2O reduction E", "", advanced=True),
    Param("Tp_charox_C", 480.0, "C", 380.0, 600.0, "chemistry", "ANALOGUE", "Char oxidation peak (air, 10 K/min)",
          "Cu-catalysed char burns 400-550 C in air.", advanced=True),
    Param("E_cu_ox", 100.0, "kJ/mol", 60.0, 180.0, "chemistry", "ANALOGUE", "Cu oxidation E",
          "Fixed at a mid-literature value for Cu2O growth; prefactor and deceleration fitted to Ott (2022) "
          "powder data. See scripts/fit_cu_oxidation.py.", advanced=True),

    # ------------------------------------------------------------------ sintering
    Param("gamma_s", 1.5, "J/m2", 1.0, 2.0, "sinter", "ANALOGUE", "Cu surface energy", "", advanced=True),
    Param("f_eta", 0.28, "-", 0.05, 10.0, "sinter", "DERIVED", "Sintering viscosity factor",
          "Multiplies the Coble + Nabarro-Herring viscosity from Frost & Ashby Cu diffusion data. Default fitted "
          "to CEA-LITEN DLP copper (22 um, 60 vol%, 1050 C/4 h H2 -> 90-94 %%): 0.28 (0.22-0.34). THE calibration "
          "knob for your powder: refit from caliper shrinkage of coupons from 3-4 interrupted sinter runs "
          "(no dilatometer needed; scripts/calibrate_sintering.py).", log=True),
    Param("kG_mult", 1.0, "-", 0.1, 10.0, "sinter", "GUESS", "Grain growth rate factor", "", log=True, advanced=True),
    Param("rho_close", 0.92, "-", 0.88, 0.95, "sinter", "ANALOGUE", "Pore closure density",
          "Scheibler: pores closed at 92-95 %.", advanced=True),
    Param("C_inhibit_ppm", 200.0, "ppm", 50.0, 2000.0, "sinter", "ANALOGUE", "Carbon inhibition scale",
          "Viscosity x (1 + (C/C_inh)^2). ~1550 ppm C held a Cu compact at ~59 %% TD (US5302562A).",
          log=True, advanced=True),

    # ------------------------------------------------------------------ limits
    Param("dT_exo_max", 20.0, "K", 5.0, 60.0, "limits", "GUESS", "Max self-heating above furnace", ""),
    Param("debind_ramp_cap_Kmin", 1.0, "K/min", 0.05, 10.0, "limits", "GUESS", "Guard ramp while binder remains",
          "Caps heating while >1 % of the binder remains, as a guard against failure modes the model does not "
          "contain (viscous slumping of the softened green body, capillary migration of liquid decomposition "
          "products, differential shrinkage). Once solvent evaporation has opened the pores the modelled gas "
          "pressure is slack, so without this guard the optimiser would pyrolyse at the furnace maximum. Relax "
          "it after a thickness-ladder debind shows parts survive faster ramps.", log=True),
    Param("sf_gas", 1.5, "-", 1.0, 4.0, "limits", "GUESS", "Safety factor on gas pressure", ""),
    Param("C_spec_ppm", 200.0, "ppm", 20.0, 2000.0, "limits", "GUESS", "Max carbon at pore closure", "", log=True),
    Param("O_spec_ppm", 300.0, "ppm", 30.0, 3000.0, "limits", "GUESS", "Max oxide oxygen at pore closure", "", log=True),
    Param("rho_target", 0.95, "-", 0.85, 0.99, "limits", "GUESS", "Target relative density", ""),
    Param("T_margin_K", 15.0, "K", 5.0, 50.0, "limits", "GUESS", "Margin below solidus", ""),
]

REGISTRY: Dict[str, Param] = {p.key: p for p in _P}


def defaults() -> Dict[str, float]:
    return {k: p.value for k, p in REGISTRY.items()}


# ---------------------------------------------------------------------------- presets
POWDER_PRESETS = {
    "ultrafine_3um": dict(d50_um=3.0, span=1.2, native_oxide_nm=3.0),
    "fine_6um": dict(d50_um=6.0, span=1.1, native_oxide_nm=3.5),
    "standard_12um": dict(d50_um=12.0, span=1.0, native_oxide_nm=4.0),
    "ifam_16um": dict(d50_um=16.0, span=1.0, native_oxide_nm=4.0),
    "cea_22um": dict(d50_um=22.0, span=1.5, native_oxide_nm=6.0),
    "coarse_30um": dict(d50_um=30.0, span=1.3, native_oxide_nm=6.0),
}

FURNACE_PRESETS = {
    "basic_tube": dict(h_conv=8.0, has_air_bleed=0.0, h2_max=0.04, dp_max_C=-40.0, max_ramp_Kmin=10.0,
                       flow_slpm=1.0, retort_L=2.0),
    "standard_retort": dict(h_conv=15.0, has_air_bleed=1.0, h2_max=0.04, dp_max_C=20.0, max_ramp_Kmin=10.0,
                            flow_slpm=2.0, retort_L=5.0),
    "advanced_h2": dict(h_conv=60.0, has_air_bleed=1.0, h2_max=1.0, dp_max_C=60.0, max_ramp_Kmin=15.0,
                        flow_slpm=5.0, retort_L=10.0),
}

PRESET_DOCS = {
    "basic_tube": "Tube furnace, N2 and 4 % forming gas only, no humidifier, no air bleed.",
    "standard_retort": "DEFAULT. Lab retort with N2, air-bleed MFC, 4 % forming gas (non-flammable, no H2 "
                       "safety case) and a room-temperature water bubbler (dew point up to +20 C).",
    "advanced_h2": "Pure-H2-rated retort, heated humidifier (dew point to +60 C), baffle for forced convection.",
}


def scenario(**overrides) -> Dict[str, float]:
    """Default scenario with overrides; validates every value against its range."""
    s = defaults()
    for k, v in overrides.items():
        if k not in REGISTRY:
            raise KeyError(f"unknown parameter {k!r}")
        s[k] = REGISTRY[k].check(v)
    return s


def apply_preset(s: Dict[str, float], powder: str | None = None, furnace: str | None = None) -> Dict[str, float]:
    s = dict(s)
    if powder:
        s.update(POWDER_PRESETS[powder])
    if furnace:
        s.update(FURNACE_PRESETS[furnace])
    return s


def registry_as_dicts() -> Iterable[dict]:
    for p in _P:
        yield asdict(p)
