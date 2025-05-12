import numpy as np
from variables import params
from functions.permeability import nD_eq
from functions.flux import fw

def saturation_derivative(t, S):
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
