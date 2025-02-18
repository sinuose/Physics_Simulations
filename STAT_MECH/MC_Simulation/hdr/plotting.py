import matplotlib.pyplot as plt
import numpy as np

def initialize_plots(lattice):
    plt.ion()  # Enable interactive mode
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    # Plot initial lattice
    im = ax1.imshow(lattice, cmap='plasma')
    ax1.set_title("Lattice State")
    plt.colorbar(im, ax=ax1)

    # Plot energy and magnetization
    line_energy, = ax2.plot([], [], 'r-', label="Energy")
    line_magnetization, = ax3.plot([], [], 'b-', label="Magnetization")
    ax2.set_title("Energy over Time")
    ax3.set_title("Magnetization over Time")
    ax2.set_xlabel("Time Step")
    ax3.set_xlabel("Time Step")
    ax2.legend()
    ax3.legend()

    return fig, ax1, ax2, ax3, im, line_energy, line_magnetization

def update_plot(im, ax1, ax2, ax3, line_energy, line_magnetization, lattice, energy, magnetization, step):
    # Update the lattice state plot
    im.set_data(lattice)
    ax1.set_title(f"Lattice State (Step {step})")

    # Update the energy and magnetization plots
    line_energy.set_data(np.arange(step + 1), energy)
    line_magnetization.set_data(np.arange(step + 1), magnetization)

    # Rescale the energy and magnetization plots
    ax2.relim()
    ax2.autoscale_view()
    ax3.relim()
    ax3.autoscale_view()

def save_final_plot(fig, path):
    plt.ioff()
    plt.savefig(path)
    plt.close()