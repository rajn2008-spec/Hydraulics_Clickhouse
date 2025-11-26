import pytest

from app.logic.pressure_loss_due_to_friction import (
    pressure_loss_due_to_friction_pipe,
    pressure_loss_due_to_friction_collar,
    pressure_loss_due_to_friction_pipe_casing_annulus,
    pressure_loss_due_to_friction_pipe_open_hole_annulus,
    pressure_loss_due_to_friction_collar_open_hole_annulus,
    pressure_loss_due_to_friction_segment,
    pressure_loss_gradient_drillstring,
    pressure_loss_gradient_drillstring_open_hole_annulus,
    equivalent_circulating_density,
)

# -----------------------------
# Component-level friction losses
# -----------------------------
@pytest.mark.parametrize("func,inputs,key,expected", [
    (pressure_loss_due_to_friction_pipe, (0.5, 1000), "ΔPdp", 500.0),
    (pressure_loss_due_to_friction_collar, (0.3, 500), "ΔPdc", 150.0),
    (pressure_loss_due_to_friction_pipe_casing_annulus, (0.5, 1000), "ΔPdpc", 500.0),
    (pressure_loss_due_to_friction_collar_open_hole_annulus, (0.3, 500), "ΔPdch", 150.0),
])
def test_pressure_loss_components(func, inputs, key, expected):
    """Check individual component friction losses return correct keys and values."""
    result = func(*inputs)
    assert key in result
    assert result[key] > 0
    assert result[key] == pytest.approx(expected, abs=0.01)

# -----------------------------
# Segment helper
# -----------------------------
def test_pressure_loss_due_to_friction_segment():
    """Check segment helper returns Δp with expected value."""
    result = pressure_loss_due_to_friction_segment(0.5, 1000)
    assert "Δp" in result
    assert result["Δp"] == pytest.approx(500.0, abs=0.01)

# -----------------------------
# Drillstring wrappers
# -----------------------------
@pytest.mark.parametrize("func,inputs,expected", [
    (pressure_loss_gradient_drillstring, (0.5, 1000, 0.3, 500), 650.0),   # pipe + collar
    (pressure_loss_gradient_drillstring_open_hole_annulus, (0.4, 1000, 0.3, 500), 550.0),   # open hole annulus
])
def test_pressure_loss_drillstring_variants(func, inputs, expected):
    """Check drillstring and open hole annulus wrappers return Δp with expected values."""
    result = func(*inputs)
    assert "Δp" in result
    assert result["Δp"] == pytest.approx(expected, abs=0.01)

# -----------------------------
# Pipe open hole annulus
# -----------------------------
def test_pressure_loss_due_to_friction_pipe_open_hole_annulus():
    """Check pipe open hole annulus returns ΔPdph with expected value."""
    result = pressure_loss_due_to_friction_pipe_open_hole_annulus(0.5, 1000, 200)
    assert "ΔPdph" in result
    assert result["ΔPdph"] >= 0
    assert result["ΔPdph"] == pytest.approx(400.0, abs=0.01)  # (1000-200)*0.5

# -----------------------------
# Equivalent Circulating Density
# -----------------------------
def test_equivalent_circulating_density():
    """Check ECD calculation matches canonical Eq-28."""
    mud_weight = 12.0  # lb/gal
    tvd = 10000        # ft
    dp_casing_annulus = 500.0
    dp_open_hole_annulus = 400.0
    dc_open_hole_annulus = 150.0

    result = equivalent_circulating_density(
        mud_weight,
        dp_casing_annulus,
        dp_open_hole_annulus,
        dc_open_hole_annulus,
        tvd
    )

    assert "ECD" in result
    ecd_value = result["ECD"]
    expected = mud_weight + (dp_casing_annulus + dp_open_hole_annulus + dc_open_hole_annulus) / (0.052 * tvd)
    assert ecd_value > 0
    assert ecd_value == pytest.approx(expected, abs=0.01)
