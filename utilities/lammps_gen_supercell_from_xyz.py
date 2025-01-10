#!/usr/bin/env python

# This function simply generates a supercell from a given xyz file
# The output is a lammps data file in atomic format.

# Keyword arguments:
# verbose = True   , prints some comments to the screen.
# forced  = True   , will overwrite the existing file (if it exists).
# forced  = False  , if file exists, will ask the user if the existing file should be overwritten.
# filename = lammps.lattice.dat  , the output filename
# cells = [x,y]  , No. unit cells to generate for each direction.
# xyz_file = 'lattice.xyz'   ,  the filename of the input xyz file to convert

# Kenny Jolley, Jan 2025

import sys
import os
import re

def lammps_gen_supercell_from_xyz(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    forced = kwargs.get('forced', True)
    filename = kwargs.get('filename', 'lammps.lattice.dat')
    cells = kwargs.get('cells', [1, 1, 1])
    xyz_file = kwargs.get('xyz_file', 'lattice.xyz')

    # Atom masses dict
    atom_masses ={
        "H": 1.008,
        "He": 4.002602,
        "Li": 6.94,
        "Be": 9.012182,
        "B": 10.81,
        "C": 12.011,
        "N": 14.007,
        "O": 15.9994,
        "F": 18.998403163,
        "Ne": 20.1797,
        "Na": 22.98976928,
        "Mg": 24.305,
        "Al": 26.98153857,
        "Si": 28.0851,
        "P": 30.973761998,
        "S": 32.066,
        "Cl": 35.45,
        "Ar": 39.948,
        "K": 39.0983,
        "Ca": 40.078,
        "Sc": 44.955908,
        "Ti": 47.867,
        "V": 50.9415,
        "Cr": 51.9961,
        "Mn": 54.938044,
        "Fe": 55.845,
        "Co": 58.933194,
        "Ni": 58.6934,
        "Cu": 63.546,
        "Zn": 65.38,
        "Ga": 69.723,
        "Ge": 72.63,
        "As": 74.921595,
        "Se": 78.971,
        "Br": 79.904,
        "Kr": 83.798,
        "Rb": 85.4678,
        "Sr": 87.62,
        "Y": 88.90584,
        "Zr": 91.224,
        "Nb": 92.90637,
        "Mo": 95.95,
        "Tc": 98,
        "Ru": 101.07,
        "Rh": 102.9055,
        "Pd": 106.42,
        "Ag": 107.8682,
        "Cd": 112.414,
        "In": 114.818,
        "Sn": 118.71,
        "Sb": 121.76,
        "Te": 127.6,
        "I": 126.90447,
        "Xe": 131.293,
        "Cs": 132.90545196,
        "Ba": 137.327,
        "La": 138.90547,
        "Ce": 140.116,
        "Pr": 140.90766,
        "Nd": 144.242,
        "Pm": 145,
        "Sm": 150.36,
        "Eu": 151.964,
        "Gd": 157.25,
        "Tb": 158.92535,
        "Dy": 162.5,
        "Ho": 164.93033,
        "Er": 167.259,
        "Tm": 168.93422,
        "Yb": 173.054,
        "Lu": 174.9668,
        "Hf": 178.49,
        "Ta": 180.94788,
        "W": 183.84,
        "Re": 186.207,
        "Os": 190.23,
        "Ir": 192.217,
        "Pt": 195.084,
        "Au": 196.966569,
        "Hg": 200.592,
        "Tl": 204.38,
        "Pb": 207.2,
        "Bi": 208.9804,
        "Po": 209,
        "At": 210,
        "Rn": 222,
        "Fr": 223,
        "Ra": 226,
        "Ac": 227,
        "Th": 232.0377,
        "Pa": 231.03588,
        "U": 238.02891,
        "Np": 237,
        "Pu": 244,
        "Am": 243,
        "Cm": 247,
        "Bk": 247,
        "Cf": 251,
        "Es": 252,
        "Fm": 257,
        "Md": 258,
        "No": 259,
        "Lr": 262,
        "Rf": 267,
        "Db": 268,
        "Sg": 269,
        "Bh": 270,
        "Hs": 269,
        "Mt": 278,
        "Ds": 281,
        "Rg": 281,
        "Cn": 285
    }

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

    # create lammps lattice data file
    if forced:
        file = open(xyz_file, 'r')
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
        fileline = file.readline()
        # parse to find the lattice info
        lattice_regex = r'Lattice="([0-9e.\-+\s]+)"'
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
            # If no match is found, exit with error
            print("Lattice information not found in the provided string")
            print(fileline)
            sys.exit()

        if verbose:
            print(lattice_matrix)

        # read in the atoms and the coordinates, note this only works for specie, x, y, z format as first cols
        specie = []
        x = []
        y = []
        z = []
        for i in range(atoms):
            fileline = file.readline().split()
            specie.append(fileline[0])
            x.append(fileline[1])
            y.append(fileline[2])
            z.append(fileline[3])
        file.close()

        # Now generate lammps data file
        # open output for writing
        outputfile = open(filename, 'w')

        # Output Lammps header
        outputfile.write(f"Lammps data file generated from xyz file: {xyz_file} \n")
        outputfile.write(f"#  This is a supercell of {cells[0]}x{cells[1]}x{cells[2]} copies of the initial file \n")
        outputfile.write(f"{atoms*cells[0]*cells[1]*cells[2]} atoms\n\n")

        # From the specie list, count total number of types and enumerate
        unique_elements = set(specie)
        specie_list = sorted(list(unique_elements))   # sort in order

        # Output the atom types line
        outputfile.write(f"{len(unique_elements)} atom types # {' '.join(specie_list)} \n")

        if verbose:
            print("Number of unique elements:", len(unique_elements))
            print("List of unique elements:", specie_list)

        # Output Cell dimensions
        outputfile.write("\n")
        outputfile.write(f"{0.0} {lattice_matrix[0][0]*cells[0]}  xlo xhi\n")
        outputfile.write(f"{0.0} {lattice_matrix[1][1]*cells[1]}  ylo yhi\n")
        outputfile.write(f"{0.0} {lattice_matrix[2][2]*cells[2]}  zlo zhi\n")

        # Tilt factors if listed (assumes vectors are restricted triclinic)
        # A = (xhi - xlo, 0, 0)
        # B = (xy, yhi - ylo, 0)
        # C = (xz, yz, zhi - zlo)
        outputfile.write(f"{lattice_matrix[1][0]} {lattice_matrix[2][0]*cells[2]} {lattice_matrix[2][1]} xy xz yz \n")


        # output the masses
        outputfile.write("\nMasses\n\n")
        for i,j in enumerate(specie_list):
            outputfile.write(f"{i+1} {atom_masses[str(specie_list[i])]}\n")
            if verbose:
                print(f"{i+1} {atom_masses[str(specie_list[i])]}")

        # Atom data
        outputfile.write("\n")
        outputfile.write("Atoms # atomic\n")
        outputfile.write("\n")

        count = 1
        for a in range(cells[0]):
            for b in range(cells[1]):
                for c in range(cells[2]):
                    for i in range(atoms):
                        outputfile.write(f"{count}  ")
                        outputfile.write(f"{specie_list.index(specie[i])+1}  "
                                         f"{float(x[i])+a*lattice_matrix[0][0] + c*lattice_matrix[2][0] + b*lattice_matrix[1][0]}  "
                                         f"{float(y[i])+b*lattice_matrix[1][1] + c*lattice_matrix[2][1]}  "
                                         f"{float(z[i])+c*lattice_matrix[2][2]}  \n")
                        count += 1

        # All done, close output file
        outputfile.close()

        if verbose:
            print("file closed: " + str(file.name))
            print(f"COMPLETED {filename} output !!")


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    my_cells = [1, 1, 1]

    # Read number of lattice cells from the command-line, or supply interactively
    print(">  Using information passed on the command-line")

    # 3 params = input filename and supercell size
    if len(sys.argv) == 5:
        my_xyz_file = str(sys.argv[1])
        my_cells[0] = int(sys.argv[2])
        my_cells[1] = int(sys.argv[3])
        my_cells[2] = int(sys.argv[4])
        lammps_gen_supercell_from_xyz(verbose=True, forced=True, cells=my_cells, xyz_file=my_xyz_file)

    # 4 params = input filename and supercell size, then output name
    elif len(sys.argv) == 6:
        my_xyz_file = str(sys.argv[1])
        my_cells[0] = int(sys.argv[2])
        my_cells[1] = int(sys.argv[3])
        my_cells[2] = int(sys.argv[4])
        my_outfile = str(sys.argv[5])
        lammps_gen_supercell_from_xyz(verbose=True, forced=True, cells=my_cells, xyz_file=my_xyz_file, filename=my_outfile)

    else:
        print(">>> ERROR  <<<")
        print("  User must pass 4 or 5 command-line arguments")
        print("   4 params = input filename and supercell size")
        print("   5 params = input filename and supercell size, then output name")
        print("    examples")
        print("   lammps_gen_supercell_from_xyz  file.xyz  2  3  3")
        print("   lammps_gen_supercell_from_xyz  file.xyz  2  3  2  output.dat")
        sys.exit()
