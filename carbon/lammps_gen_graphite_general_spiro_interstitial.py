#!/usr/bin/env python

# This function generates a graphite lattice with randomly distributed spiro interstitials
# The spiro interstitials are isolated and reconstructed automatically.

# The function can be called by other scripts or this file can be run interactively.
# When run interactively, the user must provide all parameters asked for (or just press enter for defaults).
# note this script does not include DRIP potential settings as this needs isolated molecules to work.

# Keyword arguments:
# verbose = True   , prints some comments to the screen.
# forced  = True   , will overwrite the existing file (if it exists).
# forced  = False  , if file exists, will ask the user if the existing file should be overwritten.
# a_const = 2.433  , the 'a' lattice constant
# c_const = 3.2567 , the 'c' lattice constant
# filename = lammps.lattice.dat  , the output filename
# stacking = 'ab'  , stacking order of the graphene planes
# cells = [x,y,z]  , No. unit cells to generate for each direction.

# Kenny Jolley, July 2021

import sys
import os
import math
import datetime
import numpy as np
'''from numba import jit'''
from random import seed
from random import randint


def lammps_gen_graphite_general_spiro_interstitial(**kwargs):
    # Default keyword args
    verbose = kwargs.get('verbose', False)  # verbose output
    forced = kwargs.get('forced', False)  # force overwriting of given file
    # Default constants for the ReaxFF May Potl
    a_const = kwargs.get('a_const', 2.4334)
    c_const = kwargs.get('c_const', 3.2567)
    stacking = kwargs.get('stacking', 'ab')
    filename = kwargs.get('filename', 'lammps.lattice.dat')
    cells = kwargs.get('cells', [12, 20, 2])
    lattice_model = kwargs.get('lattice_model', 'ReaxFF')
    output_format = kwargs.get('output_format', 'charge')
    int_concs = kwargs.get('layer_int_conc', [8.0, 8.0, 8.0, 8.0])

    # calculation of box size and atom total
    box_x = math.sqrt(3) * a_const * cells[0]
    box_y = a_const * cells[1]
    box_z = c_const * cells[2] * len(stacking)
    tot_atoms = int(4 * len(stacking) * cells[0] * cells[1] * cells[2])
    atoms_per_layer = 4 * cells[0] * cells[1]
    spiro_ints_layers = []
    actual_spiro_ints_pc = []
    for j in range(len(int_concs)):
        spiro_ints_layers.append(int(int_concs[j] * atoms_per_layer / 100.0 + 0.5))
        actual_spiro_ints_pc.append(100.0 * spiro_ints_layers[j] / atoms_per_layer)
    sum_spiro_ints = sum(spiro_ints_layers)
    overall_pc_ints = 100.0 * sum_spiro_ints / tot_atoms

    # carbon bond length
    cc_len = a_const / math.sqrt(3.0)
    cc_len_buf = cc_len * 1.1  # 10 % buffer on the bond length
    cc_len_buf2 = cc_len_buf * cc_len_buf

    # Welcome
    if verbose:
        print("  +--------------------------------------------+")
        print("  |         Lattice generator function         |")
        print("  |              Graphite lattice              |")
        print("  |          with spiro interstitials          |")
        print("  |               Kenny Jolley                 |")
        print("  |                July 2021                   |")
        print("  +--------------------------------------------+")
        print("   ")

        print(">  Echoing back the user supplied data")
        print("     Lattice Model       : " + str(lattice_model))
        print("     Lattice output type : " + str(output_format))
        print("     Lattice constant a   [Ang]: " + str(a_const))
        print("     Layer separation c/2 [Ang]: " + str(c_const))
        print(">  Graphite lattice with unit cell repeats:")
        print("     cells_x: " + str(cells[0]))
        print("     cells_y: " + str(cells[1]))
        print("     cells_z: " + str(cells[2]))
        print(">  Graphite lattice cell dimensions [Ang]:")
        print("     box_x: " + str(box_x))
        print("     box_y: " + str(box_y))
        print("     box_z: " + str(box_z))
        print(">  Stacking: " + str(stacking))
        print(">  Total number of atoms (perfect lattice): " + str(tot_atoms))

        print(">  Percentage spiro interstitials distribution requested: \n" + str(int_concs))
        print(">  Number of atoms in each pristine layer: " + str(atoms_per_layer))
        print(">  Spiro interstitials in each layer: \n" + str(spiro_ints_layers))
        print(">  Actual percentage of spiro interstitials in each layer:\n" + str(actual_spiro_ints_pc))
        print(">  Overall percentage of spiro interstitials: " + str(overall_pc_ints))

    # Check if the output file already exists
    # if it does and we are not allowed to overwrite, generate new filename based on the date and try again.
    if not forced:
        while True:
            if os.path.isfile(filename):
                print("> Existing file " + str(filename) + " detected.")
                print("> Generating new filename:")

                x = datetime.datetime.now()
                # Set pre-factor for output filename
                output_filename_prefac = (x.strftime("%Y") + x.strftime("%m") +
                                          x.strftime("%d") + x.strftime("%H") +
                                          x.strftime("%M") + x.strftime("%S") +
                                          "_")
                filename = os.path.join(output_filename_prefac + filename)
                print(filename)
            else:
                break

    # Generate output file
    file = open(filename, 'w+')
    if verbose:
        print("Opened file: " + str(file.name))

    # Write header info
    file.write("Lammps data file generated by lammps_gen_graphite_general_spiro_interstitial.py\n")
    file.write("# Graphite " + str(cells[0]) + "x" + str(cells[1]) + "x" + str(cells[2]) +
               " Unit cells, with " + str(stacking) +
               " stacking, model = " + str(lattice_model) +
               ", a_param = " + str(a_const) +
               ", c_param = " + str(c_const) +
               ",  Spiro interstitials in each layer: " + str(spiro_ints_layers) +
               ",  Overall percentage of spiro interstitials: " + str(overall_pc_ints) + " %\n")

    # number of atoms is the perfect lattice + total grafted interstitials
    file.write(str(tot_atoms + sum_spiro_ints) + " atoms\n\n")
    # 1 atom type
    file.write("1 atom types # C\n\n")
    # box
    file.write("0.0 " + str(box_x) + " xlo xhi\n")
    file.write("0.0 " + str(box_y) + " ylo yhi\n")
    file.write("0.0 " + str(box_z) + " zlo zhi\n\n")
    file.write("Masses\n\n")
    file.write("1 12.011\n\n")
    # comment output format in file
    file.write("Atoms # " + str(output_format) + "\n\n")

    # generate np arrays of atoms
    # atoms_array[id,coord]     # coordinates of perfect lattice
    # atoms_NN[list]         # list of the three nearest neighbours
    # atoms_NNN[list]        # list of the next nearest neighbours (not including the NN)
    # atom_deleted_flag[del] # flag set if atom is deleted

    # setup arrays
    atoms_array = np.zeros((tot_atoms, 3))
    atoms_NN = np.zeros((tot_atoms, 3), dtype=int)
    atoms_NNN = np.zeros((tot_atoms, 6), dtype=int)
    '''atoms_NNNN = np.zeros((tot_atoms, 9), dtype=int)'''
    atom_deleted_flag = np.zeros(tot_atoms)

    # generate the data for the atoms array
    if verbose:
        print("> Generating atoms array")
    atom_id = 0
    for z in range(0, cells[2]):
        for s in range(0, len(stacking)):
            z_shift = (len(stacking) * z + s) * c_const
            # stacking position a
            if stacking[s] == 'a':
                for x in range(0, cells[0]):
                    x_shift = x * math.sqrt(3) * a_const
                    for y in range(0, cells[1]):
                        y_shift = y * a_const
                        # pos 1
                        atoms_array[atom_id][0] = x_shift
                        atoms_array[atom_id][1] = y_shift
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

                        # pos 2
                        atoms_array[atom_id][0] = x_shift + a_const * 2.0 / math.sqrt(3)
                        atoms_array[atom_id][1] = y_shift
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

                        # pos 3
                        atoms_array[atom_id][0] = x_shift + a_const * math.sqrt(3) / 6.0
                        atoms_array[atom_id][1] = y_shift + a_const / 2.0
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

                        # pos 4
                        atoms_array[atom_id][0] = x_shift + a_const * math.sqrt(3) / 2.0
                        atoms_array[atom_id][1] = y_shift + a_const / 2.0
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1
            # stacking position b
            elif stacking[s] == 'b':
                for x in range(0, cells[0]):
                    x_shift = x * math.sqrt(3) * a_const
                    for y in range(0, cells[1]):
                        y_shift = y * a_const
                        # pos 1
                        atoms_array[atom_id][0] = x_shift
                        atoms_array[atom_id][1] = y_shift
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

                        # pos 2
                        atoms_array[atom_id][0] = x_shift + a_const / math.sqrt(3)
                        atoms_array[atom_id][1] = y_shift
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

                        # pos 3
                        atoms_array[atom_id][0] = x_shift + a_const * math.sqrt(3) / 2.0
                        atoms_array[atom_id][1] = y_shift + a_const / 2.0
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

                        # pos 4
                        atoms_array[atom_id][0] = x_shift + a_const * math.sqrt(3) * 5.0 / 6.0
                        atoms_array[atom_id][1] = y_shift + a_const / 2.0
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1
            # stacking position c
            elif stacking[s] == 'c':
                for x in range(0, cells[0]):
                    x_shift = x * math.sqrt(3) * a_const
                    for y in range(0, cells[1]):
                        y_shift = y * a_const
                        # pos 1
                        atoms_array[atom_id][0] = x_shift + a_const / math.sqrt(3)
                        atoms_array[atom_id][1] = y_shift
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

                        # pos 2
                        atoms_array[atom_id][0] = x_shift + a_const * 2.0 / math.sqrt(3)
                        atoms_array[atom_id][1] = y_shift
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

                        # pos 3
                        atoms_array[atom_id][0] = x_shift + a_const * math.sqrt(3) / 6.0
                        atoms_array[atom_id][1] = y_shift + a_const / 2.0
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

                        # pos 4
                        atoms_array[atom_id][0] = x_shift + a_const * math.sqrt(3) * 5.0 / 6.0
                        atoms_array[atom_id][1] = y_shift + a_const / 2.0
                        atoms_array[atom_id][2] = z_shift
                        atom_id += 1

    # for each atom, need to find the three nearest neighbours and save their ids to the atoms_NN array
    # slow brute force method handles periodic boundaries
    if verbose:
        print("> Building nearest neighbour list (could be slow)")
    for atom_id in range(tot_atoms):
        num_nebs = 0

        # only need to check atoms in current layer
        # find layer
        cur_layer = int(atom_id / atoms_per_layer)

        # set range
        id_lo = cur_layer * atoms_per_layer
        id_hi = (cur_layer + 1) * atoms_per_layer

        for atom_id2 in range(id_lo, id_hi):

            if atom_id2 != atom_id:
                # check dz, exclude other layers
                dz = abs(atoms_array[atom_id][2] - atoms_array[atom_id2][2])
                if dz < 1:
                    # check dx
                    dx = abs(atoms_array[atom_id][0] - atoms_array[atom_id2][0])
                    dx = min(dx, abs(dx - box_x))
                    if dx < cc_len_buf:
                        dy = abs(atoms_array[atom_id][1] - atoms_array[atom_id2][1])
                        dy = min(dy, abs(dy - box_y))
                        if dy < cc_len_buf:
                            # bond length squared
                            dr2 = dx * dx + dy * dy
                            # check within 2 angstroms
                            if dr2 < cc_len_buf2:
                                # save id to NN list
                                atoms_NN[atom_id][num_nebs] = atom_id2
                                num_nebs += 1
                                # We know there are only 3 NN's
                                if num_nebs >= 3:
                                    break
        '''# testing
        if num_nebs < 3:
            print("what",num_nebs,atom_id)'''

    if verbose:
        print("> Building next nearest neighbour list (could be slow)")
    # for each atom, need to find the six next nearest neighbours and save their ids to the atoms_NNN array
    for atom_id in range(tot_atoms):
        k = 0
        for j in range(3):
            nn_id = atoms_NN[atom_id][j]
            for nnn in range(3):
                if atoms_NN[nn_id][nnn] != atom_id:
                    atoms_NNN[atom_id][k] = atoms_NN[nn_id][nnn]
                    k += 1

    # Creating the spiro interstitials
    if verbose:
        print("> Creating and reconstructing the spiro interstitials")
    seed(datetime.datetime.now())

    # loop over layers and create the spiro interstitials
    for la in range(cells[2] * len(stacking)):
        id_lo = la * atoms_per_layer
        id_hi = (la + 1) * atoms_per_layer
        valid_list = [v for v in range(id_lo, id_hi)]

        # loop over spiro interstitials in each layer
        for si in range(spiro_ints_layers[la]):
            # get a random element
            r = randint(0, len(valid_list) - 1)

            # save location of atom1
            atom1 = valid_list[r]

            # atom2 is one of the nearest neighbours
            atom2 = atoms_NN[atom1][randint(0, 2)]

            # remove atom1,atom2 and all NN's and NNN's from the valid list
            valid_list.pop(r)

            # in-place list comprehension to delete element from list
            # https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating
            valid_list[:] = [x for x in valid_list if not (x in atoms_NN[atom1])]
            valid_list[:] = [x for x in valid_list if not (x in atoms_NN[atom2])]

            valid_list[:] = [x for x in valid_list if not (x in atoms_NNN[atom1])]
            valid_list[:] = [x for x in valid_list if not (x in atoms_NNN[atom2])]

            # Ensure we handle periodic boundary
            # get unit vector between the two atoms to be reconstructed
            dist = (atoms_array[atom1] - atoms_array[atom2])

            # move atoms through boundary if required
            # x
            if dist[0] > a_const * 2:
                atoms_array[atom1][0] -= box_x
            if dist[0] < -a_const * 2:
                atoms_array[atom1][0] += box_x
            # y
            if dist[1] > a_const * 2:
                atoms_array[atom1][1] -= box_y
            if dist[1] < -a_const * 2:
                atoms_array[atom1][1] += box_y

            # centre point
            cp = (atoms_array[atom1] + atoms_array[atom2]) / 2.0
            # print(cp)

            # get unit vector between the two atoms to be reconstructed
            dist = (atoms_array[atom1] - atoms_array[atom2])
            dist = dist / np.linalg.norm(dist)

            # calculate perpendicular vector
            dist_perp = np.zeros(3)
            dist_perp[0] = -dist[1]
            dist_perp[1] = dist[0]

            # duplicate atom to create the interstitial
            atoms_array = np.append(atoms_array, [atoms_array[atom1]], axis=0)

            # reconstruct the defect (ie move new atom to spiro position)
            atoms_array[-1] = cp
            atoms_array[-1][2] += cc_len

            # move atom 0.4 bond length along the perpendicular
            atoms_array[-1] += dist_perp * 0.4 * cc_len

            # move spiro and atom1 and atom2 up by .4 bond length
            atoms_array[-1][2] += cc_len * 0.4
            atoms_array[atom1][2] += cc_len * 0.4
            atoms_array[atom2][2] += cc_len * 0.4

            # wrap atoms that are now outside the boundary
            if atoms_array[atom1][0] < 0:
                atoms_array[atom1][0] += box_x
            if atoms_array[atom1][0] > box_x:
                atoms_array[atom1][0] -= box_x
            if atoms_array[atom1][1] < 0:
                atoms_array[atom1][1] += box_y
            if atoms_array[atom1][1] > box_y:
                atoms_array[atom1][1] -= box_y

            if atoms_array[-1][0] < 0:
                atoms_array[-1][0] += box_x
            if atoms_array[-1][0] > box_x:
                atoms_array[-1][0] -= box_x
            if atoms_array[-1][1] < 0:
                atoms_array[-1][1] += box_y
            if atoms_array[-1][1] > box_y:
                atoms_array[-1][1] -= box_y
            if atoms_array[-1][2] < 0:
                atoms_array[-1][2] += box_z
            if atoms_array[-1][2] > box_z:
                atoms_array[-1][2] -= box_z

    # output atom data and coordinates to the output file
    count = 0
    if output_format == 'atomic':
        for cnt in range(tot_atoms + sum_spiro_ints):
            file.write(str(count + 1) + " 1 " +
                       str(atoms_array[cnt][0]) + " " +
                       str(atoms_array[cnt][1]) + " " +
                       str(atoms_array[cnt][2]) +
                       "\n")
            count += 1
    elif output_format == 'charge':
        for cnt in range(tot_atoms + sum_spiro_ints):
            file.write(str(count + 1) + " 1  0  " +
                       str(atoms_array[cnt][0]) + " " +
                       str(atoms_array[cnt][1]) + " " +
                       str(atoms_array[cnt][2]) +
                       "\n")
            count += 1
    else:
        print(">ERROR  Output type not supported")
        print(output_format)

    # Close file and exit function
    file.close()

    if verbose:
        print("file closed: " + str(file.name))
        print("COMPLETED lattice.dat output !!")


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    '''# testing
    t1 = datetime.datetime.now()
    # call the graphite generator function
    lammps_gen_graphite_general_spiro_interstitial(verbose=True,
                                                   forced=True,
                                                   filename='lammps.lattice.dat',
                                                   )

    print(datetime.datetime.now() - t1)
    sys.exit()'''

    print("  +------------------------------------------+")
    print("  |         Lattice generator script         |")
    print("  |             Graphite lattice             |")
    print("  |         with spiro interstitials         |")
    print("  |               Kenny Jolley               |")
    print("  |                July 2021                 |")
    print("  +------------------------------------------+\n")

    # Determine the lattice supercell size, ask user for lattice cell dimensions
    my_cells = [-1, -1, -1]  # Default cell
    # X
    while True:
        try:
            my_cells[0] = input('Enter number of unit cells in the (armchair) X direction [default 12]: ')
            if my_cells[0] == "":
                my_cells[0] = 12
                break
            else:
                my_cells[0] = int(my_cells[0])
                if my_cells[0] > 0:
                    break
                else:
                    print(">ERROR:  Integer must be greater than 0.  Try again...")
        except ValueError:
            print("ERROR:  That was not a valid integer.  Try again...")

    # Y
    while True:
        try:
            my_cells[1] = input('Enter number of unit cells in the (zigzag)   Y direction [default 21]: ')
            if my_cells[1] == "":
                my_cells[1] = 21
                break
            else:
                my_cells[1] = int(my_cells[1])
                if my_cells[1] > 0:
                    break
                else:
                    print(">ERROR:  Integer must be greater than 0.  Try again...")
        except ValueError:
            print("ERROR:  That was not a valid integer.  Try again...")

    # Z
    while True:
        try:
            my_cells[2] = input('Enter number of unit cells in the (c, perp)  Z direction [default  8]: ')
            if my_cells[2] == "":
                my_cells[2] = 8
                break
            else:
                my_cells[2] = int(my_cells[2])
                if my_cells[2] > 0:
                    break
                else:
                    print(">ERROR:  Integer must be greater than 0.  Try again...")
        except ValueError:
            print("ERROR:  That was not a valid integer.  Try again...")

    print("")
    # Determine the stacking pattern of the graphene planes
    # stacking
    while True:
        my_stacking = str(input('Enter the graphene stacking pattern  (a, ab, abc, abba) [default: ab]: '))
        # if zero length, return default
        if len(my_stacking) == 0:
            my_stacking = "ab"
            break

        stacking_error = False
        for char in my_stacking:
            if (char != 'a') and (char != 'b') and (char != 'c'):
                print(">>> ERROR  <<< stacking order can contain only the letters: a,b,c")
                stacking_error = True
                break

        if not stacking_error:
            break

    # Determine lattice parameters a and c for the cell and output format
    # Choose from airebo, reaxff, hnn or custom
    print("\nNow we need to determine lattice parameters (a and c) for the cell and output format")
    print("Choose from pre-programmed models or input a custom type")
    ot = ""
    while ot != "a" and ot != "r" and ot != "h" and ot != "c":
        ot = input("a = AIREBO\n"
                   "r = ReaxFF\n"
                   "h = hNN\n"
                   "c = Custom\n"
                   "Enter lattice format type [default AIREBO]: ").lower()
        if ot == "":
            ot = "a"

    # Set appropriate cell parameters
    if ot == "a":  # AIREBO
        lat_a = 2.4175  # C-C = 1.395744276
        lat_c = 3.358
        lat_format = "atomic"
        ot = "AIREBO"
    elif ot == "r":  # ReaxFF
        lat_a = 2.4334  # C-C = 1.404924145
        lat_c = 3.2567
        lat_format = "charge"
        ot = "ReaxFF"
    elif ot == "h":  # hNN
        lat_a = 2.4636  # not correct
        lat_c = 3.2567  # not correct
        lat_format = "atomic"
        ot = "hNN"
    elif ot == "c":  # Custom
        ot = "Custom"
        # Need to ask the user for lattice options
        print("\nSince you chosen the custom option,")
        print("we need to determine lattice parameters (a and c) for the cell and output format\n")

        # A parameter
        while True:
            try:
                lat_a = input('Enter the lattice "a" parameter [default  2.4175]: ')
                if lat_a == "":
                    lat_a = 2.4175
                    break
                else:
                    lat_a = float(lat_a)
                    if lat_a > 0:
                        break
                    else:
                        print(">ERROR:  Number must be greater than 0.  Try again...")
            except ValueError:
                print("ERROR:  That was not a valid number.  Try again...")

        # C parameter
        while True:
            try:
                lat_c = input('Enter the lattice "c" parameter [default  3.358]: ')
                if lat_c == "":
                    lat_c = 3.358
                    break
                else:
                    lat_c = float(lat_c)
                    if lat_c > 0:
                        break
                    else:
                        print(">ERROR:  Number must be greater than 0.  Try again...")
            except ValueError:
                print("ERROR:  That was not a valid number.  Try again...")

        print()
        # output type
        while True:
            lat_format = input('a = atomic\n'
                               'c = charge\n'
                               'Enter output lattice format [default atomic]: ').lower()
            if lat_format == "":
                lat_format = "atomic"
                break
            else:
                if lat_format == "a" or lat_format == "atomic":
                    lat_format = "atomic"
                    break
                elif lat_format == "c" or lat_format == "charge":
                    lat_format = "charge"
                    break
                else:
                    print(">ERROR:  Output type not implemented  Try again...")
    else:
        # Not implemented, should not get here
        sys.exit()

    # Finally the spiro interstitials distribution
    print("\nFinally determine the distribution of the spiro interstitials")

    # uniform or custom distribution
    while True:
        int_dist = input('c = custom\n'
                         'n = none\n'
                         'r = ramp\n'
                         'u = uniform\n'
                         'Enter spiro interstitial distribution in the lattice [default uniform]: ').lower()
        # set default
        if int_dist == "":
            int_dist = "uniform"

        # handle options
        if int_dist == "c" or int_dist == "custom":
            int_dist = "custom"
            print("\nUser to choose the concentration of spiro interstitials for each layer")
            layers = len(my_stacking) * my_cells[2]
            layer_int_conc = []

            for i in range(layers):
                while True:
                    try:
                        int_pc = input(f'Enter the percentage of spiro interstitials for layer {i} [default  1.0]: ')
                        if int_pc == "":
                            int_pc = 1.0
                            break
                        else:
                            int_pc = float(int_pc)
                            if int_pc >= 0:
                                break
                            else:
                                print(">ERROR:  Number must not be negative.  Try again...")
                    except ValueError:
                        print("ERROR:  That was not a valid number.  Try again...")
                layer_int_conc.append(int_pc)
            break
        elif int_dist == "n" or int_dist == "none":
            int_dist = "none"
            # array remains at default zero value
            layer_int_conc = [0.0 for i in range(len(my_stacking) * my_cells[2])]
            break
        elif int_dist == "r" or int_dist == "ramp":
            int_dist = "ramp"
            print("\nPercentage of spiro interstitials varies linearly from p1 at the edges to p2 at the centre")
            while True:
                try:
                    int_pc1 = input('Enter the percentage of spiro interstitials on layer 1 [default  0.0]: ')
                    if int_pc1 == "":
                        int_pc1 = 0.0
                        break
                    else:
                        int_pc1 = float(int_pc1)
                        if int_pc1 >= 0:
                            break
                        else:
                            print(">ERROR:  Number must not be negative.  Try again...")
                except ValueError:
                    print("ERROR:  That was not a valid number.  Try again...")

            while True:
                try:
                    int_pc2 = input('Enter the percentage of spiro interstitials at the centre [default  0.0]: ')
                    if int_pc2 == "":
                        int_pc2 = 0.0
                        break
                    else:
                        int_pc2 = float(int_pc2)
                        if int_pc2 >= 0:
                            break
                        else:
                            print(">ERROR:  Number must not be negative.  Try again...")
                except ValueError:
                    print("ERROR:  That was not a valid number.  Try again...")

            # set values
            layers = len(my_stacking) * my_cells[2]
            layers2 = int(layers / 2)
            m = (int_pc2 - int_pc1) / layers2
            layer_int_conc = []
            for i in range(layers):
                if i <= layers2:
                    layer_int_conc.append(int_pc1 + m * i)
                else:
                    layer_int_conc.append(int_pc2 - m * (i - layers2))
            break
        elif int_dist == "u" or int_dist == "uniform":
            int_dist = "uniform"
            # set conc equal for all layers
            print("Percentage of spiro interstitials will be equal for all layers")
            while True:
                try:
                    int_pc = input('Enter the percentage of spiro interstitials [default  1.0]: ')
                    if int_pc == "":
                        int_pc = 1.0
                        break
                    else:
                        int_pc = float(int_pc)
                        if int_pc >= 0:
                            break
                        else:
                            print(">ERROR:  Number must not be negative.  Try again...")
                except ValueError:
                    print("ERROR:  That was not a valid number.  Try again...")
            layer_int_conc = [int_pc for i in range(len(my_stacking) * my_cells[2])]
            break
        else:
            print(">ERROR:  Output type not implemented  Try again...")

    '''print(my_cells)
    print(my_stacking)
    print(ot)
    print(lat_a)
    print(lat_c)
    print(lat_format)
    print(layer_int_conc)'''

    # call the graphite generator function
    lammps_gen_graphite_general_spiro_interstitial(verbose=True,
                                                   forced=True,
                                                   a_const=lat_a,
                                                   c_const=lat_c,
                                                   stacking=my_stacking,
                                                   cells=my_cells,
                                                   filename='lammps.lattice.dat',
                                                   lattice_model=ot,
                                                   output_format=lat_format,
                                                   layer_int_conc=layer_int_conc
                                                   )
