# Annular Hydraulics Workflow Flowchart
## Section 3.5.11 - Based on Engineering Specification

## Process Notation Legend
```
┌─────────────────────────────────────────────────────────────┐
│ Each process box contains two numbers:                       │
│                                                              │
│ [Left Number]  = Total outputs from that process            │
│ [Right Number] = Real-time outputs (in parentheses)         │
└─────────────────────────────────────────────────────────────┘
```

## Main Flowchart

```
                          ╔═══════════════════════╗
                          ║ Start Annular         ║
                          ║ Hydraulics            ║
                          ╚═════════╤═════════════╝
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                    ▼                                ▼
         ┌──────────────────────┐     ┌──────────────────────────┐
         │   Velocity           │     │   Rheology Constants     │
         │   V(0)               │     │   A(0)                   │
         └──────────┬───────────┘     └────────┬─────────────────┘
                    │                         │
                    │              ┌──────────┴─────────┬─────────┐
                    │              │                    │         │
                    │              ▼                    ▼         ▼
                    │    ┌──────────────────────┐  ┌──────────────────┐
                    │    │ Effective Viscosity  │  │ Critical Reynolds│
                    │    │ δ(b)                 │  │ λ(0)             │
                    │    └──────────────────────┘  └──────────┬───────┘
                    │                                         │
                    │                          ┌──────────────┴──────┐
                    │                          │                     │
                    │                          ▼                     ▼
                    │                ┌──────────────────────┐  ┌──────────────────┐
                    │                │ Flow Regime          │  │ Critical Annular │
                    │                │ ψ(0)                 │  │ Velocity         │
                    │                └──────────────────────┘  │ ν(0)             │
                    │                                          └────────┬─────────┘
                    │                                                   │
                    │                                    ┌──────────────┘
                    │                                    │
                    ▼                                    ▼
         ┌──────────────────────┐          ┌──────────────────────────┐
         │ Reynolds Number      │          │ Critical Flow Rate       │
         │ δ(0)                 │          │ ∑(0)                     │
         └──────────┬───────────┘          └──────────────────────────┘
                    │
                    └────────────┐
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │ Flow Regime          │
                    │ ψ(0)                 │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
    ┌──────────────────────┐      ┌──────────────────────┐
    │ Fanning Friction     │      │ (Alternative Path)   │
    │ Factor               │      │                      │
    │ ζ(0)                 │      └──────────────────────┘
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ Pressure Loss        │
    │ ∇p(0)                │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────────────────┐
    │ Pressure Loss Due to Friction    │
    │ δ(0)                             │
    └──────────┬───────────────────────┘
               │
               ▼
    ┌──────────────────────────────────┐
    │ Equivalent Circulating Density   │
    │ ξ(1)                             │
    └──────────┬───────────────────────┘
               │
               ▼
        ╔═══════════════════════╗
        ║ End Annular           ║
        ║ Hydraulics            ║
        ╚═══════════════════════╝
```

## Detailed Process Steps

### **Input Stage**
| Process | Variable | Description | Outputs |
|---------|----------|-------------|---------|
| Velocity Input | V(0) | Annular flow velocity | δ(0), ∇p(0) |
| Rheology Input | A(0) | Power law constants (n, K) | δ(b), λ(0), ν(0) |

### **Calculation Stage**
| Step | Process | Variable | Inputs | Outputs |
|------|---------|----------|--------|---------|
| 1 | Effective Viscosity | δ(b) | A(0) | λ(0), ψ(0) |
| 2 | Critical Reynolds | λ(0) | δ(b) | ν(0), ψ(0), ζ(0) |
| 3 | Critical Annular Velocity | ν(0) | λ(0) | ∑(0) |
| 4 | Reynolds Number | δ(0) | V(0) | ψ(0), ζ(0) |
| 5 | Flow Regime | ψ(0) | δ(0), λ(0) | ζ(0) |
| 6 | Critical Flow Rate | ∑(0) | ν(0) | (output only) |
| 7 | Fanning Friction Factor | ζ(0) | ψ(0), δ(0) | ∇p(0) |
| 8 | Pressure Loss | ∇p(0) | ζ(0), V(0) | δ(0) |
| 9 | Pressure Loss Due to Friction | δ(0) | ∇p(0) | ξ(1) |
| 10 | ECD | ξ(1) | δ(0) | Final Output |

