import math
from typing import Literal

# -----------------------------
# Velocity Calculations
# -----------------------------

def annularhydraulics_flow_velocity_pipe(
    flow_rate_gpm: float,
    pipe_id_in: float
) -> dict:
    """
    Computes fluid velocity inside pipe [ft/min] for annular hydraulics.

    Formula:
        V = (24.51 × Q) / d²

    Inputs:
        flow_rate_gpm : float
            Flow rate [gpm].
        pipe_id_in : float
            Pipe inside diameter [in].

    Output:
        dict with key 'V_pipe' representing velocity [ft/min].
    """
    if flow_rate_gpm <= 0 or pipe_id_in <= 0:
        return {"V_pipe": 0.0}

    V_pipe = (24.51 * flow_rate_gpm) / (pipe_id_in ** 2)
    return {"V_pipe": V_pipe}


def annularhydraulics_flow_velocity_collar(
    flow_rate_gpm: float,
    collar_id_in: float
) -> dict:
    """
    Computes fluid velocity inside collar [ft/min] for annular hydraulics.

    Formula:
        V = (24.51 × Q) / d²

    Inputs:
        flow_rate_gpm : float
            Flow rate [gpm].
        collar_id_in : float
            Collar inside diameter [in].

    Output:
        dict with key 'V_collar' representing velocity [ft/min].
    """
    if flow_rate_gpm <= 0 or collar_id_in <= 0:
        return {"V_collar": 0.0}

    V_collar = (24.51 * flow_rate_gpm) / (collar_id_in ** 2)
    return {"V_collar": V_collar}


def annularhydraulics_flow_velocity_annulus(
    flow_rate_gpm: float,
    d1_od_in: float,
    d2_od_in: float,
    context: str = "open_hole"
) -> dict:
    """
    Computes fluid velocity inside the annulus [ft/min] for open hole or cased hole.

    Formula:
        V = (24.51 × Q) / (d2² − d1²)

    Inputs:
        flow_rate_gpm : float
            Flow rate [gpm].
        d1_od_in : float
            Outer diameter of pipe or collar [in].
        d2_od_in : float
            Bit OD (open hole) or casing ID (cased hole) [in].
        context : str
            Either 'open_hole' or 'cased_hole'.

    Output:
        dict with key 'V_annulus' representing velocity [ft/min].
    """
    if flow_rate_gpm <= 0 or d1_od_in <= 0 or d2_od_in <= d1_od_in:
        return {"V_annulus": 0.0}
    if context not in {"open_hole", "cased_hole"}:
        return {"V_annulus": 0.0}

    V_annulus = (24.51 * flow_rate_gpm) / (d2_od_in ** 2 - d1_od_in ** 2)
    return {"V_annulus": V_annulus}


def annularhydraulics_velocity_drillstring_avg(
    flow_rate_gpm: float,
    area_sqft: float
) -> dict:
    """
    Computes average fluid velocity inside drillstring [ft/min] using volumetric flow and area.

    Formula:
        V = (Q × 0.133681) / A

    Inputs:
        flow_rate_gpm : float
            Flow rate [gpm].
        area_sqft : float
            Cross-sectional area [ft²].

    Output:
        dict with key 'velocity_drillstring_avg' [ft/min].
    """
    if flow_rate_gpm <= 0 or area_sqft <= 0:
        return {"velocity_drillstring_avg": 0.0}

    q_cuftmin = flow_rate_gpm * 0.133681
    return {"velocity_drillstring_avg": q_cuftmin / area_sqft}


# -----------------------------
# Rheology Calculations
# -----------------------------

def powerlaw_constants_n_string(
    phi600: float,
    phi300: float
) -> dict:
    """
    Computes flow behavior index 'n' in the string using viscometer readings.

    Formula:
        n_s = 3.32 × log10(phi600 / phi300)

    Inputs:
        phi600 : float
            Viscometer reading at 600 RPM.
        phi300 : float
            Viscometer reading at 300 RPM.

    Output:
        dict with key 'n_s' representing flow behavior index.
    """
    if phi600 <= 0 or phi300 <= 0:
        return {"n_s": 0.0}

    n_s = 3.32 * math.log10(phi600 / phi300)
    return {"n_s": n_s}


def powerlaw_constants_k_string(
    phi600: float,
    n_s: float
) -> dict:
    """
    Computes consistency index 'k' in the string [P] using viscometer reading and flow behavior index.

    Formula:
        k_s = (5.11 × phi600) / (1022^n_s)

    Inputs:
        phi600 : float
            Viscometer reading at 600 RPM.
        n_s : float
            Flow behavior index in the string.

    Output:
        dict with key 'k_s' representing consistency index [P].
    """
    if phi600 <= 0 or n_s <= 0:
        return {"k_s": 0.0}

    k_s = (5.11 * phi600) / (1022 ** n_s)
    return {"k_s": k_s}


