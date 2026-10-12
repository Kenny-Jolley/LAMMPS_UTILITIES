#!/bin/bash

# Welcome message
echo "+------------------------------------+"
echo "|  Lammps download and build script  |"
echo "|                                    |"
echo "|             Kenny Jolley           |"
echo "|               Oct 2026             |"
echo "+------------------------------------+"
echo
echo "First we list the current build tools that are loaded"
echo "> Check these are the expected tools listed"
echo

check_tool() {
	if command -v "$1" >/dev/null 2>&1; then
		printf "%-10s : FOUND (%s)\n" "$1" "$(command -v "$1")"
		printf "%-10s :" " "
		"$1" --version 2>/dev/null | head -n 1 | sed 's/^/ Version: /'
		#printf "%-15s : $($S1 --version )\n" " "
	else
		printf "%-15s : NOT FOUND\n" "$1"
	fi
	echo
}


echo "=== Compilers ==="
for tool in gcc g++ gfortran; do
	check_tool "$tool"
done

echo "=== Build Systems ==="
for tool in make cmake autoconf automake; do
	check_tool "$tool"
done

echo "=== Linkers and Binary Tools ==="
for tool in ld ar ranlib nm objdump readelf strip; do
	check_tool "$tool"
done

echo "=== MPI ==="
for tool in mpicc mpicxx mpif90 mpirun mpiexec; do
	check_tool "$tool"
done

echo "=== Python Build Environment ==="
for tool in python python3 pip pip3; do
	check_tool "$tool"
done

echo "=== Git ==="
check_tool git


echo "=== Environment Variables ==="

vars=(
	CC
	CXX
	FC
	F77
	F90
	CFLAGS
	CXXFLAGS
	FCFLAGS
	CPPFLAGS
	LDFLAGS
	LD_LIBRARY_PATH
	DYLD_LIBRARY_PATH
	LIBRARY_PATH
	CPATH
	PATH
)

for v in "${vars[@]}"; do
	if [[ -n "${!v:-}" ]]; then
		echo "$v=${!v}"
	else
		echo "$v=<not set>"
	fi
done


echo
echo "=== GCC Configuration ==="

if command -v gcc >/dev/null 2>&1; then
	gcc -v 2>&1 | tail -20
fi

echo

### Check with user everything is OK
echo "================================================================"
printf "Current working directory: %s \n" "$(pwd)"
echo "> listing files and folders:"
ls
echo
echo "CHECK THE ABOVE INFORMATION"
read -r -p "Is this build environment OK? [y/N\]: " response

case "${response,,}" in
	y|yes)
		echo "Continuing..."
		;;
	n|no|"")
		echo "Exiting."
		exit 1
		;;
	*)
		echo "Invalid response. Exiting."
		exit 1
		;;
esac


# Ensure ~/git exists
echo
echo "We now create a ~/git directory if it does not exist and cd into it"
GIT_DIR="$HOME/git"

if [ ! -d "$GIT_DIR" ]; then
    echo "Directory $GIT_DIR does not exist. Creating it..."
    mkdir -p "$GIT_DIR" || {
        echo "Error: Failed to create $GIT_DIR"
        exit 1
    }
fi

# Change into the git directory
cd "$GIT_DIR" || {
    echo "Error: Failed to change to directory $GIT_DIR"
    exit 1
}

echo "Current working directory: $(pwd)"
echo "Current contents:"
ls
echo


echo
echo "========================================"
echo " Clone LAMMPS Repository"
echo "========================================"

# Check git exists
if ! command -v git >/dev/null 2>&1; then
    echo "ERROR: git is not installed."
    exit 1
fi

# Ask user for destination folder
read -rp "Enter folder name for the LAMMPS source code: " LAMMPS_DIR

# Validate input
if [[ -z "$LAMMPS_DIR" ]]; then
    echo "ERROR: Folder name cannot be empty."
    exit 1
fi

# Check if folder already exists
if [[ -e "$LAMMPS_DIR" ]]; then
    echo "ERROR: '$LAMMPS_DIR' already exists."
    exit 1
fi

echo
echo "Cloning LAMMPS into '$LAMMPS_DIR'..."
git clone https://github.com/lammps/lammps.git "$LAMMPS_DIR"

if [[ $? -eq 0 ]]; then
    echo "LAMMPS successfully cloned."
    echo "Source directory:"
    echo "  $(realpath "$LAMMPS_DIR" 2>/dev/null || echo "$PWD/$LAMMPS_DIR")"
else
    echo "LAMMPS clone failed."
    exit 1
fi


echo
echo "========================================"
echo " Build LAMMPS"
echo "========================================"

