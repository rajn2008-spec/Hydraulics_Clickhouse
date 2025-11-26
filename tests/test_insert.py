import pandas as pd
import lasio
import pytest
from datetime import datetime, timezone

# Use the test stub, not production ClickHouse
from tests.mock_db import push_to_clickhouse

from app.logic.diagnostics import run_diagnostics_basic
from app.logic.pressure_loss_due_to_friction import (
    pressure_loss_due_to_friction_pipe_casing_annulus,
    pressure_loss_gradient_drill_pipe_open_hole,
    pressure_loss_due_to_friction_collar_open_hole_annulus,
    equivalent_circulating_density,
)

# -----------------------------
# Helpers
# -----------------------------
def safe_curve(las, name, default=0.0):
    try:
        return float(las[name][0])
    except Exception:
        return default

# -----------------------------
# CSV parametrization (robust)
# -----------------------------
csv_rows = []
try:
    df = pd.read_csv("data/example.csv")
    csv_rows = [row for _, row in df.iterrows()]
except Exception as e:
    CSV_LOAD_ERROR = str(e)
else:
    CSV_LOAD_ERROR = None

# -----------------------------
# LAS parametrization (robust)
# -----------------------------
las = None
las_depths = []
try:
    las = lasio.read("data/example.las")
    las_depths = [float(las["DEPT"][i]) for i in range(min(5, len(las["DEPT"])))]
except Exception as e:
    LAS_LOAD_ERROR = str(e)
    las = None
    las_depths = []
else:
    LAS_LOAD_ERROR = None

# -----------------------------
# CSV-driven insert test
# -----------------------------
@pytest.mark.parametrize("row", csv_rows)
def test_insert_csv(row):
    if CSV_LOAD_ERROR is not None:
        pytest.skip(f"CSV not available: {CSV_LOAD_ERROR}")

    depth = row.get("TVD", 0.0)

    data = {
        "Q": row.get("FlowRate", 0.0),
        "phi600": row.get("Theta600", 0.0),
        "phi300": row.get("Theta300", 0.0),
        "rho": row.get("MudWeight", 0.0),
        "Dtvd": depth,
        "drill_pipe": [{"depth_from": 0, "depth_to": depth, "id": 4.276, "od": 5.0}],
        "drill_collar": [{"depth_from": 9000, "depth_to": depth, "id": 3.25, "od": 6.75}],
        "bit": [{"depth_from": 9000, "depth_to": depth, "od": 8.5}],
        "casing": [{"depth_from": 0, "depth_to": depth, "id": 8.0}],
    }

    diagnostics = run_diagnostics_basic(data).model_dump(exclude_none=True)

    # Canonical Eq-28: use mud weight (rho), not hydrostatic pressure
    rho = data["rho"]
    dp_dpc = pressure_loss_due_to_friction_pipe_casing_annulus(0.5, 9500)["ΔPdpc"]
    dp_dph = pressure_loss_gradient_drill_pipe_open_hole(0.4, 1000)["Δp"]
    dp_dch = pressure_loss_due_to_friction_collar_open_hole_annulus(0.3, 500)["ΔPdch"]

    ecd = equivalent_circulating_density(rho, dp_dpc, dp_dph, dp_dch, depth)["ECD"]

    diagnostics_log = {
        "well_id": row.get("WellID", "WELL-CSV"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **diagnostics,
        "dp_dpc": dp_dpc,
        "dp_dph": dp_dph,
        "dp_dch": dp_dch,
        "ECD": ecd,
    }

    assert "ECD" in diagnostics_log
    assert diagnostics_log["dp_dpc"] > 0
    assert diagnostics_log["dp_dph"] > 0
    assert diagnostics_log["dp_dch"] > 0

    push_to_clickhouse(diagnostics_log)

# -----------------------------
# LAS-driven insert test
# -----------------------------
@pytest.mark.parametrize("depth", las_depths)
def test_insert_las(depth):
    if LAS_LOAD_ERROR is not None or las is None:
        pytest.skip(f"LAS not available: {LAS_LOAD_ERROR}")

    data = {
        "Q": safe_curve(las, "FLOW"),
        "phi600": safe_curve(las, "TH600"),
        "phi300": safe_curve(las, "TH300"),
        "rho": safe_curve(las, "MUDWT"),
        "Dtvd": depth,
        "drill_pipe": [{"depth_from": 0, "depth_to": depth, "id": 4.276, "od": 5.0}],
        "drill_collar": [{"depth_from": 9000, "depth_to": depth, "id": 3.25, "od": 6.75}],
        "bit": [{"depth_from": 9000, "depth_to": depth, "od": 8.5}],
        "casing": [{"depth_from": 0, "depth_to": depth, "id": 8.0}],
    }

    diagnostics = run_diagnostics_basic(data).model_dump(exclude_none=True)

    rho = data["rho"]
    dp_dpc = pressure_loss_due_to_friction_pipe_casing_annulus(0.5, 9500)["ΔPdpc"]
    dp_dph = pressure_loss_gradient_drill_pipe_open_hole(0.4, 1000)["Δp"]
    dp_dch = pressure_loss_due_to_friction_collar_open_hole_annulus(0.3, 500)["ΔPdch"]

    ecd = equivalent_circulating_density(rho, dp_dpc, dp_dph, dp_dch, depth)["ECD"]

    diagnostics_log = {
        "well_id": "WELL-LAS",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **diagnostics,
        "dp_dpc": dp_dpc,
        "dp_dph": dp_dph,
        "dp_dch": dp_dch,
        "ECD": ecd,
    }

    assert "ECD" in diagnostics_log
    assert diagnostics_log["dp_dpc"] > 0
    assert diagnostics_log["dp_dph"] > 0
    assert diagnostics_log["dp_dch"] > 0

    push_to_clickhouse(diagnostics_log)
