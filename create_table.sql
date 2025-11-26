CREATE TABLE diagnostics_results (
    velocity Float64,
    viscosity Float64,
    density Float64,
    diameter Float64
) ENGINE = MergeTree()
ORDER BY velocity;

