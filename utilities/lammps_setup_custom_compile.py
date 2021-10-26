#!/usr/bin/env python

# This script sets up the lammps source directory ready for compiling.


# Keyword arguments:
# verbose = True   , prints some comments to the screen.
# use_voro = True   , Includes the voro++ package.  This must be installed before compiling lammps
# use_modified_reaxff = True   , Includes the modified version of user-reax  with the carbon spline
# use_intel = True   , Includes the USER-INTEL package and applies optimised settings for the intel compiler
#           = False  , Does not include the USER-INTEL package and applies optimised settings for the gcc compiler

#  Kenny Jolley, June 2019

# imported modules
import os, sys
import shutil


def lammps_setup_custom_compile(**kwargs):

    # Default keyword args
    verbose = kwargs.get('verbose', False)
    use_voro = kwargs.get('use_voro', False)
    use_kim = kwargs.get('use_kim', False)
    use_quip = kwargs.get('use_quip', False)
    #use_modified_reaxff = kwargs.get('use_modified_reaxff', False)
    use_intel = kwargs.get('use_intel', False)
    use_intel_package = kwargs.get('use_intel_package', False)

    if verbose:
        print("\n> Running")
        print(" verbose  =  " + str(verbose))
        print(" use_voro =  " + str(use_voro))
        print(" use_modified_reaxff =  " + str(use_modified_reaxff))
        print(" use_intel =  " + str(use_intel))
        print(" use_intel_package =  " + str(use_intel_package))

    # make sure we are on the stable branch and update.
    print("> Checkout the stable branch and update")
    os.system("git checkout stable")
    os.system("git pull")

    # ensure we have clean source
    # ensure all object files are deleted
    print("> Clean all object files and purge any deprecated src files")
    os.system("make clean-all")

    if os.path.isfile("lmp_kj_mpi"):
        os.remove('lmp_kj_mpi')
    if os.path.isfile("liblammps_kj_mpi.so"):
        os.remove('liblammps_kj_mpi.so')

    # remove any deprecated src files
    os.system("make purge")
    # sync package files with src files
    print("> sync package files with src files")
    #os.system("make package-update")

    # Ensure we start with no packages
    os.system("make no-all")

    # Install packages (uncomment the packages you want included)
    print("> Install most commonly used packages")
    # Installs all packages that don't need extra libs
    os.system("make yes-most")
    os.system("make no-poems")  # some reason this don't work so remove it
    if use_voro:
        os.system("make yes-VORONOI")   # must install voro++ first, see instructions in lib/voronoi
    if use_kim:
        os.system("make yes-KIM")       # must build and install the KIM library first
    if use_quip:
        os.system("make yes-ML-QUIP")       # must build and install the KIM library first
    if use_intel_package:
        os.system("make yes-INTEL")   # This needs intel libraries to work

    # remove any deprecated src files
    print("> Purge any deprecated src files")
    os.system("make purge")
    # sync package files with src files
    print("> sync package files with src files")
    os.system("make package-update")

    # list available packages
    print("> List available packages and commands for info")
    os.system("make package")
    # list initial package status
    print("> List new package status")
    os.system("make package-status")

    # Generate the MINE directory if it does not exist
    if os.path.isdir("MAKE/MINE"):
        print("> The MINE directory exists ")
    else:
        print("> The MINE directory does not exist, creating... ")
        os.makedirs("MAKE/MINE")

    # Generate the custom makefile
    if os.path.isfile("MAKE/MINE/Makefile.kj_mpi"):
        print("> Existing file MAKE/MINE/Makefile.kj_mpi removed ")
        os.remove("MAKE/MINE/Makefile.kj_mpi")
    # Generate file
    print("> Generating: MAKE/MINE/Makefile.kj_mpi ...")
    outfile = open("MAKE/MINE/Makefile.kj_mpi", 'w')

    if use_intel:
        if use_intel_package:
            outfile.write("""# mpi = MPI with intel compiler, mac, jpeg, png, ffmpeg, intel cpus
SHELL = /bin/sh

# ---------------------------------------------------------------------
# compiler/linker settings
# specify flags and libraries needed for your compiler

CC =         mpicxx 
# Default
# OPTFLAGS = -O3
# CCFLAGS  = $(OPTFLAGS)
#

# Intel optimised (mac, magrid)
OPTFLAGS =   -xHost -O3 -fp-model fast=2 -no-prec-div -qoverride-limits -L$(MKLROOT)/lib/ -lmkl_intel_ilp64 -lmkl_sequential -lmkl_core
CCFLAGS  =   -DLAMMPS_MEMALIGN=64 -fno-alias -ansi-alias -restrict -DLMP_INTEL_USELRT -DLMP_USE_MKL_RNG $(OPTFLAGS)

# Intel optimised (athena, lovelace)
# OPTFLAGS =  -xHost -O2 -fp-model fast=2 -no-prec-div -qoverride-limits -L$(MKLROOT)/lib/intel64/ -lmkl_intel_ilp64 -lmkl_sequential -lmkl_core
# CCFLAGS =    -qopenmp -DLAMMPS_MEMALIGN=64 -qno-offload -fno-alias -ansi-alias -restrict -DLMP_INTEL_USELRT -DLMP_USE_MKL_RNG $(OPTFLAGS)


SHFLAGS =    -fPIC
DEPFLAGS =   -M

LINK =       mpicxx

LINKFLAGS =  $(OPTFLAGS)


# (athena, mac)
LIB =        -ltbbmalloc

# (lovelace)
# LIB =   -ltbbmalloc -lpthread -liomp5
SIZE =       size

ARCHIVE =    ar
ARFLAGS =    -rc
SHLIBFLAGS = -shared

# ---------------------------------------------------------------------
# LAMMPS-specific settings, all OPTIONAL
# specify settings for LAMMPS features you will use
# if you change any -D setting, do full re-compile after "make clean"

# LAMMPS ifdef settings
# see possible settings in Section 2.2 (step 4) of manual

LMP_INC =    -DLAMMPS_GZIP -DLAMMPS_MEMALIGN=64 -DLAMMPS_JPEG -DLAMMPS_PNG -DLAMMPS_FFMPEG

# MPI library
# see discussion in Section 2.2 (step 5) of manual
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

JPG_INC = -I/opt/local/include
JPG_PATH = -L/opt/local/lib
JPG_LIB = -ljpeg -lpng

# ---------------------------------------------------------------------
# build rules and dependencies
# do not edit this section

include Makefile.package.settings
include Makefile.package

EXTRA_INC = $(LMP_INC) $(PKG_INC) $(MPI_INC) $(FFT_INC) $(JPG_INC) $(PKG_SYSINC)
EXTRA_PATH = $(PKG_PATH) $(MPI_PATH) $(FFT_PATH) $(JPG_PATH) $(PKG_SYSPATH)
EXTRA_LIB = $(PKG_LIB) $(MPI_LIB) $(FFT_LIB) $(JPG_LIB) $(PKG_SYSLIB)
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

        else:    # intel compiler without USER-INTEL
            outfile.write("""# mpi = MPI with intel compiler, mac, jpeg, png, ffmpeg, intel cpus
SHELL = /bin/sh
# ---------------------------------------------------------------------
# compiler/linker settings
# specify flags and libraries needed for your compiler

CC =         mpicxx
# Default
OPTFLAGS = -xHost -O3 -std=c++11
CCFLAGS  = $(OPTFLAGS)

SHFLAGS =    -fPIC
DEPFLAGS =   -M

LINK =       mpicxx

LINKFLAGS =  $(OPTFLAGS) -std=c++11



LIB =        -ltbbmalloc
SIZE =       size

ARCHIVE =    ar
ARFLAGS =    -rc
SHLIBFLAGS = -shared

# ---------------------------------------------------------------------
# LAMMPS-specific settings, all OPTIONAL
# specify settings for LAMMPS features you will use
# if you change any -D setting, do full re-compile after "make clean"

# LAMMPS ifdef settings
# see possible settings in Section 2.2 (step 4) of manual

LMP_INC =    -DLAMMPS_GZIP -DLAMMPS_MEMALIGN=64 -DLAMMPS_JPEG -DLAMMPS_PNG -DLAMMPS_FFMPEG

# MPI library
# see discussion in Section 2.2 (step 5) of manual
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

JPG_INC = -I/opt/local/include
JPG_PATH = -L/opt/local/lib
JPG_LIB = -ljpeg -lpng

# ---------------------------------------------------------------------
# build rules and dependencies
# do not edit this section

include Makefile.package.settings
include Makefile.package

EXTRA_INC = $(LMP_INC) $(PKG_INC) $(MPI_INC) $(FFT_INC) $(JPG_INC) $(PKG_SYSINC)
EXTRA_PATH = $(PKG_PATH) $(MPI_PATH) $(FFT_PATH) $(JPG_PATH) $(PKG_SYSPATH)
EXTRA_LIB = $(PKG_LIB) $(MPI_LIB) $(FFT_LIB) $(JPG_LIB) $(PKG_SYSLIB)
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

    else:  # Default gcc

        outfile.write("""# g++_openmpi = OpenMPI with compiler set to GNU g++
SHELL = /bin/sh

# ---------------------------------------------------------------------
# compiler/linker settings
# specify flags and libraries needed for your compiler

export OMPI_CXX = g++
CC =         mpicxx

OPTFLAGS =  -march=native -mtune=native -O3
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
# see possible settings in Section 2.2 (step 4) of manual

LMP_INC =    -DLAMMPS_GZIP -DLAMMPS_MEMALIGN=64 -DLAMMPS_JPEG -DLAMMPS_PNG -DLAMMPS_FFMPEG

# MPI library
# see discussion in Section 2.2 (step 5) of manual
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

JPG_INC = -I/opt/local/include
JPG_PATH = -L/opt/local/lib
JPG_LIB = -ljpeg -lpng

# ---------------------------------------------------------------------
# build rules and dependencies
# do not edit this section

include Makefile.package.settings
include Makefile.package

EXTRA_INC = $(LMP_INC) $(PKG_INC) $(MPI_INC) $(FFT_INC) $(JPG_INC) $(PKG_SYSINC)
EXTRA_PATH = $(PKG_PATH) $(MPI_PATH) $(FFT_PATH) $(JPG_PATH) $(PKG_SYSPATH)
EXTRA_LIB = $(PKG_LIB) $(MPI_LIB) $(FFT_LIB) $(JPG_LIB) $(PKG_SYSLIB)
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

    '''
    # Copy customised reax/c source files to the src directory
    if(use_modified_reaxff):
        carbon_spline_src_dir = sys.path[0] + "/lammps_carbon_reaxff_spline_src/"

        carbon_file_1 = "reaxc_nonbonded.cpp"
        carbon_file_1_src = carbon_spline_src_dir + carbon_file_1
        carbon_file_2 = "reaxc_nonbonded.h"
        carbon_file_2_src = carbon_spline_src_dir + carbon_file_2

        # remove existing file
        if (os.path.isfile(carbon_file_1)):
            print("> Existing file " + carbon_file_1 + " removed ")
            os.remove(carbon_file_1)
        # copy modified file to src
        shutil.copy(carbon_file_1_src, carbon_file_1)
        print("> Copied updated file: " + carbon_file_1)

        # remove existing file
        if (os.path.isfile(carbon_file_2)):
            print("> Existing file " + carbon_file_2 + " removed ")
            os.remove(carbon_file_2)
        # copy modified file to src
        shutil.copy(carbon_file_2_src, carbon_file_2)
        print("> Copied updated file: " + carbon_file_2)
    '''

    print("> ")
    print("> Setup of lammps source directory is complete.")
    print("> You should check that the Makefile in /MAKE/MINE is correct for the machine you are working on.")
    print("> Check the output above is also as expected.")
    print("> ")
    print("> You can now compile lammps (using 4 cores):")
    print("> make -j 4 kj_mpi  ")
    print("> or build the shared library with:")
    print("> make -j 4 kj_mpi mode=shlib")


# If we are running this script interactively, call the function safely
if __name__ == '__main__':
    use_voro = False
    use_kim = False
    use_quip = False
    use_modified_reaxff = False
    use_intel = False
    use_intel_package = False
    
    print("  +------------------------------------------+")
    print("  |        Lammps setup compile script       |")
    print("  |                                          |")
    print("  |               Kenny Jolley               |")
    print("  |                Nov 2020                  |")
    print("  +------------------------------------------+")
    print("   ")

    print("> This script sets up the lammps source directory ready for compiling.\n")

    print("> You must clone the github repo yourself with:")
    print("   git clone https://github.com/lammps/lammps.git mylammps")
    print("> Or:")
    print("   git clone git://github.com/lammps/lammps.git mylammps\n")

    print(">  This script should then be run from the src directory of your lammps installation")
    print(">  The current directory is: ")
    print(os.getcwd())
    
    # Ask the user if they want to continue
    user_choice = str(input('Do you wish to continue? (y/n) : ')).lower().strip()
    if (user_choice != 'yes') and (user_choice != 'y'):
        sys.exit()

    # Ask user if VORO++ should be included
    print("   ")
    print("> Lammps can be built with the VORO++ package   ")
    print("> To use this package, you must install it before compiling lammps, see instructions in lib/voronoi")
    print("> VORO++ is available here:   ")
    print("> http://math.lbl.gov/voro++/ ")
    user_choice = str(input('Do you wish to include VORO++ ? (y/n) : ')).lower().strip()
    if (user_choice == 'yes') or (user_choice == 'y'):
        use_voro = True

    # Ask user if KIM should be included
    print("   ")
    print("> Lammps can be built with the KIM library   ")
    print("> To use this package, you must install it before compiling lammps, see instructions in lib/kim")
    user_choice = str(input('Do you wish to include KIM ? (y/n) : ')).lower().strip()
    if (user_choice == 'yes') or (user_choice == 'y'):
        use_kim = True

    # Ask user if Quippy should be included
    print("   ")
    print("> Lammps can be built with the ML-QUIP library   ")
    print("> To use this package, you must install it before compiling lammps, see instructions in lib/quip")
    user_choice = str(input('Do you wish to include ML-QUIP ? (y/n) : ')).lower().strip()
    if (user_choice == 'yes') or (user_choice == 'y'):
        use_quip = True


    '''print("   ")
    print("> A custom splining function between ReaxFF and ZBL for carbon systems can be added.")
    print("> This is available using the customised ReaxFF code.")
    user_choice = input('Do you wish to use the custom ReaxFF code? (y/n)?: ')
    if (user_choice == 'yes') or (user_choice == 'y'):
        use_modified_reaxff = True
    print("   ")'''

    print("   ")
    print("> This script generates a makefile.")
    print("> You need to choose between INTEL or GCC compiler options.")
    user_choice = str(input('Do you wish to use the INTEL compilers ? (y/n) : ')).lower().strip()
    if (user_choice == 'yes') or (user_choice == 'y'):
        use_intel = True

    # if we are using intel compilers, decide if we want USER-INTEL package
    if use_intel:
        print("   ")
        print("> You can use the optional USER-INTEL package.")
        user_choice = input('Do you wish to use the USER-INTEL package? (y/n)?: ')
        if (user_choice == 'yes') or (user_choice == 'y'):
            use_intel_package = True
    
    print("   ")

    # call the lammps_setup_custom_compile function
    lammps_setup_custom_compile(verbose=True,
                                use_voro=use_voro,
                                use_kim=use_kim,
                                us_quip=use_quip,
                                use_modified_reaxff=use_modified_reaxff,
                                use_intel=use_intel,
                                use_intel_package=use_intel_package)
