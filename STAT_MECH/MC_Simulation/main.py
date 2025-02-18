from hdr.monte_carlo import *
from hdr.plotting import initialize_plots, update_plot, save_final_plot

import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

if __name__ == "__main__":
    #run program
    print("Program Start")

    #constants
    N = 128
    N_vector = [N,N]
    dim = 2
    J = 1
    Tc = 2.269
    T = 1#1.3 * Tc
    # simulation parameters
    MCS = N**2
    N_MCS_steps = 1500

    # loader
    pbar1 = tqdm(total=(3.5-T)//0.05)
    while(T < 3.5):
        # containers
        energy = []
        magnetization = []
        lattice_trace = []

        # main class obj
        main_iser = IsingModel(dim, N_vector, J, T)
        # set initial conditions
        main_iser.initial_conditions()

        # Initialize plots
        #fig, ax1, ax2, ax3, im, line_energy, line_magnetization = initialize_plots(main_iser.Lattice)

        # Main loop
        print(f"Metropolis Solver Total Sweeps: {N_MCS_steps}:")
        pbar = tqdm(total=N_MCS_steps)
        # two for loops, one for the number of sweeps, and one to do sweeping:
        for j in range(N_MCS_steps):
            for i in range(MCS):
                # Iterate the lattice MCS times
                main_iser.iterate_local()

            # After 1 sweep, append energies
            energy.append(main_iser.Energy(main_iser.Lattice))
            magnetization.append(main_iser.magnetization())

            # Update the plot
            #update_plot(im, ax1, ax2, ax3, line_energy, line_magnetization, main_iser.Lattice, energy, magnetization, j)

            # update bar
            pbar.update(1)

        #update_plot(im, ax1, ax2, ax3, line_energy, line_magnetization, main_iser.Lattice, energy, magnetization, j)
        #save_final_plot(fig, os.getcwd() + f"//STAT_MECH//MC_Simulation//final_png//T={T}_L={N}.png")

        # # save output

        df = pd.DataFrame({"Energy" : energy, "Magnetization" : magnetization})
        path = os.getcwd()
        #os.mkdir(path+f"//STAT_MECH//MC_Simulation//thermal_averaging_data//T={T}")
        #os.mkdir(path+f"//STAT_MECH//MC_Simulation//thermal_averaging_data//T={T}//PNG")
        df.to_csv(path+ f"//STAT_MECH//MC_Simulation//thermal_averaging_data//T={T}//" + f"out_T={T}_L={np.max(N_vector)}.csv", index=False)
        #df.to_csv(os.getcwd() + "//STAT_MECH//MC_Simulation//out.csv", index = False)
        
        # if looping over temperatures
        T += 0.05
        pbar1.update(1)
            