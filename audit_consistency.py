# audit_consistency.py

from app.models import InputData, OutputData
from utils.parameter_names import PARAMETER_NAMES
from utils.parameter_units import PARAMETER_UNITS, convert_units

def audit_consistency():
    print("=== INPUT AUDIT ===")
    for field in InputData.model_fields:
        if field not in PARAMETER_NAMES:
            print(f"⚠️ Missing PARAMETER_NAMES entry for input: {field}")
        if field not in PARAMETER_UNITS:
            print(f"⚠️ Missing PARAMETER_UNITS entry for input: {field}")

    print("\n=== OUTPUT AUDIT ===")
    for field in OutputData.model_fields:
        if field not in PARAMETER_NAMES:
            print(f"⚠️ Missing PARAMETER_NAMES entry for output: {field}")
        if field not in PARAMETER_UNITS:
            print(f"⚠️ Missing PARAMETER_UNITS entry for output: {field}")

    print("\n=== UNIT CONVERSION CHECKS ===")
    checks = [
        ("Q", 500, "gal/min", "L/s"),
        ("rho", 9.5, "lb/gal", "kg/m3"),
        ("dp", 250, "psi", "kPa"),
        ("Vs", 100, "ft/min", "m/s"),
    ]
    for key, val, from_unit, to_unit in checks:
        converted = convert_units(val, from_unit, to_unit)
        if converted is None:
            print(f"❌ No conversion found for {key} ({from_unit} -> {to_unit})")
        else:
            print(f"✅ {key}: {val} {from_unit} -> {converted:.3f} {to_unit}")

    print("\n=== SUMMARY ===")
    print("Inputs checked:", len(InputData.model_fields))
    print("Outputs checked:", len(OutputData.model_fields))

if __name__ == "__main__":
    audit_consistency()
