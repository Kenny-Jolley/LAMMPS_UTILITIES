# LAMMPS_UTILITIES
A collection of standalone utility scripts for lammps.  
This includes lattice generators, lattice converters and example lammps input scripts.


## Requirements

This code requires [Python](http://www.python.org) to run. Currently Python 3.6+ should work, but I have only tested on version 3.10. 


## Installation

Clone the repository to a directory of your choice:
~~~
 git clone https://github.com/Kenny-Jolley/LAMMPS_UTILITIES.git
~~~

To be able to use the scripts from the command line from anywhere, you will need to add the script directories to your path. 
e.g. if you created a git directory in your home directory, add these lines for a tcsh shell:

.tcshrc:  
~~~
setenv PATH ${PATH}:$HOME/git/LAMMPS_UTILITIES/utilities
setenv PATH ${PATH}:$HOME/git/LAMMPS_UTILITIES/carbon/graphite/scripts
~~~
Or for bash:

.bashrc:  
~~~
export PATH=$PATH:$HOME/git/LAMMPS_UTILITIES/utilities
export PATH=$PATH:$HOME/git/LAMMPS_UTILITIES/carbon/graphite/scripts
~~~
To make sure the python scripts executable, run:  
~~~
chmod +x lammps_*
~~~

## Usage

The scripts can be called directly and passed options on the command line, or imported into other scripts.

For example:
`lammps_gen_graphite_airebo.py`  
This function simply generates a graphite lattice with the lattice parameters set to the relaxed values using the AIREBO potential.

### utilities

The utilities folder contains scripts for setting up lammps and manipulating the lammps input and output files.

### carbon

This folder contains scripts for setting up carbon systems.

### glass

This folder contains scripts for generating initial random lattices for borosilicate and sodium borosilicate systems. 

### lammps_examples

This folder contains a collection of input scripts for simple molecular dynamics simulations.

