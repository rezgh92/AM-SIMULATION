"""Furnace programs: segments of (ramp, hold) with an atmosphere per segment.

A segment ramps the setpoint from the previous end temperature to ``T_end_C`` at
``ramp_Kmin`` and then holds for ``hold_h``. The atmosphere (O2, H2, dew point)
applies for the whole segment. This is exactly what a Eurotherm/Nabertherm
segment program can execute, so every cycle the model evaluates is runnable.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import List

import numpy as np

from .constants import T0C


@dataclass
class Segment:
    T_end_C: float
    ramp_Kmin: float
    hold_h: float = 0.0
    O2: float = 0.0          # O2 mole fraction in the inlet (0.21 = air)
    H2: float = 0.0          # H2 mole fraction in the inlet
    dp_C: float = -60.0      # inlet dew point, degC (-60 = dry)
    note: str = ""


@dataclass
class Cycle:
    segments: List[Segment]
    T_start_C: float = 25.0
    name: str = ""

    def boundaries(self):
        """List of (t_start, t_end, segment, T_from_C) in seconds, one entry per ramp and per hold."""
        out = []
        t = 0.0
        T = self.T_start_C
        for seg in self.segments:
            dT = seg.T_end_C - T
            if abs(dT) > 1e-9:
                rate = max(seg.ramp_Kmin, 1e-6) / 60.0
                dt = abs(dT) / rate
                out.append((t, t + dt, seg, T, "ramp"))
                t += dt
            if seg.hold_h > 0:
                out.append((t, t + seg.hold_h * 3600.0, seg, seg.T_end_C, "hold"))
                t += seg.hold_h * 3600.0
            T = seg.T_end_C
        return out

    def duration_h(self) -> float:
        b = self.boundaries()
        return b[-1][1] / 3600.0 if b else 0.0

    def T_set_K(self, t: float) -> float:
        for (t0, t1, seg, T_from, kind) in self.boundaries():
            if t <= t1:
                if kind == "hold":
                    return seg.T_end_C + T0C
                frac = (t - t0) / max(t1 - t0, 1e-12)
                return T_from + frac * (seg.T_end_C - T_from) + T0C
        return self.segments[-1].T_end_C + T0C

    def to_dict(self):
        return dict(name=self.name, T_start_C=self.T_start_C, segments=[asdict(s) for s in self.segments])

    @staticmethod
    def from_dict(d):
        return Cycle([Segment(**s) for s in d["segments"]], d.get("T_start_C", 25.0), d.get("name", ""))

    def table(self) -> str:
        rows = [f"{'segment':>18} {'ramp K/min':>10} {'hold h':>7} {'O2':>8} {'H2':>6} {'dp C':>6}  note"]
        T = self.T_start_C
        for s in self.segments:
            o2 = "air" if s.O2 >= 0.2 else (f"{s.O2*1e6:.0f}ppm" if s.O2 < 0.01 else f"{100*s.O2:.1f}%")
            rows.append(f"{T:7.0f} -> {s.T_end_C:6.0f} C {s.ramp_Kmin:10.3g} {s.hold_h:7.2f} {o2:>8} "
                        f"{100*s.H2:5.1f}% {s.dp_C:6.0f}  {s.note}")
            T = s.T_end_C
        rows.append(f"total {self.duration_h():.1f} h")
        return "\n".join(rows)


def baseline_v0() -> Cycle:
    """Cycle Card v0 from docs/PROPOSAL.md section 5 (binder-agnostic worst-case envelope)."""
    return Cycle(name="v0 envelope", segments=[
        Segment(80, 0.5, 4.0, 0.0, 0.0, -60, "solvent removal"),
        Segment(150, 0.1, 12.0, 0.0, 0.0, -60, "solvent, evaporation-limited"),
        Segment(205, 0.1, 8.0, 0.0, 0.0, -60, "onset of scission"),
        Segment(300, 0.05, 6.0, 0.002, 0.0, -60, "throttled burn"),
        Segment(400, 0.05, 4.0, 0.002, 0.0, -60, "throttled burn"),
        Segment(450, 0.2, 1.0, 0.0, 0.0, -60, "complete pyrolysis, purge"),
        Segment(800, 2.0, 8.0, 0.0, 0.001, 40, "wet-H2 gasification + reduction"),
        Segment(1040, 3.0, 3.0, 0.0, 0.04, -60, "densification"),
        Segment(600, 3.0, 0.0, 0.0, 0.04, -60, "reducing cool"),
        Segment(25, 5.0, 0.0, 0.0, 0.0, -60, "inert cool"),
    ])


def ifam_reference() -> Cycle:
    """Fraunhofer IFAM / Incus LMM copper (air debind 24 h/120 C + 63 h/250 C; 2 h/1050 C H2).

    The published process also has a 24 h acetone solvent debind before this, which the
    thermal model cannot represent; its effect is approximated by starting with no solvent.
    Ramp rates are not published and are set to 1 K/min (debind) and 5 K/min (sinter).
    """
    return Cycle(name="IFAM reference", segments=[
        Segment(120, 1.0, 24.0, 0.21, 0.0, 10, "air"),
        Segment(250, 1.0, 63.0, 0.21, 0.0, 10, "air"),
        Segment(25, 5.0, 0.0, 0.0, 0.0, -60, "cool, transfer"),
        Segment(1050, 5.0, 2.0, 0.0, 1.0, -60, "H2 sinter"),
        Segment(25, 5.0, 0.0, 0.0, 1.0, -60, "cool"),
    ])


def cea_reference() -> Cycle:
    """CEA-LITEN DLP copper: 400 C / 4 h in air, then 1050 C / 4 h in H2 (400 mbar in the paper)."""
    return Cycle(name="CEA reference", segments=[
        Segment(400, 1.0, 4.0, 0.21, 0.0, 10, "air debind"),
        Segment(25, 5.0, 0.0, 0.0, 0.0, -60, "cool, transfer"),
        Segment(1050, 5.0, 4.0, 0.0, 1.0, -60, "H2 sinter"),
        Segment(25, 5.0, 0.0, 0.0, 1.0, -60, "cool"),
    ])
