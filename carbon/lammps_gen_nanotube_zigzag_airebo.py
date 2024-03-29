#!/usr/bin/env python

# This function simply generates a nanotube with a zigzag end centred in a periodic box.
# a_const defaults to the optimised value at zero K for the AIREBO force-field.
# The output is a lammps data file in atomic format (this is the required format for the AIREBO code).

# Keyword arguments:
# verbose = True   , prints some comments to the screen.
# forced  = True   , will overwrite the existing file (if it exists).
# forced  = False  , if file exists, will ask the user if the existing file should be overwritten.
# a_const = 2.4636  , the 'a' lattice constant
# filename = lammps.lattice.dat  , the output filename
# cells = [x,y]  , No. unit cells to generate for each direction.

# Kenny Jolley, Dec 2020

import sys
import os
import math


def lammps_gen_nanotube_zigzag_airebo(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    forced = kwargs.get('forced', False)
    # Default constants for the AIREBO force-field.
    a_const = kwargs.get('a_const', 2.419)
    filename = kwargs.get('filename', 'lammps.lattice.dat')
    cells = kwargs.get('cells', [1, 1])

    # box size and atom total
    box_x = math.sqrt(3) * a_const * cells[0]  # length of nanotube
    nanotube_circumference = a_const * cells[1]
    nanotube_radius = 0.5 * nanotube_circumference / math.pi
    box_y = float(int(2.0*nanotube_radius+0.5) + 20.0)
    box_z = float(int(2.0*nanotube_radius+0.5) + 20.0)

    tot_atoms = int(4 * cells[0] * cells[1])

    # Welcome
    if verbose:
        print("  +------------------------------------------------+")
        print("  |             Lattice generator script           |")
        print("  |                   Zigzag Nanotube              |")
        print("  |                  AIREBO force-field            |")
        print("  |                   Kenny Jolley                 |")
        print("  |                     Feb 2021                   |")
        print("  +------------------------------------------------+\n")

        print(">  Echoing back the user supplied data")
        print("     Lattice constant a [Ang]: " + str(a_const))
        print(">    Nanotube length [Ang]: " + str(box_x))
        print(">    Nanotube radius [Ang]: " + str(nanotube_radius))
        print(">    Nanotube circumference [Ang]: " + str(nanotube_circumference))
        print(">  Nanotube lattice with unit cell repeats:")
        print("     cells_x: " + str(cells[0]))
        print("     cells_y: " + str(cells[1]))
        print(">  Nanotube lattice cell dimensions [Ang]:")
        print("     box_x: " + str(box_x))
        print("     box_y: " + str(box_y))
        print("     box_z: " + str(box_z))
        print(">  Total number of atoms: " + str(tot_atoms))

    # Set generate file flag to true
    gen_file = True

    # Check if the file already exists
    if not forced:
        if os.path.isfile(filename):
            print("> Existing file " + str(filename) + " detected.")
            print("> lammps_gen_nanotube_zigzag_airebo function wants to overwrite this file")

            # Ask user if file should be overwritten
            user_choice = input('Do you wish to overwrite the existing file? (y/n): ').lower()

            if (user_choice == 'yes') or (user_choice == 'y') or (user_choice == 'yea'):
                print(" > Overwriting existing file ... ")
                gen_file = True
            else:
                print("File not overwritten, exiting function")
                gen_file = False

    # create lattice file
    if gen_file:
        file = open(filename, 'w+')
        if verbose:
            print("Opened file: " + str(file.name))

        # Write header info
        file.write("Lammps data file generated by lammps_gen_nanotube_zigzag_airebo\n")
        file.write("# Nanotube " + str(cells[0]) + "x" + str(cells[1]) +
                   " Unit cells, with a_param = " + str(a_const) + "\n")
        file.write(str(tot_atoms) + " atoms\n\n")
        file.write("1 atom types # C\n\n")
        file.write("0.0 " + str(box_x) + " xlo xhi\n")
        file.write("0.0 " + str(box_y) + " ylo yhi\n")
        file.write("0.0 " + str(box_z) + " zlo zhi\n\n")
        file.write("Masses\n\n")
        file.write("1 12.011\n\n")
        file.write("Atoms # atomic\n\n")

        # setup arrays to hold atom coordinates
        x = []
        y = []
        z = []

        # compute coordinates of underlying graphene lattice
        for i in range(0, cells[0]):
            x_shift = i * math.sqrt(3) * a_const
            for j in range(0, cells[1]):
                y_shift = j * a_const

                x.append(x_shift)
                y.append(y_shift)
                z.append(0.0)

                x.append(x_shift + a_const * 2.0 / math.sqrt(3))
                y.append(y_shift)
                z.append(0.0)

                x.append(x_shift + a_const * math.sqrt(3) / 6.0)
                y.append(y_shift + a_const / 2.0)
                z.append(0.0)

                x.append(x_shift + a_const * math.sqrt(3) / 2.0)
                y.append(y_shift + a_const / 2.0)
                z.append(0.0)

        # project points onto cylinder surface
        x_new = []
        y_new = []
        z_new = []
        for i in range(len(x)):
            x_new.append(x[i])
            y_new.append(nanotube_radius * math.sin(y[i] / nanotube_radius))
            z_new.append(nanotube_radius * math.cos(y[i] / nanotube_radius))

        # translate
        for i in range(len(x)):
            y_new[i] = y_new[i] + box_y/2.0
            z_new[i] = z_new[i] + box_z/2.0

        # Output data:  ID type x y z
        for i in range(len(x)):
            file.write(str(i+1) + "  1  " +
                       str(x_new[i]) + "  " +
                       str(y_new[i]) + "  " +
                       str(z_new[i]) + "\n")

        file.close()

        if verbose:
            print("file closed: " + str(file.name))
            print("COMPLETED lattice.dat output !!")


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    my_cells = [1, 1]

    # Read number of lattice cells from the command-line, or supply interactively
    if len(sys.argv) > 1:
        print(">  Using information passed on the command-line")
        # 2 params = cell size
        if len(sys.argv) == 3:
            my_cells[0] = int(sys.argv[1])
            my_cells[1] = int(sys.argv[2])
        else:
            print(">>> ERROR  <<<")
            print("  User must pass 2 command-line arguments")
            print("   2 params = box_x, box_y  (integers)")
            print("    examples")
            print("   lammps_gen_nanotube_zigzag_airebo.py 1 2 ")
            print("   lammps_gen_nanotube_zigzag_airebo.py 10 21")
            sys.exit()
    else:
        # Otherwise, ask user, cell dimensions
        while True:
            try:
                cellsize = int(input('Enter number of cells in x dir (nanotube length): '))
                if cellsize > 0:
                    break
                else:
                    print("Oops!  Integer must be greater than 0.  Try again...")
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")
        my_cells[0] = cellsize
        while True:
            try:
                cellsize = int(input('Enter number of cells in y dir (nanotube circumference): '))
                if cellsize > 0:
                    break
                else:
                    print("Oops!  Integer must be greater than 0.  Try again...")
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")
        my_cells[1] = cellsize

    # call the nanotube generator function
    lammps_gen_nanotube_zigzag_airebo(verbose=True, forced=True, cells=my_cells)
