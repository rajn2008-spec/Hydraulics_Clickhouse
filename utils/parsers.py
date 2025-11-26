# app/logic/parsers.py

import os
import tempfile
import pandas as pd
import lasio
import math
from uuid import uuid4

from app.logic.normalize import normalize_inputs
from app.logic.diagnostics import run_diagnostics_basic

# -----------------------------
# Generic File Parser
# -----------------------------
def parse_file(file):
    """
    Dispatch parser based on file extension.
    Supports .csv and .las files.
    """
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext == ".csv":
        return parse_csv(file)
    elif ext == ".las":
        return parse_las(file)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# -----------------------------
# Save Temp File
# -----------------------------
def save_temp_file(file):
    """
    Saves uploaded file to a temporary location.
    Returns the path.
    """
    suffix = os.path.splitext(file.filename)[-1]
    temp_path = os.path.join(tempfile.gettempdir(), f"{uuid4()}{suffix}")
    file.save(temp_path)
    return temp_path

# -----------------------------
# CSV Parser
# -----------------------------
def parse_csv(file):
    """
    Parses a CSV file into normalized records.
    Returns list of diagnostics results.
    """
    temp_path = save_temp_file(file)
    df = pd.read_csv(temp_path)
    results = []

    for _, row in df.iterrows():
        record = {
            k: (0.0 if (v is None or (isinstance(v, float) and math.isnan(v))) else v)
            for k, v in row.to_dict().items()
        }
        normalized = normalize_inputs(record)["normalized"]
        diagnostics = run_diagnostics_basic({**record, **normalized})
        results.append(diagnostics.model_dump(exclude_none=True))

    return results

# -----------------------------
# LAS Parser
# -----------------------------
def parse_las(file):
    """
    Parses a LAS file into normalized record.
    Returns diagnostics result.
    """
    temp_path = save_temp_file(file)
    las = lasio.read(temp_path)

    record = {
        "Dtvd": float(las["DEPT"][-1]) if "DEPT" in las.curves else 0.0,
        "Q": float(las["FLOW"][0]) if "FLOW" in las.curves else 0.0,
        "phi600": float(las["TH600"][0]) if "TH600" in las.curves else 0.0,
        "phi300": float(las["TH300"][0]) if "TH300" in las.curves else 0.0,
        "rho": float(las["MUDWT"][0]) if "MUDWT" in las.curves else 0.0,
    }

    normalized = normalize_inputs(record)["normalized"]
    diagnostics = run_diagnostics_basic({**record, **normalized})
    return diagnostics.model_dump(exclude_none=True)
