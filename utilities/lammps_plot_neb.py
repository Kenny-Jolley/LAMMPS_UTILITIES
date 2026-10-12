#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt


def read_neb_profile(filename):
    """
    Read the final NEB profile from a LAMMPS log file.

    Returns
    -------
    reaction_coordinate : ndarray
    energy : ndarray
    """

    with open(filename, "r") as f:
        lines = f.readlines()

    header_idx = None
    start_col = None

    # Checks if header is correct and gets column index of the start
    for i, line in enumerate(lines):
        #print(line)
        #print(i)
        if "RD1" in line and "PE1" in line:
            header_idx = i

        # Header found, find index of RD1
        if header_idx is not None:
            fields = line.split()
            for index, col_header in enumerate(fields):
                if col_header == "RD1":
                    start_col = index
                    break

    if start_col is None:
        raise RuntimeError("Could not find NEB profile data in logfile")

    # find the data line, which is the last line in the file
    values = lines[-1].split()
    #print(values)

    coords = []
    energies = []

    for i in range(start_col, len(values), 2):
        try:
            coords.append(float(values[i]))
            energies.append(float(values[i + 1]))
        except IndexError:
            break

    #print(coords)
    #print(energies)

    return np.array(coords), np.array(energies)


def calculate_barriers(energies):

    ts_idx = int(np.argmax(energies))
    e_initial = energies[0]
    e_final = energies[-1]
    e_ts = energies[ts_idx]

    return (
        ts_idx,
        e_initial,
        e_final,
        e_ts,
        e_ts - e_initial,   # forward barrier
        e_ts - e_final,     # reverse barrier
    )


def plot_neb(coords, energies):

    (
        ts_idx,
        e_initial,
        e_final,
        e_ts,
        forward_barrier,
        reverse_barrier,
    ) = calculate_barriers(energies)

    ts_coord = coords[ts_idx]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        coords,
        energies,
        color="blue",
        linestyle='-',  # - solid, -- dashed, -. dashdot, : dotted
        linewidth=1.5,  # width/thickness of line
        marker='*',  # style
        markeredgecolor='blue',
        markeredgewidth=1,
        markersize=6,
        label="NEB images"
    )

    ax.plot(
        ts_coord,
        e_ts,
        "ro",
        ms=10,
        label="Transition state"
    )

    # Horizontal reference lines for initial and final states
    ax.axhline(
        e_initial,
        color="green",
        linestyle="--",
        linewidth=1.5,
        alpha=0.8,
    )

    ax.axhline(
        e_final,
        color="tab:blue",
        linestyle="--",
        linewidth=1.5,
        alpha=0.8,
    )

    # Forward barrier (vertical arrow)
    x_forward = ts_coord - 0.03 * (coords.max() - coords.min())

    ax.annotate(
        "",
        xy=(x_forward, e_ts),
        xytext=(x_forward, e_initial),
        arrowprops=dict(
            arrowstyle="<->",
            lw=2,
            color="red"
        ),
    )

    ax.text(
        x_forward,
        (e_ts + e_initial) / 2,
        f"Ef = {forward_barrier:.3f} eV",
        color="red",
        ha="right",
        va="center",
        bbox=dict(fc="white", ec="none", alpha=0.8),
    )

    # Reverse barrier (vertical arrow)
    x_reverse = ts_coord + 0.03 * (coords.max() - coords.min())

    ax.annotate(
        "",
        xy=(x_reverse, e_ts),
        xytext=(x_reverse, e_final),
        arrowprops=dict(
            arrowstyle="<->",
            lw=2,
            color="purple"
        ),
    )

    ax.text(
        x_reverse,
        (e_ts + e_final) / 2,
        f"Er = {reverse_barrier:.3f} eV",
        color="purple",
        ha="left",
        va="center",
        bbox=dict(fc="white", ec="none", alpha=0.8),
    )

    # Labels for initial/final energies
    ax.text(
        coords[0] + 0.1,
        e_initial,
        f" Initial state = {e_initial:.3f} eV",
        color="green",
        va="bottom",
        ha="left",
        bbox=dict(fc="white", ec="none", alpha=0.8),
    )

    ax.text(
        coords[-1] - 0.1,
        e_final,
        f" Final state = {e_final:.3f} eV",
        color="tab:blue",
        va="bottom",
        ha="right",
        bbox=dict(fc="white", ec="none", alpha=0.8),
    )

    ax.set_xlabel("Reaction Coordinate")
    ax.set_ylabel("Energy (eV)")
    ax.set_title("NEB Energy Profile")

    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    print("NEB plotter script\n")

    # Default filename
    logfile = "log.lammps"

    if len(sys.argv) == 1:
        print(f"Reading logfile : {logfile}")
        print("> To use a custom file, pass name of the commandline\n")
    elif len(sys.argv) == 2:
        logfile = sys.argv[1]
        print(f"Reading logfile : {logfile}")

    # Get energy barrier data
    coords, energies = read_neb_profile(logfile)

    (
        ts_idx,
        e_initial,
        e_final,
        e_ts,
        forward_barrier,
        reverse_barrier,
    ) = calculate_barriers(energies)

    print(f"NEB Images             : {len(coords)}")
    print(f"Transition-state image : {ts_idx + 1}")
    print(f"Initial energy         : {e_initial:.6f} eV")
    print(f"Final energy           : {e_final:.6f} eV")
    print(f"TS energy              : {e_ts:.6f} eV")
    print(f"Forward barrier        : {forward_barrier:.6f} eV")
    print(f"Reverse barrier        : {reverse_barrier:.6f} eV")

    fig = plot_neb(coords, energies)
    fig.savefig("neb_barrier.png", dpi=300)

