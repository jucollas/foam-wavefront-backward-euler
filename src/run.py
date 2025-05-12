from simulator import run_simulation, run_simulation_with_progress
from plotter import plot_full_simulation
import numpy as np
import os

if __name__ == "__main__":
    from variables import params
    data_path = os.path.join("data", "saturation_data.npy")

    try:
        result = np.load(data_path)
        Nx = params["Nx"]
        Sw1_all, Sw2_all = result[:, :Nx], result[:, Nx:]
        x = params["x"]
    except FileNotFoundError:
        # Sw1_all, Sw2_all, x = run_simulation(data_path)
        Sw1_all, Sw2_all, x = run_simulation_with_progress(data_path)

    plot_full_simulation(Sw1_all, Sw2_all, x)
