#!/usr/bin/env python

# This function simply generates a supercell from a given xyz file
# The output is a lammps data file in atomic format.

# Keyword arguments:
# verbose = True   , prints some comments to the screen.
# forced  = True   , will overwrite the existing file (if it exists).
# forced  = False  , if file exists, will ask the user if the existing file should be overwritten.
# filename = lammps.lattice.dat  , the output filename
# cells = [x,y]  , No. unit cells to generate for each direction.
# xyzfile = 'lattice.xyz'   ,  the filename of the input xyz file to convert

# Kenny Jolley, Jan 2025

import sys
import os
import re
import math


def lammps_gen_supercell_from_xyz(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    forced = kwargs.get('forced', True)
    filename = kwargs.get('filename', 'lammps.lattice.dat')
    cells = kwargs.get('cells', [1, 1])
    xyzfile = kwargs.get('xyzfile', 'lattice.xyz')

    # Check if the file already exists
    if not forced:
        if os.path.isfile(filename):
            print("> Existing file " + str(filename) + " detected.")
            print("> lammps_gen_supercell_from_xyz function wants to overwrite this file")

            # Ask user if file should be overwritten
            user_choice = input('Do you wish to overwrite the existing file? (y/n): ').lower()

            if (user_choice == 'yes') or (user_choice == 'y') or (user_choice == 'yea'):
                print(" > Overwriting existing file ... ")
                forced = True
            else:
                print("File not overwritten, exiting function")
                forced = False
        else:
            forced = True

    # create lattice file
    if forced:
        file = open(xyzfile, 'r')
        if verbose:
            print("Opened file: " + str(file.name))

        # First line should be the number of atoms
        fileline = file.readline()
        try:
            atoms = int(fileline)
        except:
            print("Something went wrong reading the number of atoms from the input xyz file")
            print("The line read was:")
            print(fileline)
            sys.exit()

        if verbose:
            print("Atoms in xyz file: " + str(atoms))


        # Next line should be the extended xyz format containing cell size information
        # todo: this should be more robust (only works for some cases, orthorhombic etc)
        fileline = file.readline()
        # parse to find the lattice info
        lattice_regex = r'Lattice="([0-9.\s]+)"'
        # Search for the lattice vector part in the string
        match = re.search(lattice_regex, fileline)

        if match:
            # Extract the lattice vector string
            lattice_str = match.group(1)

            # Split the lattice vector string into a list of floats
            lattice_vectors = list(map(float, lattice_str.split()))

            # Reshape the list into a 3x3 matrix representing the lattice vectors
            lattice_matrix = [
                lattice_vectors[0:3],
                lattice_vectors[3:6],
                lattice_vectors[6:9]
            ]
        else:
            # If no match is found, return an empty list or raise an error
            print("Lattice information not found in the provided string")
            print(fileline)
            sys.exit()

        if verbose:
            print(lattice_matrix)

        # read in the atoms and the coordinates

        # todo  complete functions



        if verbose:
            print("file closed: " + str(file.name))
            print("COMPLETED lattice.dat output !!")



# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    my_cells = [1, 1]

    # Read number of lattice cells from the command-line, or supply interactively
    print(">  Using information passed on the command-line")

    # 3 params = input filename and supercell size
    if len(sys.argv) == 4:
        my_xyzfile = str(sys.argv[1])
        my_cells[0] = int(sys.argv[2])
        my_cells[1] = int(sys.argv[3])
        lammps_gen_supercell_from_xyz(verbose=True, forced=True, cells=my_cells, xyzfile=my_xyzfile)

    # 4 params = input filename and supercell size, then output name
    elif len(sys.argv) == 5:
        my_xyzfile = str(sys.argv[1])
        my_cells[0] = int(sys.argv[2])
        my_cells[1] = int(sys.argv[3])
        my_outfile = str(sys.argv[4])
        lammps_gen_supercell_from_xyz(verbose=True, forced=True, cells=my_cells, xyzfile=my_xyzfile,filename=my_outfile)

    else:
        print(">>> ERROR  <<<")
        print("  User must pass 3 or 4 command-line arguments")
        print("   3 params = input filename and supercell size")
        print("   4 params = input filename and supercell size, then output name")
        print("    examples")
        print("   lammps_gen_supercell_from_xyz  file.xyz  2  3")
        print("   lammps_gen_supercell_from_xyz  file.xyz  2  3   output.dat")
        sys.exit()
