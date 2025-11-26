import math

# -----------------------------
# Average Maximum Speed of Pipe Movement
# -----------------------------
def swab_surge_average_max_pipe_speed(
    pipe_length_ft: float,
    time_seconds: float
) -> dict:
    if pipe_length_ft is None or pipe_length_ft <= 0:
        return {"Vp": 0.0}
    if time_seconds is None or time_seconds <= 0:
        return {"Vp": 0.0}

    Vp = (90.0 * pipe_length_ft) / time_seconds
    return {"Vp": Vp}


# -----------------------------
# Equivalent Fluid Velocity
# -----------------------------
def swab_surge_equivalent_fluid_velocity(
    pipe_velocity_ftmin: float,
    inner_diameter_in: float,
    outer_diameter_in: float,
    context: str = "open_hole"
) -> dict:
    if pipe_velocity_ftmin is None or pipe_velocity_ftmin <= 0:
        return {"Ve": 0.0}
    if inner_diameter_in is None or inner_diameter_in <= 0:
        return {"Ve": 0.0}
    if outer_diameter_in is None or outer_diameter_in <= inner_diameter_in:
        return {"Ve": 0.0}
    if context not in {"open_hole", "cased_hole"}:
        return {"Ve": 0.0}

    ratio = inner_diameter_in ** 2 / (outer_diameter_in ** 2 - inner_diameter_in ** 2)
    Ve = pipe_velocity_ftmin * (0.45 + ratio)
    return {"Ve": Ve}


# -----------------------------
# Effective Viscosity in Annulus
# -----------------------------
def swab_surge_effective_viscosity_annulus(
    Ve_ft_per_min: float,
    k_a: float,
    n_a: float,
    d1_in: float,
    d2_in: float,
    context: str = "open_hole"
) -> dict:
    if Ve_ft_per_min is None or Ve_ft_per_min <= 0:
        return {"mu": 0.0}
    if k_a is None or k_a <= 0:
        return {"mu": 0.0}
    if n_a is None or n_a <= 0:
        return {"mu": 0.0}
    if d1_in is None or d1_in <= 0:
        return {"mu": 0.0}
    if d2_in is None or d2_in <= d1_in:
        return {"mu": 0.0}
    if context not in {"open_hole", "cased_hole"}:
        return {"mu": 0.0}

    term = (144 * Ve_ft_per_min) / (60 * (d2_in - d1_in))
    mu = 100 * k_a * (term ** (n_a - 1))
    return {"mu": mu}


# -----------------------------
# Reynolds Number in Annulus
# -----------------------------
def swab_surge_reynolds_number_annulus(
    Ve_ft_per_min: float,
    d1_in: float,
    d2_in: float,
    mud_weight_lb_per_gal: float,
    viscosity_cp: float,
    n_a: float,
    context: str = "open_hole"
) -> dict:
    if Ve_ft_per_min is None or Ve_ft_per_min <= 0:
        return {"Re": 0.0}
    if d1_in is None or d1_in <= 0:
        return {"Re": 0.0}
    if d2_in is None or d2_in <= d1_in:
        return {"Re": 0.0}
    if mud_weight_lb_per_gal is None or mud_weight_lb_per_gal <= 0:
        return {"Re": 0.0}
    if viscosity_cp is None or viscosity_cp <= 0:
        return {"Re": 0.0}
    if n_a is None or n_a <= 0:
        return {"Re": 0.0}
    if context not in {"open_hole", "cased_hole"}:
        return {"Re": 0.0}

    hydraulic_diameter = d2_in - d1_in
    correction = ((2 * n_a + 1) / (3 * n_a)) ** n_a
    Re = (928 * Ve_ft_per_min * hydraulic_diameter * mud_weight_lb_per_gal) / (60 * viscosity_cp * correction)
    return {"Re": Re}


# -----------------------------
# Critical Reynolds Numbers
# -----------------------------
def swab_surge_critical_reynolds_numbers(
    n: float
) -> dict:
    if n is None or n <= 0:
        return {"Re_min": 0.0, "Re_max": 0.0}

    Re_min = 3470 - 1370 * n
    Re_max = 4270 - 1370 * n
    return {"Re_min": Re_min, "Re_max": Re_max}


# -----------------------------
# Fanning Friction Factor
# -----------------------------
def swab_surge_fanning_friction_laminar(Re: float) -> dict:
    if Re is None or Re <= 0:
        return {"f": 0.0}
    return {"f": 24.0 / Re}


def swab_surge_fanning_friction_transitional(
    Re: float,
    Re_min: float,
    Re_max: float,
    n_a: float
) -> dict:
    if any(x is None or x <= 0 for x in [Re, Re_min, Re_max, n_a]):
        return {"f": 0.0}

    log_na = math.log10(n_a)
    bracket = (1.75 - log_na) / 7.0
    if bracket == 0.0:
        return {"f": 0.0}

    term_core = (log_na + 3.93) / (50.0 * Re_max * bracket)
    term_lam = 24.0 / Re_min
    f = ((Re - Re_min) / 800.0) * (term_core - term_lam) + term_lam
    return {"f": f if f > 0.0 else 0.0}


def swab_surge_fanning_friction_turbulent(
    Re: float,
    n_a: float
) -> dict:
    if Re is None or Re <= 0 or n_a is None or n_a <= 0:
        return {"f": 0.0}

    log_na = math.log10(n_a)
    bracket = (1.75 - log_na) / 7.0
    if bracket == 0.0:
        return {"f": 0.0}

    f = (log_na + 3.93) / (50.0 * Re * bracket)
    return {"f": f if f > 0.0 else 0.0}