def powerlaw_constants_n_annulus(
    phi300: float,
    phi3: float
) -> dict:
    """
    Computes flow behavior index 'n' in the annulus using viscometer readings.

    Formula:
        n_a = 0.5 × log10(phi300 / phi3)

    Inputs:
        phi300 : float
            Viscometer reading at 300 RPM.
        phi3 : float
            Viscometer reading at 3 RPM.

    Output:
        dict with key 'n_a' representing flow behavior index.
    """
    if phi300 <= 0 or phi3 <= 0:
        return {"n_a": 0.0}

    n_a = 0.5 * math.log10(phi300 / phi3)
    return {"n_a": n_a}


def powerlaw_constants_k_annulus(
    phi300: float,
    n_a: float
) -> dict:
    """
    Computes consistency index 'k' in the annulus [P] using viscometer reading and flow behavior index.

    Formula:
        k_a = (5.11 × phi300) / (511^n_a)

    Inputs:
        phi300 : float
            Viscometer reading at 300 RPM.
        n_a : float
            Flow behavior index in the annulus.

    Output:
        dict with key 'k_a' representing consistency index [P].
    """
    if phi300 <= 0 or n_a <= 0:
        return {"k_a": 0.0}

    k_a = (5.11 * phi300) / (511 ** n_a)
    return {"k_a": k_a}


# -----------------------------
# Effective Viscosity
# -----------------------------

def effective_viscosity_drillpipe_drillcollar(
    k_s: float,
    velocity_ftmin: float,
    id_in: float,
    n_s: float
) -> dict:
    """
    Computes effective viscosity [cP] inside drill pipe or drill collar using Eq‑7.

    Formula:
        mu = 100 * k_s × [96 * v / (60 * d)]^(n_s − 1)

    Inputs:
        k_s : float
            Consistency index in the string [P].
        velocity_ftmin : float
            Fluid velocity [ft/min].
        id_in : float
            Inside diameter of pipe or collar [in].
        n_s : float
            Flow behavior index in the string.

    Output:
        dict with key 'mu_eff_pipe_collar' representing effective viscosity [cP].
    """
    if k_s <= 0 or velocity_ftmin <= 0 or id_in <= 0 or n_s <= 0:
        return {"mu_eff_pipe_collar": 0.0}

    shear_term = (96 * velocity_ftmin) / (60 * id_in)
    mu_eff = 100 * k_s * (shear_term ** (n_s - 1))
    return {"mu_eff_pipe_collar": mu_eff}


def effective_viscosity_drillstring(
    k_s: float,
    velocity_ftmin: float,
    pipe_id_in: float,
    collar_id_in: float,
    n_s: float
) -> dict:
    """
    Effective viscosity inside drillstring (pipe/collar ID).

    Formula basis (Power Law):
        mu_eff = k_s × (gamma_dot)^(n_s - 1)

    Shear rate approximation:
        gamma_dot ≈ (8 × V) / D

    Inputs:
        k_s : float
            Drillstring consistency index.
        velocity_ftmin : float
            Average velocity inside drillstring [ft/min].
        pipe_id_in : float
            Drill pipe inner diameter [in].
        collar_id_in : float
            Drill collar inner diameter [in].
        n_s : float
            Drillstring flow behavior index.

    Output:
        dict with key 'mu' representing effective viscosity [cP].
    """
    if (
        k_s is None or k_s <= 0 or
        velocity_ftmin is None or velocity_ftmin <= 0 or
        pipe_id_in is None or pipe_id_in <= 0 or
        collar_id_in is None or collar_id_in <= 0 or
        n_s is None or n_s <= 0
    ):
        return {"mu": 0.0}

    # Use the smaller ID (pipe or collar) as controlling diameter
    d_in = min(pipe_id_in, collar_id_in)

    # Convert velocity from ft/min → in/s
    velocity_ins = velocity_ftmin * 12.0 / 60.0

    # Shear rate [1/s]
    shear_rate = (8.0 * velocity_ins) / d_in

    mu_eff = k_s * (shear_rate ** (n_s - 1))
    return {"mu": mu_eff}


