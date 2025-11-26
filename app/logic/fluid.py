# app/logic/fluid.py

import math

# -----------------------------
# Power Law Constants
# -----------------------------

def calculate_power_law_string(theta_600, theta_300):
    """Eq-3 & Eq-4: Power law constants for drillstring."""
    if not theta_600 or theta_600 <= 0 or not theta_300 or theta_300 <= 0:
        return {"n": 0.0, "k": 0.0}
    n_s = 3.32 * math.log10(theta_600 / theta_300)
    k_s = (5.11 * theta_600) / (1022 ** n_s)
    return {"n": n_s, "k": k_s}


def calculate_power_law_annulus(theta_300, theta_3):
    """Eq-5 & Eq-6: Power law constants for annulus."""
    if not theta_300 or theta_300 <= 0 or not theta_3 or theta_3 <= 0:
        return {"n_a": 0.0, "k_a": 0.0}
    n_a = 0.5 * math.log10(theta_300 / theta_3)
    k_a = (5.11 * theta_300) / (511 ** n_a)
    return {"n_a": n_a, "k_a": k_a}


# -----------------------------
# Effective Viscosity
# -----------------------------

def effective_viscosity_string(k_s, v, pipe_id, collar_id, n_s):
    """Eq-7: Effective viscosity inside the string."""
    d = collar_id if collar_id and collar_id > 0 else pipe_id
    if not d or d <= 0 or not k_s or k_s <= 0 or not v or v <= 0 or not n_s or n_s <= 0:
        return {"mu": 0.0}

    shear_rate = 96 * v
    mu = (100 * k_s * shear_rate ** (n_s - 1)) / (60 * d)
    return {"mu": mu}


def effective_viscosity_annulus(k_a, v, hole_config, pipe_od, collar_od, bit_od, casing_od, n_a):
    """Eq-8: Effective viscosity in the annulus."""
    if hole_config == "open_hole":
        d1 = collar_od if collar_od and collar_od > 0 else pipe_od
        d2 = bit_od
    elif hole_config == "cased_hole":
        d1 = pipe_od
        d2 = casing_od
    else:
        return {"mu_eff_annulus": 0.0}

    if not d1 or not d2 or d2 <= d1 or not k_a or k_a <= 0 or not v or v <= 0 or not n_a or n_a <= 0:
        return {"mu_eff_annulus": 0.0}

    shear_rate = 144 * v / (d2 - d1)
    mu = (100 * k_a * shear_rate ** (n_a - 1)) / 60
    return {"mu_eff_annulus": mu}


# -----------------------------
# Unit Conversions
# -----------------------------

def convert_flow_rate(value, from_unit, to_unit):
    """Convert flow rate between supported units. Supported: gpm ↔ m3/s"""
    if not value or value <= 0:
        return 0.0
    if from_unit == "gpm" and to_unit == "m3/s":
        return value * 6.309e-5
    elif from_unit == "m3/s" and to_unit == "gpm":
        return value / 6.309e-5
    else:
        raise ValueError(f"Unsupported flow rate conversion: {from_unit} → {to_unit}")


def convert_viscosity(value, from_unit, to_unit):
    """Convert dynamic viscosity between supported units. Supported: cP ↔ Pa·s"""
    if not value or value <= 0:
        return 0.0
    if from_unit == "cP" and to_unit == "Pa·s":
        return value / 1000
    elif from_unit == "Pa·s" and to_unit == "cP":
        return value * 1000
    else:
        raise ValueError(f"Unsupported viscosity conversion: {from_unit} → {to_unit}")


def convert_pressure(value, from_unit, to_unit):
    """Convert pressure between supported units. Supported: psi ↔ Pa"""
    if not value or value <= 0:
        return 0.0
    if from_unit == "psi" and to_unit == "Pa":
        return value * 6894.76
    elif from_unit == "Pa" and to_unit == "psi":
        return value / 6894.76
    else:
        raise ValueError(f"Unsupported pressure conversion: {from_unit} → {to_unit}")


def convert_density(value, from_unit, to_unit):
    """Convert fluid density between supported units. Supported: lb/gal ↔ kg/m3"""
    if not value or value <= 0:
        return 0.0
    if from_unit == "lb/gal" and to_unit == "kg/m3":
        return value * 119.826
    elif from_unit == "kg/m3" and to_unit == "lb/gal":
        return value / 119.826
    else:
        raise ValueError(f"Unsupported density conversion: {from_unit} → {to_unit}")
