import numpy as np

def estimate_front(Sw, x, val=0.5):
  Sw = np.asarray(Sw)

  crosses = np.where((Sw[:-1] < val) & (Sw[1:] >= val))[0]
  if len(crosses) == 0:
      return np.nan

  i = crosses[0] + 1
  x0, x1 = x[i-1], x[i]
  y0, y1 = Sw[i-1], Sw[i]

  if y1 == y0:
      return x0
  return x0 + (val - y0) * (x1 - x0) / (y1 - y0)

def moving_average(v, w=25):
  v = np.asarray(v)
  return np.convolve(v, np.ones(w)/w, mode="valid")

def estimate_front_max_grad(Sw, x):
  dSdx = np.gradient(Sw, x)
  return x[np.argmax(np.abs(dSdx))]

def calculate_velocity(sw_all, x, params, val=0.5):
  cfg = params["cfg"]
  tmin, tmax = cfg["tmin"], cfg["tmax"]

  tpart = int((tmax - tmin) * cfg["time_steps_per_unit"])
  if tpart < 2:
      return np.nan

  dt = (tmax - tmin) / (tpart - 1)

  pos_sw = np.array([estimate_front(sw_all[i], x, val=val) for i in range(len(sw_all))])
  vel = np.diff(pos_sw) / dt

  return vel

def steady_slice(arr, start_frac=0.3):
    k0 = int(len(arr) * start_frac)
    return arr[k0:]

def analyze_constant_velocity(vel, tol=0.28, start_frac=0.50):
    v = steady_slice(vel[np.isfinite(vel)], start_frac)
    mean_v = np.mean(v)
    std_v  = np.std(v)
    rel = std_v / (abs(mean_v) + 1e-12)

    print(f"[Steady from {start_frac*100:.0f}%] mean={mean_v:.6e}, std={std_v:.6e}, std/mean={rel:.4f}")
    print("✔ traveling-wave (steady speed)" if rel < tol else "✘ not steady yet / not traveling-wave")
    return mean_v, std_v, rel


def smooth_speed(v, window_size=51):
    v = np.asarray(v, dtype=float)
    if len(v) == 0:
        return v
    if window_size < 3:
        return v
    if window_size % 2 == 0:
        window_size += 1

    if np.any(np.isnan(v)):
        nans = np.isnan(v)
        if np.all(nans):
            return v
        v[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), v[~nans])

    kernel = np.ones(window_size) / window_size
    return np.convolve(v, kernel, mode="same")


def speed_metrics(v, start_frac=0.6):
    v = np.asarray(v, dtype=float)
    v = v[np.isfinite(v)]
    if len(v) < 3:
        return {"mean": np.nan, "std": np.nan, "rel": np.nan, "start_idx": 0}

    k0 = int(len(v) * start_frac)
    v2 = v[k0:] if k0 < len(v) else v

    mean_v = np.mean(v2)
    std_v = np.std(v2)
    rel = std_v / (abs(mean_v) + 1e-12)

    return {"mean": mean_v, "std": std_v, "rel": rel, "start_idx": k0}