# app/models.py

from pydantic import BaseModel
from typing import List, Dict


class InputData(BaseModel):
    # --- Flat parameters (canonical symbols from Excel) ---
    dh: float = 0.0       # Bit Outside Diameter
    dc: float = 0.0       # Casing Inside Diameter
    dpi: float = 0.0      # Drill Pipe Inside Diameter
    dpo: float = 0.0      # Drill Pipe Outside Diameter
    dci: float = 0.0      # Drill Collar Inside Diameter
    dco: float = 0.0      # Drill Collar Outside Diameter
    Q: float = 0.0        # Volumetric Flow Rate

    phi600: float = 0.0   # Viscometer Reading, 600 RPM
    phi300: float = 0.0   # Viscometer Reading, 300 RPM
    phi3: float = 0.0     # Viscometer Reading, 3 RPM

    rho: float = 0.0      # Mud Weight

    Dmd: float = 0.0      # Measured Depth
    Dtvd: float = 0.0     # True Vertical Depth
    Ldp: float = 0.0      # Drill Pipe Length
    Ldc: float = 0.0      # Drill Collars Length
    Lc: float = 0.0       # Last Casing Length
    J: float = 0.0        # Jet Diameter
    dcut: float = 0.0     # Average Particle Diameter
    T: float = 0.0        # Average Particle Thickness
    ROP: float = 0.0      # Rate of Penetration
    t: float = 0.0        # Time From Slips to Slips
    Ls: float = 0.0       # Stand Length
    Dbo: float = 0.0      # Current Bit Depth
    Dbp: float = 0.0      # Previous Bit Depth

    tau30: float = 0.0    # 30-Minute Gel Strength

    well_id: str = ""     # Well identifier

    # --- Structured multi-section profiles ---
    drill_pipe: List[Dict] = []
    drill_collar: List[Dict] = []
    casing: List[Dict] = []
    bit: List[Dict] = []
    mud_weight_profile: List[Dict] = []



class OutputData(BaseModel):
    # --- Canonical outputs ---
    depth: float = 0.0
    dh: float = 0.0
    dc: float = 0.0
    dpi: float = 0.0
    dci: float = 0.0
    dco: float = 0.0
    Q: float = 0.0
    phi600: float = 0.0       # was ɸ600
    phi300: float = 0.0       # was ɸ300
    rho: float = 0.0          # was ρ

    v_pipe: float = 0.0
    v_annulus: float = 0.0

    # --- Rheology and hydraulics ---
    V: float = 0.0
    n: float = 0.0
    k: float = 0.0
    n_a: float = 0.0
    k_a: float = 0.0
    mu: float = 0.0           # was μ
    Re: float = 0.0
    Remax: float = 0.0
    Vcrit: float = 0.0
    Qcrit: float = 0.0
    f: float = 0.0
    dp_L: float = 0.0         # was Δp_L
    dp: float = 0.0           # was Δp
    ECD: float = 0.0
    A: float = 0.0
    Vjet: float = 0.0
    dpb: float = 0.0          # was Δpb
    P: float = 0.0
    PA: float = 0.0
    Fi: float = 0.0
    gb: float = 0.0           # was γb
    tp: float = 0.0           # was τp
    gp: float = 0.0           # was γp
    Vs: float = 0.0
    Vt: float = 0.0
    Et: float = 0.0
    C: float = 0.0
    Vp: float = 0.0
    Ve: float = 0.0
    rhoe: float = 0.0         # was ρe
    Pg: float = 0.0

    # --- Pressure outputs required by test ---
    dp_casing_annulus: float = 0.0
    dp_open_hole_annulus: float = 0.0
    dc_open_hole_annulus: float = 0.0
    hydrostatic_pressure: float = 0.0

    # --- Audit fields ---
    missing_inputs: dict = {}
    audit_raw_inputs: dict = {}
    audit_normalized_inputs: dict = {}
    timestamp: str = ""