# -----------------------------
# Pressure Loss Gradient in Annulus
# -----------------------------
def swab_surge_pressure_loss_gradient_annulus(
    f: float,
    velocity_ft_per_min: float,
    mud_weight_lb_per_gal: float,
    d1_in: float,
    d2_in: float
) -> dict:
    if f is None or f <= 0:
        return {"dp_L": 0.0}
    if velocity_ft_per_min is None or velocity_ft_per_min <= 0:
        return {"dp_L": 0.0}
    if mud_weight_lb_per_gal is None or mud_weight_lb_per_gal <= 0:
        return {"dp_L": 0.0}
    if d1_in is None or d1_in <= 0:
        return {"dp_L": 0.0}
    if d2_in is None or d2_in <= d1_in:
        return {"dp_L": 0.0}

    velocity_term = (velocity_ft_per_min / 60.0) ** 2
    density_term = mud_weight_lb_per_gal / (25.81 * (d2_in - d1_in))
    dp_L = f * velocity_term * density_term
    return {"dp_L": dp_L}


# -----------------------------
# Pressure Loss Between Drill Pipe and Casing
# -----------------------------
def swab_surge_pressure_loss_between_drill_pipe_and_casing(
    gradient_psi_per_ft: float,
    casing_length_ft: float
) -> dict:
    if gradient_psi_per_ft is None or gradient_psi_per_ft < 0:
        return {"dp_dpc": 0.0}
    if casing_length_ft is None or casing_length_ft <= 0:
        return {"dp_dpc": 0.0}

    dp_dpc = gradient_psi_per_ft * casing_length_ft
    return {"dp_dpc": dp_dpc}


# -----------------------------
# Pressure Loss Between Drill Pipe and Open Hole
# -----------------------------
def swab_surge_pressure_loss_between_drill_pipe_and_open_hole(
    gradient_psi_per_ft: float,
    drill_pipe_length_ft: float,
    casing_length_ft: float
) -> dict:
    if gradient_psi_per_ft is None or gradient_psi_per_ft < 0:
        return {"dp_dph": 0.0}
    if drill_pipe_length_ft is None or drill_pipe_length_ft <= 0:
        return {"dp_dph": 0.0}
    if casing_length_ft is None or casing_length_ft < 0 or drill_pipe_length_ft <= casing_length_ft:
        return {"dp_dph": 0.0}

    open_hole_length = drill_pipe_length_ft - casing_length_ft
    dp_dph = gradient_psi_per_ft * open_hole_length
    return {"dp_dph": dp_dph}


# -----------------------------
# Pressure Loss Between Drill Collar and Open Hole
# -----------------------------
def swab_surge_pressure_loss_between_drill_collar_and_open_hole(
    gradient_psi_per_ft: float,
    drill_collar_length_ft: float
) -> dict:
    if gradient_psi_per_ft is None or gradient_psi_per_ft < 0:
        return {"dp_dch": 0.0}
    if drill_collar_length_ft is None or drill_collar_length_ft <= 0:
        return {"dp_dch": 0.0}

    dp_dch = gradient_psi_per_ft * drill_collar_length_ft
    return {"dp_dch": dp_dch}


# -----------------------------
# Gel-Breaking Pressure
# -----------------------------
def swab_surge_gel_breaking_pressure(
    length_ft: float,
    gel_strength_lbf_per_100ft2: float,
    d1_in: float,
    d2_in: float
) -> dict:
    if length_ft is None or length_ft <= 0:
        return {"Pg": 0.0}
    if gel_strength_lbf_per_100ft2 is None or gel_strength_lbf_per_100ft2 <= 0:
        return {"Pg": 0.0}
    if d1_in is None or d1_in <= 0:
        return {"Pg": 0.0}
    if d2_in is None or d2_in <= d1_in:
        return {"Pg": 0.0}

    Pg = (4.0 * length_ft * gel_strength_lbf_per_100ft2) / (1200.0 * (d2_in - d1_in))
    return {"Pg": Pg}


# -----------------------------
# Equivalent Mud Weight (Swab or Surge)
# -----------------------------
def swab_equivalent_mud_weight(
    base_mud_weight_ppg: float,
    delta_p_total_psi: float,
    tvd_ft: float
) -> dict:
    if base_mud_weight_ppg is None or base_mud_weight_ppg <= 0:
        return {"rhoe_swab": 0.0}
    if delta_p_total_psi is None or delta_p_total_psi < 0:
        return {"rhoe_swab": 0.0}
    if tvd_ft is None or tvd_ft <= 0:
        return {"rhoe_swab": 0.0}

    rhoe_swab = base_mud_weight_ppg - (delta_p_total_psi / (0.052 * tvd_ft))
    return {"rhoe_swab": rhoe_swab}


def surge_equivalent_mud_weight(
    base_mud_weight_ppg: float,
    delta_p_total_psi: float,
    tvd_ft: float
) -> dict:
    if base_mud_weight_ppg is None or base_mud_weight_ppg <= 0:
        return {"rhoe_surge": 0.0}
    if delta_p_total_psi is None or delta_p_total_psi < 0:
        return {"rhoe_surge": 0.0}
    if tvd_ft is None or tvd_ft <= 0:
        return {"rhoe_surge": 0.0}

    rhoe_surge = base_mud_weight_ppg + (delta_p_total_psi / (0.052 * tvd_ft))
    return {"rhoe_surge": rhoe_surge}
