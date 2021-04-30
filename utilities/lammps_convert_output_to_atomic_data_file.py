#!/usr/bin/env python

# This script reads a lammps dump file, and generates a lammps input data file.
# This can then be used by lammps input scripts.

# Output depends on what columns are available in the dump file.
#   If no ID column is available, atoms are numbered sequentially.
#   If no element column is available, no specie list or atomic masses are output.
#   If no element and no type column is available, all atoms are assumed to be type 1.

# The script needs to know the filename of the lammps dump files.
# When run interactively, this can be passed on the commandline, or the script can ask the user.

# Kenny Jolley  June 2019

import sys
import os
import gzip

# Self contained function converts a given lammps dump file to a lammps data file (atomic format).
def lammps_convert_output_to_atomic_data_file(filename, **kwargs):
    # Default keyword args
    verbose = kwargs.get('verbose', True)
    output_prefix = kwargs.get('output_prefix', 'lammps_')

    # Globals
    specie_list = ["ZZ"]
    #    ! Atomic symbols
    atomic_symbol = ["HH" for _ in range(114)]
    atomic_symbol[0] = "ZZ"
    atomic_symbol[1] = "H"
    atomic_symbol[2] = "He"
    atomic_symbol[3] = "Li"
    atomic_symbol[4] = "Be"
    atomic_symbol[5] = "B"
    atomic_symbol[6] = "C"
    atomic_symbol[7] = "N"
    atomic_symbol[8] = "O"
    atomic_symbol[9] = "F"
    atomic_symbol[10] = "Ne"
    atomic_symbol[11] = "Na"
    atomic_symbol[12] = "Mg"
    atomic_symbol[13] = "Al"
    atomic_symbol[14] = "Si"
    atomic_symbol[15] = "P"
    atomic_symbol[16] = "S"
    atomic_symbol[17] = "Cl"
    atomic_symbol[18] = "Ar"
    atomic_symbol[19] = "K"
    atomic_symbol[20] = "Ca"
    atomic_symbol[21] = "Sc"
    atomic_symbol[22] = "Ti"
    atomic_symbol[23] = "V"
    atomic_symbol[24] = "Cr"
    atomic_symbol[25] = "Mn"
    atomic_symbol[26] = "Fe"
    atomic_symbol[27] = "Co"
    atomic_symbol[28] = "Ni"
    atomic_symbol[29] = "Cu"
    atomic_symbol[30] = "Zn"
    atomic_symbol[31] = "Ga"
    atomic_symbol[32] = "Ge"
    atomic_symbol[33] = "As"
    atomic_symbol[34] = "Se"
    atomic_symbol[35] = "Br"
    atomic_symbol[36] = "Kr"
    atomic_symbol[37] = "Rb"
    atomic_symbol[38] = "Sr"
    atomic_symbol[39] = "Y"
    atomic_symbol[40] = "Zr"
    atomic_symbol[41] = "Nb"
    atomic_symbol[42] = "Mo"
    atomic_symbol[43] = "Tc"
    atomic_symbol[44] = "Ru"
    atomic_symbol[45] = "Rh"
    atomic_symbol[46] = "Pd"
    atomic_symbol[47] = "Ag"
    atomic_symbol[48] = "Cd"
    atomic_symbol[49] = "In"
    atomic_symbol[50] = "Sn"
    atomic_symbol[51] = "Sb"
    atomic_symbol[52] = "Te"
    atomic_symbol[53] = "I"
    atomic_symbol[54] = "Xe"
    atomic_symbol[55] = "Cs"
    atomic_symbol[56] = "Ba"
    atomic_symbol[57] = "La"
    atomic_symbol[58] = "Ce"
    atomic_symbol[59] = "Pr"
    atomic_symbol[60] = "Nd"
    atomic_symbol[61] = "Pm"
    atomic_symbol[62] = "Sm"
    atomic_symbol[63] = "Eu"
    atomic_symbol[64] = "Gd"
    atomic_symbol[65] = "Tb"
    atomic_symbol[66] = "Dy"
    atomic_symbol[67] = "Ho"
    atomic_symbol[68] = "Er"
    atomic_symbol[69] = "Tm"
    atomic_symbol[70] = "Yb"
    atomic_symbol[71] = "Lu"
    atomic_symbol[72] = "Hf"
    atomic_symbol[73] = "Ta"
    atomic_symbol[74] = "W"
    atomic_symbol[75] = "Re"
    atomic_symbol[76] = "Os"
    atomic_symbol[77] = "Ir"
    atomic_symbol[78] = "Pt"
    atomic_symbol[79] = "Au"
    atomic_symbol[80] = "Hg"
    atomic_symbol[81] = "Tl"
    atomic_symbol[82] = "Pb"
    atomic_symbol[83] = "Bi"
    atomic_symbol[84] = "Po"
    atomic_symbol[85] = "At"
    atomic_symbol[86] = "Rn"
    atomic_symbol[87] = "Fr"
    atomic_symbol[88] = "Ra"
    atomic_symbol[89] = "Ac"
    atomic_symbol[90] = "Th"
    atomic_symbol[91] = "Pa"
    atomic_symbol[92] = "U"
    atomic_symbol[93] = "Np"
    atomic_symbol[94] = "Pu"
    atomic_symbol[95] = "Am"
    atomic_symbol[96] = "Cm"
    atomic_symbol[97] = "Bk"
    atomic_symbol[98] = "Cf"
    atomic_symbol[99] = "Es"
    atomic_symbol[100] = "Fm"
    atomic_symbol[101] = "Md"
    atomic_symbol[102] = "No"
    atomic_symbol[103] = "Lr"
    atomic_symbol[104] = "Rf"
    atomic_symbol[105] = "Db"
    atomic_symbol[106] = "Sg"
    atomic_symbol[107] = "Bh"
    atomic_symbol[108] = "Hs"
    atomic_symbol[109] = "Mt"
    atomic_symbol[110] = "Ds"
    atomic_symbol[111] = "Rg"
    atomic_symbol[112] = "Cn"
    atomic_symbol[113] = "FF"  # needed for Fe3+ symbol

    #  Atomic masses in amu
    #  amu = 1.660538921E-27  # in kg
    atomic_mass = [0.0 for _ in range(114)]
    #    atomic mass (in AMU) of an element from Wikipedia (http://en.wikipedia.org/wiki/)
    atomic_mass[0] = 0.000  # ZERO
    atomic_mass[1] = 1.008  # H_    ! Wiki
    atomic_mass[2] = 4.002602  # He    ! Wiki
    atomic_mass[3] = 6.94  # Li    ! Wiki
    atomic_mass[4] = 9.012182  # Be    ! Wiki
    atomic_mass[5] = 10.81  # B_    ! Wiki
    atomic_mass[6] = 12.011  # C_    ! Wiki
    atomic_mass[7] = 14.007  # N_    ! Wiki
    atomic_mass[8] = 15.9994  # O_    ! Wiki
    atomic_mass[9] = 18.998403163  # F_    ! Wiki
    atomic_mass[10] = 20.1797  # Ne    ! Wiki
    atomic_mass[11] = 22.98976928  # Na    ! Wiki
    atomic_mass[12] = 24.305  # Mg    ! Wiki
    atomic_mass[13] = 26.98153857  # Al    ! Wiki
    atomic_mass[14] = 28.0851  # Si    ! Wiki
    atomic_mass[15] = 30.973761998  # P_    ! Wiki
    atomic_mass[16] = 32.066  # S_    ! Wiki
    atomic_mass[17] = 35.45  # Cl    ! Wiki
    atomic_mass[18] = 39.948  # Ar    ! Wiki
    atomic_mass[19] = 39.0983  # K_    ! Wiki
    atomic_mass[20] = 40.078  # Ca    ! Wiki
    atomic_mass[21] = 44.955908  # Sc    ! Wiki
    atomic_mass[22] = 47.867  # Ti    ! Wiki
    atomic_mass[23] = 50.9415  # V_    ! Wiki
    atomic_mass[24] = 51.9961  # Cr    ! Wiki
    atomic_mass[25] = 54.938044  # Mn    ! Wiki
    atomic_mass[26] = 55.845  # Fe    ! Wiki
    atomic_mass[27] = 58.933194  # Co    ! Wiki
    atomic_mass[28] = 58.6934  # Ni    ! Wiki
    atomic_mass[29] = 63.546  # Cu    ! Wiki
    atomic_mass[30] = 65.38  # Zn    ! Wiki
    atomic_mass[31] = 69.723  # Ga    ! Wiki
    atomic_mass[32] = 72.63  # Ge    ! Wiki
    atomic_mass[33] = 74.921595  # As    ! Wiki
    atomic_mass[34] = 78.971  # Se    ! Wiki
    atomic_mass[35] = 79.904  # Br    ! Wiki
    atomic_mass[36] = 83.798  # Kr    ! Wiki
    atomic_mass[37] = 85.4678  # Rb    ! Wiki
    atomic_mass[38] = 87.62  # Sr    ! Wiki
    atomic_mass[39] = 88.90584  # Y_    ! Wiki
    atomic_mass[40] = 91.224  # Zr    ! Wiki
    atomic_mass[41] = 92.90637  # Nb    ! Wiki
    atomic_mass[42] = 95.95  # Mo    ! Wiki
    atomic_mass[43] = 98.0  # Tc    ! Wiki
    atomic_mass[44] = 101.07  # Ru    ! Wiki
    atomic_mass[45] = 102.9055  # Rh    ! Wiki
    atomic_mass[46] = 106.42  # Pd    ! Wiki
    atomic_mass[47] = 107.8682  # Ag    ! Wiki
    atomic_mass[48] = 112.414  # Cd    ! Wiki
    atomic_mass[49] = 114.818  # In    ! Wiki
    atomic_mass[50] = 118.710  # Sn    ! Wiki
    atomic_mass[51] = 121.760  # Sb    ! Wiki  http://en.wikipedia.org/wiki/Antimony
    atomic_mass[52] = 127.60  # Te    ! Wiki  http://en.wikipedia.org/wiki/Tellurium
    atomic_mass[53] = 126.90447  # I_    ! Wiki  http://en.wikipedia.org/wiki/Iodine
    atomic_mass[54] = 131.293  # Xe    ! Wiki  http://en.wikipedia.org/wiki/Xenon
    atomic_mass[55] = 132.90545196  # Cs    ! Wiki  http://en.wikipedia.org/wiki/Caesium
    atomic_mass[56] = 137.327  # Ba    ! Wiki  http://en.wikipedia.org/wiki/Barium
    atomic_mass[57] = 138.90547  # La    ! Wiki  http://en.wikipedia.org/wiki/Lanthanum
    atomic_mass[58] = 140.116  # Ce    ! Wiki  http://en.wikipedia.org/wiki/Cerium
    atomic_mass[59] = 140.90766  # Pr    ! Wiki  http://en.wikipedia.org/wiki/Praseodymium
    atomic_mass[60] = 144.242  # Nd    ! Wiki  http://en.wikipedia.org/wiki/Neodymium
    atomic_mass[61] = 145.0  # Pm    ! Wiki  http://en.wikipedia.org/wiki/Promethium
    atomic_mass[62] = 150.36  # Sm    ! Wiki  http://en.wikipedia.org/wiki/Samarium
    atomic_mass[63] = 151.964  # Eu    ! Wiki  http://en.wikipedia.org/wiki/Europium
    atomic_mass[64] = 157.25  # Gd    ! Wiki  http://en.wikipedia.org/wiki/Gadolinium
    atomic_mass[65] = 158.92535  # Tb    ! Wiki  http://en.wikipedia.org/wiki/Terbium
    atomic_mass[66] = 162.5  # Dy    ! Wiki  http://en.wikipedia.org/wiki/Dysprosium
    atomic_mass[67] = 164.93033  # Ho    ! Wiki  http://en.wikipedia.org/wiki/Holmium
    atomic_mass[68] = 167.259  # Er    ! Wiki  http://en.wikipedia.org/wiki/Erbium
    atomic_mass[69] = 168.93422  # Tm    ! Wiki  http://en.wikipedia.org/wiki/Thulium
    atomic_mass[70] = 173.054  # Yb    ! Wiki  http://en.wikipedia.org/wiki/Ytterbium
    atomic_mass[71] = 174.9668  # Lu    ! Wiki  http://en.wikipedia.org/wiki/Lutetium
    atomic_mass[72] = 178.49  # Hf    ! Wiki  http://en.wikipedia.org/wiki/Hafnium
    atomic_mass[73] = 180.94788  # Ta    ! Wiki  http://en.wikipedia.org/wiki/Tantalum
    atomic_mass[74] = 183.84  # W_    ! Wiki  http://en.wikipedia.org/wiki/Tungsten
    atomic_mass[75] = 186.207  # Re    ! Wiki  http://en.wikipedia.org/wiki/Rhenium
    atomic_mass[76] = 190.23  # Os    ! Wiki  http://en.wikipedia.org/wiki/Osmium
    atomic_mass[77] = 192.217  # Ir    ! Wiki  http://en.wikipedia.org/wiki/Iridium
    atomic_mass[78] = 195.084  # Pt    ! Wiki  http://en.wikipedia.org/wiki/Platinum
    atomic_mass[79] = 196.966569  # Au    ! Wiki  http://en.wikipedia.org/wiki/Gold
    atomic_mass[80] = 200.592  # Hg    ! Wiki  http://en.wikipedia.org/wiki/Mercury_%28element%29
    atomic_mass[81] = 204.38  # Tl    ! Wiki  http://en.wikipedia.org/wiki/Thallium
    atomic_mass[82] = 207.2  # Pb    ! Wiki  http://en.wikipedia.org/wiki/Lead
    atomic_mass[83] = 208.98040  # Bi    ! Wiki  http://en.wikipedia.org/wiki/Bismuth
    atomic_mass[84] = 209.0  # Po    ! Wiki  http://en.wikipedia.org/wiki/Polonium
    atomic_mass[85] = 210.0  # At    ! Wiki  http://en.wikipedia.org/wiki/Astatine
    atomic_mass[86] = 222.0  # Rn    ! Wiki  http://en.wikipedia.org/wiki/Radon
    atomic_mass[87] = 223.0  # Fr    ! Wiki  http://en.wikipedia.org/wiki/Francium
    atomic_mass[88] = 226.0  # Ra    ! Wiki  http://en.wikipedia.org/wiki/Radium
    atomic_mass[89] = 227.0  # Ac    ! Wiki  http://en.wikipedia.org/wiki/Actinium
    atomic_mass[90] = 232.0377  # Th    ! Wiki  http://en.wikipedia.org/wiki/Thorium
    atomic_mass[91] = 231.03588  # Pa    ! Wiki  http://en.wikipedia.org/wiki/Protactinium
    atomic_mass[92] = 238.02891  # U_    ! Wiki  http://en.wikipedia.org/wiki/Uranium
    atomic_mass[93] = 237.0  # Np    ! Wiki  http://en.wikipedia.org/wiki/Neptunium
    atomic_mass[94] = 244.0  # Pu    ! Wiki  http://en.wikipedia.org/wiki/Plutonium
    atomic_mass[95] = 243.0  # Am    ! Wiki  http://en.wikipedia.org/wiki/Americium
    atomic_mass[96] = 247.0  # Cm    ! Wiki  http://en.wikipedia.org/wiki/Curium
    atomic_mass[97] = 247.0  # Bk    ! Wiki  http://en.wikipedia.org/wiki/Berkelium
    atomic_mass[98] = 251.0  # Cf    ! Wiki  http://en.wikipedia.org/wiki/Californium
    atomic_mass[99] = 252.0  # Es    ! Wiki  http://en.wikipedia.org/wiki/Einsteinium
    atomic_mass[100] = 257.0  # Fm    ! Wiki  http://en.wikipedia.org/wiki/Fermium
    atomic_mass[101] = 258.0  # Md    ! Wiki  http://en.wikipedia.org/wiki/Mendelevium
    atomic_mass[102] = 259.0  # No    ! Wiki  http://en.wikipedia.org/wiki/Nobelium
    atomic_mass[103] = 262.0  # Lr    ! Wiki  http://en.wikipedia.org/wiki/Lawrencium
    atomic_mass[104] = 267.0  # Rf    ! Wiki  http://en.wikipedia.org/wiki/Rutherfordium
    atomic_mass[105] = 268.0  # Db    ! Wiki  http://en.wikipedia.org/wiki/Dubnium
    atomic_mass[106] = 269.0  # Sg    ! Wiki  http://en.wikipedia.org/wiki/Seaborgium
    atomic_mass[107] = 270.0  # Bh    ! Wiki  http://en.wikipedia.org/wiki/Bohrium
    atomic_mass[108] = 269.0  # Hs    ! Wiki  http://en.wikipedia.org/wiki/Hassium
    atomic_mass[109] = 278.0  # Mt    ! Wiki  http://en.wikipedia.org/wiki/Meitnerium
    atomic_mass[110] = 281.0  # Ds    ! Wiki  http://en.wikipedia.org/wiki/Darmstadtium
    atomic_mass[111] = 281.0  # Rg    ! Wiki  http://en.wikipedia.org/wiki/Roentgenium
    atomic_mass[112] = 285.0  # Cn    ! Wiki  http://en.wikipedia.org/wiki/Copernicium
    atomic_mass[113] = 55.845  # Fe3+    ! Wiki

    # Welcome
    if verbose:
        print("  +--------------------------------------+")
        print("  |     Converts LAMMPS output files     |")
        print("  |     to lammps atomic data files      |")
        print("  |                                      |")
        print("  |            Kenny Jolley              |")
        print("  |             April 2021               |")
        print("  +--------------------------------------+")
        print("   ")

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
    outputfile = open(filename_out, 'w')

    # default no atoms
    atoms = 0

    # default column indices
    x_col = -1
    y_col = -1
    z_col = -1
    element_col = -1
    id_col = -1
    type_col = -1

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

        # Read the timestep
        if (fileline[0] == "ITEM:") and (fileline[1] == "TIMESTEP"):
            # The next line contains current timestep
            fileline = infile.readline()
            fileline = fileline.split()
            timestep = int(fileline[0])
            if verbose:
                print("ITEM: TIMESTEP\n" + str(timestep))

        # Read the number of atoms
        if (fileline[0] == "ITEM:") and (fileline[1] == "NUMBER") and (fileline[3] == "ATOMS"):
            # next line is the number of atoms
            fileline = infile.readline()
            fileline = fileline.split()
            atoms = int(fileline[0])
            if verbose:
                print("ITEM: NUMBER OF ATOMS\n" + str(atoms))

        # Read the bounding box parameters
        if (fileline[0] == "ITEM:") and (fileline[1] == "BOX") and (fileline[2] == "BOUNDS"):
            # next lines are the box size
            # save the box size  ( this assumes 3D with lo and hi params given )
            # boundary type is ignored.
            # x
            fileline = infile.readline()
            fileline = fileline.split()
            xlo = float(fileline[0])
            xhi = float(fileline[1])
            # y
            fileline = infile.readline()
            fileline = fileline.split()
            ylo = float(fileline[0])
            yhi = float(fileline[1])
            # z
            fileline = infile.readline()
            fileline = fileline.split()
            zlo = float(fileline[0])
            zhi = float(fileline[1])

            if verbose:
                print("ITEM: BOX BOUNDS\n" +
                      str(xlo) + "  " + str(xhi) + "\n" +
                      str(ylo) + "  " + str(yhi) + "\n" +
                      str(zlo) + "  " + str(zhi) + "\n")

        # Read the atom data
        if (fileline[0] == "ITEM:") and (fileline[1] == "ATOMS"):
            if verbose:
                print("ITEM: ATOMS")
            # find the column indices
            for i in range(2, len(fileline)):
                if fileline[i] == "x":
                    x_col = i - 2
                    if verbose:
                        print("X column found at: " + str(x_col))
                if fileline[i] == "y":
                    y_col = i - 2
                    if verbose:
                        print("Y column found at: " + str(y_col))
                if fileline[i] == "z":
                    z_col = i - 2
                    if verbose:
                        print("Z column found at: " + str(z_col))
                if fileline[i] == "element":
                    element_col = i - 2
                    if verbose:
                        print("element column found at: " + str(element_col))
                if fileline[i] == "id":
                    id_col = i - 2
                    if verbose:
                        print("id column found at: " + str(id_col))
                if fileline[i] == "type":
                    type_col = i - 2
                    if verbose:
                        print("type column found at: " + str(type_col))
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
            if element_col == -1:
                print("element column was not found")
                if type_col == -1:
                    print("type column was not found")
                    print(">> Warning: No element or atom type information is available")
                    print(">>          Assuming all atoms are of type 1")
                    max_types = 1
                else:
                    print(">> Warning: No element information is available")
                    print(">>          Using only type information from the type column")
                    max_types = 0
            else:
                # ensure we have this defined
                max_types = 0

            if id_col == -1:
                print("id column was not found")
                print("Atom ID's not known, assuming sequential")
            # break out of the while loop
            break

    # set up array for storing atom data
    atom_x_pos = [0 for _ in range(atoms + 1)]
    atom_y_pos = [0 for _ in range(atoms + 1)]
    atom_z_pos = [0 for _ in range(atoms + 1)]
    atom_type = [0 for _ in range(atoms + 1)]
    id_counter = 1
    atom_type_specie = [0 for _ in range(114)]

    # --- Now read the atom data and save to output file ---
    for i in range(1, atoms + 1):
        # read line, exit if at end of file
        fileline = infile.readline()
        if not fileline:
            break
        fileline = fileline.split()

        # Find ID
        # Do we have ID col?
        if id_col == -1:
            cur_id = int(id_counter)
            id_counter = id_counter + 1
        else:
            cur_id = int(fileline[id_col])

        # Save positions
        atom_x_pos[cur_id] = float(fileline[x_col])
        atom_y_pos[cur_id] = float(fileline[y_col])
        atom_z_pos[cur_id] = float(fileline[z_col])

        # Do we have a type col?
        if type_col != -1:
            atom_type[cur_id] = int(fileline[type_col])
            max_types = max(max_types, atom_type[cur_id])
            # do we have element col?
            if element_col != -1:
                atom_type_specie[atom_type[cur_id]] = fileline[element_col]

        else:
            # if not, we must have an element col
            if element_col != -1:

                # see if element exists in current list, if not, add it
                array_index = -1
                for j in range(0, len(specie_list)):
                    if fileline[element_col] == specie_list[j]:
                        array_index = j
                # if array_index is still -1, we need to add it
                if array_index == -1:
                    specie_list.append(fileline[element_col])
                    array_index = len(specie_list) - 1
                    max_types = array_index

                atom_type[cur_id] = int(array_index)
            else:
                # just set type to 1
                atom_type[cur_id] = 1

    # Now we need to set element list
    if type_col != -1:
        if element_col != -1:
            # create list
            specie_str = " # "
            for j in range(1, max_types + 1):
                specie_str = specie_str + atom_type_specie[j] + " "
        else:
            # null list
            specie_str = " "
    else:
        if element_col != -1:
            # create list
            specie_str = " # "
            for j in range(1, len(specie_list)):
                specie_str = specie_str + specie_list[j] + " "
        else:
            # null list
            specie_str = " "

    if element_col != -1:
        print(specie_str)

    # close the input file
    infile.close()

    # Output Lammps header
    outputfile.write("Lammps data file generated from lammps dump file: " + str(filename) + "\n")
    outputfile.write("#  The timestep read was: " + str(timestep) + "\n")
    outputfile.write(str(atoms) + " atoms\n\n")

    # atom types line
    outputfile.write(str(max_types) + " atom types" + str(specie_str) + "\n")

    # Cell dimensions
    outputfile.write("\n")
    outputfile.write(str(xlo) + "  " + str(xhi) + " xlo xhi\n")
    outputfile.write(str(ylo) + "  " + str(yhi) + " ylo yhi\n")
    outputfile.write(str(zlo) + "  " + str(zhi) + " zlo zhi\n")

    # Masses  (note we can only add the masses if we know the elements)
    if element_col != -1:
        outputfile.write("\nMasses\n\n")
        if type_col != -1:
            for j in range(1, max_types + 1):
                for i in range(114):
                    if atomic_symbol[i] == atom_type_specie[j]:
                        mass = i
                        break
                mass = atomic_mass[int(mass)]
                outputfile.write(str(j) + " " + str(mass) + "\n")
        else:
            for j in range(1, len(specie_list)):
                for i in range(114):
                    if atomic_symbol[i] == specie_list[j]:
                        mass = i
                        break
                mass = atomic_mass[int(mass)]
                outputfile.write(str(j) + " " + str(mass) + "\n")

    # Atom data
    outputfile.write("\n")
    outputfile.write("Atoms # atomic\n")
    outputfile.write("\n")
    for i in range(1, atoms + 1):
        outputfile.write(str(i) + "   ")

        outputfile.write(str(atom_type[i]) + "    ")

        outputfile.write(str(atom_x_pos[i]) + "    ")
        outputfile.write(str(atom_y_pos[i]) + "    ")
        outputfile.write(str(atom_z_pos[i]) + "    ")

        outputfile.write("\n")

    # All done, close output file
    outputfile.close()


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    # Get the filename
    if len(sys.argv) > 1:
        input_filename = str(sys.argv[1])
    else:
        input_filename = str(input('Enter the filename to convert : '))

    # if filename contains a * char, loop through all files in current directory
    # with the same prefix and suffix
    if "*" not in input_filename:
        print('No star - just converting given file')
        # call the function
        lammps_convert_output_to_atomic_data_file(input_filename, verbose=True)
    else:
        # Star in filename, search whole dir for matching files
        print('Star in filename - Trying to convert all files that match pattern')
        filename_list = input_filename.split('*')
        filename_prefix = filename_list[0]
        filename_suffix = filename_list[1]
        # get a list of files in the directory
        file_list = os.listdir(os.getcwd())

        # filter list to include valid files only
        for file in file_list:
            if filename_prefix == file[:len(filename_prefix)]:
                if filename_suffix == file[-len(filename_suffix):]:
                    print("Converting file: ", file)
                    # call the function
                    lammps_convert_output_to_atomic_data_file(file, verbose=True)
