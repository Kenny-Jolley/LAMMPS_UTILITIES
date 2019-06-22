# Utilities

A collection of scripts for setting up lammps and manipulating the lammps input and output files.

## Usage

#### `lammps_convert_output_to_XYZ.py`  

This script converts lammps output dump files to a sequence of xyz files.  Compressed files can be read (assuming gzip is installed), and star notation is used to convert all files with the same pattern.

Examples:
~~~
lammps_convert_output_to_XYZ.py  filename.txt
lammps_convert_output_to_XYZ.py  dump.dat.gz
lammps_convert_output_to_XYZ.py  dump*.dat.gz
~~~

#### `lammps_lattice_relabel_atom_ids.py`

This script reads a lammps lattice input file and relabels the atom IDs so that they are sequential.  The script also checks that the correct number of atoms are present.

~~~
lammps_lattice_relabel_atom_ids.py filename.txt
~~~

#### `lammps_setup_custom_compile.py`

This script sets up the lammps source directory ready for compiling lammps.  
The script pulls the latest stable release and handles updating all packages that don't require extra libraries.

The user can choose to include the Voro++ package, if this is already installed.
A custom splining function between ReaxFF and ZBL for carbon systems can also be added.

This script then generates a makefile.  The user can choose between optimised INTEL or GCC compiler options.
The user can then build lammps using:

~~~
make -j 4 kj_mpi
~~~
