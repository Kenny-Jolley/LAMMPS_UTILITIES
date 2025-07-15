#!/usr/bin/env python

# This script sets up the lammps source directory ready for compiling.
# All standard packages are included.
# Some optional libraries are built automatically.

# Keyword arguments:
# verbose = True             # Prints some comments to the screen.
# use_voro = True            # Builds and includes the voro++ package.
# use_kim = True             # Includes the open kim package (this must be built manually).
# use_pace = True            # Builds and includes ML_PACE package

#  Kenny Jolley, July 2025

# imported modules
import os, sys

# custom compile function
def lammps_setup_custom_compile(**kwargs):
    # mylog prints only if verbose is true
    def mylog(msg):
        if verbose:
            print(msg)

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    use_voro = kwargs.get('use_voro', False)
    use_kim = kwargs.get('use_kim', False)
    use_pace = kwargs.get('use_pace', False)

    # output header
    mylog("\n> Running")
    mylog(" verbose  =  " + str(verbose))
    mylog(" use_voro =  " + str(use_voro))
    mylog(" use_kim =  " + str(use_kim))
    mylog(" use_pace =  " + str(use_pace))

    # make sure we are on the stable branch and update.
    mylog("> Checkout the stable branch and update")
    os.system("git checkout stable")
    os.system("git pull")

    # ensure we have clean source
    # ensure all object files are deleted
    mylog("> Clean all object files and purge any deprecated src files")
    os.system("make clean-all")
    if os.path.isfile("lmp_kj_mpi"):
        os.remove('lmp_kj_mpi')
    if os.path.isfile("liblammps_kj_mpi.so"):
        os.remove('liblammps_kj_mpi.so')

    # remove any deprecated src files
    os.system("make purge")

    # Ensure we start with no packages
    os.system("make no-all")

    # Installs most packages that don't need extra libs
    mylog("> Install most commonly used packages")
    os.system("make yes-most")

    # Build and include any extra packages that have been selected
    if use_voro:
        mylog("> Building the voro++ package")
        os.system('make lib-voronoi args="-b"')
        os.system("make yes-VORONOI")
        mylog("> Done building the voro++ package")
    if use_kim:
        mylog("> Including the OPEN KIM package")
        mylog("> Warning: this one must be build manually")
        os.system("make yes-KIM")       # must build and install the KIM library first
    if use_pace:
        mylog("> Building the ML-PACE package")
        os.system('make lib-pace args="-b"')
        os.system("make yes-ML-PACE")
        mylog("> Done building the ML-PACE package")

    # remove any deprecated src files
    mylog("> Purge any deprecated src files")
    os.system("make purge")

    # sync package files with src files
    mylog("> sync package files with src files")
    os.system("make package-update")

    # list available packages
    mylog("> List available packages and commands for info")
    os.system("make package")

    # list initial package status
    mylog("> List new package status")
    os.system("make package-status")

    # Generate the MINE directory if it does not exist
    if os.path.isdir("MAKE/MINE"):
        mylog("> The MINE directory exists ")
    else:
        mylog("> The MINE directory does not exist, creating... ")
        os.makedirs("MAKE/MINE")

    # Generate the custom makefile
    if os.path.isfile("MAKE/MINE/Makefile.kj_mpi"):
        mylog("> Existing file MAKE/MINE/Makefile.kj_mpi removed ")
        os.remove("MAKE/MINE/Makefile.kj_mpi")

    # Generate file
    mylog("> Generating: MAKE/MINE/Makefile.kj_mpi ...")
    outfile = open("MAKE/MINE/Makefile.kj_mpi", 'w')


    outfile.write("""# modified linux simple
SHELL = /bin/sh

# ---------------------------------------------------------------------
# compiler/linker settings
# specify flags and libraries needed for your compiler

export OMPI_CXX = g++
CC =         mpicxx

OPTFLAGS =  -march=native -mtune=native -O3 -std=c++11
CCFLAGS  = $(OPTFLAGS)

SHFLAGS =    -fPIC
DEPFLAGS =   -M

LINK =       mpicxx
LINKFLAGS =  $(OPTFLAGS)
LIB =
SIZE =       size

ARCHIVE =    ar
ARFLAGS =    -rc
SHLIBFLAGS = -shared

# ---------------------------------------------------------------------
# LAMMPS-specific settings, all OPTIONAL
# specify settings for LAMMPS features you will use
# if you change any -D setting, do full re-compile after "make clean"

# LAMMPS ifdef settings
# see possible settings in Section 3.5 of the manual

LMP_INC =    -DLAMMPS_GZIP -DLAMMPS_MEMALIGN=64

# MPI library
# see discussion in Section 3.4 of the manual
# MPI wrapper compiler/linker can provide this info
# can point to dummy MPI library in src/STUBS as in Makefile.serial
# use -D MPICH and OMPI settings in INC to avoid C++ lib conflicts
# INC = path for mpi.h, MPI compiler settings
# PATH = path for MPI library
# LIB = name of MPI library

MPI_INC =       -DMPICH_SKIP_MPICXX -DOMPI_SKIP_MPICXX=1
MPI_PATH =
MPI_LIB =

# FFT library
# see discussion in Section 2.2 (step 6) of manual
# can be left blank to use provided KISS FFT library
# INC = -DFFT setting, e.g. -DFFT_FFTW, FFT compiler settings
# PATH = path for FFT library
# LIB = name of FFT library

FFT_INC =
FFT_PATH =
FFT_LIB =

# JPEG and/or PNG library
# see discussion in Section 2.2 (step 7) of manual
# only needed if -DLAMMPS_JPEG or -DLAMMPS_PNG listed with LMP_INC
# INC = path(s) for jpeglib.h and/or png.h
# PATH = path(s) for JPEG library and/or PNG library
# LIB = name(s) of JPEG library and/or PNG library

JPG_INC = 
JPG_PATH = 
JPG_LIB = 

#  library for loading shared objects (defaults to -ldl, should be empty on Windows)
# uncomment to change the default

# override DYN_LIB =

# ---------------------------------------------------------------------
# build rules and dependencies
# do not edit this section

include Makefile.package.settings
include Makefile.package

EXTRA_INC = $(LMP_INC) $(PKG_INC) $(MPI_INC) $(FFT_INC) $(JPG_INC) $(PKG_SYSINC)
EXTRA_PATH = $(PKG_PATH) $(MPI_PATH) $(FFT_PATH) $(JPG_PATH) $(PKG_SYSPATH)
EXTRA_LIB = $(PKG_LIB) $(MPI_LIB) $(FFT_LIB) $(JPG_LIB) $(PKG_SYSLIB) $(DYN_LIB)
EXTRA_CPP_DEPENDS = $(PKG_CPP_DEPENDS)
EXTRA_LINK_DEPENDS = $(PKG_LINK_DEPENDS)

# Path to src files

vpath %.cpp ..
vpath %.h ..

# Link target

$(EXE): main.o $(LMPLIB) $(EXTRA_LINK_DEPENDS)
\t$(LINK) $(LINKFLAGS) main.o $(EXTRA_PATH) $(LMPLINK) $(EXTRA_LIB) $(LIB) -o $@
\t$(SIZE) $@

# Library targets

$(ARLIB): $(OBJ) $(EXTRA_LINK_DEPENDS)
\t@rm -f ../$(ARLIB)
\t$(ARCHIVE) $(ARFLAGS) ../$(ARLIB) $(OBJ)
\t@rm -f $(ARLIB)
\t@ln -s ../$(ARLIB) $(ARLIB)

$(SHLIB): $(OBJ) $(EXTRA_LINK_DEPENDS)
\t$(CC) $(CCFLAGS) $(SHFLAGS) $(SHLIBFLAGS) $(EXTRA_PATH) -o ../$(SHLIB) \\
\t\t$(OBJ) $(EXTRA_LIB) $(LIB)
\t@rm -f $(SHLIB)
\t@ln -s ../$(SHLIB) $(SHLIB)

# Compilation rules

%.o:%.cpp
\t$(CC) $(CCFLAGS) $(SHFLAGS) $(EXTRA_INC) -c $<

# Individual dependencies

depend : fastdep.exe $(SRC)
\t@./fastdep.exe $(EXTRA_INC) -- $^ > .depend || exit 1

fastdep.exe: ../DEPEND/fastdep.c
\tcc -O -o $@ $<

sinclude .depend
""")


    mylog("> ")
    mylog("> Setup of lammps source directory is complete.")
    mylog("> You should check that the Makefile in /MAKE/MINE is correct for the machine you are working on.")
    mylog("> Check the output above is also as expected.")
    mylog("> ")
    mylog("> You can now compile lammps (using 4 cores):")
    mylog("> make -j 4 kj_mpi  ")
    mylog("> or build the shared library with:")
    mylog("> make -j 4 kj_mpi mode=shlib")


