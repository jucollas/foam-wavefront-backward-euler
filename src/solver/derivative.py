import numpy as np
from variables import params
from functions.permeability import nD_eq
from functions.flux import fw

def saturation_derivative(t, S):
    """
    Computes the time derivative of water saturation in a two-layer porous medium system.

    This function models the transport of water through two horizontal layers using the 
    fractional flow formulation, foam effects, and interlayer coupling. 
    It includes advective, diffusive, and source/sink terms.

    Args:
        t (float): Time (not used explicitly, required for ODE solver compatibility).
        S (ndarray): Flattened array of water saturations, consisting of two layers:
            - S[:Nx]: Saturation in layer 1.
            - S[Nx:]: Saturation in layer 2.

    Returns:
        ndarray: Concatenated time derivative of saturations for both layers.

    Constants and parameters used:
        - cfg["phi"]: Porosity.
        - cfg["u1"], cfg["u2"]: Superficial velocities in layers 1 and 2.
        - cfg["k1"], cfg["k2"]: Permeabilities in layers 1 and 2.
        - cfg["theta_s"]: Interlayer exchange coefficient.
        - dx: Spatial discretization step.
        - diff_coef: Diffusion coefficient.
    """
    cfg, dx, Nx, diff_coef = params["cfg"], params["dx"], params["Nx"], params["diff_coef"]
    Sw1, Sw2 = S[:Nx], S[Nx:]
    dSw1, dSw2 = np.zeros_like(Sw1), np.zeros_like(Sw2)

    nD1, nD2 = nD_eq(Sw1), nD_eq(Sw2)
    fw1, fw2 = fw(Sw1, nD1, cfg["k1"]), fw(Sw2, nD2, cfg["k2"])

    for i in range(1, Nx - 1):
        dSw1[i] = (
            - cfg["u1"] * (fw1[i] - fw1[i-1]) / dx
            - cfg["theta_s"] * (Sw1[i] - Sw2[i])
            + diff_coef * (Sw1[i+1] - 2*Sw1[i] + Sw1[i-1]) / dx**2
        ) / cfg["phi"]

        dSw2[i] = (
            - cfg["u2"] * (fw2[i] - fw2[i-1]) / dx
            + cfg["theta_s"] * (Sw1[i] - Sw2[i])
            + diff_coef * (Sw2[i+1] - 2*Sw2[i] + Sw2[i-1]) / dx**2
        ) / cfg["phi"]

    return np.concatenate([dSw1, dSw2])
