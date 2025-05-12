from variables import cfg
from functions.permeability import krw, krg

def fw(Sw, nD, k):
    lw = k * krw(Sw) / cfg["mu_w"]
    lg = k * krg(Sw, nD) / cfg["mu_g"]
    return lw / (lw + lg + 1e-12)
