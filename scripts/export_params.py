"""Export the controllable-variable registry and presets for the dashboard (single source of truth)."""
import json
from pathlib import Path
from cupola import params

out = dict(
    registry=list(params.registry_as_dicts()),
    groups=params.GROUPS,
    powder_presets=params.POWDER_PRESETS,
    furnace_presets=params.FURNACE_PRESETS,
    preset_docs=params.PRESET_DOCS,
)
p = Path(__file__).resolve().parents[1] / "dashboard" / "engine" / "params.json"
p.write_text(json.dumps(out, indent=1))
print(f"wrote {p} ({len(out['registry'])} parameters)")
