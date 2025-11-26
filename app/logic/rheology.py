# -----------------------------
# Annular Critical Velocity & Flow Rate (Imperial)
# -----------------------------

def calculate_annular_critical_velocity(Re_min: float, k_a: float, n_a: float,
                                        rho_lbgal: float, d1_in: float, d2_in: float) -> dict:
    """
    Eq-13: Annular Critical Velocity [ft/min]
    Returns dict keyed by canonical OutputData symbol 'Vcrit'.
    """
    if not Re_min or Re_min <= 0 or not k_a or k_a <= 0 or not n_a or n_a <= 0 \
       or not rho_lbgal or rho_lbgal <= 0 or not d1_in or d1_in <= 0 or not d2_in or d2_in <= d1_in \
       or n_a == 2:
        return {"Vcrit": 0.0}

    dh = d2_in - d1_in
    rheology_term = ((2 * n_a + 1) / (3 * n_a)) ** n_a
    geometry_term = 144 ** (1 - n_a)

    numerator = 100 * Re_min * k_a * rheology_term
    denominator = 928 * rho_lbgal * dh * geometry_term

    Vcrit = 60 * (numerator / denominator) ** (1 / (2 - n_a))
    return {"Vcrit": Vcrit}


def calculate_annular_critical_flow_rate(v_crit_ftmin: float, d1_in: float, d2_in: float) -> dict:
    """
    Eq-14: Annular Critical Flow Rate [gal/min]
    Returns dict keyed by canonical OutputData symbol 'Qcrit'.
    """
    if not v_crit_ftmin or v_crit_ftmin <= 0 or not d1_in or d1_in <= 0 or not d2_in or d2_in <= d1_in:
        return {"Qcrit": 0.0}

    Qcrit = (2.45 * v_crit_ftmin * (d2_in ** 2 - d1_in ** 2)) / 60
    return {"Qcrit": Qcrit}


def calculate_criticals(inputs: dict) -> dict:
    """
    Wrapper to compute annular critical velocity and flow rate.
    Expects casing diameter (dc), hole diameter (dh), rheology parameters (n_a, k_a),
    fluid density (rho), and Re_min from critical_reynolds(n).
    Returns dict with keys 'Vcrit' and 'Qcrit'.
    """
    d_casing = inputs.get("dc", 0.0)
    d_hole   = inputs.get("dh", 0.0)
    n_a      = inputs.get("n_a", 0.0)
    k_a      = inputs.get("k_a", 0.0)
    rho      = inputs.get("rho", 0.0)
    Re_min   = inputs.get("Re_min", 0.0)

    if not all([d_casing, d_hole, n_a, k_a, rho, Re_min]) or d_hole <= d_casing:
        return {"Vcrit": 0.0, "Qcrit": 0.0}

    # Critical velocity
    vcrit_dict = calculate_annular_critical_velocity(Re_min, k_a, n_a, rho, d_casing, d_hole)
    Vcrit = vcrit_dict.get("Vcrit", 0.0)

    # Critical flow rate
    qcrit_dict = calculate_annular_critical_flow_rate(Vcrit, d_casing, d_hole)
    Qcrit = qcrit_dict.get("Qcrit", 0.0)

    return {"Vcrit": Vcrit, "Qcrit": Qcrit}
