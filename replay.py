import uuid
import logging
from datetime import datetime

from historical_feed import read_batches
from app.logic.diagnostics import run_diagnostics_basic
from app.logic.normalize import normalize_inputs
from utils.db import insert_batch, log_ingestion_metadata

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def process_historical_file(filepath, batch_size=100):
    run_id = str(uuid.uuid4())
    file_name = filepath.split("/")[-1]
    source_type = file_name.split(".")[-1].upper()
    logging.info(f"Starting replay for {file_name} with run_id: {run_id}")

    total_rows = 0
    error_count = 0
    buffer = []

    for batch in read_batches(filepath, batch_size):
        processed = []
        for row in batch:
            try:
                normalized = normalize_inputs(row)["normalized"]
                row.update(normalized)

                diagnostics = run_diagnostics_basic(row).model_dump(exclude_none=True)
                diagnostics["run_id"] = run_id
                diagnostics["timestamp"] = datetime.utcnow()
                diagnostics["source"] = "replay"
                diagnostics["well_id"] = row.get("well_id", "UNKNOWN")

                processed.append(diagnostics)
            except Exception as e:
                logging.warning(f"[WARN] Row failed: {e}")
                error_count += 1

        if processed:
            # FIX: insert_batch only takes one argument
            insert_batch(processed)
            buffer.extend(processed)
            total_rows += len(processed)

    status = "SUCCESS" if error_count == 0 else "PARTIAL"
    log_ingestion_metadata(
        run_id,
        file_name,
        "UNKNOWN",
        source_type,
        total_rows,
        error_count,
        0,
        status
    )

    logging.info(f"Replay complete for {file_name} - {total_rows} rows, {error_count} errors")
