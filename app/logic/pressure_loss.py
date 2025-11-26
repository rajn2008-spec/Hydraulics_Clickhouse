# -----------------------------
# Pressure Loss Gradient (Imperial)
# -----------------------------

def pressure_loss_gradient_pipe_collar(
    f: float,
    v_ftmin: float,
    rho_lbgal: float,
    d_in: float
) -> dict:
    """
    Eq-21: Pressure loss gradient inside drill pipe or drill collar.

    Formula:
        dp_per_ft = f × (v/60)² × (rho / (25.81 × d))
    """
    if (
        f is None or f <= 0 or
        v_ftmin is None or v_ftmin <= 0 or
        rho_lbgal is None or rho_lbgal <= 0 or
        d_in is None or d_in <= 0
    ):
        return {"dp_per_ft": 0.0}

    dp_per_ft = f * (v_ftmin / 60.0) ** 2 * (rho_lbgal / (25.81 * d_in))
    return {"dp_per_ft": dp_per_ft}


def pressure_loss_gradient_annulus_open_cased_hole(
    f: float,
    v_ftmin: float,
    rho_lbgal: float,
    hole_type: str,
    pipe_od_in: float = 0.0,
    collar_od_in: float = 0.0,
    bit_od_in: float = 0.0,
    casing_id_in: float = 0.0
) -> dict:
    """
    Eq-22: Pressure loss gradient inside the annulus (open hole or cased hole).

    Formula:
        dp_per_ft = f × (v/60)² × (rho / (25.81 × (d2 − d1)))
    """
    if (
        f is None or f <= 0 or
        v_ftmin is None or v_ftmin <= 0 or
        rho_lbgal is None or rho_lbgal <= 0
    ):
        return {"dp_per_ft": 0.0}

    # Open hole case
    if hole_type.lower() == "open":
        if pipe_od_in <= 0 or collar_od_in <= 0 or bit_od_in <= 0:
            return {"dp_per_ft": 0.0}
        d1_in = max(pipe_od_in, collar_od_in)
        d2_in = bit_od_in

    # Cased hole case
    elif hole_type.lower() == "cased":
        if pipe_od_in <= 0 or casing_id_in <= 0:
            return {"dp_per_ft": 0.0}
        d1_in = pipe_od_in
        d2_in = casing_id_in

    else:
        return {"dp_per_ft": 0.0}

    if d2_in <= d1_in:
        return {"dp_per_ft": 0.0}

    dh_in = d2_in - d1_in
    dp_per_ft = f * (v_ftmin / 60.0) ** 2 * (rho_lbgal / (25.81 * dh_in))
    return {"dp_per_ft": dp_per_ft}
