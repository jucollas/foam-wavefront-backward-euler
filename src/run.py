from simulator import run_simulation, run_simulation_with_progress
from plotter import plot_full_simulation
import numpy as np
import os

if __name__ == "__main__":
    from variables import params

    # Define the path where simulation data will be stored or loaded from
    data_path = os.path.join("data", "saturation_data.npy")

    try:
        # Try to load existing simulation data
        result = np.load(data_path)
        Nx = params["Nx"]
        Sw1_all, Sw2_all = result[:, :Nx], result[:, Nx:]
        x = params["x"]

    except FileNotFoundError:
        # If file not found, run the simulation with progress bar and save result
        # Sw1_all, Sw2_all, x = run_simulation(data_path)  # Without progress bar
        Sw1_all, Sw2_all, x = run_simulation_with_progress(data_path)  # With progress bar

    # Plot the full simulation results
    plot_full_simulation(Sw1_all, Sw2_all, x)
