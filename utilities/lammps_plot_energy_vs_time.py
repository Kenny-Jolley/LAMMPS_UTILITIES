#!/usr/bin/env python

# This function reads a lammps log.lammps file, and plots the Total energy vs time.
# By default we plot all parts even if split into different runs.

# Keyword arguments:
# verbose    = True  , prints some comments to the screen.
# overwrite  = True  , will overwrite the existing file.


# Kenny Jolley, Nov 2019

# imported modules
import sys
import matplotlib.pyplot as plt
import numpy as np


# function reads a lammps log.lammps file, and plots the Total energy vs time.
def lammps_plot_energy_vs_time(**kwargs):
    # Default keyword args
    verbose = kwargs.get('verbose', False)
    filename = kwargs.get('logfile', 'log.lammps')
    overwrite = kwargs.get('overwrite', False)
    legend = kwargs.get('legend', True)

    # Welcome
    if verbose:
        print("  +-------------------------------------------+")
        print("  | This script reads a log.lammps file and   |")
        print("  | plots the total energy [eV] vs time [ps]  |")
        print("  |                                           |")
        print("  |               Kenny Jolley                |")
        print("  |                 June 2021                 |")
        print("  +-------------------------------------------+")
        print("")
        print("Verbose:      ", verbose)
        print("overwrite:    ", overwrite)
        print("legend:       ", legend)

        print("\n>  Reading Lammps log file: " + str(filename))

    # open file and read in data
    infile = open(filename, 'r')

    # data arrays
    data_time = []
    data_temp = []
    lammps_data_vals = 0
    lammps_unit_type = 'metal'  # Set units to metal as default (modified if set in log file)
    data_blocks = 0
    data_block_start_ids = []

    # Find and read in the data
    while 1:
        # reset flags for header and column search
        header_cols_found = 0
        time_col = -1
        temp_col = -1

        # read line, exit if at end of file
        fileline = infile.readline()
        if not fileline:
            break

        # split line into a list
        fileline = fileline.split()

        # if list is zero length, then skip
        if len(fileline) == 0:
            continue

        # Ignore comments: if first element begins with a # then skip
        if fileline[0][0] == "#":
            continue

        # Find and set the correct unit type (supports real and metal)
        if fileline[0] == "units":
            lammps_unit_type = fileline[1]

        # todo: more robust search for header line
        # Now find the line with Time and Temp in the header
        for i in range(0, len(fileline)):
            if fileline[i] == "Time":
                time_col = i
                header_cols_found = header_cols_found + 1
            if fileline[i] == "TotEng":
                temp_col = i
                header_cols_found = header_cols_found + 1

        # If both columns are found, we have the header
        if header_cols_found == 2:

            # Record count of data blocks, and record data id value
            data_blocks = data_blocks + 1
            data_block_start_ids.append(int(lammps_data_vals))

            if verbose:
                print("A data section was found ")
                print("TotEng column found: " + str(temp_col))
                print("Time column found: " + str(time_col))

            # now we save the data ( break at end of file, or end of data section)
            while 1:
                # read line, exit if at end of file
                fileline = infile.readline()
                if not fileline:
                    break

                # exit at end of data block
                if fileline[0] == "L":
                    break

                # split line into a list
                fileline = fileline.split()

                # exit if len < temp or time col  (ie if line is incomplete)
                if (len(fileline) < time_col) + (len(fileline) < temp_col):
                    break

                data_time.append(float(fileline[time_col]))
                data_temp.append(float(fileline[temp_col]))

                # count number of data points read
                lammps_data_vals = lammps_data_vals + 1

    # Close the file
    infile.close()

    # Check the data was found
    if lammps_data_vals == 0:
        print("Could not find the data header, exiting...")
        print("Time column found: " + str(time_col))
        print("TotEng column found: " + str(temp_col))
        sys.exit()

    print(" ")
    print("Lammps units: " + str(lammps_unit_type))

    # Print final times and energies, converting units if required
    # Simulation time
    # ps
    if lammps_unit_type == "metal":
        print("Simulation time: " + str(data_time[lammps_data_vals - 1]) + " ps")
    # fs to ps
    if lammps_unit_type == "real":
        print("Simulation time: " + str(data_time[lammps_data_vals - 1] / 1000.0) + " ps")

    # Final energy
    # eV
    if lammps_unit_type == "metal":
        print("Final TotEng: " + str(data_temp[lammps_data_vals - 1]) + " eV")
    # Kcal/mol to eV
    if lammps_unit_type == "real":
        print("Final TotEng: " + str(data_temp[lammps_data_vals - 1] / 23.061) + " eV")

    # plotting the data
    color_list = ["red", "green", "blue", "purple", "olive", "maroon"]

    # Create a new figure of size 12x8 points, using 100 dots per inch
    fig = plt.figure(figsize=(12, 8), dpi=100)
    # Create a new subplot from a grid of 1x1
    ax = fig.add_subplot(111)

    # Labels
    plt.title('Energy (eV) vs time (ps)')
    plt.xlabel('Time, ps')
    plt.ylabel('Energy, eV')

    # Plot Temperature vs time
    mylabel = "Total Energy"

    # convert data if required
    if lammps_unit_type == "real":
        data_time = np.asarray(data_time)
        data_temp = np.asarray(data_temp)
        data_time = data_time / 1000.0
        data_temp = data_temp / 23.061

    print("\nThere were " + str(data_blocks) + " simulation data blocks in the log file")
    print("Block starting ids: " + str(data_block_start_ids))

    if data_blocks > 1:
        for i in range(0, data_blocks - 1):
            ax.plot(data_time[data_block_start_ids[i]:data_block_start_ids[i + 1]],
                    data_temp[data_block_start_ids[i]:data_block_start_ids[i + 1]],
                    color=color_list[i % 5],
                    linewidth=1.5,
                    linestyle="-",
                    label=mylabel + " - Block " + str(i))

        ax.plot(data_time[data_block_start_ids[data_blocks - 1]:],
                data_temp[data_block_start_ids[data_blocks - 1]:],
                color=color_list[(data_blocks - 1) % 5],
                linewidth=1.5,
                linestyle="-",
                label=mylabel + " - Block " + str((data_blocks - 1)))

    else:
        ax.plot(data_time, data_temp, color=color_list[0], linewidth=1.5, linestyle="-", label=mylabel)
    plt.legend()

    # set x range between 0 and total simulation time.
    plt.xlim([0, data_time[-1]])

    # Save figure using 100 dots per inch
    filename = "_figure_plot_Energy_vs_time.png"
    plt.savefig(filename, dpi=300)
    filename = "_figure_plot_Energy_vs_time.pdf"
    plt.savefig(filename, dpi=300)

    # Save raw data to a csv file
    filename = "_figure_plot_Energy_vs_time.csv"
    file = open(filename, 'w')
    # header
    line = "Simtime (ps),Energy (eV)\n"
    file.write(line)
    # data
    for i in range(0, lammps_data_vals - 1):
        line = str(data_time[i]) + ','
        line = line + str(data_temp[i]) + ','
        line = line + '\n'
        file.write(line)
    file.close()


# If we are running this script interactively, call the function safely
if __name__ == '__main__':

    # Get the filename from commandline, if present
    if len(sys.argv) > 1:
        supplied_filename = str(sys.argv[1])

        # call the function safely
        lammps_plot_energy_vs_time(verbose=True,
                                   overwrite=True,
                                   filename=supplied_filename)

    else:
        # call the function safely (use default filename)
        lammps_plot_energy_vs_time(verbose=True,
                                   overwrite=True)
