import numpy as np
import random as rnd
#from scipy.constants import Boltzmann as kb
from scipy.ndimage import convolve

kb = 1

class IsingModel():
    def __init__(self, 
                 dim, 
                 N_vector,
                 J,
                 T):
        
        # need the constants of the grid
        self.dim      = dim         # dimensions of the ising
        self.N_vector = N_vector    # dimensions of the space
        self.J = J
        self.T = T

    def initial_conditions(self):
        # need to know the dimensions
        if self.dim != len(self.N_vector):
            print("Dimenions do not equal the length vector")
            return 0
        else:
            self.Lattice = 2 * np.random.randint(0,2,self.N_vector) - 1
            self.LatticeShape = np.shape(self.Lattice)
            # get kernel for all stuff
            self.ConvKernel = self.gen_kernel(self.dim)
            # compute initial energy
            self.Energy_Curr = self.Energy(self.Lattice)

    def gen_kernel(self, ndim):
        kernel = np.zeros((3,) * ndim, dtype=int)
        center = (1,) * ndim
        for axis in range(ndim):
            for offset in (-1, 1):
                neighbor = list(center)
                neighbor[axis] += offset
                kernel[tuple(neighbor)] = 1
        return kernel

    def Energy(self, Lattice):
        # Compute the convolution of sigma with the kernel
        convolved = convolve(Lattice, self.ConvKernel, mode='wrap')
        # Multiply element-wise by sigma to get \sigma_i \sigma_j
        sigma_sigma = Lattice * convolved
        # Sum the result to get the total \sum \sigma_i \sigma_j
        # E = - J * \sum_i \sum_j \sigma_i * \sigma_j
        return (-self.J * np.sum(sigma_sigma)) / 2  # Divide by 2 to correct double-counting 

    def iterate_local(self):
        '''
        Optimized Iterate function
        '''
        random_pt = tuple([rnd.randrange(dim_size) for dim_size in self.LatticeShape])
        spin = self.Lattice[random_pt]
        
        # Calculate sum of neighboring spins using convolution
        neighbor_sum = convolve(self.Lattice, self.ConvKernel, mode='wrap')[random_pt]
        
        # Energy change from flipping the spin: ΔE = 2 * J * spin * neighbor_sum
        deltaE = 2 * self.J * spin * neighbor_sum
        
        if deltaE < 0 or rnd.uniform(0, 1) < np.exp(-deltaE / (kb * self.T)):
            self.Lattice[random_pt] *= -1
            self.Energy_Curr += deltaE

    def iterate(self):
        # take random spin, flip or not
        # Generate random indices for each dimension
        random_pt = tuple([rnd.randrange(dim_size) for dim_size in self.LatticeShape])
        LatticeTemp = self.Lattice.copy()  # Get a copy of the lattice
        LatticeTemp[random_pt] = -1 * LatticeTemp[random_pt]  # Flip the spin
        # compute energy difference
        Energy_new = self.Energy(LatticeTemp)
        deltaE = Energy_new - self.Energy_Curr
        # Markov Chain
        if deltaE < 0:
            self.Lattice = LatticeTemp      # update the lattice   
            self.Energy_Curr = Energy_new   # update the energy
            del LatticeTemp
        else:
            w = np.exp(-1/(kb * self.T) * deltaE)
            r = rnd.uniform(0, 1)
            if r < w:
                self.Lattice = LatticeTemp    # update the lattice
                self.Energy_Curr = Energy_new # update the energy
                del LatticeTemp
            

    def magnetization(self):
        # M = \sum_{\sigma_i}
        return np.sum(self.Lattice)


    
