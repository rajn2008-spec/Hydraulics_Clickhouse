# app/logic/diagnostics.py

import math
from datetime import datetime
from app.models import OutputData
from app.logic.normalize import normalize_inputs
from app.logic.flow import (
    annularhydraulics_flow_velocity_annulus,
    annularhydraulics_velocity_drillstring_avg,
    powerlaw_constants_n_string,
    powerlaw_constants_k_string,
    powerlaw_constants_n_annulus,
    powerlaw_constants_k_annulus,
    evaluate_reynolds,
    effective_viscosity_drillstring,
    effective_viscosity_inside_annulus_openhole_casedhole,
)
from app.logic.rheology import (
    calculate_annular_critical_velocity,
    calculate_annular_critical_flow_rate,
)
from app.logic.pressure_loss import (
    pressure_loss_gradient_pipe_collar,
    pressure_loss_gradient_annulus_open_cased_hole,
)
from app.logic.pressure_loss_due_to_friction import (
    pressure_loss_gradient_drillstring,
    pressure_loss_due_to_friction_pipe,
    pressure_loss_due_to_friction_collar,
    pressure_loss_gradient_drill_pipe_open_hole,
    pressure_loss_gradient_drillstring_open_hole_annulus,
    pressure_loss_due_to_friction_pipe_casing_annulus,
    pressure_loss_due_to_friction_pipe_open_hole_annulus,
    pressure_loss_due_to_friction_collar_open_hole_annulus,
    equivalent_circulating_density,
)

# ---------------------------------------------------------
# GEOMETRY RESOLUTION
# ---------------------------------------------------------

def resolve_geometry(raw: dict, depth: float) -> dict:
    """Pick geometry values based on depth intervals."""
    def pick_interval(items, key, default):
        for s in items:
            if s.get("depth_from", 0) <= depth <= s.get("depth_to", 0):
                return s.get(key, default)
        return default

    dh = pick_interval(raw.get("bit", []), "od", 0.0)
    dc = pick_interval(raw.get("casing", []), "id", dh)
    dpi = pick_interval(raw.get("drill_pipe", []), "id", 0.0)
    dci = pick_interval(raw.get("drill_collar", []), "id", 0.0)
    dco = pick_interval(raw.get("drill_collar", []), "od", 0.0)

    return {"dh": dh, "dc": dc, "dpi": dpi, "dci": dci, "dco": dco}

# ---------------------------------------------------------
# RHEOLOGY
# ---------------------------------------------------------

def calculate_power_law_constants(inputs: dict) -> dict:
    theta600 = inputs.get("phi600")
    theta300 = inputs.get("phi300")
    theta3 = inputs.get("phi3")

    if not (theta600 and theta300 and theta3):
        return {"n": 0.0, "k": 0.0, "n_a": 0.0, "k_a": 0.0}

    n_s = powerlaw_constants_n_string(theta600, theta300)["n_s"]
    k_s = powerlaw_constants_k_string(theta600, n_s)["k_s"]
    n_a = powerlaw_constants_n_annulus(theta300, theta3)["n_a"]
    k_a = powerlaw_constants_k_annulus(theta300, n_a)["k_a"]

    return {"n": n_s, "k": k_s, "n_a": n_a, "k_a": k_a}

# ---------------------------------------------------------
# VELOCITIES
# ---------------------------------------------------------

def calculate_velocity(inputs: dict) -> dict:
    Q = inputs.get("Q")
    dpi = inputs.get("dpi")
    dci = inputs.get("dci")
    dh = inputs.get("dh")
    dc = inputs.get("dc")

    if not (Q and dpi and dci and dh and dc and dc > dh):
        return {"velocity_drillstring_avg": 0.0, "V_annulus": 0.0}

    d_in = min(dpi, dci)
    area_sqft = (math.pi * (d_in / 12.0) ** 2) / 4.0

    v_ds = annularhydraulics_velocity_drillstring_avg(Q, area_sqft)["velocity_drillstring_avg"]
    v_ann = annularhydraulics_flow_velocity_annulus(Q, dh, dc)["V_annulus"]

    return {"velocity_drillstring_avg": v_ds, "V_annulus": v_ann}

# ---------------------------------------------------------
# EFFECTIVE VISCOSITY
# ---------------------------------------------------------

def calculate_effective_viscosity(inputs: dict) -> dict:
    k_s = inputs.get("k")
    n_s = inputs.get("n")
    dpi = inputs.get("dpi")
    dci = inputs.get("dci")
    v_ds = inputs.get("velocity_drillstring_avg")

    k_a = inputs.get("k_a")
    n_a = inputs.get("n_a")
    v_ann = inputs.get("V_annulus")
    dh = inputs.get("dh")
    dc = inputs.get("dc")

    if not all([k_s, n_s, dpi, dci, v_ds, k_a, n_a, v_ann, dh, dc]):
        return {"mu": 0.0, "mu_eff_annulus": 0.0}

    mu_ds = effective_viscosity_drillstring(k_s, v_ds, dpi, dci, n_s)["mu"]
    mu_ann = effective_viscosity_inside_annulus_openhole_casedhole(
        k_a, v_ann, dh, dc, n_a, "cased_hole"
    )["mu_eff_annulus"]

    return {"mu": mu_ds, "mu_eff_annulus": mu_ann}

# ---------------------------------------------------------
# REYNOLDS NUMBERS
# ---------------------------------------------------------

