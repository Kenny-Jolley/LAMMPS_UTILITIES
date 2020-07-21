#!/usr/bin/env python

#  This script finds the optimal a lattice parameter for graphene,
#  using the ReaxFF potential.

#  Optimisation parameters are hard-coded for now.


import sys
from scipy.optimize import minimize
import numpy as np
from lammps_gen_graphene_reaxff import lammps_gen_graphene_reaxff

# test that the lammps import works
try:
    from lammps import lammps
    lmp_test = lammps(cmdargs=["-log", "none", "-nocite", "-screen", "none"])
    version = lmp_test.version()
    print("LAMMPS version: " + str(version))
    lmp_test.close()              # destroy a LAMMPS object
except ImportError:
    print("Error importing LAMMPS, exiting ...")
    sys.exit()


# function that we want to minimise
def objective_funtion(params):
    # get lattice parameters
    a_const = params[0]

    # hard code the lattice size
    cells_x = 5
    cells_y = 8

    cells = [cells_x, cells_y]

    # generate the initial lammps input file
    lammps_gen_graphene_reaxff(verbose=False,
                               forced=True,
                               cells=cells,
                               a_const=a_const)

    # create lammps object
    lmp = lammps(cmdargs=["-log", "none", "-nocite", "-screen", "none"])
    
    # initialise lammps
    lmp.command("dimension 3")
    lmp.command("boundary p p p")  # set to p p s  for bilayers etc.
    lmp.command("units  real")
    lmp.command("atom_style    charge")

    # read init data, and setup simulation
    lmp.command("read_data lammps.lattice.dat")

    # define the potential
    lmp.command("pair_style hybrid/overlay reax/c NULL  zbl 1.0 1.15")
    lmp.command("pair_coeff * * reax/c ffield C")
    lmp.command("pair_coeff * * zbl 6.0 6.0")
    
    # set neighbour list
    lmp.command("neighbor    2. bin")
    lmp.command("neigh_modify    every 1 delay 0 check no ")
    lmp.command("fix   99 all qeq/reax 1 0.0 10.0 1e-6 reax/c")
    
    # Define an nve simulation
    lmp.command("fix        1 all nve")
    lmp.command("timestep        0.1")
    
    lmp.command("run 0 post no")
    
    # natoms = lmp.get_natoms()
    # print("Num atoms: " + str(natoms))
    
    total_energy = lmp.extract_compute("thermo_pe", 0, 0)

    lmp.close()              # destroy a LAMMPS object
    
    print(params, total_energy)
    return total_energy


# initial guess for the lattice parameters
initialGuess = np.array([2.43])

# optimise
res = minimize(objective_funtion,
               initialGuess,
               method='nelder-mead',
               options={'xtol': 1e-6, 'disp': True}
               )


print("Optimisation complete:")
print(res.x)

