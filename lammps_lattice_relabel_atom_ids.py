#!/usr/bin/env python

# This function reads a lammps lattice input file and relabels the atom IDs so that
# they are sequential.  The script also checks that the correct number of atoms are present

# Keyword arguments:
# verbose    = True  , prints some comments to the screen.
# overwrite  = True  , will overwrite the existing file.
# overwrite  = False , will create a new file with the current date-time appended to the filename
# filename = lammps.lattice.dat  , the lammps lattice file to read

#  Kenny Jolley, May 2019

# imported modules
import sys
import os
import datetime

# function reads a lammps lattice input file and relabels the atom IDs
def lammps_lattice_relabel_atom_ids(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    filename = kwargs.get('filename', 'lammps.lattice.dat')
    overwrite = kwargs.get('overwrite', False)

    # Welcome
    if(verbose):
        print("  +------------------------------------------+")
        print("  | This script reads a lammps lattice input |")
        print("  |      file and relabels the atom IDs      |")
        print("  |                                          |")
        print("  |               Kenny Jolley               |")
        print("  |                 May 2019                 |")
        print("  |          kenny.jolley@gmail.com          |")
        print("  +------------------------------------------+")
        print("   ")

        print(">  Lammps input filename: " + str(filename))


    # output filename
    x = datetime.datetime.now()
    output_filename = (x.strftime("%Y") + x.strftime("%m") +
                       x.strftime("%d") + x.strftime("%H") +
                       x.strftime("%M") + x.strftime("%S") + "_lammps.lattice.dat" )

    # Open input file
    infile = open(filename, 'r')
    if(verbose):
        print("Opened file: " + str(infile.name) )

    # Create output file
    outfile = open(output_filename, 'w+')
    if(verbose):
        print("Opened file: " + str(outfile.name) )


    # Read and write the header, stop after reading the 'Atoms' line
    while 1:
        fileline = infile.readline()
        filelinesplit = fileline.split()
        
        # Save the number of atoms
        if len(filelinesplit)>1:
            if (filelinesplit[1]=='atoms'):
                atoms = int(filelinesplit[0])

        # Stopping criteria
        if len(filelinesplit)>0:
            if (filelinesplit[0]=='Atoms'):
                # print the "Atoms" line
                outfile.write(str(fileline))
                # and write the next blank line
                fileline = infile.readline()
                outfile.write(str(fileline))
                break




        outfile.write(str(fileline))


    # Now we need to read the atom data lines, and modify the first column
    # with a sequential counter
    counter = 1
    while 1:
        fileline = infile.readline()
        if not fileline: break
        
        fileline = fileline.split()
        
        if len(filelinesplit)==0:
            break
        
        outfile.write( str(counter) + "  ")
        for x in range(1,len(fileline)):
            outfile.write( str(fileline[x]) + "  ")
            
        outfile.write("\n")

        counter = counter + 1
      
    infile.close()
    outfile.close()


    # Test if no. atoms are as expected
    if(verbose):
        print("\nAtoms expected in file: " + str(atoms) )
        print("Atoms actually read   : " + str(counter-1) )
    if (atoms != (counter-1)):
        print(">>> WARNING: There is a mismatch between the number of atoms field at the top of the file, with the actual number of atom records in the file")
        print("\nAtoms expected in file: " + str(atoms) )
        print("Atoms actually read   : " + str(counter-1) )
      

    # overwrite existing file if required
    if(overwrite):
        os.remove(filename)
        os.rename(output_filename,filename)


# If we are running this script interactively, call the function safely
if __name__ == '__main__':
    
    verbose=True
    overwrite=False

    # Get the filename from commandline, if present
    if( len(sys.argv) > 1 ):
        filename = str(sys.argv[1])

        # call the function safely
        lammps_lattice_relabel_atom_ids(verbose=verbose, overwrite=overwrite, filename=filename)

    else:
        # call the function safely (use default filename)
        lammps_lattice_relabel_atom_ids(verbose=verbose, overwrite=overwrite)