# If we are running this script interactively, call the function safely
if __name__ == '__main__':
    use_voro = False
    use_kim = False
    use_pace = False
    
    print("  +------------------------------------------+")
    print("  |        Lammps setup compile script       |")
    print("  |                                          |")
    print("  |               Kenny Jolley               |")
    print("  |                July 2025                 |")
    print("  +------------------------------------------+")
    print("   ")

    print("> This script sets up the lammps source directory ready for compiling.\n")

    print("> You must clone the github repo yourself with:")
    print("   git clone https://github.com/lammps/lammps.git mylammps")
    print("> Or:")
    print("   git clone git@github.com:lammps/lammps.git mylammps\n")
    print(">  Where 'mylammps' can be set to any name you wish for your build\n\n")
    print(">  This script should then be run from the src directory of your lammps installation")
    print(">  The current directory is: ")
    print(os.getcwd())
    
    # Ask the user if they want to continue
    user_choice = str(input('Do you wish to continue? (y/n) : ')).lower().strip()
    if (user_choice != 'yes') and (user_choice != 'y'):
        print(">  Script exiting...")
        sys.exit()

    # Ask user if VORO++ should be included
    print("   ")
    print("> Lammps can be built with the VORO++ package")
    print("> This script can build and include VORO++ automatically for you")
    user_choice = str(input('Do you wish to build and include VORO++ ? (y/n) : ')).lower().strip()
    if (user_choice == 'yes') or (user_choice == 'y'):
        use_voro = True

    # Ask user if KIM should be included
    print("   ")
    print("> Lammps can be built with the KIM library")
    print("> To use this package, you MUST install it before compiling lammps, see instructions in lib/kim")
    user_choice = str(input('Do you wish to include KIM ? (y/n) : ')).lower().strip()
    if (user_choice == 'yes') or (user_choice == 'y'):
        use_kim = True

    # Ask user if ML_PACE should be included
    print("   ")
    print("> Lammps can be built with the ML_PACE package")
    print("> This package is needed to use the ACE potential")
    print("> This script can build and include ML_PACE automatically for you")
    user_choice = str(input('Do you wish to build and include ML_PACE ? (y/n) : ')).lower().strip()
    if (user_choice == 'yes') or (user_choice == 'y'):
        use_pace = True

    print("   ")
    print("> This script generates the makefile using simple default settings for GCC linux.")
    print("> Remember to check this file if you are using other systems or compilers")
    print("   ")

    # call the lammps_setup_custom_compile function
    lammps_setup_custom_compile(verbose=True,
                                use_voro=use_voro,
                                use_kim=use_kim,
                                use_pace=use_pace,
                                )
