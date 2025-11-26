# app/logic/bit_hydraulics.py

import math
from typing import List, Dict

# -----------------------------
# Unit helpers
# -----------------------------

def _gpm_to_cuft_per_min(gpm: float) -> float:
    # 1 gallon = 0.133681 ft^3
    return gpm * 0.133681 if gpm else 0.0

def _area_sqft_from_diameter_in(d_in: float) -> float:
    if not d_in or d_in <= 0:
        return 0.0
    return math.pi * (d_in / 2.0) ** 2 / 144.0

# -----------------------------
# Bit-level equations
# -----------------------------

def total_flow_area(jet_diameters_32nds: list[float]) -> dict:
    """
    Computes total flow area from a list of jet diameters measured in 1/32 inch units.

    Equation:
        A = (J₁² + J₂² + ... + Jₓ²) / 1303.8

    Inputs:
        jet_diameters_32nds : list of float
            Each value is a jet diameter in units of 1/32 inch.

    Output:
        dict with key 'A' representing total flow area in square inches.
    """
    if not jet_diameters_32nds or not all(j > 0 for j in jet_diameters_32nds):
        return {"A": 0.0}

    sum_of_squares = sum(j**2 for j in jet_diameters_32nds)
    A = sum_of_squares / 1303.8
    return {"A": A}

def jet_velocity(flow_rate_gpm: float, total_flow_area_in2: float) -> dict:
    """
    Computes jet velocity based on flow rate and total flow area.

    Equation:
        V_jet = (19.249 × Q) / A

    Inputs:
        flow_rate_gpm : float
            Volumetric flow rate [gal/min].
        total_flow_area_in2 : float
            Total flow area [in²].

    Output:
        dict with key 'V_jet' representing jet velocity [ft/min].
    """
    if flow_rate_gpm is None or flow_rate_gpm < 0:
        return {"V_jet": 0.0}
    if total_flow_area_in2 is None or total_flow_area_in2 <= 0:
        return {"V_jet": 0.0}

    V_jet = (19.249 * flow_rate_gpm) / total_flow_area_in2
    return {"V_jet": V_jet}

def pressure_loss_at_bit(
    mud_weight_lb_per_gal: float,
    flow_rate_gpm: float,
    total_flow_area_in2: float
) -> dict:
    """
    Computes pressure loss at the bit due to jet nozzle restriction [psi].

    Equation:
        Δpb = (156 × ρ × Q²) / (1303.8 × A)²

    Inputs:
        mud_weight_lb_per_gal : float
            Mud weight [lb/gal].
        flow_rate_gpm : float
            Flow rate [gal/min].
        total_flow_area_in2 : float
            Total flow area [in²].

    Output:
        dict with key 'Δpb' representing pressure loss at the bit [psi].
    """
    if (
        mud_weight_lb_per_gal is None or mud_weight_lb_per_gal <= 0 or
        flow_rate_gpm is None or flow_rate_gpm <= 0 or
        total_flow_area_in2 is None or total_flow_area_in2 <= 0
    ):
        return {"dpb": 0.0}

    denominator = (1303.8 * total_flow_area_in2) ** 2
    Δpb = (156 * mud_weight_lb_per_gal * flow_rate_gpm ** 2) / denominator
    return {"dpb": Δpb}


def hydraulic_power(
    flow_rate_gpm: float,
    pressure_loss_at_bit_psi: float
) -> dict:
    """
    Computes hydraulic power delivered to the bit [hp].

    Equation:
        P = (Q × Δpb) / 1714

    Inputs:
        flow_rate_gpm : float
            Flow rate [gal/min].
        pressure_loss_at_bit_psi : float
            Pressure loss at the bit [psi].

    Output:
        dict with key 'P' representing hydraulic power [hp].
    """
    if flow_rate_gpm is None or flow_rate_gpm <= 0:
        return {"P": 0.0}
    if pressure_loss_at_bit_psi is None or pressure_loss_at_bit_psi <= 0:
        return {"P": 0.0}

    P = (flow_rate_gpm * pressure_loss_at_bit_psi) / 1714
    return {"P": P}

def hydraulic_power_per_unit_area(
    hydraulic_power_hp: float,
    bit_diameter_in: float
) -> dict:
    """
    Computes hydraulic power per unit area [hp/in²].

    Equation:
        P_A = (1.2732 × P) / d_h²

    Inputs:
        hydraulic_power_hp : float
            Hydraulic power [hp].
        bit_diameter_in : float
            Bit outside diameter [in].

    Output:
        dict with key 'P_A' representing hydraulic power per unit area [hp/in²].
    """
    if hydraulic_power_hp is None or hydraulic_power_hp <= 0:
        return {"P_A": 0.0}
    if bit_diameter_in is None or bit_diameter_in <= 0:
        return {"P_A": 0.0}

    P_A = (1.2732 * hydraulic_power_hp) / (bit_diameter_in ** 2)
    return {"P_A": P_A}

