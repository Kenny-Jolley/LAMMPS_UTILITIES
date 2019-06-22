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
Generates a `10 x 10 x 10` unit cell lattice with `ab` stacking.
~~~
lammps_gen_graphite_airebo.py 10 10 10 abc
~~~
Generates a `10 x 10 x 10` unit cell lattice with `abc` stacking.  You can generate any stacking sequence by substituting `abc` with any sequence containing the letters `a`,`b` and `c`.


#### `lammps_gen_graphite_reaxff.py`  

This function simply generates a graphite lattice for the May 2016 ReaxFF forcefield.
The output is a lammps data file in charge format (this is the required format for the ReaxFF code).

Lattice parameters are set to:
~~~
a_const = 2.433  , the 'a' lattice constant
c_const = 3.2567 , the 'c' lattice constant
~~~

The script can be run interactively with:
~~~
lammps_gen_graphite_reaxff.py
~~~
Or passed instructions on the commandline:
~~~
lammps_gen_graphite_reaxff.py 10 10 10
~~~
Generates a `10 x 10 x 10` unit cell lattice with `ab` stacking.
~~~
lammps_gen_graphite_reaxff.py 10 10 10 abc
~~~
Generates a `10 x 10 x 10` unit cell lattice with `abc` stacking. You can generate any stacking sequence by substituting `abc` with any sequence containing the letters `a`,`b` and `c`.


#### `lammps_gen_random_lattice_C_atomic.py`  

This function generates a random lattice of carbon atoms.  The minimum separation between the carbon atoms is 1 Angstrom.
Output file is in lammps atomic format.
The script can be run interactively with:
~~~
lammps_gen_random_lattice_C_atomic.py
~~~
Or passed instructions on the commandline:
~~~
lammps_gen_random_lattice_C_atomic.py 5000 2.5
~~~
Where the first number is the number of atoms to generate and the second number is the density in g/cm<sup>3</sup>.

#### `lammps_gen_reaxff_ffield_carbon_may2016.py`  

This function simply generates the ffield file for the May 2016 version of the reaxff potential in the current directory.



