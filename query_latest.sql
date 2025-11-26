CREATE TABLE cuttings_transport (
  timestamp DateTime DEFAULT now(),
  source String,
  depth Float64,
  annular_velocity Float64,
  slip_velocity Float64,
  transport_ratio Float64,
  cuttings_concentration Float64,
  hole_diameter Float64,
  pipe_od Float64,
  flow_rate Float64,
  mud_density Float64,
  plastic_viscosity Float64,
  yield_point Float64
) ENGINE = MergeTree()
ORDER BY timestamp;

