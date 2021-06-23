#!/usr/bin/env python

# This function reads a lattice from a lammps input data file and applies the strain specified.

# Keyword arguments:
# verbose    = True  , prints some comments to the screen.
# strain_x   = 0.0  , percentage strain to apply in the x direction.
# strain_y   = 0.0  , percentage strain to apply in the y direction.
# strain_z   = 0.0  , percentage strain to apply in the z direction.
# filename = lammps.lattice.dat  , the lammps lattice file to read

# Kenny Jolley, July 2020

# imported modules
import sys
import datetime
import numpy as np


# function reads a lammps log.lammps file, and plots the Total energy vs time.
def lammps_lattice_strain(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    strain_x = kwargs.get('strain_x', 0.0)
    strain_y = kwargs.get('strain_y', 0.0)
    strain_z = kwargs.get('strain_z', 0.0)
    filename = kwargs.get('filename', 'lammps.lattice.dat')

    # Welcome
    if verbose:
        print("  +------------------------------------------+")
        print("  | This script reads a lammps lattice input |")
        print("  |   file and applies user defined strain   |")
        print("  |                                          |")
        print("  |               Kenny Jolley               |")
        print("  |                 July 2020                |")
        print("  |          kenny.jolley@gmail.com          |")
        print("  +------------------------------------------+")
        print("   ")

        print(">  Lammps input filename: " + str(filename))
        print(">  Percentage strain to apply: ")
        print("     Strain in x: " + str(strain_x) + " %")
        print("     Strain in y: " + str(strain_y) + " %")
        print("     Strain in z: " + str(strain_z) + " %")

    # convert to multiplier
    mult_x = (float(strain_x) / 100.0) + 1.0
    mult_y = (float(strain_y) / 100.0) + 1.0
    mult_z = (float(strain_z) / 100.0) + 1.0

    # output filename
    x = datetime.datetime.now()
    output_filename = (x.strftime("%Y") + x.strftime("%m") +
                       x.strftime("%d") + x.strftime("%H") +
                       x.strftime("%M") + x.strftime("%S") + "_lammps.lattice.dat")

    # Open input file
    infile = open(filename, 'r')
    row_count = 0
    if verbose:
        print("Opened input file : " + str(infile.name))

    # Create output file
    outfile = open(output_filename, 'w+')
    if verbose:
        print("Opened output file: " + str(outfile.name))

    # Read and write the header, stop after reading the 'Atoms' line
    # add note to first line
    fileline = infile.readline()
    outfile.write(str(fileline[:-1]) + " + strained: " + str(strain_x) + "% x " +
                  str(strain_y) + "% x " +
                  str(strain_z) + "%\n")
    row_count = row_count + 1

    while True:
        fileline = infile.readline()
        fileline_split = fileline.split()

        if len(fileline_split) > 3:
            if fileline_split[2] == 'xlo' and fileline_split[3] == 'xhi':
                fileline_split[1] = str(float(fileline_split[1]) * mult_x)

        if len(fileline_split) > 3:
            if fileline_split[2] == 'ylo' and fileline_split[3] == 'yhi':
                fileline_split[1] = str(float(fileline_split[1]) * mult_y)

        if len(fileline_split) > 3:
            if fileline_split[2] == 'zlo' and fileline_split[3] == 'zhi':
                fileline_split[1] = str(float(fileline_split[1]) * mult_z)

        for i in range(len(fileline_split)):
            outfile.write(str(fileline_split[i]) + " ")
        outfile.write("\n")
        row_count = row_count + 1

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

    # Rescale x y z coordinates, these are the last three cols
    data[:, data.shape[1] - 3] = data[:, data.shape[1] - 3] * mult_x
    data[:, data.shape[1] - 2] = data[:, data.shape[1] - 2] * mult_y
    data[:, data.shape[1] - 1] = data[:, data.shape[1] - 1] * mult_z

    # Print atom data to file
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            d = data[i][j]
            if int(d) == d:
                outfile.write(str(int(d)) + " ")
            else:
                outfile.write(str(d) + " ")
        outfile.write("\n")
    outfile.close()

    if verbose:
        print(">  Done ")


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    my_strain = [0, 0, 0]
    my_filename = 'lammps.lattice.dat'

    # Read number of lattice cells from the command-line, or supply interactively
    if len(sys.argv) > 1:
        print(">  Using information passed on the command-line")
        # 3 params = strain default lattice
        if len(sys.argv) == 4:
            my_strain[0] = float(sys.argv[1])
            my_strain[1] = float(sys.argv[2])
            my_strain[2] = float(sys.argv[3])
        elif len(sys.argv) == 5:
            my_filename = str(sys.argv[1])
            my_strain[0] = float(sys.argv[2])
            my_strain[1] = float(sys.argv[3])
            my_strain[2] = float(sys.argv[4])
        else:
            print(">>> ERROR  <<<")
            print("  User must pass either 3 or 4 command-line arguments")
            print("   1st param should be the filename to read (this is optional) ")
            print("   Then 3 params = strain_x, strain_y, strain_z  (floats, percentage strain)")
            print("    examples")
            print("   lammps_lattice_strain.py file.dat 1 0 0")
            print("   lammps_lattice_strain.py file.dat 10 5 1")
            print("   lammps_lattice_strain.py 0 0 1")
            sys.exit()
    else:
        # Otherwise, ask user
        my_filename = str(input('Enter filename of lattice data file to apply strain to: '))

        # x strain
        while True:
            try:
                my_strain[0] = float(input('Enter percentage strain in x dir : '))
                break
            except ValueError:
                print("Oops!  That was not a valid float.  Try again...")
        # y strain
        while True:
            try:
                my_strain[1] = float(input('Enter percentage strain in y dir : '))
                break
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")
        # z strain
        while True:
            try:
                my_strain[2] = float(input('Enter percentage strain in z dir : '))
                break
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")

    # call the lattice strain function
    lammps_lattice_strain(verbose=True,
                          filename=my_filename,
                          strain_x=my_strain[0],
                          strain_y=my_strain[1],
                          strain_z=my_strain[2])
