import pytest

from app.logic.friction import (
    fanning_factor_pipe_collar_turbulent,
    fanning_friction_transitional_annulus,
)

def test_fanning_factor_pipe_collar_turbulent_basic():
    """Check turbulent pipe/collar friction factor is positive and within expected canonical range."""
    result = fanning_factor_pipe_collar_turbulent(10000, 0.8)
    assert isinstance(result, float)
    assert 0 < result < 1.0
    assert result < 0.1  # sanity check

@pytest.mark.parametrize("Re, roughness", [
    (5000, 0.8),
    (20000, 0.5),
    (100000, 0.1),
    (2000, 1.0),   # edge case: lower Re, high roughness
])
def test_fanning_factor_pipe_collar_turbulent_parametrized(Re, roughness):
    """Parametrized check for turbulent pipe/collar friction factor."""
    result = fanning_factor_pipe_collar_turbulent(Re, roughness)
    assert isinstance(result, float)
    assert 0 < result < 1.0
    assert result < 0.1

def test_fanning_friction_transitional_annulus_basic():
    """Check transitional annulus friction factor is positive and within expected canonical range."""
    result = fanning_friction_transitional_annulus(5000, 3000, 10000, 0.9)["f"]
    assert isinstance(result, float)
    assert 0 < result < 1.0
    assert result < 0.2  # sanity check

@pytest.mark.parametrize("Re, Re_amin, Re_amax, n_a", [
    (4000, 2000, 8000, 0.8),
    (6000, 3000, 12000, 0.5),
    (10000, 5000, 20000, 0.1),
    (2000, 1000, 4000, 1.0),  # edge case: low Re, high roughness
])
def test_fanning_friction_transitional_annulus_parametrized(Re, Re_amin, Re_amax, n_a):
    """Parametrized check for transitional annulus friction factor."""
    result = fanning_friction_transitional_annulus(Re, Re_amin, Re_amax, n_a)["f"]
    assert isinstance(result, float)
    assert 0 < result < 1.0
    assert result < 0.2
