from simulator import run_simulation, run_simulation_with_progress
from solver.velocity import calculate_velocity, analyze_constant_velocity, moving_average
from plotter import plot_full_simulation, plot_simulation_and_report
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

    vel_sw1, vel_sw2 = calculate_velocity(Sw1_all, x, params), calculate_velocity(Sw2_all, x, params)
    v1_s = moving_average(vel_sw1[np.isfinite(vel_sw1)], w=25)
    v2_s = moving_average(vel_sw2[np.isfinite(vel_sw2)], w=25)
    mean_v1, std_v1, rel1 = analyze_constant_velocity(v1_s)
    mean_v2, std_v2, rel2 = analyze_constant_velocity(v2_s)


    # Plot the full simulation results
    #plot_full_simulation(Sw1_all, Sw2_all, x, params, vel_sw1, vel_sw2, stride=50, pause_time=0.05)
    plot_simulation_and_report(Sw1_all, Sw2_all, x, vel_sw1, vel_sw2, params)

