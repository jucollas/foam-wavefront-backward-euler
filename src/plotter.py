import matplotlib.pyplot as plt
from functions.permeability import nD_eq
import time
import numpy as np
import matplotlib.pyplot as plt
from solver.velocity import smooth_speed, speed_metrics, analyze_constant_velocity


def create_figure_report(t_vel, v1, v2, start_frac=0.9):
    """
    t_vel debe tener longitud Nt-1 (misma que v1 y v2).
    Calcula mean/std/std-mean usando analyze_constant_velocity (misma lógica que tu análisis).
    """
    index_start = int(len(v1) * start_frac)

    ignore = -50
    t_vel = t_vel[:ignore]
    v1 = v1[:ignore]
    v2 = v2[:ignore]

    fig2, ax = plt.subplots(figsize=(10, 4))
    ax.set_title("front speed vs time")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("v [m/s]")
    ax.grid(True)

    l1_s,   = ax.plot(t_vel, v1, label="Sw1 v (smooth)")
    l2_s,   = ax.plot(t_vel, v2, label="Sw2 v (smooth)")


    mean_v1 = np.mean(v1[index_start:])
    mean_v2 = np.mean(v2[index_start:])

    h1 = ax.axhline(mean_v1, linestyle="--", label=f"Sw1 mean (steady)={mean_v1:.3e} v[m/s]")
    h2 = ax.axhline(mean_v2, linestyle="--", label=f"Sw2 mean (steady)={mean_v2:.3e} v[m/s]")

    # Banda sombreada del régimen estable (desde start_frac)
    if len(t_vel) > 0:
        t0 = t_vel[int(len(t_vel) * start_frac)]
        t1 = t_vel[-1]
    else:
        t0, t1 = 0.0, 1.0
    band = ax.axvspan(t0, t1, alpha=0.12, label=f"Steady zone (from {int(start_frac*100)}%)")

    ax.legend(loc="best")
    fig2.tight_layout()

    handles = {
        "ax": ax,
        "l1_s": l1_s, "l2_s": l2_s,
        "h1": h1, "h2": h2,
        "band": band,
        # por si quieres usarlo luego fuera
        "metrics": {
            "sw1": {"mean": mean_v1},
            "sw2": {"mean": mean_v2},
        }
    }
    return fig2, handles

"""def create_figure_report(t_vel, v1, v2, start_frac=0.6, smooth_w=51):
    
    t_vel debe tener longitud Nt-1 (misma que v1 y v2).
    
    v1s = smooth_speed(v1, smooth_w)
    v2s = smooth_speed(v2, smooth_w)

    m1 = speed_metrics(v1s, start_frac=start_frac)
    m2 = speed_metrics(v2s, start_frac=start_frac)

    fig2, ax = plt.subplots(figsize=(10, 4))
    ax.set_title("Reporte: velocidad del frente vs tiempo")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("v [m/s]")
    ax.grid(True)

    # Curvas
    l1_raw, = ax.plot(t_vel, v1, alpha=0.25, label="Sw1 v (raw)")
    l2_raw, = ax.plot(t_vel, v2, alpha=0.25, label="Sw2 v (raw)")
    l1_s,   = ax.plot(t_vel, v1s, label="Sw1 v (suave)")
    l2_s,   = ax.plot(t_vel, v2s, label="Sw2 v (suave)")

    # Promedios (régimen estable)
    h1 = ax.axhline(m1["mean"], linestyle="--", label=f"Sw1 mean (steady)={m1['mean']:.3e}")
    h2 = ax.axhline(m2["mean"], linestyle="--", label=f"Sw2 mean (steady)={m2['mean']:.3e}")

    # Banda sombreada del régimen estable (desde start_frac)
    t0 = t_vel[int(len(t_vel) * start_frac)] if len(t_vel) > 0 else 0.0
    band = ax.axvspan(t0, t_vel[-1] if len(t_vel) else 1.0, alpha=0.12, label=f"Steady zone (from {int(start_frac*100)}%)")

    # Texto resumen
    txt = ax.text(
        0.02, 0.98,
        (f"Sw1: mean={m1['mean']:.3e}, std={m1['std']:.3e}, std/mean={m1['rel']:.3f}\n"
         f"Sw2: mean={m2['mean']:.3e}, std={m2['std']:.3e}, std/mean={m2['rel']:.3f}"),
        transform=ax.transAxes, va="top"
    )

    ax.legend(loc="best")
    fig2.tight_layout()

    # Devolvemos handles por si luego quieres actualizar
    handles = {
        "ax": ax, "txt": txt,
        "l1_raw": l1_raw, "l2_raw": l2_raw,
        "l1_s": l1_s, "l2_s": l2_s,
        "h1": h1, "h2": h2,
        "band": band
    }
    return fig2, handles"""