def impact_force(
    mud_weight_lb_per_gal: float,
    flow_rate_gpm: float,
    jet_velocity_ft_per_min: float
) -> dict:
    """
    Computes impact force at the bit due to fluid exiting the jets [lbf].

    Equation:
        F_i = (ρ × Q × V_jet) / 115920

    Inputs:
        mud_weight_lb_per_gal : float
            Mud weight [lb/gal].
        flow_rate_gpm : float
            Flow rate [gal/min].
        jet_velocity_ft_per_min : float
            Jet velocity [ft/min].

    Output:
        dict with key 'F_i' representing impact force [lbf].
    """
    if (
        mud_weight_lb_per_gal is None or mud_weight_lb_per_gal <= 0 or
        flow_rate_gpm is None or flow_rate_gpm <= 0 or
        jet_velocity_ft_per_min is None or jet_velocity_ft_per_min <= 0
    ):
        return {"F_i": 0.0}

    F_i = (mud_weight_lb_per_gal * flow_rate_gpm * jet_velocity_ft_per_min) / 115920
    return {"F_i": F_i}


def calculate_nozzle_velocity(flow_rate_gpm: float, nozzle_diameter_in: float) -> Dict[str, float]:
    if not flow_rate_gpm or not nozzle_diameter_in or nozzle_diameter_in <= 0:
        return {"nozzle_velocity_ftmin": 0.0}
    q_cuftmin = _gpm_to_cuft_per_min(flow_rate_gpm)
    area_sqft = _area_sqft_from_diameter_in(nozzle_diameter_in)
    if area_sqft <= 0:
        return {"nozzle_velocity_ftmin": 0.0}
    return {"nozzle_velocity_ftmin": q_cuftmin / area_sqft}

def calculate_total_nozzle_area(nozzle_diameters_in: List[float]) -> Dict[str, float]:
    if not nozzle_diameters_in:
        return {"total_nozzle_area_sqft": 0.0}
    area = sum(_area_sqft_from_diameter_in(d) for d in nozzle_diameters_in if d and d > 0)
    return {"total_nozzle_area_sqft": area if area > 0 else 0.0}

def calculate_bit_pressure_loss(flow_rate_gpm: float, nozzle_diameters_in: List[float], mud_density_ppg: float) -> Dict[str, float]:
    # Simplified: ΔP_bit ∝ ρ * (Q / A)^2 (field-style proxy; replace with exact if available)
    if not flow_rate_gpm or not nozzle_diameters_in or not mud_density_ppg or mud_density_ppg <= 0:
        return {"bit_pressure_loss_psi": 0.0}
    area = calculate_total_nozzle_area(nozzle_diameters_in)["total_nozzle_area_sqft"]
    if area <= 0:
        return {"bit_pressure_loss_psi": 0.0}
    v_ftmin = _gpm_to_cuft_per_min(flow_rate_gpm) / area
    # Use a conservative scaling coefficient if you have one; otherwise keep this as a proxy
    dp_psi = mud_density_ppg * (v_ftmin ** 2) * 1e-4
    return {"bit_pressure_loss_psi": dp_psi}

def calculate_bit_efficiency(hhp_bit: float, hhp_total: float) -> Dict[str, float]:
    # Efficiency = HHP_bit / HHP_total
    if not hhp_bit or not hhp_total or hhp_total <= 0:
        return {"bit_efficiency": 0.0}
    return {"bit_efficiency": hhp_bit / hhp_total}


# -----------------------------
# Wrapper: compose bit hydraulics from inputs
# -----------------------------

def run_bit_hydraulics(inputs: dict) -> dict:
    """
    Computes bit-level hydraulics using canonical equations.

    Inputs expected:
      - Q : flow rate [gpm]
      - nozzle_diameters_32nds : list of jet diameters [in/32]
      - ρ : mud weight [lb/gal]
      - d_h : bit outside diameter [in]
      - HHP_total : total hydraulic horsepower [hp] (optional for efficiency)

    Returns:
      dict with audit-grade outputs (0.0 defaults):
        - A : total flow area [in²]
        - V_jet : jet velocity [ft/min]
        - Δpb : pressure loss at the bit [psi]
        - P : hydraulic power [hp]
        - P_A : hydraulic power per unit area [hp/in²]
        - F_i : impact force [lbf]
        - bit_efficiency : ratio of P to HHP_total
    """
    Q = inputs.get("Q", 0.0)
    jets_32nds = inputs.get("nozzle_diameters_32nds", []) or []
    rho = inputs.get("rho", inputs.get("ρ", 0.0))
    d_h = inputs.get("d_h", 0.0)
    HHP_total = inputs.get("HHP_total", 0.0)

    # Total flow area [in²]
    A = total_flow_area(jets_32nds).get("A", 0.0)

    # Jet velocity [ft/min]
    V_jet = jet_velocity(Q, A).get("V_jet", 0.0) if A > 0 else 0.0

    # Pressure loss at bit [psi]
    dpb = pressure_loss_at_bit(rho, Q, A).get("dpb", 0.0) if A > 0 else 0.0

    # Hydraulic power [hp]
    P = hydraulic_power(Q, dpb).get("P", 0.0) if dpb > 0 else 0.0

    # Hydraulic power per unit area [hp/in²]
    P_A = hydraulic_power_per_unit_area(P, d_h).get("P_A", 0.0) if P > 0 and d_h > 0 else 0.0

    # Impact force [lbf]
    F_i = impact_force(rho, Q, V_jet).get("F_i", 0.0) if V_jet > 0 else 0.0

    # Bit efficiency
    bit_eff = P / HHP_total if P > 0 and HHP_total > 0 else 0.0

    return {
        "A": A,
        "V_jet": V_jet,
        "dpb": dpb,
        "P": P,
        "P_A": P_A,
        "F_i": F_i,
        "bit_efficiency": bit_eff,
    }
