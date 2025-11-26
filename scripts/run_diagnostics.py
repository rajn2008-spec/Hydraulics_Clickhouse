# run_diagnostics.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.logic.diagnostics import run_diagnostics_basic

# Gradients (dp_per_ft) live in pressure_loss.py
from app.logic.pressure_loss import (
    pressure_loss_gradient_pipe_collar,
    pressure_loss_gradient_annulus_open_cased_hole,
)

from app.logic.pressure_loss_due_to_friction import (
    pressure_loss_due_to_friction_pipe_casing_annulus,
    pressure_loss_due_to_friction_pipe_open_hole_annulus,
    pressure_loss_due_to_friction_collar_open_hole_annulus,
    pressure_loss_gradient_drill_pipe_open_hole,
    pressure_loss_gradient_drillstring_open_hole_annulus,
    equivalent_circulating_density,
)

# Canonical sample data
sample_data = {
    "Q": 500,
    "phi600": 80,
    "phi300": 50,
    "rho": 9.5,
    "Dtvd": 9500,
    "drill_pipe": [
        {"depth_from": 0, "depth_to": 10000, "id": 4.276, "od": 5.0}
    ],
    "drill_collar": [
        {"depth_from": 9000, "depth_to": 12000, "id": 3.25, "od": 6.75}
    ],
    "bit": [
        {"depth_from": 9000, "depth_to": 10000, "od": 8.5},
        {"depth_from": 12000, "depth_to": 13000, "od": 8.5}
    ],
    "casing": [
        {"depth_from": 0, "depth_to": 13000, "id": 8.0}
    ]
}

# Run diagnostics orchestration
diagnostics = run_diagnostics_basic(sample_data)

# Friction factor placeholder
f = 0.02

# Pull canonical outputs
v_pipe = diagnostics.v_pipe
v_ann  = diagnostics.v_annulus
mu     = diagnostics.mu
rho    = sample_data["rho"]
tvd    = sample_data["Dtvd"]

# Geometry lengths
length_casing = sample_data["casing"][0]["depth_to"] - sample_data["casing"][0]["depth_from"]
length_dpoh   = sample_data["bit"][0]["depth_to"] - sample_data["bit"][0]["depth_from"]
length_dcoh   = sample_data["drill_collar"][0]["depth_to"] - sample_data["drill_collar"][0]["depth_from"]

dp_od   = float(sample_data["drill_pipe"][0]["od"])
dp_id   = float(sample_data["drill_pipe"][0]["id"])
dc_od   = float(sample_data["drill_collar"][0]["od"])
dc_id   = float(sample_data["drill_collar"][0]["id"])
csg_id  = float(sample_data["casing"][0]["id"])
hole_od = float(sample_data["bit"][0]["od"])

# Compute gradients (dp_per_ft)
grad_dpch = pressure_loss_gradient_annulus_open_cased_hole(
    f=f,
    v_ftmin=v_ann,
    rho_lbgal=rho,
    pipe_od_in=dp_od,
    casing_id_in=csg_id
)["dp_per_ft"]

grad_dpoh = pressure_loss_gradient_drill_pipe_open_hole(
    f=f,
    v_ftmin=v_pipe,
    rho_lbgal=rho,
    d1_od=dp_od,
    hole_od=hole_od
)["dp_per_ft"]

grad_dcoh = pressure_loss_gradient_drillstring_open_hole_annulus(
    f=f,
    v_ftmin=v_ann,
    rho_lbgal=rho,
    d1_od=dc_od,
    hole_od=hole_od
)["dp_per_ft"]

# Compute total pressure losses (dP)
dp_dpc = pressure_loss_due_to_friction_pipe_casing_annulus(grad_dpch, length_casing).get("dPdpc", 0.0)
dp_dph = pressure_loss_due_to_friction_pipe_open_hole_annulus(grad_dpoh, length_dpoh, length_dcoh).get("dPdph", 0.0)
dp_dch = pressure_loss_due_to_friction_collar_open_hole_annulus(grad_dcoh, length_dcoh).get("dPdch", 0.0)

# Equivalent circulating density
ecd_dict = equivalent_circulating_density(rho, dp_dpc, dp_dph, dp_dch, tvd)
ecd = ecd_dict.get("ECD", 0.0)

# Diagnostics log dictionary
diagnostics_log = {
    **diagnostics.model_dump(exclude_none=True),
    "depth": tvd,
    "Q": sample_data["Q"],
    "rho": sample_data["rho"],
    "Dtvd": sample_data["Dtvd"],
    "dp_dpc": dp_dpc,
    "dp_dph": dp_dph,
    "dp_dch": dp_dch,
    "ECD": ecd
}

# Output diagnostics
print("\n--- Hydraulic Diagnostics ---")
for key, value in diagnostics.model_dump(exclude_none=True).items():
    print(f"{key}: {value}")

print("\n--- Pressure Losses ---")
print(f"Drill Pipe–Casing Loss (dp_dpc): {dp_dpc:.2f} psi")
print(f"Drill Pipe–Open Hole Loss (dp_dph): {dp_dph:.2f} psi")
print(f"Drill Collar–Open Hole Loss (dp_dch): {dp_dch:.2f} psi")

print("\n--- Equivalent Circulating Density ---")
print(f"ECD: {ecd:.2f} lb/gal")
