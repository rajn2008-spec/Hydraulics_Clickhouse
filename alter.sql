ALTER TABLE diagnostics_results MODIFY COLUMN velocity Nullable(Float64);
ALTER TABLE diagnostics_results MODIFY COLUMN viscosity Nullable(Float64);
ALTER TABLE diagnostics_results MODIFY COLUMN density Nullable(Float64);
ALTER TABLE diagnostics_results MODIFY COLUMN diameter Nullable(Float64);
ALTER TABLE diagnostics_results MODIFY COLUMN Re Nullable(Float64);

