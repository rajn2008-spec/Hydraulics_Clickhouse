# app/logic/hydraulics.py

import math
from datetime import datetime

from app.models import OutputData

# Geometry
from app.logic.geometry import (
    get_annular_diameters,
)

# Fluid (power law + viscosity)
from app.logic.fluid import (
    calculate_power_law_string,
    calculate_power_law_annulus,
    effective_viscosity_string,
    effective_viscosity_annulus,
)

# Flow (velocities, viscosities, Reynolds, regime)
from app.logic.flow import (
    annularhydraulics_flow_velocity_pipe,
    annularhydraulics_flow_velocity_collar,
    annularhydraulics_flow_velocity_annulus,
    annularhydraulics_velocity_drillstring_avg,
    effective_viscosity_drillpipe_drillcollar,
    effective_viscosity_drillstring,
    effective_viscosity_inside_annulus_openhole_casedhole,
    evaluate_reynolds,
    critical_reynolds,
    classify_flow,
)

# ---------------------------------------------------------
# Diagnostics Orchestration
# ---------------------------------------------------------

def run_diagnostics(inputs: dict) -> OutputData:
    """
    Orchestrates hydraulics calculations using geometry, fluid, and flow modules.
    Returns OutputData aligned with canonical ASCII schema.
    """

    diagnostics = {}

    # -----------------------------------------------------
    # Power Law Constants (string + annulus)
    # -----------------------------------------------------
    diagnostics.update(
        calculate_power_law_string(
            inputs.get("phi600", 0.0),
            inputs.get("phi300", 0.0)
        )
    )

    diagnostics.update(
        calculate_power_law_annulus(
            inputs.get("phi300", 0.0),
            inputs.get("phi3", 0.0)
        )
    )

    # -----------------------------------------------------
    # Velocities
    # -----------------------------------------------------
    diagnostics.update(
        annularhydraulics_flow_velocity_pipe(
            inputs.get("Q", 0.0),
            inputs.get("dpi", 0.0)
        )
    )

    diagnostics.update(
        annularhydraulics_flow_velocity_collar(
            inputs.get("Q", 0.0),
            inputs.get("dci", 0.0)
        )
    )

    diagnostics.update(
        annularhydraulics_flow_velocity_annulus(
            inputs.get("Q", 0.0),
            inputs.get("dc", 0.0),
            inputs.get("dh", 0.0),
            context="open_hole"  # caller decides context
        )
    )

    # Drillstring average velocity
    area_pipe_sqft = (
        math.pi * (inputs.get("dpi", 0.0) / 2) ** 2 / 144
        if inputs.get("dpi", 0.0) > 0 else 0.0
    )

    diagnostics.update(
        annularhydraulics_velocity_drillstring_avg(
            inputs.get("Q", 0.0),
            area_pipe_sqft
        )
    )

    # -----------------------------------------------------
    # Effective Viscosities
    # -----------------------------------------------------
    diagnostics.update(
        effective_viscosity_drillpipe_drillcollar(
            diagnostics.get("k", 0.0),
            diagnostics.get("V_pipe", 0.0),
            inputs.get("dpi", 0.0),
            diagnostics.get("n", 0.0)
        )
    )

    diagnostics.update(
        effective_viscosity_drillpipe_drillcollar(
            diagnostics.get("k", 0.0),
            diagnostics.get("V_collar", 0.0),
            inputs.get("dci", 0.0),
            diagnostics.get("n", 0.0)
        )
    )

    diagnostics.update(
        effective_viscosity_drillstring(
            diagnostics.get("k", 0.0),
            diagnostics.get("velocity_drillstring_avg", 0.0),
            inputs.get("dpi", 0.0),
            inputs.get("dci", 0.0),
            diagnostics.get("n", 0.0)
        )
    )

    diagnostics.update(
        effective_viscosity_inside_annulus_openhole_casedhole(
            diagnostics.get("k_a", 0.0),
            diagnostics.get("V_annulus", 0.0),
            inputs.get("dc", 0.0),
            inputs.get("dh", 0.0),
            diagnostics.get("n_a", 0.0),
            context="open_hole"
        )
    )

    # -----------------------------------------------------
    # Reynolds Numbers
    # -----------------------------------------------------
    diagnostics.update(
        evaluate_reynolds(
            data={
                "drill_pipe": inputs.get("drill_pipe", []),
                "drill_collar": inputs.get("drill_collar", []),
                "casing": inputs.get("casing", []),
                "bit": inputs.get("bit", []),
            },
            depth=inputs.get("Dmd", 0.0),
            v_pipe_ftmin=diagnostics.get("velocity_drillstring_avg", 0.0),
            v_annulus_ftmin=diagnostics.get("V_annulus", 0.0),
            mu_pipe_cp=diagnostics.get("mu", 0.0),
            mu_annulus_cp=diagnostics.get("mu_eff_annulus", 0.0),
            n_s=diagnostics.get("n", 0.0),
            n_a=diagnostics.get("n_a", 0.0),
            rho_lbgal=inputs.get("rho", 0.0),
        )
    )

    # -----------------------------------------------------
    # Audit Trail
    # -----------------------------------------------------
    diagnostics["audit_raw_inputs"] = inputs
    diagnostics["timestamp"] = datetime.now().isoformat()

    # -----------------------------------------------------
    # Return only keys defined in OutputData
    # -----------------------------------------------------
    return OutputData(
        **{k: v for k, v in diagnostics.items() if k in OutputData.__annotations__}
    )
