# utils/db.py
import os
import logging
import re
from datetime import datetime, timezone
from clickhouse_driver import Client

# -----------------------------
# Client Setup
# -----------------------------
clickhouse_host = os.getenv("CLICKHOUSE_HOST", "localhost")
clickhouse_port = int(os.getenv("CLICKHOUSE_PORT", "9000"))
client = Client(host=clickhouse_host, port=clickhouse_port)

USE_REAL_DB = True

logging.info(f"ClickHouse client initialized with host={clickhouse_host}, port={clickhouse_port}")

# -----------------------------
# Safe Float Conversion
# -----------------------------
def safe_float(value) -> float:
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = re.search(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', value)
        return float(m.group(0)) if m else 0.0
    return 0.0

# -----------------------------
# Missing Input Check
# -----------------------------
def check_missing_inputs(row: dict, required_keys: list[str]) -> dict:
    missing = {}
    for key in required_keys:
        val = row.get(key)
        if val is None or (isinstance(val, (int, float)) and val == 0.0):
            missing[key] = "missing or zero"
    return missing

# -----------------------------
# Minimal Insert
# -----------------------------
def push_to_clickhouse(data: dict):
    """
    Lightweight insert for connectivity testing.
    """
    if USE_REAL_DB:
        try:
            query = """
                INSERT INTO diagnostics_results (V, mu, density, dh, Re, timestamp, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            payload = [
                (
                    safe_float(data.get("V")),
                    safe_float(data.get("mu")),
                    safe_float(data.get("rho")),
                    safe_float(data.get("dh")),
                    safe_float(data.get("Re")),
                    datetime.now(timezone.utc),
                    data.get("source", "test")
                )
            ]
            client.execute(query, payload, types_check=True)
            logging.info("✅ Minimal insert into ClickHouse succeeded")
        except Exception:
            logging.exception("❌ Minimal insert failed")
    else:
        logging.info("📋 Mock insert payload:")
        for k, val in data.items():
            logging.info(f"  {k}: {val}")

# -----------------------------
# Full Diagnostics Insert
# -----------------------------
def insert_diagnostics(row: dict):
    """
    Full insert aligned to canonical ASCII schema.
    """
    allowed_fields = [
        "dh", "dc", "dpi", "dpo", "dci", "dco",
        "Q", "phi600", "phi300", "phi3", "P",
        "Dmd", "Dtvd", "Ldp", "Ldc", "Lc", "J",
        "dcut", "T", "ROP", "t", "Ls", "Dbo", "Dbp", "tau30",
        "V", "n", "k", "mu", "Re", "Remax", "Vcrit", "Qcrit",
        "f", "dp_L", "dp", "ECD", "A", "Vjet", "dpb", "PA",
        "Fi", "gb", "tp", "gp", "Vs", "Vt", "Et", "C",
        "Vp", "Ve", "rhoe", "Pg",
        "timestamp", "source"
    ]

    filtered = {}
    for k in allowed_fields:
        if k in row:
            val = row[k]
            if isinstance(val, (int, float)):
                filtered[k] = safe_float(val)
            elif isinstance(val, str):
                filtered[k] = val
            else:
                filtered[k] = "" if k in ["source", "timestamp"] else 0.0

    columns = ", ".join(f"`{c}`" for c in filtered.keys())
    values = [filtered[k] for k in filtered]

    if USE_REAL_DB:
        try:
            client.execute(
                f"INSERT INTO diagnostics_results ({columns}) VALUES",
                [values]
            )
            logging.info("✅ Full diagnostics insert into ClickHouse succeeded")
        except Exception:
            logging.exception("❌ Full diagnostics insert failed")
    else:
        logging.info("📋 Mock full insert payload:")
        for k, val in filtered.items():
            logging.info(f"  {k}: {val}")
