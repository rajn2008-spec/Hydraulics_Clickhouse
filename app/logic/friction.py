import math

# -----------------------------
# Fanning Friction Factor (Imperial)
# -----------------------------

def fanning_factor_pipe_collar_laminar(Re: float) -> dict:
    return {"f": 16.0/Re} if Re and Re > 0 else {"f": 0.0}

def fanning_factor_annulus_laminar(Re: float) -> dict:
    return {"f": 24.0/Re} if Re and Re > 0 else {"f": 0.0}



def fanning_factor_pipe_collar_turbulent(Re: float, n_s: float) -> dict:
    """
    Eq-19: Fanning friction factor for turbulent flow inside drill pipe/collar.

    Formula:
        f = (log10(n_s) + 3.93) / [ 50 * Re * ((1.75 - log10(n_s)) / 7) ]

    Returns dict keyed by canonical OutputData symbol 'f'.
    """
    if (
        Re is None or Re <= 0 or
        n_s is None or n_s <= 0
    ):
        return {"f": 0.0}

    log_ns = math.log10(n_s)
    denom = 50.0 * Re * ((1.75 - log_ns) / 7.0)
    f = (log_ns + 3.93) / denom
    return {"f": f}




def fanning_friction_turbulent_annulus(Re: float, n_a: float) -> dict:
    """
    Eq-20: Fanning friction factor for turbulent flow in annulus.

    Formula:
        f = (log10(n_a) + 3.93) / [ 50 * Re * ((1.75 - log10(n_a)) / 7) ]

    Returns dict keyed by canonical OutputData symbol 'f'.
    """
    if (
        Re is None or Re <= 0 or
        n_a is None or n_a <= 0
    ):
        return {"f": 0.0}

    log_na = math.log10(n_a)
    denom = 50.0 * Re * ((1.75 - log_na) / 7.0)
    f = (log_na + 3.93) / denom
    return {"f": f}


def fanning_factor_pipe_collar_transitional(Re: float, Re_smin: float, Re_smax: float, n_s: float) -> float:
    """
    Eq-17 (correct grouping):
      A = (log10(n_s) + 3.93) / ( ((1.75 - log10(n_s)) / 7) * (50 * Re_smax) )
      f = ((Re - Re_smin) / 800) * ( A - 16/Re_smin ) + 16/Re_smin
    """
    # Gates
    if Re is None or Re_smin is None or Re_smax is None or n_s is None:
        return 0.0
    if Re <= 0 or Re_smin <= 0 or Re_smax <= 0 or n_s <= 0:
        return 0.0

    log_ns = math.log10(n_s)
    denom = ((1.75 - log_ns) / 7.0) * (50.0 * Re_smax)
    A = (log_ns + 3.93) / denom

    F = ((Re - Re_smin) / 800.0) * (A - (16.0 / Re_smin)) + (16.0 / Re_smin)
    return F



def fanning_friction_transitional_annulus(Re: float, Re_amin: float, Re_amax: float, n_a: float) -> dict:
    """
    Eq-18: Fanning friction factor for transitional flow in annulus.

    A = (log10(n_a) + 3.93) / [ ((1.75 - log10(n_a)) / 7) * (50 * Re_amax) ]
    f = ((Re - Re_amin) / 800) * (A - 24/Re_amin) + 24/Re_amin

    Returns dict keyed by canonical OutputData symbol 'f'.
    """
    if (
        Re is None or Re_amin is None or Re_amax is None or n_a is None or
        Re <= 0 or Re_amin <= 0 or Re_amax <= 0 or n_a <= 0
    ):
        return {"f": 0.0}

    log_na = math.log10(n_a)
    denom = ((1.75 - log_na) / 7.0) * (50.0 * Re_amax)
    A = (log_na + 3.93) / denom

    laminar_tail = 24.0 / Re_amin
    f = ((Re - Re_amin) / 800.0) * (A - laminar_tail) + laminar_tail
    return {"f": f}

