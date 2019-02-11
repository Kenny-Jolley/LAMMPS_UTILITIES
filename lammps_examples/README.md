# Example lammps input scripts

A collection of input scripts for simple molecular dynamics simulations.

To run the scripts you will need a lattice file in the appropriate format as well as the input file for the potential (ie CH.airebo, ffield).


To run, use a command like:

`mpirun -n 12  lmp_kj_mpi < lammps_airebo_npt.IN > commandline_out.txt &`

replace `lmp_kj_mpi` with the name of your lammps executable.

