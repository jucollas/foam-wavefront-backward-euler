import numpy as np
from variables import cfg

def nD_eq(Sw):
    """
    Computes the dimensionless variable nD used in the foam model.

    Returns `tanh(A * (Sw - Sw_star))` when Sw > Sw_star, and 0 otherwise.
    This function represents a smooth transition regulating foam strength based on water saturation.

    Args:
        Sw (ndarray): Water saturation.

    Returns:
        ndarray: Values of nD for each Sw input.

    Constants used:
        - A: Foam model parameter.
        - Sw_star: Critical water saturation.
    """
    return np.where(Sw > cfg["Sw_star"], np.tanh(cfg["A"] * (Sw - cfg["Sw_star"])), 0.0)


def krw(Sw):
    """
    Computes the relative permeability to water (krw) using an empirical model.

    Applies a power-law relationship based on water saturation.
    If Sw <= Swc (connate water saturation), permeability is set to 0.

    Args:
        Sw (ndarray): Water saturation.

    Returns:
        ndarray: Relative permeability to water.

    Constants used:
        - Swc: Connate water saturation.
        - Sgr: Residual gas saturation.
    """
    return np.where(Sw <= cfg["Swc"], 0.0,
                    0.2 * ((Sw - cfg["Swc"]) / (1 - cfg["Swc"] - cfg["Sgr"]))**4.2)


def krg0(Sw):
    """
    Computes the relative permeability to gas in the absence of foam (krg0).

    Uses a power-law based function depending on water saturation.
    If Sw >= 1 - Sgr (fully saturated with water), permeability is set to 0.

    Args:
        Sw (ndarray): Water saturation.

    Returns:
        ndarray: Relative gas permeability without foam effects.

    Constants used:
        - Swc: Connate water saturation.
        - Sgr: Residual gas saturation.
    """
    return np.where(Sw >= 1 - cfg["Sgr"], 0.0,
                    0.94 * ((1 - Sw - cfg["Sgr"]) / (1 - cfg["Swc"] - cfg["Sgr"]))**1.3)


def MRF(nD):
    """
    Computes the Mobility Reduction Factor (MRF) due to foam effects.

    This factor increases with nD, indicating higher foam presence and thus lower gas mobility.
    The result is clipped between 1 and 1e6 to ensure numerical stability.

    Args:
        nD (ndarray): Dimensionless foam control variable.

    Returns:
        ndarray: Foam-based gas mobility reduction factor.
    """
    return np.clip(18500 * nD + 1, 1, 1e6)


def krg(Sw, nD):
    """
    Computes the relative permeability to gas considering foam effects.

    The foam reduces gas mobility by dividing the base gas permeability (krg0) by MRF(nD).

    Args:
        Sw (ndarray): Water saturation.
        nD (ndarray): Dimensionless variable nD (from `nD_eq`).

    Returns:
        ndarray: Relative permeability to gas with foam effects.
    """
    return krg0(Sw) / MRF(nD)
