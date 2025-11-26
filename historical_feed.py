# historical_feed.py

import os
import uuid
import logging
import pandas as pd
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.logic.diagnostics import run_diagnostics_basic
from utils.db import insert_batch, create_table_from_schema, log_ingestion_metadata
from app.logic.normalize import normalize_inputs

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def validate_geometry_array(name, array):
    inch_to_m = 0.0254
    ft_to_m = 0.3048
    errors = []
    validated = []

    for i, segment in enumerate(array):
        seg = {}
        seg_errors = []

        # Depth validation
        df = segment.get("depth_from", 0.0)
        dt = segment.get("depth_to", 0.0)
        if df <= 0 or dt <= df or dt > 15000:
            seg_errors.append({
                "message": f"{name}[{i}] invalid depth range: {df}-{dt}",
                "severity": "critical"
            })
            seg["depth_from_m"] = 0.0
            seg["depth_to_m"] = 0.0
        else:
            seg["depth_from_m"] = df * ft_to_m
            seg["depth_to_m"] = dt * ft_to_m

        # Diameter validation
        for key in ["id", "od"]:
            val = segment.get(key, 0.0)
            if val <= 0 or val > 30:
                seg_errors.append({
                    "message": f"{name}[{i}] invalid {key}: {val} in",
                    "severity": "critical"
                })
                seg[f"{key}_m"] = 0.0
            else:
                seg[f"{key}_m"] = val * inch_to_m

        errors.extend(seg_errors)
        validated.append({**segment, **seg, "validation_errors": seg_errors})

    return validated, [e["message"] for e in errors if e["severity"] == "critical"]


def get_param(las, name, default=0.0):
    try:
        return float(las.params.get(name).value)
    except Exception:
        return default


def read_batches(filepath, batch_size=100):
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
        records = df.to_dict(orient="records")

    elif filepath.endswith(".json"):
        df = pd.read_json(filepath)
        records = df.to_dict(orient="records")

    elif filepath.endswith(".las"):
        import lasio
        from app.ingest.loaders import extract_well_id_from_las

        las = lasio.read(filepath)
        df = las.df().reset_index()
        well_id = extract_well_id_from_las(las, filepath)

        # Geometry arrays
        drill_pipe_raw = [{
            "depth_from": 0,
            "depth_to": get_param(las, "DP_TD", 10000),
            "id": get_param(las, "DP_ID", 4.276),
            "od": get_param(las, "DP_OD", 5.0)
        }]

        drill_collar_raw = [{
            "depth_from": get_param(las, "DC_TOP", 9000),
            "depth_to": get_param(las, "DC_TD", 12000),
            "id": get_param(las, "DC_ID", 3.25),
            "od": get_param(las, "DC_OD", 6.75)
        }]

        bit_raw = [{
            "depth_from": get_param(las, "BIT_TOP", 9000),
            "depth_to": get_param(las, "BIT_TD", 10000),
            "od": get_param(las, "BIT_OD", 8.5)
        }]

        casing_raw = [{
            "depth_from": 0,
            "depth_to": get_param(las, "CASING_TD", 13000),
            "id": get_param(las, "CASING_ID", 8.0)
        }]

        drill_pipe, pipe_errors = validate_geometry_array("drill_pipe", drill_pipe_raw)
        drill_collar, collar_errors = validate_geometry_array("drill_collar", drill_collar_raw)
        bit, bit_errors = validate_geometry_array("bit", bit_raw)
        casing, casing_errors = validate_geometry_array("casing", casing_raw)

        geometry_errors = pipe_errors + collar_errors + bit_errors + casing_errors

        records = df.to_dict(orient="records")
        for row in records:
            row["drill_pipe"] = drill_pipe
            row["drill_collar"] = drill_collar
            row["bit"] = bit
            row["casing"] = casing
            row["geometry_errors"] = geometry_errors
            row["has_critical_geometry_error"] = bool(geometry_errors)
            row["well_id"] = well_id

    else:
        raise ValueError("Unsupported file format")

    for i in range(0, len(records), batch_size):
        yield records[i:i + batch_size]


def process_batch(batch, run_id, table_created_flag):
    buffer = []
    error_count = 0

    for row in batch:
        try:
            normalized = normalize_inputs(row)["normalized"]
            row.update(normalized)

            diagnostics = run_diagnostics_basic(row).model_dump(exclude_none=True)
            diagnostics["run_id"] = run_id
            diagnostics["timestamp"] = datetime.utcnow()
            diagnostics["well_id"] = row.get("well_id", "UNKNOWN")
            diagnostics["geometry_errors"] = row.get("geometry_errors", [])

            buffer.append(diagnostics)

        except Exception as e:
            logging.warning(f"Row failed: {e}")
            error_count += 1

    if buffer:
        if not table_created_flag["created"]:
            create_table_from_schema(buffer[0])
            table_created_flag["created"] = True

        # ✅ FIX: insert_batch should only take buffer unless you update the signature
        insert_batch(buffer)

        logging.info(f"Inserted batch with {len(buffer)} rows, {error_count} errors")

    return error_count


def process_historical_file(filepath, batch_size=100, insert_every=100):
    run_id = str(uuid.uuid4())
    file_name = os.path.basename(filepath)
    source_type = os.path.splitext(file_name)[-1].lstrip(".").upper()
    logging.info(f"Starting ingestion for {file_name} with run_id: {run_id}")
    table_created_flag = {"created": False}
    start_time = time.time()

    batches = list(read_batches(filepath, batch_size))
    total_rows = sum(len(batch) for batch in batches)
    error_count = 0

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_batch, batch, run_id, table_created_flag) for batch in batches]
        for future in as_completed(futures):
            try:
                error_count += future.result()
            except Exception as e:
                logging.exception(f"Batch failed: {e}")
                error_count += 1

    duration = round(time.time() - start_time, 2)
    status = "SUCCESS" if error_count == 0 else "PARTIAL"

    log_ingestion_metadata(
        run_id,
        file_name,
        "UNKNOWN",
        source_type,
        total_rows,
        error_count,
        duration,
        status
    )

    logging.info(f"Ingestion complete for {file_name} - {total_rows} rows, {error_count} errors, {duration}s")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python historical_feed.py <path_to_file> [insert_every]")
        sys.exit(1)

    filepath = sys.argv[1]
    insert_every = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    process_historical_file(filepath, batch_size=100, insert_every=insert_every)
