docker exec -i clickhouse-server clickhouse-client --query "
CREATE TABLE diagnostics_results (
    run_id UUID,
    timestamp DateTime,
    annular_velocity Float64,
    superficial_velocity Float64,
    flow_behavior_index Float64,
    consistency_index Float64,
    effective_viscosity Float64,
    reynolds_number Float64,
    flow_regime String,
    critical_annular_velocity Float64,
    pressure_loss_gradient Float64,
    pressure_loss_friction Float64,
    equivalent_circulating_density Float64,
    audit_raw_inputs JSON,
    audit_normalized_inputs JSON
) ENGINE = MergeTree
ORDER BY timestamp;"