read -rp "Build LAMMPS now? [y/N\]: " BUILD

if [[ "$BUILD" =~ ^[Yy]$ ]]; then

    cd "$LAMMPS_DIR" || exit 1

    mkdir -p build
    cd build || exit 1

    echo
    echo "Detecting available CPUs..."

    if command -v nproc >/dev/null 2>&1; then
        AVAILABLE_CPUS=$(nproc)
    elif command -v sysctl >/dev/null 2>&1; then
        AVAILABLE_CPUS=$(sysctl -n hw.ncpu)
    else
        AVAILABLE_CPUS=1
    fi

    echo "Available CPUs: $AVAILABLE_CPUS"

    read -rp \
        "Number of CPUs to use for compilation [$AVAILABLE_CPUS\]: " \
        BUILD_CPUS

    BUILD_CPUS=${BUILD_CPUS:-$AVAILABLE_CPUS}

    # Validate input
    if ! [[ "$BUILD_CPUS" =~ ^[0-9]+$ ]] || [[ "$BUILD_CPUS" -lt 1 ]]; then
        echo "Invalid CPU count."
        exit 1
    fi

    echo
    echo "Configuring LAMMPS..."


cmake ../cmake \
        -D BUILD_MPI=on \
        -D BUILD_SHARED_LIBS=on \
	-D PKG_AMOEBA=yes \
	-D PKG_ASPHERE=yes \
	-D PKG_BOCS=yes \
	-D PKG_BODY=yes \
	-D PKG_BPM=yes \
	-D PKG_BROWNIAN=yes \
	-D PKG_CG-DNA=yes \
	-D PKG_CG-SPICA=yes \
	-D PKG_CLASS2=yes \
	-D PKG_COLLOID=yes \
	-D PKG_COMPRESS=yes \
	-D PKG_CORESHELL=yes \
	-D PKG_DIELECTRIC=yes \
	-D PKG_DIFFRACTION=yes \
	-D PKG_DIPOLE=yes \
	-D PKG_DPD-BASIC=yes \
	-D PKG_DPD-MESO=yes \
	-D PKG_DPD-REACT=yes \
	-D PKG_DPD-SMOOTH=yes \
	-D PKG_DRUDE=yes \
	-D PKG_EFF=yes \
	-D PKG_ELECTRODE=yes \
	-D PKG_EXTRA-COMMAND=yes \
	-D PKG_EXTRA-COMPUTE=yes \
	-D PKG_EXTRA-DUMP=yes \
	-D PKG_EXTRA-FIX=yes \
	-D PKG_EXTRA-MOLECULE=yes \
	-D PKG_EXTRA-PAIR=yes \
	-D PKG_FEP=yes \
	-D PKG_GRANULAR=yes \
	-D PKG_GRANSURF=yes \
	-D PKG_INTERLAYER=yes \
	-D PKG_KSPACE=yes \
	-D PKG_LATBOLTZ=yes \
	-D PKG_MANIFOLD=yes \
	-D PKG_MANYBODY=yes \
	-D PKG_MC=yes \
	-D PKG_MEAM=yes \
	-D PKG_MESONT=yes \
	-D PKG_MGPT=yes \
	-D PKG_MISC=yes \
	-D PKG_ML-PACE=yes \
	-D PKG_MOFFF=yes \
	-D PKG_MOLECULE=yes \
	-D PKG_ORIENT=yes \
	-D PKG_PERI=yes \
	-D PKG_PHONON=yes \
	-D PKG_PLUGIN=yes \
	-D PKG_PTM=yes \
	-D PKG_QEQ=yes \
	-D PKG_QTB=yes \
	-D PKG_REACTION=yes \
	-D PKG_REAXFF=yes \
	-D PKG_REPLICA=yes \
	-D PKG_RIGID=yes \
	-D PKG_SHOCK=yes \
	-D PKG_SMTBQ=yes \
	-D PKG_SPH=yes \
	-D PKG_SPIN=yes \
	-D PKG_SRD=yes \
	-D PKG_TALLY=yes \
	-D PKG_UEF=yes \
	-D DOWNLOAD_VORO=yes \
	-D PKG_VORONOI=yes \
	-D PKG_YAFF=yes \


    if [[ $? -ne 0 ]]; then
        echo "CMake configuration failed."
        exit 1
    fi

    echo
    echo "Building LAMMPS using $BUILD_CPUS CPU(s)..."

    cmake --build . -j"$BUILD_CPUS"

    if [[ $? -eq 0 ]]; then
        echo
        echo "LAMMPS build completed successfully."
    else
        echo
        echo "LAMMPS build failed."
        exit 1
    fi

fi


