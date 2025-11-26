# app/logic/normalize.py

def normalize_inputs(raw: dict) -> dict:
    """
    Normalize raw input dictionary into canonical InputData symbols.
    Returns both raw and normalized dicts.
    """

    def safe_float(val, default=0.0):
        try:
            return float(val)
        except Exception:
            return default

    normalized = {
        # -------------------------------------------------
        # Flow & mud (ASCII only)
        # -------------------------------------------------
        "Q": safe_float(raw.get("flow_rate", raw.get("Q", 0.0))),       # gpm
        "rho": safe_float(raw.get("mud_weight", raw.get("rho", 0.0))), # lb/gal

        # -------------------------------------------------
        # Geometry (ASCII only)
        # -------------------------------------------------
        "dh": safe_float(raw.get("bit_od", raw.get("dh", 0.0))),       # bit OD [in]
        "dc": safe_float(raw.get("casing_id", raw.get("dc", 0.0))),    # casing ID [in]
        "dpi": safe_float(raw.get("drill_pipe_id", raw.get("dpi", 0.0))),
        "dpo": safe_float(raw.get("drill_pipe_od", raw.get("dpo", 0.0))),
        "dci": safe_float(raw.get("drill_collar_id", raw.get("dci", 0.0))),
        "dco": safe_float(raw.get("drill_collar_od", raw.get("dco", 0.0))),

        # -------------------------------------------------
        # Depths (ASCII only)
        # -------------------------------------------------
        "Dmd": safe_float(raw.get("measured_depth_ft", raw.get("Dmd", 0.0))),
        "Dtvd": safe_float(raw.get("true_vertical_depth_ft", raw.get("Dtvd", 0.0))),

        # -------------------------------------------------
        # Viscometer readings (ASCII only)
        # -------------------------------------------------
        "phi600": safe_float(raw.get("theta_600", raw.get("phi600", 0.0))),
        "phi300": safe_float(raw.get("theta_300", raw.get("phi300", 0.0))),
        "phi3": safe_float(raw.get("theta_3", raw.get("phi3", 0.0))),

        # -------------------------------------------------
        # Swab/surge extras (ASCII only)
        # -------------------------------------------------
        "Ls": safe_float(raw.get("stand_length", raw.get("Ls", 0.0))),
        "t": safe_float(raw.get("time_slips", raw.get("t", 0.0))),
        "Lc": safe_float(raw.get("Lc", 0.0)),
        "Ldp": safe_float(raw.get("Ldp", 0.0)),
        "Ldc": safe_float(raw.get("Ldc", 0.0)),
        "tau30": safe_float(raw.get("gel_strength_30min", raw.get("tau30", 0.0))),
        "gel_dpc": safe_float(raw.get("gel_dpc", 0.0)),
        "gel_dph": safe_float(raw.get("gel_dph", 0.0)),
        "gel_dch": safe_float(raw.get("gel_dch", 0.0)),
    }

    return {"raw": raw, "normalized": normalized}
