"""Validation against published copper VPP data. Tolerances reflect the anchors' own spread."""
import pytest

from cupola import validation as V


@pytest.mark.parametrize("T_C,measured", V.ROUMANIE_OX)
def test_roumanie_compact_oxidation(T_C, measured):
    # intrinsic law is fitted to Ott powder data only; compacts are an out-of-sample check
    pred = V.cu_compact_oxidation(T_C)
    assert pred == pytest.approx(measured, rel=0.45)


def test_cea_density_is_the_calibration_point():
    r = V.cea_case()
    assert 0.89 <= r.kpi["rho_final"] <= 0.95
    assert r.kpi["C_final_ppm"] < 50          # air debind at 400 C leaves little carbon (measured 190 ppm)


def test_ifam_solvent_debind_beats_air_only():
    """Measured: 95.3 % (solvent + air) vs ~92 % (air only). The model must reproduce the ordering."""
    a = V.ifam_case(solvent_debind=True).kpi["rho_final"]
    b = V.ifam_case(solvent_debind=False).kpi["rho_final"]
    assert a > b
    assert 0.01 < a - b < 0.08
