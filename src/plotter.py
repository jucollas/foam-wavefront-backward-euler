import matplotlib.pyplot as plt
from functions.permeability import nD_eq
import time

def plot_full_simulation(Sw1_all, Sw2_all, x, pause_time=0.1):
    plt.ion()  # Activa el modo interactivo
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

    plt.ioff()  # Desactiva el modo interactivo si ya no se necesita
    plt.show()
