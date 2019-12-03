#!/usr/bin/env python

# This function simply generates a graphite lattice for the Hybrid DRIP-AIREBO forcefield.
# The output is a lammps data file in molecular format (this is the required format for the DRIP code).

# Keyword arguments:
# verbose = True   , prints some comments to the screen.
# forced  = True   , will overwrite the existing file (if it exists).
# forced  = False  , if file exists, will ask the user if the existing file should be overwritten.
# a_const = 2.4175 , the 'a' lattice constant
# c_const = 3.358  , the 'c' lattice constant
# filename = lammps.lattice.dat  , the output filename
# stacking = 'ab'  , stacking order of the graphene planes
# cells = [x,y,z]  , No. unit cells to generate for each direction.

# Kenny Jolley, Nov 2019

import sys
import os
import math

def lammps_gen_graphite_drip_airebo(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    forced = kwargs.get('forced', False)
    # Default constants for the DRIP Potential
    a_const = kwargs.get('a_const', 2.4195913)  # 2.4175,  2.45893461, 2.4195913
    c_const = kwargs.get('c_const', 3.42424712) # 3.41593,  3.41615256, 3.42424712
    stacking = kwargs.get('stacking', 'ab')
    filename = kwargs.get('filename', 'lammps.lattice.dat')
    cells = kwargs.get('cells', [1,1,1])
    
    # box size and atom total
    box_x = math.sqrt(3) * a_const * cells[0]
    box_y =                a_const * cells[1]
    box_z =                c_const * cells[2] * len(stacking)
    tot_atoms = int(4 * len(stacking) * cells[0] * cells[1] * cells[2])
    
    # Welcome
    if(verbose):
        print("  +------------------------------------------+")
        print("  |         Lattice generator script         |")
        print("  |             Graphite lattice             |")
        print("  |                DRIP-AIREBO               |")
        print("  |               Kenny Jolley               |")
        print("  |                 Nov 2019                 |")
        print("  |          kenny.jolley@gmail.com          |")
        print("  +------------------------------------------+")
        print("   ")

        print(">  Echoing back the user supplied data")
        print("     Lattice constant a   [Ang]: " + str(a_const) )
        print("     Layer seperation c/2 [Ang]: " + str(c_const) )
        print(">  Graphite lattice with unit cell repeats:")
        print("     cells_x: " + str(cells[0]) )
        print("     cells_y: " + str(cells[1]) )
        print("     cells_z: " + str(cells[2]) )
        print(">  Graphite lattice cell dimensions [Ang]:")
        print("     box_x: " + str(box_x) )
        print("     box_y: " + str(box_y) )
        print("     box_z: " + str(box_z) )
        print(">  Stacking: " + str(stacking))
        print(">  Total number of atoms: " + str(tot_atoms) )

    # Set generate file flag to true
    gen_file = True
    
    # Check if the file already exists
    if(not forced):
        if(os.path.isfile(filename)):
            print("> Existing file " + str(filename) + " detected.")
            print("> lammps_gen_graphite_drip_airebo function wants to overwrite this file")
        
            # Ask user if file should be overwritten (python 2/3 handling)
            if sys.version_info[0] < 3:
                user_choice = raw_input('Do you wish to overwrite the existing file? (y/n): ')
            else:
                user_choice = input('Do you wish to overwrite the existing file? (y/n): ')
    
            user_choice = user_choice.lower()
            
            if ((user_choice == 'yes') or (user_choice == 'y') or (user_choice == 'yea') ):
                print(" > Overwriting existing file ... ")
                gen_file = True
            else:
                print( "File not overwritten, exiting function")
                gen_file = False


    # create lattice file
    if(gen_file):
        file = open(filename, 'w+')
        if(verbose):
            print("Opened file: " + str(file.name) )
        
        # Write header info
        file.write("Lammps data file generated by lammps_gen_graphite_drip_airebo.py\n")
        file.write("# Graphite " + str(cells[0]) + "x" + str(cells[1]) + "x" + str(cells[2]) + " Unit cells, with " + str(stacking) + " stacking.  a_param = " + str(a_const) + " , c_param = " + str(c_const) + "\n")
        file.write(str(tot_atoms) + " atoms\n\n")
        file.write("1 atom types # C\n\n")
        file.write("0.0 " + str(box_x) + " xlo xhi\n")
        file.write("0.0 " + str(box_y) + " ylo yhi\n")
        file.write("0.0 " + str(box_z) + " zlo zhi\n\n")
        file.write("Masses\n\n")
        file.write("1 12.011\n\n")
        file.write("Atoms # molecular\n\n")

        # ID mol charge x y z
        count = 1
        for x in range(0,cells[0]):
            Xshift = x * math.sqrt(3) * a_const
            for y in range(0,cells[1]):
                Yshift = y * a_const
                for z in range(0,cells[2]):
                    for l in range(0,len(stacking)):
                        mol = int(len(stacking)*z+l)+1
                        Zshift = (len(stacking)*z+l)*c_const
                        # stacking position a
                        if( stacking[l] == 'a'):
                            file.write(str(count)   + "   " + str(mol) + "  1  " + str(Xshift) + "  " + str(Yshift) + "  " + str(Zshift) + "\n")
                            file.write(str(count+1) + "   " + str(mol) + "  1  " + str(Xshift + a_const * 2.0/math.sqrt(3)) + "  " + str(Yshift) + "  " + str(Zshift) + "\n")
                            file.write(str(count+2) + "   " + str(mol) + "  1  " + str(Xshift + a_const * math.sqrt(3)/6.0) + "  " + str(Yshift + a_const /2.0) + "  " + str(Zshift) + "\n")
                            file.write(str(count+3) + "   " + str(mol) + "  1  " + str(Xshift + a_const * math.sqrt(3)/2.0) + "  " + str(Yshift + a_const /2.0) + "  " + str(Zshift) + "\n")
                            count = count + 4
                        # stacking position b
                        elif(stacking[l] == 'b'):
                            file.write(str(count)   + "   " + str(mol) + "  1  " + str(Xshift) + "  " + str(Yshift) + "  " + str(Zshift) + "\n")
                            file.write(str(count+1) + "   " + str(mol) + "  1  " + str(Xshift + a_const / math.sqrt(3)) + "  " + str(Yshift) + "  " + str(Zshift) + "\n")
                            file.write(str(count+2) + "   " + str(mol) + "  1  " + str(Xshift + a_const * math.sqrt(3)/2.0) + "  " + str(Yshift + a_const /2.0) + "  " + str(Zshift) + "\n")
                            file.write(str(count+3) + "   " + str(mol) + "  1  " + str(Xshift + a_const * math.sqrt(3)*5.0/6.0) + "  " + str(Yshift + a_const /2.0) + "  " + str(Zshift) + "\n")
                            count = count + 4
                        # stacking position c
                        elif (stacking[l] == 'c'):
                            file.write(str(count)   + "   " + str(mol) + "  1  " + str(Xshift + a_const / math.sqrt(3)) + "  " + str(Yshift) + "  " + str(Zshift) + "\n")
                            file.write(str(count+1) + "   " + str(mol) + "  1  " + str(Xshift + a_const * 2.0/math.sqrt(3)) + "  " + str(Yshift) + "  " + str(Zshift) + "\n")
                            file.write(str(count+2) + "   " + str(mol) + "  1  " + str(Xshift + a_const * math.sqrt(3)/6.0) + "  " + str(Yshift + a_const /2.0) + "  " + str(Zshift) + "\n")
                            file.write(str(count+3) + "   " + str(mol) + "  1  " + str(Xshift + a_const * math.sqrt(3)*5.0/6.0) + "  " + str(Yshift + a_const /2.0) + "  " + str(Zshift) + "\n")
                            count = count + 4
        file.close()

        if(verbose):
            print("file closed: " + str(file.name))
            print("COMPLETED lattice.dat output !!")






# If we are running this script interactively, call the function safely
if __name__ == '__main__':
    forced=True
    cells = [1,1,1]

    # Read number of lattice cells from the command-line, or supply interactively
    if( len(sys.argv) > 1 ):
        print(">  Using information passed on the command-line")
        # 3 params = cell size, default ab stacking
        if( len(sys.argv) == 4):
            cells[0] = int(sys.argv[1])
            cells[1] = int(sys.argv[2])
            cells[2] = int(sys.argv[3])
            stacking = 'ab'
        # 4 params = cell size, user chosen stacking
        elif( len(sys.argv) == 5):
            cells[0] = int(sys.argv[1])
            cells[1] = int(sys.argv[2])
            cells[2] = int(sys.argv[3])
            stacking = str(sys.argv[4])
            # check stacking contains only a b c chars
            for char in stacking:
                #print "char: ", char
                if ( ( char != 'a') and ( char != 'b') and ( char != 'c') ):
                    print(">>> ERROR  <<< stacking order can contain only the letters: a,b,c")
                    print(">> defaulting to ab")
                    stacking = 'ab'
        else:
            print(">>> ERROR  <<<")
            print("  User must pass either 3 or 4 command-line arguments")
            print("   3 params = box_x, box_y, box_z  (integers)")
            print("   4 params = box_x, box_y, box_z  (integers), stacking (string e.g.: ab,abc)")
            print("    examples")
            print("   lammps_gen_graphite_drip.py 1 2 3")
            print("   lammps_gen_graphite_drip.py 3 5 7 ab")
            print("   lammps_gen_graphite_drip.py 3 5 7 abc")
            print("   lammps_gen_graphite_drip.py 10 20 5 abcababcab")
            sys.exit()


    else:
        # Otherwise, ask user, cell dimensions
        while True:
            try:
                if sys.version_info[0] < 3:
                    cellsize = int(raw_input('Enter number of cells in x dir : '))
                else:
                    cellsize = int(input('Enter number of cells in x dir : '))
                if (cellsize > 0):
                    break
                else:
                    print("Oops!  Integer must be greater than 0.  Try again...")
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")
        cells[0] = cellsize
        while True:
            try:
                if sys.version_info[0] < 3:
                    cellsize = int(raw_input('Enter number of cells in y dir : '))
                else:
                    cellsize = int(input('Enter number of cells in y dir : '))
                if (cellsize > 0):
                    break
                else:
                    print("Oops!  Integer must be greater than 0.  Try again...")
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")
        cells[1] = cellsize
        while True:
            try:
                if sys.version_info[0] < 3:
                    cellsize = int(raw_input('Enter number of cells in z dir : '))
                else:
                    cellsize = int(input('Enter number of cells in z dir : '))
                if (cellsize > 0):
                    break
                else:
                    print("Oops!  Integer must be greater than 0.  Try again...")
            except ValueError:
                print("Oops!  That was not a valid integer.  Try again...")
        cells[2] = cellsize
    
        # stacking
        stacking_valid = False
        while not stacking_valid:
            if sys.version_info[0] < 3:
                stacking = str(raw_input('What stacking do you want (ab,abc)?: '))
            else:
                stacking = str(input('What stacking do you want (ab,abc)?: '))
    
            stacking_error = False
            if(len(stacking) < 1):
                print(">>> ERROR  <<< stacking order cannot be zero length")
                stacking_error = True
            else:
                # check stacking contains only a b c chars
                for char in stacking:
                    #print "char: ", char
                    if( not stacking_error):
                        if ( (char != 'a') and (char != 'b') and (char != 'c') ):
                            print(">>> ERROR  <<< stacking order can contain only the letters: a,b,c")
                            stacking_error = True
                            
            if( not stacking_error):
                stacking_valid = True
                

    # call the graphite generator function
    lammps_gen_graphite_drip_airebo(verbose=True,forced=forced, cells=cells, stacking=stacking)


