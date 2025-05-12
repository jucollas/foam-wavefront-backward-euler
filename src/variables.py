from config_loader import load_config
import numpy as np

cfg = load_config()

# Mesh and space-related variables
Nx = cfg["Nx"]
L = cfg["L"]
x = np.linspace(0, L, Nx)
dx = L / Nx
diff_coef = cfg["diff_scale"] * dx**2

# Grouped for reuse
params = {
    "Nx": Nx,
    "L": L,
    "x": x,
    "dx": dx,
    "cfg": cfg,
    "diff_coef": diff_coef
}
