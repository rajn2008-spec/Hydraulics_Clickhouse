# app/logic/units.py

from utils.parameter_units import PARAMETER_UNITS, convert_units, convert_value_for_param

# -----------------------------
# Unit Conversions
# -----------------------------

def inches_to_mm(inches):
    return inches * 25.4 if inches and inches > 0 else 0.0

def mm_to_inches(mm):
    return mm / 25.4 if mm and mm > 0 else 0.0

def lb_per_gal_to_kg_per_m3(lb_per_gal):
    return lb_per_gal * 119.826 if lb_per_gal and lb_per_gal > 0 else 0.0

def kg_per_m3_to_lb_per_gal(kg_per_m3):
    return kg_per_m3 / 119.826 if kg_per_m3 and kg_per_m3 > 0 else 0.0

def ft_per_min_to_m_per_s(ft_per_min):
    return ft_per_min * 0.00508 if ft_per_min and ft_per_min > 0 else 0.0

def m_per_s_to_ft_per_min(m_per_s):
    return m_per_s / 0.00508 if m_per_s and m_per_s > 0 else 0.0

def ft_hr_to_m_s(ft_hr):
    return ft_hr * 0.00008467 if ft_hr and ft_hr > 0 else 0.0

def m_s_to_ft_hr(m_s):
    return m_s / 0.00008467 if m_s and m_s > 0 else 0.0

def gal_min_to_l_s(gpm):
    return gpm * 0.06309 if gpm and gpm > 0 else 0.0

def l_s_to_gal_min(lps):
    return lps / 0.06309 if lps and lps > 0 else 0.0

# -----------------------------
# Normalization (Swab/Surge)
# -----------------------------

def normalize_units(form: dict) -> dict:
    """
    Normalize swab/surge form inputs into canonical InputData symbols.
    Returns dict keyed by canonical ASCII names.
    """
    normalized = {}
    try:
        normalized["Ls"] = float(form.get("stand_length", 0.0))
        normalized["t"] = float(form.get("time_slips", 0.0))
        normalized["d1"] = float(form.get("d1", 0.0))
        normalized["d2"] = float(form.get("d2", 0.0))
        normalized["rho"] = float(form.get("mud_weight", 0.0))          # ASCII instead of ρ
        normalized["k_a"] = float(form.get("k_a", 0.0))
        normalized["n_a"] = float(form.get("n_a", 0.0))
        normalized["Lc"] = float(form.get("L_c", 0.0))
        normalized["Ldp"] = float(form.get("L_dp", 0.0))
        normalized["Ldc"] = float(form.get("L_dc", 0.0))
        normalized["gel_dpc"] = float(form.get("gel_dpc", 0.0))
        normalized["gel_dph"] = float(form.get("gel_dph", 0.0))
        normalized["gel_dch"] = float(form.get("gel_dch", 0.0))
        normalized["tau30"] = float(form.get("gel_strength_30min", 0.0))  # ASCII instead of τ30
        normalized["Dtvd"] = float(form.get("tvd", 0.0))

    except Exception:
        return {
            "Ls": 0.0, "t": 0.0, "d1": 0.0, "d2": 0.0, "rho": 0.0,
            "k_a": 0.0, "n_a": 0.0, "Lc": 0.0, "Ldp": 0.0, "Ldc": 0.0,
            "gel_dpc": 0.0, "gel_dph": 0.0, "gel_dch": 0.0,
            "Dtvd": 0.0, "tau30": 0.0
        }

    return normalized
