# tests/conftest.py
def build_payload(depth: int, use_profile: bool = False) -> dict:
    base = {
        "depth": depth,
        "Q": 500,
        "phi600": 60,
        "phi300": 30,
        "Dtvd": 10000,
        "drill_pipe": [{"id": 4.0, "od": 5.0, "depth_from": 0, "depth_to": 10000}],
        "drill_collar": [{"id": 2.5, "od": 6.5, "depth_from": 0, "depth_to": 10000}],
        "casing": [{"id": 8.5, "depth_from": 0, "depth_to": 10000}],
        "bit": [{"od": 8.5, "depth_from": 0, "depth_to": 10000}],
    }
    if use_profile:
        base["mud_weight_profile"] = [
            {"weight_from": 11.5, "weight_to": 12.0, "depth_from": 0, "depth_to": 5000},
            {"weight_from": 12.0, "weight_to": 12.5, "depth_from": 5000, "depth_to": 10000}
        ]
        base["rho"] = 12.0  # average mud weight
    else:
        base["rho"] = 12.0

    return base