def effective_viscosity_inside_annulus_openhole_casedhole(
    k_a: float,
    velocity_ftmin: float,
    d1_od_in: float,
    d2_od_in: float,
    n_a: float,
    context: str
) -> dict:
    """
    Computes effective viscosity [cP] inside the annulus for open hole or cased hole using Eq‑8.

    Formula:
        mu = 100 * k_a × [144 * v / (60 * (d2 − d1))]^(n_a − 1)

    Inputs:
        k_a : float
            Consistency index in the annulus [P].
        velocity_ftmin : float
            Fluid velocity [ft/min].
        d1_od_in : float
            Outer diameter of pipe or collar [in].
        d2_od_in : float
            Bit OD (open hole) or casing ID (cased hole) [in].
        n_a : float
            Flow behavior index in the annulus.
        context : str
            Must be either 'open_hole' or 'cased_hole'.

    Output:
        dict with keys:
            'mu_eff_annulus' → effective viscosity [cP]
            'context' → 'open_hole' or 'cased_hole'
    """
    if context not in {"open_hole", "cased_hole"}:
        return {"mu_eff_annulus": 0.0, "context": "invalid"}

    if k_a <= 0 or velocity_ftmin <= 0 or d1_od_in <= 0 or d2_od_in <= d1_od_in or n_a <= 0:
        return {"mu_eff_annulus": 0.0, "context": context}

    shear_term = (144 * velocity_ftmin) / (60 * (d2_od_in - d1_od_in))
    mu_eff = 100 * k_a * (shear_term ** (n_a - 1))
    return {"mu_eff_annulus": mu_eff, "context": context}


# -----------------------------
# Reynolds Number & Corrections
# -----------------------------

def correction_string(n: float) -> float:
    return ((3 * n + 1) / (4 * n)) ** n if n > 0 else 0.0


def correction_annulus(n: float) -> float:
    return ((2 * n + 1) / (3 * n)) ** n if n > 0 else 0.0


def reynolds_number_pipe_collar(
    v_ftmin: float,
    pipe_id_in: float,
    collar_id_in: float,
    mu_cp: float,
    n_s: float,
    rho_lbgal: float
) -> dict:
    """
    Computes Reynolds Number inside drill pipe or drill collar using Eq‑9.

    Formula:
        Re = [928 × v × d × rho] / [60 × mu × ((3n + 1)/(4n))^n]

    Inputs:
        v_ftmin : float
            Fluid velocity [ft/min].
        pipe_id_in : float
            Pipe inside diameter [in].
        collar_id_in : float
            Collar inside diameter [in].
        mu_cp : float
            Effective viscosity [cP].
        n_s : float
            Flow behavior index in the string.
        rho_lbgal : float
            Fluid density [lb/gal].

    Output:
        dict with key 'Re_pipe_collar' representing Reynolds Number (dimensionless).
    """
    d = collar_id_in if collar_id_in and collar_id_in > 0 else pipe_id_in
    if d <= 0 or v_ftmin <= 0 or mu_cp <= 0 or n_s <= 0 or rho_lbgal <= 0:
        return {"Re_pipe_collar": 0.0}

    correction = ((3 * n_s + 1) / (4 * n_s)) ** n_s
    Re = (928 * v_ftmin * d * rho_lbgal) / (60 * mu_cp * correction)
    return {"Re_pipe_collar": Re}


def reynolds_number_annulus(
    v_ftmin: float,
    hole_config: Literal["open_hole", "cased_hole"],
    pipe_od_in: float,
    collar_od_in: float,
    bit_od_in: float,
    casing_id_in: float,
    mu_cp: float,
    n_a: float,
    rho_lbgal: float
) -> dict:
    """
    Computes Reynolds Number inside the annulus using Eq‑10.

    Formula:
        Re = [928 × v × (d2 − d1) × rho] /
             [60 × mu × ((2n_a + 1)/(3n_a))^n_a]
    """
    if hole_config == "open_hole":
        d1 = max(pipe_od_in, collar_od_in)
        d2 = bit_od_in
    elif hole_config == "cased_hole":
        d1 = pipe_od_in
        d2 = casing_id_in
    else:
        return {"Re_annulus": 0.0}

    Dh = d2 - d1
    if Dh <= 0 or v_ftmin <= 0 or mu_cp <= 0 or n_a <= 0 or rho_lbgal <= 0:
        return {"Re_annulus": 0.0}

    correction = ((2 * n_a + 1) / (3 * n_a)) ** n_a
    Re = (928 * v_ftmin * Dh * rho_lbgal) / (60 * mu_cp * correction)
    return {"Re_annulus": Re}


def critical_reynolds_number_string_annulus_min(n: float) -> dict:
    """
    Computes minimum critical Reynolds Number using Eq‑11.

    Formula:
        Re_min = 3470 − 1370n

    Input:
        n : float
            Flow behavior index (n_s for string or n_a for annulus).

    Output:
        dict with key 'Re_crit_min' representing minimum critical Reynolds Number.
    """
    if n <= 0:
        return {"Re_crit_min": 0.0}

    Re_min = 3470 - 1370 * n
    return {"Re_crit_min": Re_min}


