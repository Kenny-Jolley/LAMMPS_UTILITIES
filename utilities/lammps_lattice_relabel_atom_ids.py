#!/usr/bin/env python

# This function reads a lammps lattice input file and relabels the atom IDs so that
# they are sequential.  The script also checks that the correct number of atoms are present

# Keyword arguments:
# verbose    = True  , prints some comments to the screen.
# overwrite  = True  , will overwrite the existing file.
# overwrite  = False , will create a new file with the current date-time appended to the filename
# filename = lammps.lattice.dat  , the lammps lattice file to read

#  Kenny Jolley, May 2019

# imported modules
import sys
import os
import datetime
import numpy as np


# function reads a lammps lattice input file and relabels the atom IDs
def lammps_lattice_relabel_atom_ids(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    filename = kwargs.get('filename', 'lammps.lattice.dat')
    overwrite = kwargs.get('overwrite', False)

    # Welcome
    if verbose:
        print("  +------------------------------------------+")
        print("  | This script reads a lammps lattice input |")
        print("  |      file and relabels the atom IDs      |")
        print("  |                                          |")
        print("  |               Kenny Jolley               |")
        print("  |                 May 2019                 |")
        print("  +------------------------------------------+")
        print("   ")

        print(">  Lammps input filename: " + str(filename))

    # output filename
    x = datetime.datetime.now()
    output_filename = (x.strftime("%Y") + x.strftime("%m") +
                       x.strftime("%d") + x.strftime("%H") +
                       x.strftime("%M") + x.strftime("%S") + "_lammps.lattice.dat")

    # Open input file
    infile = open(filename, 'r')
    row_count = 0
    if verbose:
        print("Opened file: " + str(infile.name))

    # Create output file
    outfile = open(output_filename, 'w+')
    if verbose:
        print("Opened file: " + str(outfile.name))

    # Read and write the header, stop after reading the 'Atoms' line
    atoms = 0
    while True:
        fileline = infile.readline()
        outfile.write(str(fileline))
        row_count = row_count + 1
        fileline_split = fileline.split()
        
        # Save the number of atoms
        if len(fileline_split) > 1:
            if fileline_split[1] == 'atoms':
                atoms = int(fileline_split[0])

        # Stopping criteria
        if len(fileline_split) > 0:
            if fileline_split[0] == 'Atoms':
                # Write the next blank line and exit
                fileline = infile.readline()
                row_count = row_count + 1
                outfile.write(str(fileline))
                break
    infile.close()

    # Now we need to read in all the data lines to a numpy array
    data = np.loadtxt(filename, skiprows=row_count)
    # print(data)

    # Test if no. atoms are as expected
    if verbose:
        print("\nAtoms expected in file: " + str(atoms))
        print("Atoms actually read   : " + str(data.shape[0]))
    if atoms != data.shape[0]:
        print(">>> WARNING: atoms field at the top of the file does NOT match "
              "with the actual number of atom records in the file")
        print("\nAtoms expected in file: " + str(atoms))
        print("Atoms actually read   : " + str(data.shape[0]))

    # Sort atom data into order by first column
    data = data[data[:, 0].argsort()]
    # print(data)

    # Print sorted data to file, relabel ids starting at 1
    for i in range(data.shape[0]):
        outfile.write(str(i+1) + " ")
        for j in range(data.shape[1]-1):
            d = data[i][j+1]
            if int(d) == d:
                outfile.write(str(int(d)) + " ")
            else:
                outfile.write(str(d) + " ")
        outfile.write("\n")
    outfile.close()

    # overwrite existing file if required
    if overwrite:
        os.remove(filename)
        os.rename(output_filename, filename)


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    # Get the filename from commandline, if present
    if len(sys.argv) > 1:
        # call the function safely
        lammps_lattice_relabel_atom_ids(verbose=True, overwrite=False, filename=str(sys.argv[1]))
    else:
        # call the function safely (use default filename)
        lammps_lattice_relabel_atom_ids(verbose=True, overwrite=False)
