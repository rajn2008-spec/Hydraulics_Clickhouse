# utils/parameter_names.py

PARAMETER_NAMES = {
    # General Hydraulics
    "Q": "Volumetric Flow Rate (gpm)",
    "rho": "Mud Weight (lb/gal)",
    "Dmd": "Measured Depth (ft)",
    "Dtvd": "True Vertical Depth (ft)",
    "Dbo": "Current Bit Depth (ft)",
    "Dbp": "Previous Bit Depth (ft)",
    "ROP": "Rate of Penetration (ft/hr)",
    "dh": "Bit Outside Diameter (in)",
    "dc": "Casing Inside Diameter (in)",
    "dpi": "Drill Pipe Inside Diameter (in)",
    "dpo": "Drill Pipe Outside Diameter (in)",
    "dci": "Drill Collar Inside Diameter (in)",
    "dco": "Drill Collar Outside Diameter (in)",

    "phi600": "Viscometer Reading 600 RPM",
    "phi300": "Viscometer Reading 300 RPM",
    "phi3": "Viscometer Reading 3 RPM",
    "tau30": "30-Minute Gel Strength (lbf/100ft2)",

    # ASCII replacements for Greek keys
    "dp": "Pressure Loss (psi)",
    "dp_L": "Pressure Loss Gradient (psi/ft)",
    "mu": "Effective Viscosity (cP)",

    "ECD": "Equivalent Circulating Density (lb/gal)",
    "Re": "Reynolds Number",
    "Remax": "Critical Reynolds Number (max)",
    "n": "Flow Behavior Index",
    "k": "Consistency Index",

    "flow_string": "Flow Regime (Drillstring)",
    "flow_annulus": "Flow Regime (Annulus)",

    # Bit Hydraulics
    "A": "Total Flow Area (in2)",
    "Vjet": "Jet Velocity (ft/min)",
    "dpb": "Bit Pressure Loss (psi)",
    "hydraulic_power_hp": "Hydraulic Power (hp)",
    "PA": "Hydraulic Power per Area (hp/in2)",
    "Fi": "Impact Force (lbf)",

    # Cuttings Transport
    "gb": "Boundary Shear Rate (s^-1)",
    "tp": "Particle Shear Stress (lbf/100ft2)",
    "gp": "Particle Shear Rate (s^-1)",
    "Vs": "Slip Velocity (ft/min)",
    "Vt": "Transport Velocity (ft/min)",
    "Et": "Transport Efficiency (%)",
    "C": "Cuttings Concentration (%)",

    # Swab & Surge
    "Vp": "Pipe Velocity (ft/min)",
    "Ve": "Equivalent Fluid Velocity (ft/min)",
    "rhoe": "Equivalent Mud Weight (lb/gal)",
    "Pg": "Gel-Breaking Pressure (psi)",
    "swab_pressure": "Swab Pressure (psi)",
    "surge_pressure": "Surge Pressure (psi)",
    "swab_velocity": "Swab Velocity (ft/min)",
    "surge_velocity": "Surge Velocity (ft/min)",
    "swab_force": "Swab Force (lbf)",
    "surge_force": "Surge Force (lbf)",

    # Derived Outputs
    "v_pipe": "Velocity Drill Pipe (ft/min)",
    "v_ann": "Velocity Annulus (ft/min)",
    "Re_pipe": "Reynolds Number (Pipe)",
    "Re_ann": "Reynolds Number (Annulus)",
    "mu_e_pipe": "Effective Viscosity (Pipe, cP)",
    "mu_e_ann": "Effective Viscosity (Annulus, cP)",
    "n_string": "Flow Behavior Index (Pipe)",
    "k_string": "Consistency Index (Pipe)",
    "n_annulus": "Flow Behavior Index (Annulus)",
    "k_annulus": "Consistency Index (Annulus)",

    # Normalization-only Inputs
    "d1": "Inner Diameter (in)",
    "d2": "Outer Diameter (in)",
    "gel_dpc": "Gel Strength DP–Casing (lbf/100ft2)",
    "gel_dph": "Gel Strength DP–Hole (lbf/100ft2)",
    "gel_dch": "Gel Strength DC–Hole (lbf/100ft2)",
    "k_a": "Consistency Index (Annulus)",
    "n_a": "Flow Behavior Index (Annulus)",
    "well_id": "Well Identifier",

    # Missing Inputs patched
    "Ldp": "Drill Pipe Length (ft)",
    "Ldc": "Drill Collar Length (ft)",
    "Lc": "Casing Length (ft)",
    "J": "Jet Nozzle Size (32nds in)",
    "dcut": "Cuttings Diameter (in)",
    "T": "Thickness (in)",
    "t": "Time (s)",
    "Ls": "Stand Length (ft)",
    "drill_pipe": "Drill Pipe Profile",
    "drill_collar": "Drill Collar Profile",
    "casing": "Casing Profile",
    "bit": "Bit Profile",
    "mud_weight_profile": "Mud Weight Profile",

    # Missing Outputs patched
    "V": "Average Velocity (ft/min)",
    "Vcrit": "Critical Velocity (ft/min)",
    "Qcrit": "Critical Flow Rate (gal/min)",
    "f": "Friction Factor (dimensionless)",
    "P": "Pressure (psi)",
    "missing_inputs": "Audit: Missing Inputs",
    "audit_raw_inputs": "Audit: Raw Inputs",
    "audit_normalized_inputs": "Audit: Normalized Inputs",
    "timestamp": "Timestamp (ISO 8601)",
}
