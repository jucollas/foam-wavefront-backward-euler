# Foam Wavefront Backward Euler Simulation

This project implements a numerical simulation using the **Backward Euler method** to solve the flow of two-phase fluid (water and gas) through porous media. The simulation is designed to model the dynamics of foam injection and its movement through the medium, as well as its impact on saturation levels over time.

## Overview

The project simulates the evolution of water and gas saturation profiles (`Sw1` and `Sw2`) over time in a 1D domain. The **Backward Euler** method is used for time-stepping, and the model incorporates a foam-related term to capture the effect of foam on gas saturation dynamics.

The core of the model is based on the following elements:

* **Permeability functions** (`krw`, `krg`): Defines the relative permeabilities of water and gas as a function of water saturation.
* **Flux calculations** (`fw`): Computes the fluxes of water and gas across the grid.
* **Saturation derivative**: Computes the time derivative of the saturation profiles based on the flux and derivative equations.

The simulation solves these equations iteratively and plots the saturation profiles at different time points.

## Installation

To run this project, you'll need to have Python 3.x and some required packages. You can set up the environment and install the dependencies by running:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### Required Libraries

* **NumPy**: For numerical operations and array handling.
* **Matplotlib**: For plotting the simulation results.
* **tqdm**: For progress bars during simulations.

## Usage

### Running the Simulation

To run the simulation, use the following command:

```bash
python run.py
```

This will:

1. Attempt to load previously saved simulation data (`saturation_data.npy`).
2. If the data file is not found, the simulation will run, and the results will be saved in the `data/` directory.
3. After the simulation finishes, the results will be plotted interactively, showing the evolution of water and gas saturation over time.

### Files

* `run.py`: Main script to execute the simulation.
* `simulation.py`: Contains functions that set up and run the simulation using the Backward Euler method.
* `plotter.py`: Contains plotting functions to visualize the simulation results.
* `derivative.py`: Contains the function that computes the time derivative of water and gas saturation.
* `flux.py`: Contains flux calculations based on permeability models.
* `permeability.py`: Contains functions to calculate relative permeabilities and foam-related terms.
* `variables.py`: Contains configuration and parameter initialization.
* `config_loader.py`: Loads configuration values from a JSON file.

### Configuration

The model configuration, such as domain size, initial conditions, and time parameters, is stored in a JSON file. You can modify the configuration in the `config/constants.json` file.

```json
{
  "phi": 0.25,
  "Swc": 0.2,
  "Sgr": 0.18,
  "mu_w": 1e-3,
  "mu_g": 2e-5,
  "k1": 2e-11,
  "k2": 1e-11,
  "Sw_star": 0.37,
  "A": 400,
  "theta_s": 3.2e-4,
  "u1": 2.93e-6,
  "u2": 1.465e-6,
  "L": 0.1,
  "Nx": 200,
  "Sw_inj": 0.372,
  "Sw_ini": 0.72,
  "diff_scale": 0.001,
  "tmin": 0,
  "tmax": 5000,
  "time_steps_per_unit": 3,
  "refinements": 10
}
```

### Visualization

The simulation will plot the saturation profiles (`Sw1` and `Sw2`) along with the foam model (`nD1`, `nD2`) at different time steps. These plots are shown interactively during the simulation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

