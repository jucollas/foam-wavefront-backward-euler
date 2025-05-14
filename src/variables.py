from config_loader import load_config
import numpy as np

# Load configuration dictionary from JSON file
cfg = load_config()

# Mesh and space-related variables
Nx = cfg["Nx"]  # Number of spatial cells
L = cfg["L"]    # Total length of the domain [m]
x = np.linspace(0, L, Nx)  # Discretized spatial domain
dx = L / Nx     # Cell width
diff_coef = cfg["diff_scale"] * dx**2  # Numerical diffusion coefficient

# Grouped parameter dictionary for reuse across modules
params = {
    "Nx": Nx,             # Number of cells
    "L": L,               # Length of the domain
    "x": x,               # Spatial grid
    "dx": dx,             # Grid spacing
    "cfg": cfg,           # Configuration parameters loaded from file
    "diff_coef": diff_coef  # Diffusion coefficient used in the derivative
}
