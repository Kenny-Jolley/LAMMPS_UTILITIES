#!/usr/bin/env python

# This function reads lammps output dump files and computes the center of mass and radial histogram of the atoms.

# The script needs to know the filename of the lammps dump files.
# When run interactively, this can be passed on the commandline, or the script can ask the user.
# Give a single filename dump01234.dat.gz or a general pattern dump*.dat.gz


# Keyword arguments:
# verbose           = True , prints some comments to the screen.
# header            = True , output includes header lines (No. atoms, and system size)
# output_prefix     = 'str',  filename prefix of the output xyz files
# write_id_col      = True ,  output includes atom id column
# write_element_col = True ,  output includes atom element column
# sort_by_id        = True ,  sorts the atoms in order of id number
# filename          = dump*.dat.gz  , the lammps dump file(s) to read

#  Kenny Jolley, July 2020

# imported modules
import math
import sys
import os
import gzip


# function reads lammps output dump file and computes the center of mass and radial histogram of the atoms.
def lammps_dump_analysis_cell_radius(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    overwrite_output = kwargs.get('overwrite_output', False)
    filename = kwargs.get('filename', 'dump*.dat.gz')
    output_filename = kwargs.get('output_filename', 'output.txt')

    # Welcome
    if verbose:
        print("  +------------------------------------------+")
        print("  |        LAMMPS dump file analysis         |")
        print("  |   Calculates cell radius distribution    |")
        print("  |               Kenny Jolley               |")
        print("  |                 Dec 2021                 |")
        print("  +------------------------------------------+\n")

        print("Verbose:          ", verbose)
        print("Input file:       ", filename)
        print("Output file:      ", output_filename)
        print("Overwrite output: ", overwrite_output)

    # - Get xyz atom coordinates -
    # determine if the file is zipped
    lammps_files_zipped = (filename[-3:] == '.gz')

    # Open file for reading - extract if needed
    if lammps_files_zipped:
        infile = gzip.open(str(filename), 'rt')
    else:
        infile = open(filename, 'r')

    # Default variables
    num_atoms = 10000000
    # xyz data arrays
    atom_x_pos = []
    atom_y_pos = []
    atom_z_pos = []

    # --- read the input file and save data ---
    while True:
        # read line, exit if at end of file
        fileline = infile.readline()
        if not fileline:
            break

        # split line into a list
        fileline = fileline.split()

        # if list is zero length, then skip
        if len(fileline) == 0:
            continue

        # Firstly find the number of atoms
        if (fileline[0] == "ITEM:") and (fileline[1] == "NUMBER") and (fileline[3] == "ATOMS"):
            # next line is the number of atoms
            fileline = infile.readline()
            fileline = fileline.split()
            num_atoms = fileline[0]
            if verbose:
                print("> Atoms: " + str(num_atoms))

        # now we look for the atom data
        if (fileline[0] == "ITEM:") and (fileline[1] == "ATOMS"):
            # find the column indices
            x_col = -1
            y_col = -1
            z_col = -1

            for i in range(2, len(fileline)):
                if fileline[i] == "x":
                    x_col = i-2
                if fileline[i] == "y":
                    y_col = i-2
                if fileline[i] == "z":
                    z_col = i-2

            # check that all required columns were found
            if x_col == -1:
                print("X column was not found")
                sys.exit()
            if y_col == -1:
                print("Y column was not found")
                sys.exit()
            if z_col == -1:
                print("Z column was not found")
                sys.exit()

            # --- Now read the atom data and save to arrays ---
            while True:
                # read line, exit if at end of file
                fileline = infile.readline()
                if not fileline:
                    break

                fileline = fileline.split()

                # save xyz data in lists
                atom_x_pos.append(float(fileline[x_col]))
                atom_y_pos.append(float(fileline[y_col]))
                atom_z_pos.append(float(fileline[z_col]))

    # Debug print xyz coords
    # for x, y, z in zip(atom_x_pos, atom_y_pos, atom_z_pos):
    #     print(x, y, z)

    # Close input file
    infile.close()

    # Calculate center of mass
    tot_x = 0
    tot_y = 0
    tot_z = 0
    for x, y, z in zip(atom_x_pos, atom_y_pos, atom_z_pos):
        tot_x += x
        tot_y += y
        tot_z += z
    tot_x /= len(atom_x_pos)
    tot_y /= len(atom_y_pos)
    tot_z /= len(atom_z_pos)

    if int(num_atoms) != len(atom_x_pos):
        print("Warning, did not read in expected number of atoms")
        print('num_atoms ', num_atoms)
        print('len array ', len(atom_z_pos))

    # Histogram calc
    hist_min = 0
    hist_bin_width = 0.05
    hist_max = 10

    hist_steps = (hist_max-hist_min)/hist_bin_width
    print(hist_steps)

    hist_vals = [hist_min + hist_bin_width * x for x in range(int(hist_steps)+1)]
    hist_count = [0 for _ in range(int(hist_steps) + 1)]
    print(hist_vals)

    # sort into bins
    for x, y, z in zip(atom_x_pos, atom_y_pos, atom_z_pos):
        dx = x - tot_x
        dy = y - tot_y
        dz = z - tot_z
        dr = math.sqrt(dx*dx + dy*dy + dz*dz)

        # add one to relevant bin
        b = int((dr-hist_min) / hist_bin_width)
        if b < len(hist_count):
            hist_count[b] += 1

    print(hist_vals)
    print(hist_count)

    # open/setup output data file
    if overwrite_output or not os.path.isfile(output_filename):
        # open file for writing, make header
        output_file = open(output_filename, 'w')
        # Write header
        output_file.write('Dump filename,atoms,CoM x,CoM y,CoM z,')
        for x in hist_vals:
            output_file.write(str(x) + ',')
        output_file.write('\n')
    else:
        # open for appending
        output_file = open(output_filename, 'a')

    # Print data
    output_file.write(str(filename) + ',' +
                      str(num_atoms) + ',' +
                      str(tot_x) + ',' +
                      str(tot_y) + ',' +
                      str(tot_z) + ','
                      )
    for x in hist_count:
        output_file.write(str(x) + ',')
    output_file.write('\n')
    # Close files
    output_file.close()


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    # Get the filename
    if len(sys.argv) > 1:
        in_filename = str(sys.argv[1])
    else:
        in_filename = 'dump*.dat.gz'  # str(input('Enter the filename to convert : '))

    # if filename contains a * char, loop through all files in current dir with the same prefix and suffix
    if "*" not in in_filename:
        print('> Single file calculation: ', in_filename)
        print('> No * - Calculation for given file only')
        # call the function
        lammps_dump_analysis_cell_radius(filename=in_filename,
                                         verbose=True,
                                         overwrite_output=True,
                                         output_filename='output.csv')
    else:
        # Star in filename, search whole dir for matching files
        print('Multi-file calculation: ', in_filename)
        print('* - Calculation for all matching files')
        filename_list = in_filename.split('*')
        filename_prefix = filename_list[0]
        filename_suffix = filename_list[1]
        # get a list of files in the directory
        file_list = os.listdir(os.getcwd())

        # overwrite file flag
        file_write_flag = True

        # filter list to include valid files only
        for file in file_list:
            if filename_prefix == file[:len(filename_prefix)]:
                if filename_suffix == file[-len(filename_suffix):]:
                    print(file)
                    # call the function
                    lammps_dump_analysis_cell_radius(filename=file,
                                                     verbose=True,
                                                     overwrite_output=file_write_flag,
                                                     output_filename='output.csv')

                    # ensure subsequent call don't overwrite output
                    file_write_flag = False
