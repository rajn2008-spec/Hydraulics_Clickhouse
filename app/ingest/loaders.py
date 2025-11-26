# 🔹 Flexible column mapping for CSVs
COLUMN_MAP = {
    "Dtvd": ["TVD", "Depth", "MeasuredDepth"],
    "Q": ["FlowRate", "Flow", "GPM"],
    "phi600": ["Theta600", "600rpm", "Vis600"],
    "phi300": ["Theta300", "300rpm", "Vis300"],
    "rho": ["MudWeight", "Density", "MW"],
    "dpi": ["DP_ID", "DrillPipeID"],
    "dpo": ["DP_OD", "DrillPipeOD"],
    "dci": ["DC_ID", "DrillCollarID"],
    "dco": ["DC_OD", "DrillCollarOD"],
    "dh": ["BIT_OD", "BitOD"],
    "dc": ["CASING_ID", "CasingID"],
    # ✅ Add geometry keys explicitly
    "DP_TD": ["DP_TD"],
    "DC_TOP": ["DC_TOP"],
    "DC_TD": ["DC_TD"],
    "BIT_TOP": ["BIT_TOP"],
    "BIT_TD": ["BIT_TD"],
    "BIT_OD": ["BIT_OD"],
    "CASING_TD": ["CASING_TD"],
    "CASING_ID": ["CASING_ID"],
}

def resolve_column(row, key, default=0.0):
    for candidate in COLUMN_MAP.get(key, []):
        if candidate in row and pd.notna(row[candidate]):
            try:
                return float(row[candidate])
            except Exception:
                return default
    return default

# 🔹 Load LAS file
def load_las(filepath):
    las = lasio.read(filepath)

    def get_param(name, default=0.0):
        try:
            return float(las.params.get(name).value)
        except Exception:
            return default

    def get_curve(name, default=0.0):
        try:
            return float(las[name][0])
        except Exception:
            return default

    return {
        "Dtvd": get_curve("DEPT", 0.0),
        "Q": get_curve("FLOW", 0.0),
        "phi600": get_curve("TH600", 0.0),
        "phi300": get_curve("TH300", 0.0),
        "rho": get_curve("MUDWT", 0.0),
        "drill_pipe": [{
            "depth_from": 0,
            "depth_to": get_param("DP_TD", 10000),
            "id": get_param("DP_ID", 4.276),
            "od": get_param("DP_OD", 5.0)
        }],
        "drill_collar": [{
            "depth_from": get_param("DC_TOP", 9000),
            "depth_to": get_param("DC_TD", 12000),
            "id": get_param("DC_ID", 3.25),
            "od": get_param("DC_OD", 6.75)
        }],
        "bit": [{
            "depth_from": get_param("BIT_TOP", 9000),
            "depth_to": get_param("BIT_TD", 10000),
            "od": get_param("BIT_OD", 8.5)
        }],
        "casing": [{
            "depth_from": 0,
            "depth_to": get_param("CASING_TD", 13000),
            "id": get_param("CASING_ID", 8.0)
        }]
    }

# 🔹 Ingest single LAS file
def ingest_las(filepath):
    data = load_las(filepath)
    normalized = normalize_inputs(data)["normalized"]
    diagnostics = run_diagnostics_with_geometry({**data, **normalized}, depth=data["Dtvd"])
    diagnostics["source_file"] = filepath
    insert_diagnostics_row(diagnostics)

    # Bit hydraulics if nozzle data present
    if "J" in normalized and "dh" in normalized:
        bit_results = run_bit_hydraulics(
            flow_rate_gpm=normalized.get("Q", 0.0),
            mud_weight_ppg=normalized.get("rho", normalized.get("ρ", 0.0)),
            jet_diameters_in=normalized.get("J", 0.0),
            bit_od_in=normalized.get("dh", 0.0)
        )
        bit_results["source_file"] = filepath
        # ✅ Define or import insert_bit_hydraulics_row
        # insert_bit_hydraulics_row(bit_results)
