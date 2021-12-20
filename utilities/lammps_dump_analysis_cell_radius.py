#!/usr/bin/env python

# This function converts the output dump files of a lammps simulation to xyz files.

# The script needs to know the filenames of the lammps dump files.
# When run interactively, this can be passed on the commandline, or the script can ask the user.

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
import sys
import os
import gzip


# function converts a given file in lammps output format, to xyz format
def lammps_convert_dump_to_xyz(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    header = kwargs.get('header', True)
    header_atoms = kwargs.get('header_atoms', True)
    output_prefix = kwargs.get('output_prefix', 'xyz_')
    write_id_col = kwargs.get('write_id_col', True)
    write_element_col = kwargs.get('write_element_col', True)
    sort_by_id = kwargs.get('sort_by_id', True)
    filename = kwargs.get('filename', 'dump*.dat.gz')

    # Welcome
    if verbose:
        print("  +------------------------------------------+")
        print("  |    Converts LAMMPS dump files to XYZ     |")
        print("  |                                          |")
        print("  |               Kenny Jolley               |")
        print("  |                July 2020                 |")
        print("  +------------------------------------------+")
        print("\n")
        print("Verbose:      ", verbose)
        print("header:       ", header)
        print("header_atoms: ", header_atoms)

        print("write_id_col:      ", write_id_col)
        print("write_element_col: ", write_element_col)
        print("sort_by_id:        ", sort_by_id)
        print("filename:      ", filename)
        print("output_prefix: ", output_prefix)
        print("\n")

    # determine if the file is zipped
    lammps_files_zipped = (filename[-3:] == '.gz')

    # Open file for reading - extract if needed
    if lammps_files_zipped:
        infile = gzip.open(str(filename), 'rt')
        filename = filename[:-3]
    else:
        infile = open(filename, 'r')

    # output filename
    filename_out = str(output_prefix) + str(filename)
    # open output for writing
    output_file = open(filename_out, 'w')

    # --- read the input file and write the output ---
    while 1:
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

            if verbose:
                print("Atoms: " + str(fileline[0]))
            if header or header_atoms:
                output_file.write(str(fileline[0]) + '\n')

        # now we look for the cell size parameters
        if (fileline[0] == "ITEM:") and (fileline[1] == "BOX") and (fileline[2] == "BOUNDS"):
            # next lines are the box size
            # save the box size  ( this assumes  xlo xhi  is given and that xlo =0)
            # x
            fileline = infile.readline()
            fileline = fileline.split()
            dump_file_box_x = float(fileline[1])
            # y
            fileline = infile.readline()
            fileline = fileline.split()
            dump_file_box_y = float(fileline[1])
            # z
            fileline = infile.readline()
            fileline = fileline.split()
            dump_file_box_z = float(fileline[1])

            if verbose:
                print("Size: " +
                      str(dump_file_box_x) + '  ' +
                      str(dump_file_box_y) + '  ' +
                      str(dump_file_box_z) + '\n')
            if header:
                output_file.write(str(dump_file_box_x) + '  ' +
                                  str(dump_file_box_y) + '  ' +
                                  str(dump_file_box_z) + '\n')

        # now we look for the atom data
        if (fileline[0] == "ITEM:") and (fileline[1] == "ATOMS"):
            # find the column indices
            x_col = -1
            y_col = -1
            z_col = -1
            element_col = -1
            id_col = -1
            for i in range(2, len(fileline)):
                if fileline[i] == "x":
                    x_col = i-2
                if fileline[i] == "y":
                    y_col = i-2
                if fileline[i] == "z":
                    z_col = i-2
                if fileline[i] == "element":
                    element_col = i-2
                if fileline[i] == "id":
                    id_col = i-2
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
            if write_element_col:
                if element_col == -1:
                    print("element column was not found")
                    sys.exit()
            if write_id_col:
                if id_col == -1:
                    print("id column was not found")
                    sys.exit()

            # --- Now read the atom data and save to output file ---

            # if we are not sorting, just get the data and save to output
            if not sort_by_id:
                while 1:
                    # read line, exit if at end of file
                    fileline = infile.readline()
                    if not fileline:
                        break

                    fileline = fileline.split()
                    if write_id_col:
                        output_file.write(str(fileline[id_col]) + ' ')
                    if write_element_col:
                        output_file.write(str(fileline[element_col]) + ' ')

                    output_file.write(str(fileline[x_col]) + ' ' +
                                      str(fileline[y_col]) + ' ' +
                                      str(fileline[z_col]) + '\n')
            else:
                # We need to sort the data
                if id_col == -1:
                    print("id column was not found")
                    print("We need the id column to sort the data on it")
                    sys.exit()

                # find max id (in case it differs from atoms
                max_id = 0
                file_pos = infile.tell()
                while 1:
                    # read line, exit if at end of file
                    fileline = infile.readline()
                    if not fileline:
                        break
                    fileline = fileline.split()
                    max_id = max(max_id, int(fileline[id_col]))
                # print(max_id)

                # Reset file position to top of atoms list
                infile.seek(file_pos)

                # setup some arrays
                atom_x_pos = ["" for _ in range(max_id + 1)]
                atom_y_pos = ["" for _ in range(max_id + 1)]
                atom_z_pos = ["" for _ in range(max_id + 1)]
                atom_el_col = ["" for _ in range(max_id + 1)]
                atom_valid_flag = [0 for _ in range(max_id + 1)]

                # read data into arrays
                while 1:
                    # read line, exit if at end of file
                    fileline = infile.readline()
                    if not fileline:
                        break

                    fileline = fileline.split()

                    # save data in order
                    atom_x_pos[int(fileline[id_col])] = str(fileline[x_col])
                    atom_y_pos[int(fileline[id_col])] = str(fileline[y_col])
                    atom_z_pos[int(fileline[id_col])] = str(fileline[z_col])
                    atom_valid_flag[int(fileline[id_col])] = 1

                    if write_element_col:
                        if len(str(fileline[element_col])) == 1:
                            atom_el_col[int(fileline[id_col])] = str(fileline[element_col]) + '_'
                        else:
                            atom_el_col[int(fileline[id_col])] = str(fileline[element_col])

                # write data to output file
                for i in range(len(atom_y_pos)):
                    if atom_valid_flag[i]:
                        if write_id_col:
                            output_file.write(str(i) + ' ')

                        if write_element_col:
                            output_file.write(str(atom_el_col[i]) + ' ')

                        output_file.write(str(atom_x_pos[i]) + ' ')
                        output_file.write(str(atom_y_pos[i]) + ' ')
                        output_file.write(str(atom_z_pos[i]) + '\n')

    # Close files
    infile.close()
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
        print('no star - just converting given file')
        # call the function
        lammps_convert_dump_to_xyz(filename=in_filename,
                                   verbose=True,
                                   header=True,
                                   header_atoms=True,
                                   write_id_col=True,
                                   write_element_col=False,
                                   sort_by_id=True)
    else:
        # Star in filename, search whole dir for matching files
        print('star - just all files that fit pattern')
        filename_list = in_filename.split('*')
        filename_prefix = filename_list[0]
        filename_suffix = filename_list[1]
        # get a list of files in the directory
        file_list = os.listdir(os.getcwd())

        # filter list to include valid files only
        for file in file_list:
            if filename_prefix == file[:len(filename_prefix)]:
                if filename_suffix == file[-len(filename_suffix):]:
                    print(file)
                    # call the function
                    lammps_convert_dump_to_xyz(filename=file,
                                               verbose=True,
                                               header=True,
                                               header_atoms=True,
                                               write_id_col=True,
                                               write_element_col=False,
                                               sort_by_id=True)
