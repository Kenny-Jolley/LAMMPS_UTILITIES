#!/usr/bin/env python

# This function generates an AA stacked graphite lattice
# with a user specified atom intercalated between the planes.
# The output is a lammps data file in atomic format (ID, Type, x, y, z).

# Keyword arguments:
# verbose = True   , prints some comments to the screen.
# forced  = True   , will overwrite the existing file (if it exists).
# forced  = False  , if file exists, will ask the user if the existing file should be overwritten.
# a_const = 2.466 , the 'a' lattice constant
# c_const = 3.358  , the 'c' lattice constant
# filename = lammps.lattice.dat  , the output filename
# cells = [x,y,z]  , No. unit cells to generate for each direction.
# intercalant = 'Li'  The intercalated atom

# vdW-df-cx
# a_const = 2.466
# c_const = 6.575/2
# vdW-df-obk8
# a_const = 2.465
# c_const = 6.699/2
# vdW-df-ob86
# a_const = 2.466
# c_const = 6.637/2

# Kenny Jolley, April 2023

import sys
import os
import math


# Function create
def lammps_gen_graphite_aa_intercalate_mc8(**kwargs):
    # Default keyword args
    verbose = kwargs.get('verbose', False)
    forced = kwargs.get('forced', False)
    intercalant = kwargs.get('intercalant', 'Na')
    # Default constants
    a_const = kwargs.get('a_const', 2.466)
    c_const = kwargs.get('c_const', 3.6)
    filename = kwargs.get('filename', 'lammps.lattice.dat')
    cells = kwargs.get('cells', [1, 1, 1])

    # Globals
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
    #  1 amu = 1.660538921E-27 kg
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

    # cells in x and y dir should be divisible by 2 for periodicity
    if cells[1] % 2 != 0:
        print(f'unit cells in y direction must be divisible by two')
        print('>>>ERROR<<<')
        return
    if cells[0] % 2 != 0:
        print(f'unit cells in x direction must be divisible by two')
        print('>>>ERROR<<<')
        return

    # box size and atom total
    box_x = math.sqrt(3) * a_const * cells[0]
    box_y = a_const * cells[1]
    box_z = c_const * cells[2]
    tot_atoms = int(4 * cells[0] * cells[1] * cells[2] +
                    1 / 2 * cells[0] * cells[1] * cells[2])

    # Welcome
    if verbose:
        print("  +------------------------------------------+")
        print("  |         Lattice generator script         |")
        print("  |             Graphite lattice             |")
        print("  |         with intercalated element MC8    |")
        print("  |       x and y dimension divisible by 2   |")
        print("  |               Kenny Jolley               |")
        print("  |                April 2023                |")
        print("  +------------------------------------------+")
        print("   ")

        print(f">  Echoing back the user supplied data")
        print(f"     Lattice constant a   [Ang]: {a_const}")
        print(f"     Layer separation c/2 [Ang]: {c_const}")
        print(f">  Graphite lattice with unit cell repeats:")
        print(f"     cells_x: {cells[0]}")
        print(f"     cells_y: {cells[1]}")
        print(f"     cells_z: {cells[2]}")
        print(f">  Graphite lattice cell dimensions [Ang]:")
        print(f"     box_x:   {box_x}")
        print(f"     box_y:   {box_y}")
        print(f"     box_z:   {box_z}")
        print(f">  Stacking: AA")
        print(f">  Intercalated element: {intercalant}")
        print(f">  Total number of atoms: {tot_atoms}")

    # Set generate file flag to true
    gen_file = True

    # Check if the file already exists
    if not forced:
        if os.path.isfile(filename):
            print(f"> Existing file {filename} detected.")
            print("> lammps_gen_graphite_aa_intercalate_mc8 function wants to overwrite this file")

            user_choice = input('Do you wish to overwrite the existing file? (y/n): ')
            user_choice = user_choice.lower()

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
            print(f"Opened file: {file.name}")

        # Write header info
        file.write("Lammps data file generated by lammps_gen_graphite_aa_intercalate_mc8\n")
        file.write(f"# Graphite {cells[0]}x{cells[1]}x{cells[2]} Unit cells, " +
                   f"MC8 intercalation with {intercalant} in AA stacking. " +
                   f" a_param = {a_const}, c_param = {c_const}\n")
        file.write(f"{tot_atoms} atoms\n\n")
        file.write(f"2 atom types # C {intercalant}\n\n")
        file.write(f"0.0 {box_x} xlo xhi\n")
        file.write(f"0.0 {box_y} ylo yhi\n")
        file.write(f"0.0 {box_z} zlo zhi\n\n")
        file.write("Masses\n\n")
        file.write("1 12.011\n")

        element_not_found = True
        for i in range(114):
            if atomic_symbol[i] == intercalant:
                file.write(f'2 {atomic_mass[i]}\n\n')
                element_not_found = False
                break
        if element_not_found:
            print('>>> ERROR <<<')
            print(f'The element {intercalant} given is not valid')
            return

        file.write("Atoms # atomic\n\n")

        # ID mol charge x y z
        count = 1
        for x in range(0, cells[0]):
            x_shift = x * math.sqrt(3) * a_const
            for y in range(0, cells[1]):
                y_shift = y * a_const
                for z in range(0, cells[2]):
                    z_shift = z * c_const
                    file.write(f'{count}  1  {x_shift:.12f} {y_shift:.12f} {z_shift:.12f}\n')
                    file.write(f'{count + 1}  1  {x_shift + a_const * 2.0 / math.sqrt(3):.12f} ' +
                               f'{y_shift:.12f} {z_shift:.12f}\n')
                    file.write(f'{count + 2}  1  {x_shift + a_const * math.sqrt(3) / 6.0:.12f} ' +
                               f'{y_shift + a_const / 2.0:.12f} {z_shift:.12f}\n')
                    file.write(f'{count + 3}  1  {x_shift + a_const * math.sqrt(3) / 2.0:.12f} ' +
                               f'{y_shift + a_const / 2.0:.12f} {z_shift:.12f}\n')
                    count += 4

        # intercalated elements
        for x in range(0, cells[0]):
            x_shift = x * math.sqrt(3) * a_const
            for y in range(0, cells[1]):
                y_shift = y * a_const
                for z in range(0, cells[2]):
                    z_shift = z * c_const + 0.5 * c_const
                    # for even y row
                    if y % 2 == 0:
                        if x % 2 == 0:
                            file.write(f'{count}  2  {x_shift + a_const / math.sqrt(3):.12f} ' +
                                       f'{y_shift:.12f} {z_shift:.12f}\n')
                            count += 1
                    else:
                        if x % 2 == 1:
                            file.write(f'{count}  2  {x_shift + a_const / math.sqrt(3):.12f} ' +
                                       f'{y_shift:.12f} {z_shift:.12f}\n')
                            count += 1
        file.close()

        if verbose:
            print(f"file closed: {file.name}")
            print("COMPLETED lattice.dat output !!")


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    # Default cell and stacking
    cells_user = [1, 1, 1]
    int_element = 'Na'

    # Read number of lattice cells from the command-line, or supply interactively
    if len(sys.argv) > 1:
        print(">  Using information passed on the command-line")
        # 3 params = cell size, default ab stacking
        if len(sys.argv) == 4:
            cells_user[0] = int(sys.argv[1])
            cells_user[1] = int(sys.argv[2])
            cells_user[2] = int(sys.argv[3])
        # 4 params = cell size, user chosen element
        elif len(sys.argv) == 5:
            cells_user[0] = int(sys.argv[1])
            cells_user[1] = int(sys.argv[2])
            cells_user[2] = int(sys.argv[3])
            int_element = str(sys.argv[4])
        else:
            print(">>> ERROR  <<<")
            print("  User must pass either 3 or 4 command-line arguments")
            print("   3 params = box_x, box_y, box_z  (integers)")
            print("   4 params = box_x, box_y, box_z  (integers), Intercalant (string e.g.: Li, Na)")
            print("    examples")
            print("   lammps_gen_graphite_AA_intercalate_C8N.py 2 2 1")
            print("   lammps_gen_graphite_AA_intercalate_C8N.py 2 4 2 Li")
            print("   lammps_gen_graphite_AA_intercalate_C8N.py 4 4 2 Na")
            sys.exit()

    else:
        # Otherwise, ask user, cell dimensions
        while True:
            try:
                cell_size = int(input('Enter number of cells in x dir (must be divisible by 2): '))
                if cell_size > 0:
                    if cell_size % 2 == 0:
                        break
                    else:
                        print(f'You entered {cell_size} which is not divisible by 2. Try again...')
                else:
                    print(f"You entered {cell_size}, but number of unit cells must be greater than 0. Try again...")
            except ValueError:
                print(f"Value entered is not a valid integer.  Try again...")
        cells_user[0] = cell_size
        while True:
            try:
                cell_size = int(input('Enter number of cells in y dir (must be divisible by 2): '))
                if cell_size > 0:
                    if cell_size % 2 == 0:
                        break
                    else:
                        print(f'You entered {cell_size} which is not divisible by 2. Try again...')
                else:
                    print(f"You entered {cell_size}, but number of unit cells must be greater than 0. Try again...")
            except ValueError:
                print(f"Value entered is not a valid integer.  Try again...")
        cells_user[1] = cell_size
        while True:
            try:
                cell_size = int(input('Enter number of cells in z dir : '))
                if cell_size > 0:
                    break
                else:
                    print("Oops!  Integer must be greater than 0.  Try again...")
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")
        cells_user[2] = cell_size

        # Intercalated element
        user_input = input(f'Enter element to intercalate (default: {int_element}): ')
        if len(user_input) != 0:
            int_element = user_input

    # call the graphite generator function
    lammps_gen_graphite_aa_intercalate_mc8(verbose=True,
                                           forced=True,
                                           cells=cells_user,
                                           intercalant=int_element)
