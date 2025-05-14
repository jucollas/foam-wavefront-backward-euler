import matplotlib.pyplot as plt
from functions.permeability import nD_eq
import time

def plot_full_simulation(Sw1_all, Sw2_all, x, pause_time=0.1):
    """
    Plots the full time evolution of saturation and foam strength profiles.

    This function visualizes the evolution of water saturation in two layers
    (`Sw1` and `Sw2`) and the corresponding foam model output (`nD1`, `nD2`)
    over a spatial domain `x`. The plot updates in real time using interactive mode.

    Args:
        Sw1_all (ndarray): 2D array where each row corresponds to the saturation profile 
            of layer 1 at a given time.
        Sw2_all (ndarray): 2D array where each row corresponds to the saturation profile 
            of layer 2 at a given time.
        x (ndarray): 1D spatial coordinate array.
        pause_time (float, optional): Time in seconds to pause between frames. 
            Default is 0.1 seconds.

    Returns:
        None
    """
    plt.ion()  # Activate interactive mode
    fig, ax = plt.subplots(figsize=(10, 4))

    line1, = ax.plot([], [], label='Sw1')
    line2, = ax.plot([], [], label='Sw2')
    line3, = ax.plot([], [], '--', label='nD1', color='orange')
    line4, = ax.plot([], [], '--', label='nD2', color='red')

    ax.set_xlabel('x [m]')
    ax.set_ylabel('Saturation')
    ax.set_ylim(0, 1.2)
    ax.grid()
    ax.legend()

    for t_index in range(0, len(Sw1_all), 50):
        line1.set_data(x, Sw1_all[t_index])
        line2.set_data(x, Sw2_all[t_index])
        line3.set_data(x, nD_eq(Sw1_all[t_index]))
        line4.set_data(x, nD_eq(Sw2_all[t_index]))
        ax.set_title(f'Saturation profile at t = {t_index} s')
        ax.set_xlim(x[0], x[-1])
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(pause_time)

    plt.ioff()  # Turn off interactive mode if no longer needed
    plt.show()