## Variable Mapping

```
VARIABLE NOTATION:
  V(0)  = Velocity (input)
  A(0)  = Rheology Constants (Power Law: n, K)
  δ(b)  = Effective Viscosity
  λ(0)  = Critical Reynolds Number
  ν(0)  = Critical Annular Velocity
  δ(0)  = Reynolds Number (or Pressure Loss due to Friction)
  ψ(0)  = Flow Regime (Laminar/Turbulent)
  ∑(0)  = Critical Flow Rate
  ζ(0)  = Fanning Friction Factor
  ∇p(0) = Pressure Loss Gradient
  ξ(1)  = Equivalent Circulating Density (ECD) - FINAL OUTPUT

SUBSCRIPTS:
  (0)  = Process state zero
  (1)  = Process state one
  (b)  = Base/Bulk state
```

## Detailed Data Flow

### **Path 1: Velocity → Reynolds Number → Flow Regime**
```
Velocity (V)
    ↓
Reynolds Number (Re = ρ·V·D_h/μ)
    ↓
    ├─→ Flow Regime Classification (Laminar/Turbulent)
    └─→ Fanning Friction Factor (f)
```

### **Path 2: Power Law Constants → Effective Viscosity → Critical Reynolds**
```
Power Law Constants (n, K)
    ↓
Effective Viscosity (μ_eff)
    ↓
Critical Reynolds Number (Re_c)
    ↓
    ├─→ Critical Annular Velocity (V_c)
    ├─→ Flow Regime Classification
    └─→ Fanning Friction Factor (f)
```

### **Path 3: Critical Annular Velocity → Flow Rate**
```
Critical Annular Velocity (V_c)
    ↓
Critical Annular Flow Rate (Q_c = V_c × A)
```

### **Path 4: Reynolds Number → Flow Properties**
```
Reynolds Number (Re)
    ↓
    ├─→ Flow Regime (Laminar/Turbulent)
    └─→ Fanning Friction Factor (f)
```

### **Path 5: Pressure Loss → ECD**
```
Pressure Loss Gradient (∇p) / Pressure Loss Due to Friction (ΔP_f)
    ↓
Equivalent Circulating Density (ECD = ρ + ΔP_f/(0.052·D))
```

## Summary of Calculations

| **Step** | **Input** | **Calculation** | **Output** |
|----------|-----------|-----------------|-----------|
| 1 | V, ρ, D_h, μ | Re = ρ·V·D_h/μ | Reynolds Number |
| 2 | n, K, γ | μ_eff = K·γ^(n-1) | Effective Viscosity |
| 3 | Re | Classify based on Re critical | Flow Regime |
| 4 | Re, D_h | f = f(Re, D_h/ε) | Fanning Friction Factor |
| 5 | V_c, A | Q_c = V_c × A | Critical Flow Rate |
| 6 | f, ΔL, ρ, V, D_h | ΔP_f = f·(ΔL/D_h)·(ρ·V²/2gc) | Pressure Loss |
| 7 | ΔP_f, ρ | ECD = ρ + (ΔP_f/(0.052·D)) | Equivalent Circulating Density |

## Key Relationships

- **Reynolds Number (Re)**: Determines flow regime and friction factor
- **Effective Viscosity (μ_eff)**: Depends on power law constants and shear rate
- **Critical Reynolds (Re_c)**: Threshold between laminar and turbulent flow
- **Flow Regime**: Determines friction factor calculation method
- **Pressure Loss Gradient**: Accumulates into total pressure drop
- **ECD**: Final output depending on total pressure loss

---

**Please share your comparison flowchart or reference document so I can compare and validate this against your engineering specifications.**
