#!/usr/bin/env python

#  This script finds the optimal a and c lattice parameters for graphite,
#  using the GAP-20 potential.

#  Optimisation parameters are hard-coded for now.


import sys
from scipy.optimize import minimize
import numpy as np
from lammps_gen_graphite_gap import lammps_gen_graphite_gap

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
def objective_function(params):
    # get lattice parameters
    a_const = params[0]
    c_const = params[1]

    # hard code the lattice size
    cells_x = 5
    cells_y = 8
    cells_z = 3
    cells = [cells_x, cells_y, cells_z]
    
    # hard code the lattice stacking sequence
    stacking = 'ab'

    # generate the initial lammps input file
    lammps_gen_graphite_gap(verbose=False,
                            forced=True,
                            cells=cells,
                            stacking=stacking,
                            a_const=a_const,
                            c_const=c_const)

    # create lammps object
    lmp = lammps(cmdargs=["-log", "none", "-nocite", "-screen", "none"])
    
    # initialise lammps
    lmp.command("dimension 3")
    lmp.command("boundary p p p")  # set to p p s  for bilayers etc.
    lmp.command("units  metal")
    lmp.command("atom_style    atomic")

    # read init data, and setup simulation
    lmp.command("read_data lammps.lattice.dat")

    # define the potential
    lmp.command("pair_style    quip")
    # Provide the full path to the Carbon_GAP_20.xml file. Note that the quotations should be left empty for GAP_20.
    lmp.command('pair_coeff   * * /Users_HD3/makj/Carbon_GAP_20/Carbon_GAP_20_potential/Carbon_GAP_20.xml "" 6 ')
    
    # set neighbour list
    lmp.command("neighbor    2. bin")
    lmp.command("neigh_modify    every 10 delay 0 check no one 10000 page 10000000")

    # Define an nve simulation
    lmp.command("fix        1 all nve")
    lmp.command("timestep        0.0001")
    
    lmp.command("run 0 post no")
    
    # natoms = lmp.get_natoms()
    # print("Num atoms: " + str(natoms))
    
    total_energy = lmp.extract_compute("thermo_pe", 0, 0)

    lmp.close()              # destroy a LAMMPS object
    
    print(params, total_energy)
    return total_energy


# initial guess for the lattice parameters
initialGuess = np.array([2.42, 3.35])

# optimise
res = minimize(objective_function,
               initialGuess,
               method='nelder-mead',
               options={'xtol': 1e-6, 'disp': True}
               )

print("Optimisation complete:")
print(res.x)
