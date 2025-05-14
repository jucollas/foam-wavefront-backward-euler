import numpy as np
from tqdm import tqdm
from solver.euler import euler_method, euler_method_with_progress
from solver.derivative import saturation_derivative
from variables import params

def run_simulation(save_path='data/saturation_data.npy'):
    """
    Runs the full simulation without displaying progress.

    Solves the saturation evolution equations using the Euler method 
    and saves the results to a file. The initial condition consists of 
    uniform initial saturation with injection saturation at the inlet.

    Args:
        save_path (str, optional): Path to save the saturation data. 
            Default is 'data/saturation_data.npy'.

    Returns:
        tuple: A tuple containing three elements:
            - Sw1_all (ndarray): 2D array of saturation in layer 1 over time.
            - Sw2_all (ndarray): 2D array of saturation in layer 2 over time.
            - x (ndarray): 1D array representing the spatial domain.
    """
    cfg = params["cfg"]
    Nx = params["Nx"]

    S0 = np.ones(2 * Nx) * cfg["Sw_ini"]
    S0[0] = cfg["Sw_inj"]
    S0[Nx] = cfg["Sw_inj"]

    tpart = int((cfg["tmax"] - cfg["tmin"]) * cfg["time_steps_per_unit"])
    result = euler_method(saturation_derivative, S0, cfg["tmin"], cfg["tmax"], tpart, cfg["refinements"])

    np.save(save_path, result)
    return result[:, :Nx], result[:, Nx:], params["x"]


def run_simulation_with_progress(save_path='data/saturation_data.npy'):
    """
    Runs the full simulation with a progress bar.

    This function is similar to `run_simulation`, but includes a tqdm 
    progress bar to monitor the simulation progress. It uses the refined 
    Euler method to solve the saturation evolution equations.

    Args:
        save_path (str, optional): Path to save the saturation data. 
            Default is 'data/saturation_data.npy'.

    Returns:
        tuple: A tuple containing three elements:
            - Sw1_all (ndarray): 2D array of saturation in layer 1 over time.
            - Sw2_all (ndarray): 2D array of saturation in layer 2 over time.
            - x (ndarray): 1D array representing the spatial domain.
    """
    cfg = params["cfg"]
    Nx = params["Nx"]

    S0 = np.ones(2 * Nx) * cfg["Sw_ini"]
    S0[0] = cfg["Sw_inj"]
    S0[Nx] = cfg["Sw_inj"]

    tpart = int((cfg["tmax"] - cfg["tmin"]) * cfg["time_steps_per_unit"])

    with tqdm(total=tpart, desc="Solving", unit="step") as pbar:
        result = euler_method_with_progress(saturation_derivative, S0, cfg["tmin"], cfg["tmax"], tpart, cfg["refinements"], pbar)
    
    np.save(save_path, result)
    
    return result[:, :Nx], result[:, Nx:], params["x"]
