import pytest
from app.logic.diagnostics import run_diagnostics_basic
from tests.conftest import build_payload


@pytest.mark.parametrize("depth,use_profile", [
    (8500, False),   # fixed mud weight
    (10000, True)    # depth-aware mud weight profile
])
def test_diagnostics(depth, use_profile):
    data = build_payload(depth, use_profile)
    diagnostics = run_diagnostics_basic(data).model_dump(exclude_none=True)

    required_keys = [
    "depth", "dh", "dc", "dpi", "dci", "dco", "Q", "phi600", "phi300", "rho",
    "v_pipe", "v_annulus", "n", "k", "n_a", "k_a",
    "mu", "dp_casing_annulus", "dp_open_hole_annulus",
    "dc_open_hole_annulus", "hydrostatic_pressure", "ECD"
]

    for key in required_keys:
        assert key in diagnostics, f"Missing key: {key}"

    ecd_value = diagnostics["ECD"]
    assert isinstance(ecd_value, (float, int))
    assert 10.0 <= ecd_value <= 20.0

    expected_hydrostatic = 0.052 * diagnostics["rho"] * diagnostics["depth"]
    assert diagnostics["hydrostatic_pressure"] == pytest.approx(expected_hydrostatic, abs=0.1)

    dp_total = (
        diagnostics.get("dp_casing_annulus", 0.0) +
        diagnostics.get("dp_open_hole_annulus", 0.0) +
        diagnostics.get("dc_open_hole_annulus", 0.0)
    )
    ecd_expected = diagnostics["rho"] + dp_total / (0.052 * diagnostics["depth"])
    assert diagnostics["ECD"] == pytest.approx(ecd_expected, rel=1e-3)
