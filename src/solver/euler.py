import numpy as np
from tqdm import tqdm

def euler_method(f, x0, tmin, tmax, tpart, refin=10):
    """
    Solves an ODE system using the implicit backward Euler method with fixed-point refinement.

    This method computes the numerical solution of a differential equation using 
    the backward Euler scheme. The implicit step is approximated iteratively 
    using a fixed number of refinement iterations.

    Args:
        f (callable): Function f(t, x) representing the right-hand side of the ODE dx/dt = f(t, x).
        x0 (ndarray): Initial condition vector.
        tmin (float): Start time of the simulation.
        tmax (float): End time of the simulation.
        tpart (int): Number of time steps (discretization).
        refin (int, optional): Number of fixed-point refinement iterations (default is 10).

    Returns:
        ndarray: Array of solution vectors at each time point.
    """
    time_points = np.linspace(tmin, tmax, tpart)
    results = [x0]
    for i in range(1, len(time_points)):
        t = time_points[i]
        dt = time_points[i] - time_points[i - 1]
        x_pred = results[-1] + dt * f(t, results[-1])
        for _ in range(refin):
            x_pred = results[-1] + dt * f(t, x_pred)
        results.append(x_pred)
    return np.array(results)


def euler_method_with_progress(f, x0, tmin, tmax, tpart, refinements, pbar):
    """
    Solves an ODE system using backward Euler with fixed-point refinement and a progress bar.

    This function behaves like `euler_method`, but includes an external progress bar
    to monitor the iteration over time steps, which is useful for long simulations.

    Args:
        f (callable): Function f(t, x) representing the right-hand side of the ODE dx/dt = f(t, x).
        x0 (ndarray): Initial condition vector.
        tmin (float): Start time of the simulation.
        tmax (float): End time of the simulation.
        tpart (int): Number of time steps (discretization).
        refinements (int): Number of fixed-point refinement iterations.
        pbar (tqdm.tqdm): TQDM progress bar object to update during simulation.

    Returns:
        ndarray: Array of solution vectors at each time point.
    """
    time_points = np.linspace(tmin, tmax, tpart)
    results = [x0]
    
    for i in range(1, len(time_points)):
        t = time_points[i]
        dt = time_points[i] - time_points[i - 1]

        x_pred = results[-1] + dt * f(t, results[-1])
        for _ in range(refinements):
            x_pred = results[-1] + dt * f(t, x_pred)
        
        results.append(x_pred)
        pbar.update(1)
    
    return np.array(results)
