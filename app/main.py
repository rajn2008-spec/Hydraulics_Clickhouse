from flask import Flask, request, render_template, jsonify
from datetime import datetime, timezone
import logging
import os
import csv
import json

# Your own modules
from app.models import InputData
from app.logic.diagnostics import run_diagnostics_basic
from utils.db import check_missing_inputs, insert_diagnostics
from utils.parameter_names import PARAMETER_NAMES

# Flask setup
app = Flask(__name__, template_folder="templates")

# Logging
logging.basicConfig(level=logging.INFO)

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Step 1: Parse form inputs
        form_data = {k: request.form.get(k) for k in request.form}
        inputs = InputData(**{
            k: (float(v) if v and v.replace('.', '', 1).isdigit() else v)
            for k, v in form_data.items()
        })

        # Step 2: Run diagnostics
        outputs = run_diagnostics_basic(inputs.dict())

        # Step 3: Merge inputs + outputs + metadata
        timestamp = datetime.now(timezone.utc)
        row = {
            **inputs.model_dump(exclude_none=True),
            **outputs.model_dump(exclude_none=True),
            "timestamp": timestamp,
            "source": "form"
        }

        # Step 3a: Check for missing inputs (canonical ASCII keys)
        required_keys: list[str] = ["v_ann", "mu", "rho", "dh", "Re"]
        row["missing_inputs"] = check_missing_inputs(row, required_keys)

        if row["missing_inputs"]:
            logging.warning(f"⚠️ Missing inputs detected (zero-filled): {row['missing_inputs']}")

        # Step 5: Export to CSV/JSON
        os.makedirs("exports", exist_ok=True)
        well_id = row.get("well_id", "UNKNOWN")
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        base_name = f"{well_id}_{timestamp_str}"

        with open(f"exports/{base_name}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writeheader()
            writer.writerow(row)

        with open(f"exports/{base_name}.json", "w") as f:
            json.dump(row, f, indent=2, default=str)

        # Step 6: Render results
        return render_template(
            "results.html",
            results=outputs.model_dump(exclude_none=True),
            parameter_names=PARAMETER_NAMES
        )

    except Exception as e:
        logging.exception("❌ Submission error")
        return render_template("form.html", error=f"❌ Submission failed: {str(e)}")

@app.route("/health")
def health():
    return "OK", 200

@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})

# -----------------------------
# Main Function (Test Harness)
# -----------------------------
def main():
    form_data = InputData(
        Q=450,
        phi600=55,
        phi300=35,
        phi3=5,
        dpi=4.5,
        dci=6.0,
        dh=8.5,
        dc=6.5,
        P=2500,
        Dmd=9500,
        Dtvd=9300,
        tau30=300,
        rho=9.5,
        well_id="TX-DEV-001",
        drill_pipe=[{"section": 1, "id": 4.5, "od": 5.0, "depth_from": 0, "depth_to": 5000}],
        drill_collar=[{"section": 1, "id": 6.0, "od": 6.5, "depth_from": 0, "depth_to": 9500}],
        casing=[{"section": 1, "id": 9.625, "depth_from": 0, "depth_to": 7000}],
        bit=[{"section": 1, "od": 8.5, "depth_from": 9000, "depth_to": 9500}],
        mud_weight_profile=[
            {"section": 1, "weight_from": 9.0, "weight_to": 9.5, "depth_from": 0, "depth_to": 5000},
            {"section": 2, "weight_from": 9.5, "weight_to": 10.0, "depth_from": 5000, "depth_to": 9500}
        ]
    )

    results = run_diagnostics_basic(form_data.dict())
    print(results.json(indent=2))

    row = {
        **form_data.model_dump(exclude_none=True),
        **results.model_dump(exclude_none=True),
        "timestamp": datetime.now(timezone.utc),
        "source": "test"
    }

    missing_inputs = check_missing_inputs(row, ["v_ann", "mu", "rho", "dh", "Re"])
    if missing_inputs:
        logging.warning(f"⚠️ Missing inputs detected: {missing_inputs}")

    insert_diagnostics(row)

    print("Row keys being inserted:", list(row.keys()))
    print("\n📊 Diagnostics Output:")
    for k, v in results.model_dump(exclude_none=True).items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True)
    main()
