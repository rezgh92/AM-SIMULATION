"""Assemble the single-file dashboard from its sources.

    python scripts/build_dashboard.py [out.html]

Inlines dashboard/src/{style.css,app.js}, the JavaScript engine, the parameter registry, the
precomputed at-rest data (dashboard/build/precompute.mjs) and any 3-D results
(dashboard/data/3d_*.json, from scripts/run_3d.py) into dashboard/dist/cupola-studio.html.
"""
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH = ROOT / "dashboard"


def js_json(obj) -> str:
    # safe inside a <script> element
    return json.dumps(obj, separators=(",", ":"), allow_nan=False).replace("</", "<\\/")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DASH / "dist" / "cupola-studio.html"
    html = (DASH / "src" / "index.html").read_text()
    css = (DASH / "src" / "style.css").read_text()
    app = (DASH / "src" / "app.js").read_text()
    engine = (DASH / "engine" / "cupola.js").read_text()
    params = json.loads((DASH / "engine" / "params.json").read_text())
    pre_path = DASH / "data" / "precomputed.json"
    pre = json.loads(pre_path.read_text()) if pre_path.exists() else {}
    geo = {}
    for f in sorted((DASH / "data").glob("3d_*.json")):
        geo[f.stem[3:]] = json.loads(f.read_text())
    data = dict(params=params, pre=pre, geo3d=geo, built=dt.date.today().isoformat())
    for marker, text in (("/*@CSS@*/", css), ("/*@ENGINE@*/", engine),
                         ("/*@DATA@*/", "window.CUPOLA_DATA = " + js_json(data) + ";"), ("/*@APP@*/", app)):
        assert marker in html, marker
        assert "</script" not in text or marker == "/*@CSS@*/", f"{marker} source contains </script"
        html = html.replace(marker, text)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"wrote {out} ({out.stat().st_size / 1e6:.2f} MB; 3-D: {', '.join(geo) or 'none'})")


if __name__ == "__main__":
    main()
