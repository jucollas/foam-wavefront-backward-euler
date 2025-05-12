import numpy as np
from variables import cfg

def nD_eq(Sw):
    return np.where(Sw > cfg["Sw_star"], np.tanh(cfg["A"] * (Sw - cfg["Sw_star"])), 0.0)

def krw(Sw):
    return np.where(Sw <= cfg["Swc"], 0.0, 0.2 * ((Sw - cfg["Swc"]) / (1 - cfg["Swc"] - cfg["Sgr"]))**4.2)

def krg0(Sw):
    return np.where(Sw >= 1 - cfg["Sgr"], 0.0, 0.94 * ((1 - Sw - cfg["Sgr"]) / (1 - cfg["Swc"] - cfg["Sgr"]))**1.3)

def MRF(nD):
    return np.clip(18500 * nD + 1, 1, 1e6)

def krg(Sw, nD):
    return krg0(Sw) / MRF(nD)
