DROP TABLE IF EXISTS diagnostics_results;

CREATE TABLE diagnostics_results (
    -- Identifiers & metadata
    well_id String,
    timestamp DateTime,
    source String,
    missing_inputs String,

    -- Raw inputs / geometry
    dh Float64,
    dc Float64,
    ddpi Float64,
    ddpo Float64,
    ddci Float64,
    ddco Float64,
    Q Float64,
    e600 Float64,
    v0300 Float64,
    v03 Float64,
    P Float64,
    Dmd Float64,
    Dvd Float64,
    Ldp Float64,
    Ldc Float64,
    Lc Float64,
    J Float64,
    dcut Float64,
    T Float64,
    ROP Float64,
    t Float64,
    Ls Float64,
    Doc Float64,
    Dbp Float64,
    T30 Float64,
    tvd Float64,

    -- Drillstring / casing / bit
    drill_pipe Float64,
    drill_collar Float64,
    casing Float64,
    bit Float64,
    mud_weight_profile String,

    -- Intermediate diagnostics
    velocity Float64,
    velocity_drill_pipe Float64,
    velocity_drill_collar Float64,
    velocity_drillstring_avg Float64,
    velocity_annulus_ftmin Float64,
    mu_eff_drill_pipe Float64,
    mu_eff_drill_collar Float64,
    mu_eff_drillstring_avg Float64,
    mu_eff_annulus Float64,
    hydrostatic_pressure Float64,
    viscosity Float64,
    density Float64,

    -- Rheology & hydraulics outputs
    V Float64,
    n Float64,
    k Float64,
    mu Float64,
    Re Float64,
    Remax Float64,
    Verit Float64,
    Qcrit Float64,
    f Float64,
    A_p_L Float64,
    Ap Float64,
    ECD Float64,
    A Float64,
    Vjet Float64,
    Apb Float64,
    P_hp Float64,
    PA Float64,
    Fi Float64,
    Yb Float64,
    Tp Float64,
    Yp Float64,
    Vs Float64,
    Vt Float64,
    Et Float64,
    C Float64,
    Vp Float64,
    Ve Float64,
    Pe Float64,
    Pg Float64,

    -- Cuttings transport metrics
    slip_velocity Float64,
    transport_ratio Float64,
    cuttings_concentration Float64,

    -- Swab/surge metrics
    surge_pressure Float64,
    swab_pressure Float64
) ENGINE = MergeTree()
ORDER BY (well_id, timestamp);

