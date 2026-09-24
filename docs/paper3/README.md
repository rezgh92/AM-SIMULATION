# Paper 3: co-firing copper in a printed glass-ceramic

This folder holds the manuscript, figures, data and literature notes for the simulation study of co-firing copper with a cordierite-type glass-ceramic printed by multi-material vat photopolymerisation.

| Folder | Contents |
|---|---|
| `manuscript/` | LaTeX sources. `main.tex` is the two-column journal layout; `review.tex` is the double-spaced copy with line numbers for submission. `build.sh` builds both. `cover_letter.md` and `highlights.txt` are submission items. |
| `figures/` | Every figure as vector PDF and 300 dpi PNG. |
| `data/` | The JSON output behind every figure. |
| `lit/` | Literature dossiers. Every number used in the model is listed there with its source, the verification level and an exact quote. |

## Reproducing the results

Run all commands from the repository root with `PYTHONPATH=src:scripts/paper3`. The co-firing model lives in `src/cupola/cofire/` and the two-material 3-D model in `src/cupola/fem3d/cosinter.py`.

```bash
D=docs/paper3/data; F=docs/paper3/figures
python scripts/paper3/verify_glass.py      $D/verify_glass.json        # closed-form check (Fig. 2a)
python scripts/paper3/verify_bilayer.py    $D/verify_bilayer.json      # 3-D vs Timoshenko (Fig. 2b)
python scripts/paper3/ibm_check.py         $D/ibm_check.json           # IBM schedule (Table 2)
python scripts/paper3/atmosphere_window.py $D/atmosphere_window.json   # Fig. 3
python scripts/paper3/race_map.py          $D/race_map.json            # Fig. 4
python scripts/paper3/free_sintering.py    $D/free_sintering.json      # Fig. 5
python scripts/paper3/optimise.py          $D/opt_main.json 18 15 8 mismatch 4
python scripts/paper3/design_map.py        $D/design_map.json '{"t_B": 4.0}'
python scripts/paper3/package3d.py baseline      $D/package_baseline.json
python scripts/paper3/package3d.py $D/opt_main.json $D/package_optimised.json
python scripts/paper3/cooling.py           $D/cooling.json             # Fig. 9
python scripts/paper3/morris.py            $D/morris.json $D/opt_main.json 16
python scripts/paper3/fig_overview.py $F
python scripts/paper3/fig_results_a.py $D $F
python scripts/paper3/fig_results_b.py $D $F
python scripts/paper3/fig_cooling.py $D $F
python scripts/paper3/fig_graphical_abstract.py $D $F
sh docs/paper3/manuscript/build.sh
```

Timings on four cores: the optimiser takes about 1.5 h, each 3-D package run 1–2 h, and the Morris screening about 10 min. Everything else takes minutes.
