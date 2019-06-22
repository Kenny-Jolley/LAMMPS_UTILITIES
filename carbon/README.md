# Carbon scripts

A collection of scripts for creating and manipulating lammps data files for carbon systems.

## Usage

#### `lammps_gen_graphite_airebo.py`  

This function simply generates a graphite lattice for the AIREBO forcefield.
The output is a lammps data file in atomic format (this is the required format for the AIREBO code).

Lattice parameters are set to:
~~~
a_const = 2.4175 , the 'a' lattice constant
c_const = 3.358  , the 'c' lattice constant
~~~

The script can be run interactively with:
~~~
lammps_gen_graphite_airebo.py
~~~
Or passed instructions on the commandline:
~~~
lammps_gen_graphite_airebo.py 10 10 10
~~~
Generates a `10 x 10 x 10` unit cell lattice with ab stacking
~~~
lammps_gen_graphite_airebo.py 10 10 10 abc
~~~
Generates a `10 x 10 x 10` unit cell lattice with `abc` stacking


