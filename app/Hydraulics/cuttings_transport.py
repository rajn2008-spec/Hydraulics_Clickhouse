import math

# -----------------------------
# Cuttings Transport Equations
# -----------------------------

def boundary_shear_rate(d_cut_in, mud_weight_ppg):
    if not d_cut_in or d_cut_in <= 0 or not mud_weight_ppg or mud_weight_ppg <= 0:
        return {"gb": 0.0}
    gb = 186 / (d_cut_in * math.sqrt(mud_weight_ppg))
    return {"gb": gb}

def particle_shear_stress(thickness_in, mud_weight_ppg):
    if not thickness_in or thickness_in <= 0 or not mud_weight_ppg or mud_weight_ppg <= 0:
        return {"tp": 0.0}
    tp = 7.9 * math.sqrt(thickness_in * (20.8 - mud_weight_ppg))
    return {"tp": tp}

def particle_shear_rate(tau_p, k_a, n_a):
    if not tau_p or tau_p <= 0 or not k_a or k_a <= 0 or not n_a or n_a <= 0:
        return {"gp": 0.0}
    gp = (tau_p / k_a) ** (1 / n_a)
    return {"gp": gp}

def classify_flow_regime(gamma_p, gamma_b):
    if not gamma_p or gamma_p <= 0 or not gamma_b or gamma_b <= 0:
        return {"flow_regime": "invalid"}
    return {"flow_regime": "laminar" if gamma_p <= gamma_b else "turbulent"}

def slip_velocity_laminar(tau_p, gamma_p, d_cut_in, mud_weight_ppg):
    if not tau_p or tau_p <= 0 or not gamma_p or gamma_p <= 0 or not d_cut_in or d_cut_in <= 0 or not mud_weight_ppg or mud_weight_ppg <= 0:
        return {"Vs": 0.0}
    Vs = 1.22 * tau_p * math.sqrt((gamma_p * d_cut_in) / math.sqrt(mud_weight_ppg))
    return {"Vs": Vs}

def slip_velocity_turbulent(tau_p, mud_weight_ppg):
    if not tau_p or tau_p <= 0 or not mud_weight_ppg or mud_weight_ppg <= 0:
        return {"Vs": 0.0}
    Vs = (16.62 * tau_p) / math.sqrt(mud_weight_ppg)
    return {"Vs": Vs}

def transport_velocity(V_annular, V_slip):
    if not V_annular or V_annular <= 0 or not V_slip or V_slip <= 0:
        return {"Vt": 0.0}
    Vt = V_annular - V_slip
    return {"Vt": Vt}

def transport_efficiency(V_transport, V_annular):
    if not V_transport or V_transport <= 0 or not V_annular or V_annular <= 0:
        return {"Et": 0.0}
    Et = (V_transport / V_annular) * 100
    return {"Et": Et}

def cuttings_concentration(ROP_ft_hr, hole_diameter_in, Et_percent, flow_rate_gpm):
    if not ROP_ft_hr or ROP_ft_hr <= 0 or not hole_diameter_in or hole_diameter_in <= 0 or not Et_percent or Et_percent <= 0 or not flow_rate_gpm or flow_rate_gpm <= 0:
        return {"C": 0.0}
    C = ((ROP_ft_hr * hole_diameter_in ** 2) / (14.71 * Et_percent * flow_rate_gpm)) * 100
    return {"C": C}

# -----------------------------
# Orchestrator
# -----------------------------

def run_cuttings_transport_logic(form):
    """
    Orchestrates cuttings transport diagnostics.
    Accepts normalized form input and returns canonical outputs.
    """
    diagnostics = {}
    diagnostics.update(boundary_shear_rate(form.get("dcut", 0.0), form.get("rho", form.get("ρ", 0.0))))
    diagnostics.update(particle_shear_stress(form.get("T", 0.0), form.get("rho", form.get("ρ", 0.0))))
    diagnostics.update(particle_shear_rate(diagnostics.get("tp", 0.0), form.get("k_a", 0.0), form.get("n_a", 0.0)))
    diagnostics.update(classify_flow_regime(diagnostics.get("gp", 0.0), diagnostics.get("gb", 0.0)))

    # Slip velocity based on flow regime
    if diagnostics.get("flow_regime") == "laminar":
        diagnostics.update(slip_velocity_laminar(diagnostics.get("tp", 0.0), diagnostics.get("gp", 0.0), form.get("dcut", 0.0), form.get("rho", form.get("ρ", 0.0))))
    elif diagnostics.get("flow_regime") == "turbulent":
        diagnostics.update(slip_velocity_turbulent(diagnostics.get("tp", 0.0), form.get("rho", form.get("ρ", 0.0))))
    else:
        diagnostics["Vs"] = 0.0

    diagnostics.update(transport_velocity(form.get("V", 0.0), diagnostics.get("Vs", 0.0)))
    diagnostics.update(transport_efficiency(diagnostics.get("Vt", 0.0), form.get("V", 0.0)))
    diagnostics.update(cuttings_concentration(form.get("ROP", 0.0), form.get("dh", 0.0), diagnostics.get("Et", 0.0), form.get("Q", 0.0)))

    return diagnostics
