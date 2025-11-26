import pytest
from app.models import InputData, OutputData
from utils.parameter_names import PARAMETER_NAMES
from utils.parameter_units import PARAMETER_UNITS, convert_units

@pytest.mark.parametrize("field", InputData.model_fields)
def test_input_fields_have_names_and_units(field):
    """Ensure every InputData field has a name and unit mapping."""
    assert field in PARAMETER_NAMES, f"Missing PARAMETER_NAMES entry for input: {field}"
    assert field in PARAMETER_UNITS, f"Missing PARAMETER_UNITS entry for input: {field}"

@pytest.mark.parametrize("field", OutputData.model_fields)
def test_output_fields_have_names_and_units(field):
    """Ensure every OutputData field has a name and unit mapping."""
    assert field in PARAMETER_NAMES, f"Missing PARAMETER_NAMES entry for output: {field}"
    assert field in PARAMETER_UNITS, f"Missing PARAMETER_UNITS entry for output: {field}"

def test_unit_conversions():
    """Check representative unit conversions exist and return numeric values."""
    checks = [
        ("Q", 500, "gal/min", "L/s"),
        ("rho", 9.5, "lb/gal", "kg/m³"),
        ("Δp", 250, "psi", "kPa"),
        ("Vs", 100, "ft/min", "m/s"),
    ]
    for key, val, from_unit, to_unit in checks:
        converted = convert_units(val, from_unit, to_unit)
        assert converted is not None, f"No conversion found for {key} ({from_unit} → {to_unit})"
        assert isinstance(converted, (float, int)), f"Conversion for {key} did not return a number"
        assert converted >= 0, f"Conversion for {key} returned non-positive value: {converted}"
