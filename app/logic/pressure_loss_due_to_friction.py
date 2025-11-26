# -----------------------------
# Pressure Loss by Component (Imperial)
# -----------------------------

def pressure_loss_due_to_friction_pipe(gradient_dp: float, length_dp: float) -> dict:
    """
    Total pressure loss due to friction inside the drill pipe [psi].

    Equation:
        dPdp = gradient_dp * length_dp
    """
    if not gradient_dp or gradient_dp < 0 or not length_dp or length_dp <= 0:
        return {"dPdp": 0.0}
    dPdp = gradient_dp * length_dp
    return {"dPdp": dPdp}


def pressure_loss_due_to_friction_collar(gradient_dc: float, length_dc: float) -> dict:
    """
    Total pressure loss due to friction inside the drill collar [psi].

    Equation:
        dPdc = gradient_dc * length_dc
    """
    if not gradient_dc or gradient_dc < 0 or not length_dc or length_dc <= 0:
        return {"dPdc": 0.0}
    dPdc = gradient_dc * length_dc
    return {"dPdc": dPdc}


def pressure_loss_due_to_friction_pipe_casing_annulus(
    gradient_dpch: float,
    length_c: float
) -> dict:
    """
    Total pressure loss in the pipe–casing annulus [psi].

    Equation:
        dPdpc = gradient_dpch * length_c
    """
    if gradient_dpch is None or gradient_dpch < 0 or length_c is None or length_c <= 0:
        return {"dPdpc": 0.0}
    dPdpc = gradient_dpch * length_c
    return {"dPdpc": dPdpc}


def pressure_loss_due_to_friction_pipe_open_hole_annulus(
    gradient_dpoh: float,
    length_dp: float,
    length_c: float
) -> dict:
    """
    Total pressure loss between drill pipe and open hole [psi].

    Equation:
        dPdph = gradient_dpoh * (length_dp - length_c)
    """
    if not gradient_dpoh or gradient_dpoh < 0:
        return {"dPdph": 0.0}
    if not length_dp or length_dp <= 0 or length_c is None or length_c < 0:
        return {"dPdph": 0.0}

    effective_length = length_dp - length_c
    if effective_length <= 0:
        return {"dPdph": 0.0}

    dPdph = gradient_dpoh * effective_length
    return {"dPdph": dPdph}


def pressure_loss_due_to_friction_collar_open_hole_annulus(
    gradient_dcoh: float,
    length_dc: float
) -> dict:
    """
    Total pressure loss between drill collar and open hole [psi].

    Equation:
        dPdch = gradient_dcoh * length_dc
    """
    if gradient_dcoh is None or gradient_dcoh < 0:
        return {"dPdch": 0.0}
    if length_dc is None or length_dc <= 0:
        return {"dPdch": 0.0}

    dPdch = gradient_dcoh * length_dc
    return {"dPdch": dPdch}


def pressure_loss_due_to_friction_segment(
    gradient_per_ft: float,
    length_ft: float
) -> dict:
    """
    Converts a pressure loss gradient [psi/ft] into total pressure loss [psi].

    Equation:
        dp = gradient_per_ft * length_ft
    """
    if gradient_per_ft is None or gradient_per_ft <= 0 or length_ft is None or length_ft <= 0:
        return {"dp": 0.0}

    return {"dp": gradient_per_ft * length_ft}


# -----------------------------
# Drillstring Wrappers (Imperial)
# -----------------------------

def pressure_loss_gradient_drill_pipe_open_hole(gradient_dpoh: float, length_dpoh: float) -> dict:
    """Total pressure loss for drill pipe in open hole annulus [psi]."""
    if not gradient_dpoh or gradient_dpoh < 0 or not length_dpoh or length_dpoh <= 0:
        return {"dp": 0.0}
    dp = gradient_dpoh * length_dpoh
    return {"dp": dp}


def pressure_loss_gradient_drillstring(
    gradient_dp: float, length_dp: float,
    gradient_dc: float, length_dc: float
) -> dict:
    """
    Wrapper: total pressure loss across the drillstring (pipe + collar).
    """
    dp_loss = pressure_loss_due_to_friction_segment(gradient_dp, length_dp).get("dp", 0.0)
    dc_loss = pressure_loss_due_to_friction_segment(gradient_dc, length_dc).get("dp", 0.0)
    return {"dp": dp_loss + dc_loss}


def pressure_loss_gradient_drillstring_open_hole_annulus(
    gradient_dpoh: float, length_dpoh: float,
    gradient_dcoh: float, length_dcoh: float
) -> dict:
    """
    Wrapper: total pressure loss in the open hole annulus (drill pipe + drill collar).
    """
    dp_open_hole_loss = pressure_loss_due_to_friction_segment(gradient_dpoh, length_dpoh).get("dp", 0.0)
    dc_open_hole_loss = pressure_loss_due_to_friction_segment(gradient_dcoh, length_dcoh).get("dp", 0.0)
    return {"dp": dp_open_hole_loss + dc_open_hole_loss}


# -----------------------------
# Equivalent Circulating Density (Imperial)
# -----------------------------

def equivalent_circulating_density(
    rho_lbgal: float,
    dp_casing_annulus: float,
    dp_open_hole_annulus: float,
    dc_open_hole_annulus: float,
    tvd_ft: float
) -> dict:
    """
    Eq-28: Equivalent Circulating Density (ECD) in lb/gal.

    Equation:
        ECD = rho + (dp_dpch + dp_dpoh + dp_dcoh) / (0.052 * TVD)
    """
    if (
        rho_lbgal is None or rho_lbgal <= 0 or
        tvd_ft is None or tvd_ft <= 0
    ):
        return {"ECD": 0.0}

    friction_total = (
        (dp_casing_annulus or 0.0) +
        (dp_open_hole_annulus or 0.0) +
        (dc_open_hole_annulus or 0.0)
    )

    ECD = rho_lbgal + (friction_total / (0.052 * tvd_ft))
    return {"ECD": round(ECD, 3)}
