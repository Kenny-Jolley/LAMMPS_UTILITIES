# Utilities

A collection of scripts for setting up lammps and manipulating the lammps input and output files.

## Usage

#### `lammps_convert_output_to_XYZ.py`  

This script converts lammps output dump files to a sequence of xyz files.  Compressed files can be read (assuming gzip is installed), and star notation is used to convert all files with the same pattern.

Examples:
~~~
lammps_convert_output_to_XYZ.py  filename.txt
lammps_convert_output_to_XYZ.py  dump.dat.gz
lammps_convert_output_to_XYZ.py  'dump*.dat.gz'
~~~

#### `lammps_lattice_relabel_atom_ids.py`

This script reads a lammps lattice input file and relabels the atom IDs so that they are sequential.  The script also checks that the correct number of atoms are present.

~~~
lammps_lattice_relabel_atom_ids.py filename.txt
~~~

#### `lammps_setup_custom_compile.py`

This script sets up the lammps source directory ready for compiling lammps.  
The script pulls the latest stable release and handles updating all packages that don't require extra libraries.

The user can choose to include the Voro++ package, if this is already installed.
The user can also choose to use the USER-INTEL package.  This requires the intel compiler to work.

This script then generates a makefile.  The user can then build lammps (on 4 cores) using:
~~~
make -j 4 kj_mpi
~~~

and the library using:
~~~
make -j 4 kj_mpi mode=shlib
~~~

When running lammps on a mac, you may run into problems locating the shared intel libraries. eg:
~~~
makj% ./lmp_kj_mpi 
dyld: Library not loaded: @rpath/libtbbmalloc.dylib
  Referenced from: /Network/Servers/magrid-server-5.lut.ac.uk/Volumes/Users_HD3/MD_NFS/makj/test/./lmp_kj_mpi
  Reason: image not found
Abort
makj%
~~~

This occurs because the compiled binary and library files contain rpath links to the intel libraries which cannot be found. (Not sure why this happens, probably something to do with recent updates to macOS and the system integrity protection):
~~~
makj% otool -L liblammps_kj_mpi.so
liblammps_kj_mpi.so:
	../liblammps_kj_mpi.so (compatibility version 0.0.0, current version 0.0.0)
	@rpath/libmkl_intel_ilp64.dylib (compatibility version 0.0.0, current version 0.0.0)
	@rpath/libmkl_sequential.dylib (compatibility version 0.0.0, current version 0.0.0)
	@rpath/libmkl_core.dylib (compatibility version 0.0.0, current version 0.0.0)
	/opt/local/lib/libjpeg.9.dylib (compatibility version 13.0.0, current version 13.0.0)
	/opt/local/lib/libpng16.16.dylib (compatibility version 54.0.0, current version 54.0.0)
	@rpath/libtbbmalloc.dylib (compatibility version 0.0.0, current version 0.0.0)
	/Users/makj/openmpi-4.0.1_install/lib/libmpi.40.dylib (compatibility version 61.0.0, current version 61.1.0)
	/usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 400.9.4)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1252.250.1)
~~~


You can fix this issue by modifying the library paths in the executable manually:
~~~
install_name_tool -change @rpath/libmkl_intel_ilp64.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_intel_ilp64.dylib  lmp_kj_mpi 
install_name_tool -change @rpath/libmkl_sequential.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_sequential.dylib  lmp_kj_mpi 
install_name_tool -change @rpath/libmkl_core.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_core.dylib  lmp_kj_mpi 
install_name_tool -change @rpath/libtbbmalloc.dylib /opt/intel/compilers_and_libraries/mac/tbb/lib/libtbbmalloc.dylib  lmp_kj_mpi 
~~~

This works for the library too:
~~~
install_name_tool -change @rpath/libmkl_intel_ilp64.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_intel_ilp64.dylib  liblammps_kj_mpi.so
install_name_tool -change @rpath/libmkl_sequential.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_sequential.dylib  liblammps_kj_mpi.so
install_name_tool -change @rpath/libmkl_core.dylib /opt/intel/compilers_and_libraries/mac/mkl/lib/libmkl_core.dylib  liblammps_kj_mpi.so
install_name_tool -change @rpath/libtbbmalloc.dylib /opt/intel/compilers_and_libraries/mac/tbb/lib/libtbbmalloc.dylib  liblammps_kj_mpi.so
~~~



