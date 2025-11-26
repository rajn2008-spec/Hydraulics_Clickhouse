# app/logic/geometry.py
import math

def get_active_section(sections, current_depth):
    """
    Returns the active section based on current depth.
    Always returns a dict (possibly with defaults).
    """
    for section in sections:
        if section.get("depth_from", 0.0) <= current_depth <= section.get("depth_to", 0.0):
            return section
    return {"depth_from": 0.0, "depth_to": 0.0, "id": 0.0, "od": 0.0}


def get_active_diameter(sections, current_depth, key="od"):
    """
    Returns the diameter (id or od) from the active section.
    """
    section = get_active_section(sections, current_depth)
    return section.get(key, 0.0)


def get_bit_diameter(bit_sections, depth):
    """
    Returns the bit diameter at a given depth.
    """
    for section in reversed(bit_sections):
        if depth >= section.get("depth", 0.0):
            return section.get("od", 0.0)
    return 0.0


def infer_hole_config(casing_id, bit_od):
    if casing_id and casing_id > 0:
        return "cased_hole"
    elif bit_od and bit_od > 0:
        return "open_hole"
    return "invalid"


def get_annular_diameters(config, drill_pipe_od, drill_collar_od, bit_od, casing_id):
    if config == "open_hole":
        d1 = drill_collar_od if drill_collar_od and drill_collar_od > 0 else drill_pipe_od
        d2 = bit_od
    elif config == "cased_hole":
        d1 = drill_pipe_od
        d2 = casing_id
    elif config == "transition_zone":
        d1 = drill_collar_od if drill_collar_od and drill_collar_od > 0 else drill_pipe_od
        d2 = casing_id
    else:
        return 0.0, 0.0
    return d1 or 0.0, d2 or 0.0


def calculate_annular_critical_flow_rate(V_crit, hole_config, pipe_od, collar_od, casing_id, bit_od):
    """
    Calculates annular critical flow rate in gal/min using hole config logic.
    Returns dict keyed by canonical OutputData symbol 'Qcrit'.
    """
    d1, d2 = get_annular_diameters(hole_config, pipe_od, collar_od, casing_id, bit_od)
    if not V_crit or V_crit <= 0 or not d1 or d1 <= 0 or not d2 or d2 <= d1:
        return {"Qcrit": 0.0}
    Qcrit = (2.45 * V_crit * (d2**2 - d1**2)) / 60
    return {"Qcrit": Qcrit}


def get_mud_weight_at_depth(mud_weight_profile: list, depth: float) -> dict:
    """
    Resolves mud weight at a given depth from a depth-ranged mud weight profile.
    Returns dict keyed by canonical OutputData symbol 'rho'.
    """
    for section in mud_weight_profile:
        if section.get("depth_from", 0.0) <= depth <= section.get("depth_to", 0.0):
            rho_val = (section.get("weight_from", 0.0) + section.get("weight_to", 0.0)) / 2.0
            return {"rho": rho_val}
    return {"rho": 0.0}
