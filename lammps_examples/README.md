# Example lammps input scripts

A collection of input scripts for simple molecular dynamics simulations.

To run the scripts you will need a lattice file in the appropriate format as well as the input file for the potential (i.e. CH.airebo, ffield).


To run, use a command like:  
`mpirun -n 12  lmp_kj_mpi < lammps_airebo_npt.IN > commandline_out.txt &`

replace `lmp_kj_mpi` with the name of your lammps executable.


## CH.airebo
This is the potential input file for the AIREBO simulations.  This file is a modified version of the one that is distributed with lammps.  Here `rcmax_CC = 1.92`.  The original value was `2.0`.

## ffield
This is the potential input file for the ReaxFF simulations.  This file is from the paper:  
`R. Smith, K. Jolley et al, A ReaXFF carbon potential for radiation damage studies, NIMB 393 (2017) 49–53`

