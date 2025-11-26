# app/logic/sections.py

from typing import Literal

# -----------------------------
# Annular Critical Velocity & Flow Rate (Imperial)
# -----------------------------

def calculate_annular_critical_velocity(
    hole_config: Literal["open_hole", "cased_hole"],
    Re_min: float,
    k_a: float,
    n_a: float,
    rho_lbgal: float,
    pipe_od_in: float,
    collar_od_in: float,
    bit_od_in: float,
    casing_id_in: float
) -> dict:
    """
    Eq-13: Annular Critical Velocity [ft/min]

    Vcrit = 60 * [
        (100 * Re_min * k_a * ((2*n_a + 1)/(3*n_a))**n_a)
        /
        (928 * rho * (d2 - d1) * (144/(d2 - d1))**(1 - n_a))
    ]**(1/(2 - n_a))

    Returns dict keyed by 'Vcrit'.
    """
    # Geometry selection
    if hole_config == "open_hole":
        d1 = max(pipe_od_in or 0.0, collar_od_in or 0.0)
        d2 = bit_od_in or 0.0
    elif hole_config == "cased_hole":
        d1 = pipe_od_in or 0.0
        d2 = casing_id_in or 0.0
    else:
        return {"Vcrit": 0.0}

    # Gates
    if (
        not Re_min or Re_min <= 0 or
        not k_a or k_a <= 0 or
        not n_a or n_a <= 0 or n_a == 2.0 or
        not rho_lbgal or rho_lbgal <= 0 or
        not d1 or d1 <= 0 or not d2 or d2 <= d1
    ):
        return {"Vcrit": 0.0}

    dh = d2 - d1
    rheology_term = ((2 * n_a + 1) / (3 * n_a)) ** n_a
    geometry_term = (144 / dh) ** (1 - n_a)

    numerator = 100 * Re_min * k_a * rheology_term
    denominator = 928 * rho_lbgal * dh * geometry_term

    Vcrit = 60 * (numerator / denominator) ** (1 / (2 - n_a))
    return {"Vcrit": Vcrit}


def calculate_annular_critical_flow_rate(
    hole_config: Literal["open_hole", "cased_hole"],
    v_crit_ftmin: float,
    pipe_od_in: float,
    collar_od_in: float,
    bit_od_in: float,
    casing_id_in: float
) -> dict:
    """
    Computes annular critical flow rate [gal/min] using Eq-14.

    Formula:
        Qcrit = (2.45 * Vcrit * (d2**2 - d1**2)) / 60

    Returns dict keyed by 'Qcrit'.
    """
    # Geometry selection
    if hole_config == "open_hole":
        d1 = max(pipe_od_in or 0.0, collar_od_in or 0.0)
        d2 = bit_od_in or 0.0
    elif hole_config == "cased_hole":
        d1 = pipe_od_in or 0.0
        d2 = casing_id_in or 0.0
    else:
        return {"Qcrit": 0.0}

    # Gates
    if (
        v_crit_ftmin is None or v_crit_ftmin <= 0 or
        d1 <= 0 or d2 <= d1
    ):
        return {"Qcrit": 0.0}

    Qcrit = (2.45 * v_crit_ftmin * (d2 ** 2 - d1 ** 2)) / 60
    return {"Qcrit": Qcrit}


# -----------------------------
# Section Geometry Helpers
# -----------------------------

def drill_pipe(sections: list[dict]) -> list[dict]:
    """Normalize drill pipe sections."""
    if not sections:
        return [{"section": "drill_pipe", "id": 0.0, "od": 0.0, "depth_from": 0.0, "depth_to": 0.0}]
    return [
        {
            "section": s.get("section", "drill_pipe"),
            "id": s.get("id", 0.0),
            "od": s.get("od", 0.0),
            "depth_from": s.get("depth_from", 0.0),
            "depth_to": s.get("depth_to", 0.0),
        }
        for s in sections
    ]


def drill_collar(sections: list[dict]) -> list[dict]:
    """Normalize drill collar sections."""
    if not sections:
        return [{"section": "drill_collar", "id": 0.0, "od": 0.0, "depth_from": 0.0, "depth_to": 0.0}]
    return [
        {
            "section": s.get("section", "drill_collar"),
            "id": s.get("id", 0.0),
            "od": s.get("od", 0.0),
            "depth_from": s.get("depth_from", 0.0),
            "depth_to": s.get("depth_to", 0.0),
        }
        for s in sections
    ]


def casing(sections: list[dict]) -> list[dict]:
    """Normalize casing sections."""
    if not sections:
        return [{"section": "casing", "id": 0.0, "depth_from": 0.0, "depth_to": 0.0}]
    return [
        {
            "section": s.get("section", "casing"),
            "id": s.get("id", 0.0),
            "depth_from": s.get("depth_from", 0.0),
            "depth_to": s.get("depth_to", 0.0),
        }
        for s in sections
    ]


def bit(sections: list[dict]) -> list[dict]:
    """Normalize bit sections."""
    if not sections:
        return [{"section": "bit", "od": 0.0, "depth_from": 0.0, "depth_to": 0.0}]
    return [
        {
            "section": s.get("section", "bit"),
            "od": s.get("od", 0.0),
            "depth_from": s.get("depth_from", 0.0),
            "depth_to": s.get("depth_to", 0.0),
        }
        for s in sections
    ]


def load_geometry_sections(raw: dict) -> dict:
    """Loads and normalizes all geometry sections from raw input."""
    return {
        "drill_pipe": drill_pipe(raw.get("drill_pipe", [])),
        "drill_collar": drill_collar(raw.get("drill_collar", [])),
        "casing": casing(raw.get("casing", [])),
        "bit": bit(raw.get("bit", [])),
    }
