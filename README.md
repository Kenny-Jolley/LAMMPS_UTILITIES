# LAMMPS_UTILITIES
A collection of standalone utility scripts for lammps.  
This includes lattice generators, lattice converters and example lammps input scripts.


## Requirements

This code requires [Python](http://www.python.org) to run. Currently Python 3.5+ should work, but I have only tested on version 3.8. 


## Installation

Clone the repository to a directory of your choice:
~~~
 git clone git://github.com/Kenny-Jolley/LAMMPS_UTILITIES.git
~~~
Ensure that each directory is added to your path.  
e.g. if you created a git directory in your home directory, add these lines for a tcsh shell:

.tcshrc:  
~~~
setenv PATH ${PATH}:$HOME/git/LAMMPS_UTILITIES/utilities
setenv PATH ${PATH}:$HOME/git/LAMMPS_UTILITIES/carbon
~~~
Or for bash:

.bashrc:  
~~~
export PATH=$PATH:$HOME/git/LAMMPS_UTILITIES/utilities
export PATH=$PATH:$HOME/git/LAMMPS_UTILITIES/carbon
~~~
To make sure the python scripts executable, run:  
~~~
chmod +x lammps_*
~~~

## Usage

The scripts can be called directly and passed options on the command line, or imported into other scripts.

For example:
`lammps_gen_reaxff_ffield_carbon_may2016.py`  
This function simply generates the ffield file for the May 2016 version of the reaxff potential in the current directory.

### utilities

The utilities folder contains scripts for setting up lammps and manipulating the lammps input and output files.

### carbon

This folder contains scripts for setting up carbon systems.

### lammps_examples

This folder contains a collection of input scripts for simple molecular dynamics simulations.

