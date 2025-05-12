import numpy as np
from tqdm import tqdm

def euler_method(f, x0, tmin, tmax, tpart, refin=10):
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


