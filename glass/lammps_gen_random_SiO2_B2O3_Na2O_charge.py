#!/usr/bin/env python

# This function generates a random lattice of Si, B, Na and O atoms (SiO2 and B2O3 formula units).
# Output file is in lammps charge format

# Keyword arguments:
# verbose = True                 , prints some comments to the screen.
# forced  = True                 , will overwrite the existing file (if it exists).
# forced  = False                , if file exists, will ask the user if the existing file should be overwritten.
# num_SiO2 = 1000                , default the number of SiO2 formula units in the lattice
# num_B2O3 = 1000                , default the number of B2O3 formula units in the lattice
# filename = lammps.lattice.dat  , the default output filename
# use_min_sep = True             , Ensure atoms are no closer than min_sep
# min_sep = 1.0                  , Minimum separation distance between atoms in random lattice (if used).
# si_charge = 4                  , charge on Si atoms
# o_charge = -2                  , charge on O atoms
# b_charge = 3                   , charge on B atoms
# density = 2000.0               , density in kg/m3

#    Kenny Jolley, March 2021

# imported modules
import sys
import os
import math
import random


# function generates a random lattice of SiO2 formula units, and saves the file to disk
def lammps_gen_random_SiO2_B2O3_Na2O_charge(**kwargs):
    # Default keyword args
    verbose = kwargs.get('verbose', False)
    forced = kwargs.get('forced', True)
    num_SiO2 = kwargs.get('num_SiO2', 1000)
    num_B2O3 = kwargs.get('num_B2O3', 1000)
    num_Na2O = kwargs.get('num_Na2O', 1000)
    si_charge = kwargs.get('si_charge', 1.89)
    o_charge = kwargs.get('o_charge', -0.945)
    b_charge = kwargs.get('b_charge', 1.4175)
    na_charge = kwargs.get('na_charge', 0.4725)
    density = kwargs.get('density', 2000.0)
    filename = kwargs.get('filename', 'lammps.lattice.dat')
    use_min_sep = kwargs.get('use_min_sep', True)
    min_sep = kwargs.get('min_sep', 1.2)
    min_sep2 = min_sep*min_sep

    # System Mass
    amu = 1.660538921E-27  # in kg
    si_mass = 28.0855
    o_mass = 15.9994
    b_mass = 10.811
    na_mass = 22.98976928

    total_mass = ((num_SiO2 * (si_mass + 2.0 * o_mass)) +
                  (num_B2O3 * (2.0 * b_mass + 3.0 * o_mass)) +
                  (num_Na2O * (2.0 * na_mass + o_mass))
                  ) * amu

    total_atoms = (3 * num_SiO2) + (5 * num_B2O3) + (3*num_Na2O)

    nsi = num_SiO2
    nb = 2*num_B2O3
    no = 2 * num_SiO2 + 3 * num_B2O3 + num_Na2O
    nna = 2 * num_Na2O

    # System volume
    volume_m3 = total_mass / density

    # cube side length
    cube_size_m = math.pow(volume_m3, (1.0 / 3.0))
    cube_size_ang = cube_size_m * 1e10

    # Welcome
    if verbose:
        print("  +------------------------------------------+")
        print("  |         Lattice generator script         |")
        print("  |      Random SiO2,B2O3, Na2O lattice      |")
        print("  |                                          |")
        print("  |               Kenny Jolley               |")
        print("  |               March 2021                 |")
        print("  +------------------------------------------+")
        print("   ")
        print("  Generating a random distribution of SiO2 atoms")
        print("  SiO2 formula units : " + str(num_SiO2))
        print("  B2O3 formula units : " + str(num_B2O3))
        print("  Na2O formula units : " + str(num_Na2O))
        print("  Silicon atoms      : " + str(nsi))
        print("  Boron atoms        : " + str(nb))
        print("  Oxygen atoms       : " + str(no))
        print("  Sodium atoms       : " + str(nna))
        print("  Total atoms        : " + str(total_atoms))
        print("  Total mass  : " + str(total_mass) + " kg")
        print("  Density     : " + str(density) + " kg/m^3")
        print("  Total Vol   : " + str(volume_m3) + " m^3")
        print("  Cube size   : " + str(cube_size_m) + " m")
        print("  Cube size   : " + str(cube_size_ang) + " Angstrom")
        print("  Writing file:  " + str(filename))
        print("   ")
        if use_min_sep:
            print("  Checking atoms are not placed within:  " + str(min_sep) + " Ang")
            print("  This is slow for large systems. ")
            print("   ")

    # Check if the file already exists
    if not forced:
        if os.path.isfile(filename):
            print("> Existing file " + str(filename) + " detected.")
            print("> lammps_gen_random_SiO2_B2O3_Na2O_charge function wants to overwrite this file")

            # Ask user if file should be overwritten
            user_choice = input('Do you wish to overwrite the existing file? (y/n): ')
            user_choice = user_choice.lower()

            if (user_choice == 'yes') or (user_choice == 'y') or (user_choice == 'yea'):
                print(" > Overwriting existing file ... ")
            else:
                print("File not overwritten, exiting function")
                return

    # Generate file
    file = open(filename, 'w+')
    if verbose:
        print("  Opened file: " + str(file.name))

    # Write header info
    file.write("Lammps data file generated by lammps_gen_random_SiO2_B2O3_Na2O_charge\n")
    file.write("#  Random lattice with " +
               str(nsi) + " Si atoms (charge = " + str(si_charge) + ") and " +
               str(nb) + " B atoms (charge = " + str(b_charge) + ") and " +
               str(nna) + " Na atoms (charge = " + str(na_charge) + ") and " +
               str(no) + " O atoms (charge = " + str(o_charge) +
               "), at a density of " + str(density) + " kg/m^3\n")
    file.write(str(total_atoms) + " atoms\n\n")
    file.write("4 atom types # O Si B Na\n\n")
    file.write("0.0 " + str(cube_size_ang) + " xlo xhi\n")
    file.write("0.0 " + str(cube_size_ang) + " ylo yhi\n")
    file.write("0.0 " + str(cube_size_ang) + " zlo zhi\n\n")
    file.write("Masses\n\n")
    file.write("1 " + str(o_mass) + "\n")
    file.write("2 " + str(si_mass) + "\n")
    file.write("3 " + str(b_mass) + "\n")
    file.write("4 " + str(na_mass) + "\n\n")
    file.write("Atoms # charge\n\n")

    # Create atom arrays
    atom_pos_x = [-1.0 for _ in range(total_atoms+1)]
    atom_pos_y = [-1.0 for _ in range(total_atoms+1)]
    atom_pos_z = [-1.0 for _ in range(total_atoms+1)]

    # Generate first position
    atom_pos_x[0] = random.uniform(0, cube_size_ang)
    atom_pos_y[0] = random.uniform(0, cube_size_ang)
    atom_pos_z[0] = random.uniform(0, cube_size_ang)

    # Generate positions
    for i in range(1, total_atoms + 1):
        if verbose:
            if (100 * float(i)) % total_atoms == 0:
                print(".", end='')
                sys.stdout.flush()
            if (10 * float(i)) % total_atoms == 0:
                print(str(100 * float(i) / total_atoms) + " %")

        # Generate position
        while True:
            # generate atom i
            atom_pos_x[i] = random.uniform(0, cube_size_ang)
            atom_pos_y[i] = random.uniform(0, cube_size_ang)
            atom_pos_z[i] = random.uniform(0, cube_size_ang)

            # check it is no closer than min_sep if required
            if use_min_sep:
                sep_test = 1
                # loop over all atoms generated so far
                for j in range(0, i):
                    # x coord
                    # print i, j
                    dx = atom_pos_x[i] - atom_pos_x[j]
                    dx2 = abs(dx + cube_size_ang)
                    dx3 = abs(dx - cube_size_ang)
                    dx1 = abs(dx)
                    # min x-sep
                    dxm = min(dx1, dx2)
                    dxm = min(dxm, dx3)

                    # if within x dist, check other coords
                    if dxm < min_sep:
                        dy = atom_pos_y[i] - atom_pos_y[j]
                        dy2 = abs(dy + cube_size_ang)
                        dy3 = abs(dy - cube_size_ang)
                        dy1 = abs(dy)
                        # min y-sep
                        dym = min(dy1, dy2)
                        dym = min(dym, dy3)
                        # if within y dist, check other coords
                        if dym < min_sep:
                            dz = atom_pos_z[i] - atom_pos_z[j]
                            dz2 = abs(dz + cube_size_ang)
                            dz3 = abs(dz - cube_size_ang)
                            dz1 = abs(dz)
                            # min z-sep
                            dzm = min(dz1, dz2)
                            dzm = min(dzm, dz3)

                            # if within z dist, do the full calculation
                            if dzm < min_sep:
                                # full calc
                                dr2 = dxm * dxm + dym * dym + dzm * dzm
                                if dr2 < min_sep2:
                                    # print("too close")
                                    sep_test = 0
            else:  # if we are not checking for min sep, we just break
                break

            # break if passed min separation test
            if sep_test:
                break

    # now we have an array of coords, we can write the rest of the file
    # Si atoms
    for i in range(1, nsi + 1):
        # Output to file
        file.write(str(i) + "  2  " +
                   str(si_charge) + "  " +
                   str(atom_pos_x[i]) + "  " +
                   str(atom_pos_y[i]) + "  " +
                   str(atom_pos_z[i]) + "\n")
    # B atoms
    for i in range(1 + nsi, 1 + nsi + nb):
        # Output to file
        file.write(str(i) + "  3  " +
                   str(b_charge) + "  " +
                   str(atom_pos_x[i]) + "  " +
                   str(atom_pos_y[i]) + "  " +
                   str(atom_pos_z[i]) + "\n")
    # O atoms
    for i in range(1 + nsi + nb, 1 + nsi + nb + no):
        # Output to file
        file.write(str(i) + "  1  " +
                   str(o_charge) + "  " +
                   str(atom_pos_x[i]) + "  " +
                   str(atom_pos_y[i]) + "  " +
                   str(atom_pos_z[i]) + "\n")
    # Na atoms
    for i in range(1 + nsi + nb + no, total_atoms + 1):
        # Output to file
        file.write(str(i) + "  4  " +
                   str(na_charge) + "  " +
                   str(atom_pos_x[i]) + "  " +
                   str(atom_pos_y[i]) + "  " +
                   str(atom_pos_z[i]) + "\n")


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    # Read number of SiO2 formula units, Si charge, O charge and density from the command-line, or supply interactively
    if len(sys.argv) > 1:
        print(">  Using information passed on the command-line")
        # 8 params = number of SiO2 formula units, Si charge, O charge and density
        if len(sys.argv) == 9:
            _num_SiO2 = int(sys.argv[1])
            _num_B2O3 = int(sys.argv[2])
            _num_Na2O = int(sys.argv[3])
            _o_charge = float(sys.argv[4])
            _si_charge = float(sys.argv[5])
            _b_charge = float(sys.argv[6])
            _na_charge = float(sys.argv[7])
            _density = float(sys.argv[8])

            # call the lattice generator function
            lammps_gen_random_SiO2_B2O3_Na2O_charge(verbose=True,
                                                    num_SiO2=_num_SiO2,
                                                    num_B2O3=_num_B2O3,
                                                    num_Na2O=_num_Na2O,
                                                    b_charge=_b_charge,
                                                    si_charge=_si_charge,
                                                    o_charge=_o_charge,
                                                    na_charge=_na_charge,
                                                    density=_density)  # ,use_min_sep=False)

        elif len(sys.argv) == 5:
            _num_SiO2 = int(sys.argv[1])
            _num_B2O3 = int(sys.argv[2])
            _num_Na2O = int(sys.argv[3])
            _density = float(sys.argv[4])

            # call the lattice generator function
            lammps_gen_random_SiO2_B2O3_Na2O_charge(verbose=True,
                                                    num_SiO2=_num_SiO2,
                                                    num_B2O3=_num_B2O3,
                                                    num_Na2O=_num_Na2O,
                                                    density=_density)  # ,use_min_sep=False)

        else:
            print(">>> ERROR  <<<")
            print("  User must pass 4 command-line arguments")
            print("     number of SiO2 and B2O3 and Na2O formula units and density")
            print("     example:")
            print("  lammps_gen_random_SiO2_B2O3_Na2O_charge.py 700 300 100 2100")
            print("")

            print("or ")
            print("  User must pass 8 command-line arguments")
            print("     number of SiO2 and B2O3 and Na2O formula units (integer),"
                  "     O charge Si charge, B charge, Na charge and density  (float) ")
            print("     example:")
            print("  lammps_gen_random_SiO2_B2O3_Na2O_charge.py 700 300 100 -2 4 3 1 2100")

            sys.exit()
    else:
        # Otherwise, ask user for the number of atoms and density
        while True:
            try:
                _num_SiO2 = int(input('Enter number of SiO2 formula units required : '))
                if _num_SiO2 > 0:
                    break
                else:
                    print("Oops!  Integer must be greater than 0.  Try again...")
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")

        while True:
            try:
                _num_B2O3 = int(input('Enter number of B2O3 formula units required : '))
                if _num_B2O3 > 0:
                    break
                else:
                    print("Oops!  Integer must be greater than 0.  Try again...")
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")

        while True:
            try:
                _num_Na2O = int(input('Enter number of Na2O formula units required : '))
                if _num_Na2O > 0:
                    break
                else:
                    print("Oops!  Integer must be greater than 0.  Try again...")
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")

        while True:
            try:
                _o_charge = float(input('Enter the O charge : '))
                break
            except ValueError:
                print("Oops!  That was not a valid number.  Try again...")
        while True:
            try:
                _si_charge = float(input('Enter the Si charge : '))
                break
            except ValueError:
                print("Oops!  That was not a valid number.  Try again...")

        while True:
            try:
                _b_charge = float(input('Enter the B charge : '))
                break
            except ValueError:
                print("Oops!  That was not a valid number.  Try again...")

        while True:
            try:
                _na_charge = float(input('Enter the Na charge : '))
                break
            except ValueError:
                print("Oops!  That was not a valid number.  Try again...")

        while True:
            try:
                _density = float(input('Enter the density [kg/m^3] : '))
                break
            except ValueError:
                print("Oops!  That was not a valid number.  Try again...")

        # call the lattice generator function
        lammps_gen_random_SiO2_B2O3_Na2O_charge(verbose=True,
                                                num_SiO2=_num_SiO2,
                                                num_B2O3=_num_B2O3,
                                                num_Na2O=_num_Na2O,
                                                b_charge=_b_charge,
                                                si_charge=_si_charge,
                                                o_charge=_o_charge,
                                                na_charge=_na_charge,
                                                density=_density)  # ,use_min_sep=False)
