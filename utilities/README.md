# Utilities

A collection of scripts for setting up lammps and manipulating the lammps input and output files.

## Usage

#### `lammps_convert_output_to_XYZ.py`  

This script converts lammps output dump files to a sequence of xyz files

~~~
lammps_convert_output_to_XYZ.py  filename.txt
lammps_convert_output_to_XYZ.py  dump.dat.gz
lammps_convert_output_to_XYZ.py  dump*.dat.gz
~~~

#### `lammps_lattice_relabel_atom_ids.py`

This function reads a lammps lattice input file and relabels the atom IDs so that they are sequential.  The script also checks that the correct number of atoms are present.

`lammps_lattice_relabel_atom_ids.py filename.txt`


