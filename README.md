# LAMMPS_UTILITIES
A collection of utility scripts for lammps


## Requirements

This code requires [Python](http://www.python.org) to run. Currently Python 2.7, 3.5+ should work. 


## Installation

Clone the repository to a directory of your choice:

`git clone https://github.com/Kenny-Jolley/LAMMPS_UTILITIES.git `

Ensure that this directory is added to your path:  
tcsh:  
`setenv PATH ${PATH}:$HOME/git/LAMMPS_UTILITIES`  
bash:  
`export PATH=$PATH:$HOME/git/LAMMPS_UTILITIES` 

To make sure the python scripts executable, run:  
`chmod +x lammps_*`


## Usage

The scripts can be called directly and passed options on the command line, or imported into other scripts.


### md setup

`lammps_gen_reaxff_ffield_carbon_may2016.py`  
This function simply generates the ffield file for the May 2016 version of the reaxff potential in the current directory.



