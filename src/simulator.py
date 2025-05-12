import numpy as np
from tqdm import tqdm
from solver.euler import euler_method, euler_method_with_progress
from solver.derivative import saturation_derivative
from variables import params

def run_simulation(save_path='data/saturation_data.npy'):
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

