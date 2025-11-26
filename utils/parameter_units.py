# app/utils/parameter_units.py

from typing import Optional, Tuple

# Canonical units registry
PARAMETER_UNITS = {
    # General hydraulics
    "Q": "gal/min",
    "rho": "lb/gal",
    "Dmd": "ft",
    "Dtvd": "ft",
    "Dbo": "ft",
    "Dbp": "ft",
    "ROP": "ft/hr",
    "dh": "in",
    "dc": "in",
    "dpi": "in",
    "dpo": "in",
    "dci": "in",
    "dco": "in",
    "phi600": "dial units",
    "phi300": "dial units",
    "phi3": "dial units",
    "tau30": "lbf/100ft2",

    # ASCII replacements
    "dp": "psi",
    "dp_L": "psi/ft",
    "mu": "cP",

    "ECD": "lb/gal",
    "Re": "dimensionless",
    "Remax": "dimensionless",
    "n": "dimensionless",
    "k": "lb*s^n/ft2",
    "flow_string": "regime",
    "flow_annulus": "regime",

    # Bit hydraulics
    "A": "in2",
    "Vjet": "ft/min",

    # ASCII replacement
    "dpb": "psi",

    "hydraulic_power_hp": "hp",
    "PA": "hp/in2",
    "Fi": "lbf",

    # Cuttings transport
    "gb": "s^-1",
    "tp": "lbf/100ft2",
    "gp": "s^-1",

    "Vs": "ft/min",
    "Vt": "ft/min",
    "Et": "%",
    "C": "%",

    # Swab & surge
    "Vp": "ft/min",
    "Ve": "ft/min",

    # ASCII replacement
    "rhoe": "lb/gal",

    "Pg": "psi",
    "swab_pressure": "psi",
    "surge_pressure": "psi",
    "swab_velocity": "ft/min",
    "surge_velocity": "ft/min",
    "swab_force": "lbf",
    "surge_force": "lbf",

    # Derived outputs
    "v_pipe": "ft/min",
    "v_ann": "ft/min",
    "Re_pipe": "dimensionless",
    "Re_ann": "dimensionless",

    # ASCII replacements
    "mu_e_pipe": "cP",
    "mu_e_ann": "cP",

    "n_string": "dimensionless",
    "k_string": "lb*s^n/ft2",
    "n_annulus": "dimensionless",
    "k_annulus": "lb*s^n/ft2",

    # Normalization-only inputs
    "d1": "in",
    "d2": "in",
    "gel_dpc": "lbf/100ft2",
    "gel_dph": "lbf/100ft2",
    "gel_dch": "lbf/100ft2",
    "k_a": "lb*s^n/ft2",
    "n_a": "dimensionless",
    "well_id": "meta",

    # Patched inputs
    "Ldp": "ft",
    "Ldc": "ft",
    "Lc": "ft",
    "J": "in/32",
    "dcut": "in",
    "T": "in",
    "t": "s",
    "Ls": "ft",

    # Structured profiles
    "drill_pipe": "profile",
    "drill_collar": "profile",
    "casing": "profile",
    "bit": "profile",
    "mud_weight_profile": "profile",

    # Patched outputs
    "V": "ft/min",
    "Vcrit": "ft/min",
    "Qcrit": "gal/min",
    "f": "dimensionless",
    "P": "psi",
    "missing_inputs": "meta",
    "audit_raw_inputs": "meta",
    "audit_normalized_inputs": "meta",
    "timestamp": "meta",
}

# Metric targets for display
metric_target_by_key = {
    "Q": "L/s",
    "rho": "kg/m3",
    "dp": "kPa",
    "Vs": "m/s",
    "V": "m/s",
    "Vcrit": "m/s",
    "Qcrit": "L/s",
    "v_pipe": "m/s",
    "v_ann": "m/s",
    "ECD": "kg/m3",
}

# Minimal conversion map
UNIT_CONVERSIONS = {
    ("gal/min", "L/s"): 0.06309,
    ("L/s", "gal/min"): 1 / 0.06309,

    ("lb/gal", "kg/m3"): 119.826,
    ("kg/m3", "lb/gal"): 1 / 119.826,

    ("psi", "kPa"): 6.89476,
    ("kPa", "psi"): 1 / 6.89476,

    ("ft/min", "m/s"): 0.00508,
    ("m/s", "ft/min"): 1 / 0.00508,

    ("ft", "m"): 0.3048,
    ("m", "ft"): 1 / 0.3048,

    ("in", "mm"): 25.4,
    ("mm", "in"): 1 / 25.4,
}

def convert_units(value: float, from_unit: str, to_unit: str) -> Optional[float]:
    if from_unit == to_unit:
        return float(value)
    factor = UNIT_CONVERSIONS.get((from_unit, to_unit))
    if factor is None:
        return None
    return float(value) * factor

def convert_value_for_param(key: str, value: float, to_metric: bool = False) -> Tuple[float, str]:
    base_unit = PARAMETER_UNITS.get(key, "")
    if not to_metric:
        return float(value), base_unit

    target_unit = metric_target_by_key.get(key, base_unit)
    converted = convert_units(value, base_unit, target_unit)
    if converted is None:
        return float(value), base_unit
    return converted, target_unit