def critical_reynolds_number_string_annulus_max(n: float) -> dict:
    """
    Computes maximum critical Reynolds Number using Eq‑12.

    Formula:
        Re_max = 4270 − 1370n

    Input:
        n : float
            Flow behavior index (n_s for string or n_a for annulus).

    Output:
        dict with key 'Re_crit_max' representing maximum critical Reynolds Number.
    """
    if n <= 0:
        return {"Re_crit_max": 0.0}

    Re_max = 4270 - 1370 * n
    return {"Re_crit_max": Re_max}


def evaluate_reynolds(
    data: dict,
    depth: float,
    v_pipe_ftmin: float,
    v_annulus_ftmin: float,
    mu_pipe_cp: float,
    mu_annulus_cp: float,
    n_s: float,
    n_a: float,
    rho_lbgal: float
) -> dict:
    """
    Orchestrates Reynolds Number evaluation for both pipe/collar (Eq‑9) and annulus (Eq‑10).

    Delegates to:
        - reynolds_number_pipe_collar()
        - reynolds_number_annulus()

    Inputs:
        data : dict
            Geometry data containing drill pipe, drill collar, casing, bit info.
        depth : float
            Current depth [ft] (not used in formula, but kept for context).
        v_pipe_ftmin : float
            Fluid velocity inside pipe [ft/min].
        v_annulus_ftmin : float
            Fluid velocity inside annulus [ft/min].
        mu_pipe_cp : float
            Effective viscosity inside pipe [cP].
        mu_annulus_cp : float
            Effective viscosity inside annulus [cP].
        n_s : float
            Flow behavior index in the string.
        n_a : float
            Flow behavior index in the annulus.
        rho_lbgal : float
            Fluid density [lb/gal].

    Output:
        dict with keys:
            'Re_pipe_collar' → Reynolds Number inside pipe/collar
            'Re_annulus' → Reynolds Number inside annulus
    """
    if not rho_lbgal or rho_lbgal <= 0:
        return {"Re_pipe_collar": 0.0, "Re_annulus": 0.0}

    # Pipe/collar ID
    pipe_id_in = None
    collar_id_in = None
    if data.get("drill_collar"):
        collar_id_in = data["drill_collar"][0].get("id")
    if data.get("drill_pipe"):
        pipe_id_in = data["drill_pipe"][0].get("id")

    # Annulus geometry
    pipe_od_in = None
    bit_od_in = None
    casing_id_in = None
    if data.get("drill_pipe"):
        pipe_od_in = data["drill_pipe"][0].get("od")
    if data.get("bit"):
        bit_od_in = data["bit"][0].get("od")
    if data.get("casing"):
        casing_id_in = data["casing"][0].get("id")

    Re_pipe = reynolds_number_pipe_collar(
        v_pipe_ftmin, pipe_id_in or 0.0, collar_id_in or 0.0,
        mu_pipe_cp, n_s, rho_lbgal
    )["Re_pipe_collar"]

    Re_annulus = reynolds_number_annulus(
        v_annulus_ftmin,
        "open_hole" if bit_od_in else "cased_hole",
        pipe_od_in or 0.0,
        collar_id_in or 0.0,
        bit_od_in or 0.0,
        casing_id_in or 0.0,
        mu_annulus_cp,
        n_a,
        rho_lbgal
    )["Re_annulus"]

    return {"Re_pipe_collar": Re_pipe, "Re_annulus": Re_annulus}


# -----------------------------
# Critical Reynolds & Flow Regime
# -----------------------------

def critical_reynolds(n: float) -> tuple[float, float]:
    """
    Calculate critical Reynolds numbers for laminar → transitional → turbulent boundaries.
    Returns (Re_min, Re_max).
    """
    if n <= 0:
        return (0.0, 0.0)
    Re_min = 2100 * (n + 1) / (3 * n)
    Re_max = 4000 * (n + 1) / (3 * n)
    return (Re_min, Re_max)


def classify_flow(Re: float, Re_min: float, Re_max: float) -> str:
    """
    Classify flow regime based on Reynolds number and critical thresholds.
    Returns one of: 'invalid', 'laminar', 'transitional', 'turbulent'.
    """
    if Re <= 0:
        return "invalid"
    if Re < Re_min:
        return "laminar"
    elif Re_min <= Re <= Re_max:
        return "transitional"
    else:
        return "turbulent"
