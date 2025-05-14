from variables import cfg
from functions.permeability import krw, krg

def fw(Sw, nD, k):
    """
    Computes the fractional flow of water (fw) in a two-phase (water-gas) system with foam.

    This function calculates the ratio of water mobility to the total mobility (water + gas),
    considering the presence of foam, which reduces gas mobility via the MRF.

    Args:
        Sw (ndarray): Water saturation.
        nD (ndarray): Dimensionless foam parameter (computed from `nD_eq`).
        k (float or ndarray): Absolute permeability of the layer.

    Returns:
        ndarray: Water fractional flow (values between 0 and 1).

    Constants used:
        - mu_w: Water viscosity.
        - mu_g: Gas viscosity (without foam).
    """
    lw = k * krw(Sw) / cfg["mu_w"]
    lg = k * krg(Sw, nD) / cfg["mu_g"]
    return lw / (lw + lg + 1e-12)
