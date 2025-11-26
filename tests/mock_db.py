# tests/mock_db.py

def push_to_clickhouse(log: dict):
    """Mock ClickHouse insert for testing."""
    print("Mock insert:", log)
