from simulator import run_simulation, run_simulation_with_progress
from solver.velocity import calculate_velocity, analyze_constant_velocity, moving_average, smooth_speed
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

    smooth_w = 51
    

    vel_sw1, vel_sw2 = calculate_velocity(Sw1_all, x, params), calculate_velocity(Sw2_all, x, params)

    cfg = params["cfg"]
    dt = (cfg["tmax"] - cfg["tmin"]) / (Sw1_all.shape[0] - 1)
    t_vel = np.arange(len(vel_sw1)) * dt

    v_sw1_smooth = smooth_speed(vel_sw1, smooth_w)
    v_sw2_smooth = smooth_speed(vel_sw2, smooth_w)

    plot_simulation_and_report(Sw1_all, Sw2_all, x, t_vel, v_sw1_smooth, v_sw2_smooth, dt)