def calculate_reynolds_number(inputs: dict) -> dict:
    res = evaluate_reynolds(
        data=inputs.get("geometry_data", inputs),
        depth=inputs.get("Dmd", 0),
        v_pipe_ftmin=inputs.get("velocity_drillstring_avg") or 0.0,
        v_annulus_ftmin=inputs.get("V_annulus") or 0.0,
        mu_pipe_cp=inputs.get("mu") or 0.0,
        mu_annulus_cp=inputs.get("mu_eff_annulus") or 0.0,
        n_s=inputs.get("n") or 0.0,
        n_a=inputs.get("n_a") or 0.0,
        rho_lbgal=inputs.get("rho") or 0.0,
    )
    return {
        "Re_pipe_collar": res["Re_pipe_collar"],
        "Re_annulus": res["Re_annulus"],
    }

# ---------------------------------------------------------
# PRESSURE LOSSES
# ---------------------------------------------------------

def calculate_pressure_losses(inputs: dict) -> dict:
    Q = inputs.get("Q", 0.0)
    mu = inputs.get("mu", 0.0)

    dp_casing = Q * mu * 0.001
    dp_open_hole = Q * mu * 0.002
    dc_open_hole = Q * mu * 0.0005

    return {
        "dp_casing_annulus": dp_casing,
        "dp_open_hole_annulus": dp_open_hole,
        "dc_open_hole_annulus": dc_open_hole,
    }

# ---------------------------------------------------------
# HYDROSTATIC + ECD
# ---------------------------------------------------------

def calculate_hydrostatic_pressure(inputs: dict) -> dict:
    rho = inputs.get("rho", inputs.get("rhoe", 0.0))
    depth = inputs.get("depth", 0.0)
    return {"hydrostatic_pressure": 0.052 * rho * depth}

def calculate_ecd(inputs: dict) -> dict:
    rho = inputs.get("rho", inputs.get("rhoe", 0.0))
    dp_open_hole = inputs.get("dp_open_hole_annulus", 0.0)
    depth = inputs.get("depth", 0.0)

    if depth > 0:
        ecd = rho + dp_open_hole / (0.052 * depth)
    else:
        ecd = 0.0

    return {"ECD": ecd}

# ---------------------------------------------------------
# OUTPUT MAPPING
# ---------------------------------------------------------

OUTPUT_MAP = {
    "velocity_drillstring_avg": "v_pipe",
    "V_annulus": "v_annulus",
    "n": "n",
    "k": "k",
    "n_a": "n_a",
    "k_a": "k_a",
    "mu": "mu",
    "mu_eff_annulus": "mu_eff_annulus",
    "Re_pipe_collar": "Re_pipe",
    "Re_annulus": "Re_annulus",
    "dp_casing_annulus": "dp_casing_annulus",
    "dp_open_hole_annulus": "dp_open_hole_annulus",
    "dc_open_hole_annulus": "dc_open_hole_annulus",
    "hydrostatic_pressure": "hydrostatic_pressure",
    "ECD": "ECD",
    "rho": "rho",
    "rhoe": "rhoe",
    "dh": "dh",
    "dc": "dc",
    "dpi": "dpi",
    "dci": "dci",
    "dco": "dco",
    "Q": "Q",
    "phi600": "phi600",
    "phi300": "phi300",
}

# ---------------------------------------------------------
# MAIN DIAGNOSTICS
# ---------------------------------------------------------

def run_diagnostics_basic(raw_inputs: dict, mud_weight_profile=None) -> OutputData:
    normalized_bundle = normalize_inputs(raw_inputs)
    raw = normalized_bundle["raw"]
    inputs = normalized_bundle["normalized"]

    diagnostics = {}

    # 1) Geometry
    depth = raw_inputs.get("depth", raw_inputs.get("Dmd", 0.0))
    geom = resolve_geometry(raw_inputs, depth)
    diagnostics.update(geom)

    # 2) Rheology
    diagnostics.update(calculate_power_law_constants(inputs))

    # 3) Velocities
    diagnostics.update(calculate_velocity({**inputs, **diagnostics}))

    # 4) Effective viscosity
    diagnostics.update(calculate_effective_viscosity({**inputs, **diagnostics}))

    # 5) Reynolds numbers
    diagnostics.update(calculate_reynolds_number({**inputs, **diagnostics}))

    # 6) Pressure losses
    diagnostics.update(calculate_pressure_losses({**inputs, **diagnostics}))

    # 7) Depth
    diagnostics["depth"] = depth

    # 8) Mud weight profile average
    mw_profile = raw_inputs.get("mud_weight_profile", [])
    if mw_profile:
        avg_weights = [
            (s.get("weight_from", 0.0) + s.get("weight_to", 0.0)) / 2
            for s in mw_profile
            if s.get("weight_from") is not None and s.get("weight_to") is not None
        ]
        diagnostics["rhoe"] = sum(avg_weights) / len(avg_weights) if avg_weights else 0.0
    else:
        diagnostics["rhoe"] = 0.0

    # 9) Resolve rho
    diagnostics["rho"] = inputs.get("rho", diagnostics["rhoe"])

    # 10) Hydrostatic + ECD
    diagnostics.update(calculate_hydrostatic_pressure({**inputs, **diagnostics}))
    diagnostics.update(calculate_ecd({**inputs, **diagnostics}))

    # 11) Audit trail
    diagnostics["audit_raw_inputs"] = raw
    diagnostics["audit_normalized_inputs"] = inputs
    diagnostics["timestamp"] = datetime.now().isoformat()

    # 12) Canonical mapping
    for internal, canonical in OUTPUT_MAP.items():
        diagnostics[canonical] = diagnostics.get(internal, diagnostics.get(canonical, 0.0))

    # 13) Return only declared OutputData fields
    return OutputData(**{k: v for k, v in diagnostics.items() if k in OutputData.__annotations__})

def run_diagnostics_basic_test(payload, mud_weight_profile=None):
    return run_diagnostics_basic(payload)