def plot_simulation_and_report(Sw1_all, Sw2_all, x, t_vel, vel_sw1, vel_sw2, dt, stride=50, pause_time=0.05):
    plt.ion()

    fig2, _ = create_figure_report(t_vel, vel_sw1, vel_sw2, start_frac=0.4)
    fig2.show()

    # ---- Figura 1 (simulación) ----p

    fig1, ax = plt.subplots(figsize=(10, 4))
    line1, = ax.plot([], [], label='Sw1')
    line2, = ax.plot([], [], label='Sw2')
    line3, = ax.plot([], [], '--', label='nD1')
    line4, = ax.plot([], [], '--', label='nD2')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('Saturation')
    ax.set_ylim(0, 1.2)
    ax.set_xlim(x[0], x[-1])
    ax.grid()
    ax.legend()

    vel_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, va="top")

    Nt = len(Sw1_all)
    for t_index in range(0, Nt, stride):
        Sw1 = Sw1_all[t_index]
        Sw2 = Sw2_all[t_index]

        line1.set_data(x, Sw1)
        line2.set_data(x, Sw2)
        line3.set_data(x, nD_eq(Sw1))
        line4.set_data(x, nD_eq(Sw2))

        t_real = t_index * dt
        v1 = vel_sw1[t_index-1] if t_index > 0 and (t_index-1) < len(vel_sw1) else np.nan
        v2 = vel_sw2[t_index-1] if t_index > 0 and (t_index-1) < len(vel_sw2) else np.nan

        ax.set_title(f'Saturation profile at t = {t_real:.3f} s')
        vel_text.set_text(f"v_front Sw1: {v1:.4e} m/s\nv_front Sw2: {v2:.4e} m/s")

        fig1.canvas.draw()
        fig1.canvas.flush_events()
        time.sleep(pause_time)

    plt.ioff()
    plt.show()

def plot_full_simulation(Sw1_all, Sw2_all, x, params, vel_sw1=None, vel_sw2=None, stride=50, pause_time=0.1):
    """
    Animación interactiva de Sw1/Sw2 + nD1/nD2 y muestra velocidad instantánea por frame.

    vel_sw1, vel_sw2: arrays de longitud Nt-1 (típico de np.diff(pos)/dt)
    dt: paso de tiempo real entre frames (en segundos)
    stride: cada cuántos pasos de tiempo se dibuja un frame
    """
    cfg = params["cfg"]
    dt = (cfg["tmax"] - cfg["tmin"]) / (Sw1_all.shape[0] - 1)
    Nt = len(Sw1_all)

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 4))

    line1, = ax.plot([], [], label='Sw1')
    line2, = ax.plot([], [], label='Sw2')
    line3, = ax.plot([], [], '--', label='nD1')
    line4, = ax.plot([], [], '--', label='nD2')

    ax.set_xlabel('x [m]')
    ax.set_ylabel('Saturation')
    ax.set_ylim(0, 1.2)
    ax.grid()
    ax.legend()
    ax.set_xlim(x[0], x[-1])

    # Texto tipo HUD en esquina superior izquierda
    vel_text = ax.text(
        0.02, 0.95, "", transform=ax.transAxes,
        va="top"
    )

    for t_index in range(0, Nt, stride):
        Sw1 = Sw1_all[t_index]
        Sw2 = Sw2_all[t_index]

        line1.set_data(x, Sw1)
        line2.set_data(x, Sw2)
        line3.set_data(x, nD_eq(Sw1))
        line4.set_data(x, nD_eq(Sw2))

        # Tiempo real (aprox)
        t_real = t_index * dt

        # Velocidad instantánea (v[k] es entre k y k+1)
        v1 = np.nan
        v2 = np.nan
        if vel_sw1 is not None and t_index > 0 and (t_index - 1) < len(vel_sw1):
            v1 = vel_sw1[t_index - 1]
        if vel_sw2 is not None and t_index > 0 and (t_index - 1) < len(vel_sw2):
            v2 = vel_sw2[t_index - 1]

        ax.set_title(f'Saturation profile at t = {t_real:.3f} s')

        vel_text.set_text(
            f"v_front Sw1: {v1:.4e} m/s\n"
            f"v_front Sw2: {v2:.4e} m/s"
        )

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(pause_time)

    plt.ioff()
    plt.show()