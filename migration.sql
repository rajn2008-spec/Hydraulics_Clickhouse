-- Drop the old table if it exists
DROP TABLE IF EXISTS diagnostics_results;

-- Recreate with full schema
CREATE TABLE diagnostics_results (
    -- InputData fields
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
    well_id String,

    -- OutputData fields
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

    -- Metadata
    missing_inputs String,
    timestamp DateTime,
    source String
) ENGINE = MergeTree()
ORDER BY (well_id, timestamp);

