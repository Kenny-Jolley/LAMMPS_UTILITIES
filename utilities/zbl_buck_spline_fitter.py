#!/usr/bin/env python

# This script plots the ZBL and buckingham potential for given parameters and calculates
# a spline function that joins them together.


#    Kenny Jolley, April 2021

# imported modules
# import sys
# import os
import math
import numpy as np
import matplotlib.pyplot as plt
import datetime

from sympy.core.symbol import symbols
from sympy.solvers.solveset import nonlinsolve
# from sympy.polys.polytools import is_zero_dimensional

# --------------------------------------------
# Configurable variables
# --------------------------------------------

# atom 1
atom1_name = "B"
atom1_Z = 5  # number of protons
atom1_Q = 1.4175  # electric charge

# atom 2
atom2_name = "O"
atom2_Z = 8  # number of protons
atom2_Q = -0.945  # electric charge

# Buckingham Potential Parameters
buck_A = 15176.81
buck_rho = 0.15
buck_C = 9.0821

# Spline offset (preferred to be zero, but sometimes we need to ensure spline points are not negative)
spline_offset = 50
sp_1 = 0.40
sp_2 = 1.00

# Plots
make_plots = True
plot_fig_size_w = 9
plot_fig_size_h = 6
plot_dpi = 200

# --------------------------------------------


# Constants
q = 1.60217646e-19
epsilon = 8.854187817e-12

E = (q * q / (4 * math.pi * epsilon))
E2 = E / (q * 1e-10)
# print(E2)

# ZBL Potential Parameters
ABOHR = 0.53
ACONST = 0.88534
POW = 0.23

A = ACONST * ABOHR / (atom1_Z ** POW + atom2_Z ** POW)
d1 = -3.1998 / A
d2 = -0.94229 / A
d3 = -0.4029 / A
d4 = -0.20162 / A

CCONST = atom1_Z * atom2_Z * E2
c1 = CCONST * 0.18175
c2 = CCONST * 0.50986
c3 = CCONST * 0.28022
c4 = CCONST * 0.028171

# Get date today
x = datetime.datetime.now()
# Set pre-factor for output filename
output_filename_prefac = (x.strftime("%Y") + x.strftime("%m") +
                          x.strftime("%d") + x.strftime("%H") +
                          x.strftime("%M") + x.strftime("%S") +
                          "_Plot_")


# print(A)


# ZBL functions

# ZBL
def ZBL(r, c1, c2, c3, c4, d1, d2, d3, d4, offset):
    return (c1 * np.exp(d1 * r) + c2 * np.exp(d2 * r) + c3 * np.exp(d3 * r) + c4 * np.exp(d4 * r)) / r + offset


# ZBL - first derivative
def ZBL_dr(r, c1, c2, c3, c4, d1, d2, d3, d4):
    return (c1 * d1 * np.exp(d1 * r) + c2 * d2 * np.exp(d2 * r) + c3 * d3 * np.exp(d3 * r) + c4 * d4 * np.exp(
        d4 * r)) / r \
           - (c1 * np.exp(d1 * r) + c2 * np.exp(d2 * r) + c3 * np.exp(d3 * r) + c4 * np.exp(d4 * r)) / r ** 2


# ZBL - second derivative
def ZBL_dr2(r, c1, c2, c3, c4, d1, d2, d3, d4):
    return (c1 * d1 * d1 * np.exp(d1 * r) + c2 * d2 * d2 * np.exp(d2 * r) + c3 * d3 * d3 * np.exp(
        d3 * r) + c4 * d4 * d4 * np.exp(d4 * r)) / r \
           - 2 * (c1 * d1 * np.exp(d1 * r) + c2 * d2 * np.exp(d2 * r) + c3 * d3 * np.exp(d3 * r) + c4 * d4 * np.exp(
        d4 * r)) / r ** 2 \
           + 2 * (c1 * np.exp(d1 * r) + c2 * np.exp(d2 * r) + c3 * np.exp(d3 * r) + c4 * np.exp(d4 * r)) / r ** 3


#
# Plot the ZBL potential
if make_plots:
    plt.figure(figsize=(plot_fig_size_w, plot_fig_size_h))
    x = np.linspace(0.01, 6, 1000)
    y = ZBL(x, c1, c2, c3, c4, d1, d2, d3, d4, spline_offset) - spline_offset
    plt.plot(x, y, label='ZBL(r)')

    y = ZBL_dr(x, c1, c2, c3, c4, d1, d2, d3, d4)
    plt.plot(x, y, label=r'$\frac{d}{dr} ZBL(r)$')

    y = ZBL_dr2(x, c1, c2, c3, c4, d1, d2, d3, d4)
    plt.plot(x, y, label=r'$\frac{d^2}{dr^2} ZBL(r)$')

    plt.xlabel(r'Pair separation, $\AA$',
               fontweight='bold',
               size=16)
    plt.ylabel("Potential Energy, eV",
               fontweight='bold',
               size=16)

    plt.title("ZBL pair potential for the " + str(atom1_name) + "-" + str(atom2_name) + " interaction",
              fontweight='bold',
              size=18)

    plt.ylim(-1000, 1000)  # set y range of y axis
    plt.xlim(0, 6)  # set x range of x axis
    plt.xticks(np.linspace(0, 6, 13))

    plt.legend(loc='upper right',
               fontsize=18,
               )
    plt.grid(True)

    # Save ZBL plot
    plt.savefig(output_filename_prefac + 'ZBL.png', format="png", dpi=plot_dpi)
    # plt.show()


# Buckingham functions (includes coulomb part)
# Buck
def Buck(r, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2, offset):
    return buck_A * np.exp(-r / buck_rho) - (buck_C / r ** 6) + ((atom1_Q * atom2_Q * E2) / r) + offset


# Buck - first derivative
def Buck_dr(r, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2):
    return -(buck_A * np.exp(-r / buck_rho)) / buck_rho + (6.0 * buck_C / r ** 7) - (atom1_Q * atom2_Q * E2) / r ** 2


# Buck - second derivative
def Buck_dr2(r, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2):
    return (buck_A * np.exp(-r / buck_rho)) / buck_rho ** 2 - (42.0 * buck_C / r ** 8) + (
            2.0 * atom1_Q * atom2_Q * E2) / r ** 3


#
# Plot the Buck potential
if make_plots:
    plt.figure(figsize=(plot_fig_size_w, plot_fig_size_h))
    x = np.linspace(0.01, 6, 1000)
    y = Buck(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2, spline_offset) - spline_offset
    plt.plot(x, y, label='Buck(r)')

    y = Buck_dr(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)
    plt.plot(x, y, label=r'$\frac{d}{dr} Buck(r)$')

    y = Buck_dr2(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)
    plt.plot(x, y, label=r'$\frac{d^2}{dr^2} Buck(r)$')

    plt.xlabel(r'Pair separation, $\AA$',
               fontweight='bold',
               size=16)
    plt.ylabel("Potential Energy, eV",
               fontweight='bold',
               size=16)

    plt.title("Buck pair potential for the " + str(atom1_name) + "-" + str(atom2_name) + " interaction",
              fontweight='bold',
              size=18)

    plt.ylim(-1000, 1000)  # set y range of y axis
    plt.xlim(0, 6)  # set x range of x axis
    plt.xticks(np.linspace(0, 6, 13))

    plt.legend(loc='upper right',
               fontsize=18,
               )
    plt.grid(True)

    # Save BUCK plot
    plt.savefig(output_filename_prefac + 'BUCK.png', format="png", dpi=plot_dpi)
    # plt.show()


# Spline fitting

# V - value of potential energy at splines
V1 = ZBL(sp_1, c1, c2, c3, c4, d1, d2, d3, d4, spline_offset)
V2 = Buck(sp_2, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2, spline_offset)

# F - Gradient of potential energy at splines
F1 = ZBL_dr(sp_1, c1, c2, c3, c4, d1, d2, d3, d4)
F2 = Buck_dr(sp_2, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)

# G - Second derivative of potential energy at splines
G1 = ZBL_dr2(sp_1, c1, c2, c3, c4, d1, d2, d3, d4)
G2 = Buck_dr2(sp_2, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)

# print values at spline points
print("Values and gradients at spline points")
print("V1: ", V1)
print("V2: ", V2)
print("F1: ", F1)
print("F2: ", F2)
print("G1: ", G1)
print("G2: ", G2)

# define equations
f0, f1, f2, f3, f4, f5 = symbols('f0,f1,f2,f3,f4,f5', real=True)

eq1 = f0 + f1 * sp_1 + f2 * sp_1 ** 2 + f3 * sp_1 ** 3 + f4 * sp_1 ** 4 + f5 * sp_1 ** 5 - math.log(V1)
eq2 = f0 + f1 * sp_2 + f2 * sp_2 ** 2 + f3 * sp_2 ** 3 + f4 * sp_2 ** 4 + f5 * sp_2 ** 5 - math.log(V2)
eq3 = f1 + 2 * f2 * sp_1 + 3 * f3 * sp_1 ** 2 + 4 * f4 * sp_1 ** 3 + 5 * f5 * sp_1 ** 4 - F1 / V1
eq4 = f1 + 2 * f2 * sp_2 + 3 * f3 * sp_2 ** 2 + 4 * f4 * sp_2 ** 3 + 5 * f5 * sp_2 ** 4 - F2 / V2
eq5 = 2 * f2 + 6 * f3 * sp_1 + 12 * f4 * sp_1 ** 2 + 20 * f5 * sp_1 ** 3 - (G1 / V1) + (F1 / V1) ** 2
eq6 = 2 * f2 + 6 * f3 * sp_2 + 12 * f4 * sp_2 ** 2 + 20 * f5 * sp_2 ** 3 - (G2 / V2) + (F2 / V2) ** 2

system = [eq1, eq2, eq3, eq4, eq5, eq6]
# print(is_zero_dimensional(system))

the_solution = nonlinsolve(system, [f0, f1, f2, f3, f4, f5])
print("The full solution: ")
print(the_solution)

f0 = float(the_solution.args[0][0])
f1 = float(the_solution.args[0][1])
f2 = float(the_solution.args[0][2])
f3 = float(the_solution.args[0][3])
f4 = float(the_solution.args[0][4])
f5 = float(the_solution.args[0][5])
print("Spline function parameters:")
print("f0: ", f0)
print("f1: ", f1)
print("f2: ", f2)
print("f3: ", f3)
print("f4: ", f4)
print("f5: ", f5)


# Spline equations
# Spline
def spline(r_, f0_, f1_, f2_, f3_, f4_, f5_):
    return np.exp(f0_ + f1_ * r_ + f2_ * r_ ** 2 + f3_ * r_ ** 3 + f4_ * r_ ** 4 + f5_ * r_ ** 5)


# Spline - first derivative
def spline_dr(r_, f0_, f1_, f2_, f3_, f4_, f5_):
    return (5.0 * f5_ * r_ ** 4 + 4.0 * f4_ * r_ ** 3 + 3.0 * f3_ * r_ ** 2 + 2.0 * f2_ * r_ + f1_) * \
           spline(r_, f0_, f1_, f2_, f3_, f4_, f5_)


# Spline - second derivative
def spline_dr2(r_, f0_, f1_, f2_, f3_, f4_, f5_):
    return ((5.0 * f5_ * r_ ** 4 + 4.0 * f4_ * r_ ** 3 + 3.0 * f3_ * r_ ** 2 + 2.0 * f2_ * r_ + f1_) ** 2 *
            spline(r_, f0_, f1_, f2_, f3_, f4_, f5_) +
            (20.0 * f5_ * r_ ** 3 + 12.0 * f4_ * r_ ** 2 + 6.0 * f3_ * r_ + 2.0 * f2_) *
            spline(r_, f0_, f1_, f2_, f3_, f4_, f5_)
            )


#
# Plot the Spline part
if make_plots:
    plt.figure(figsize=(plot_fig_size_w, plot_fig_size_h))
    x = np.linspace(sp_1, sp_2, 1000)

    y = spline(x, f0, f1, f2, f3, f4, f5)
    plt.plot(x, y, label='Spline(r)')

    y = spline_dr(x, f0, f1, f2, f3, f4, f5)
    plt.plot(x, y, label=r'$\frac{d}{dr} Spline(r)$')

    y = spline_dr2(x, f0, f1, f2, f3, f4, f5)
    plt.plot(x, y, label=r'$\frac{d^2}{dr^2} Spline(r)$')

    plt.xlabel(r'Pair separation, $\AA$',
               fontweight='bold',
               size=16)
    plt.ylabel("Potential Energy, eV",
               fontweight='bold',
               size=16)

    plt.title("Spline pair potential for the " + str(atom1_name) + "-" + str(atom2_name) + " interaction",
              fontweight='bold',
              size=18)

    plt.ylim(-1000, 1000)  # set y range of y axis
    plt.xlim(0, 6)  # set x range of x axis
    plt.xticks(np.linspace(0, 6, 13))

    plt.legend(loc='upper right',
               fontsize=18,
               )
    plt.grid(True)

    # Save Spline plot
    plt.savefig(output_filename_prefac + 'Spline.png', format="png", dpi=plot_dpi)
    # plt.show()


# Composite plot value
if make_plots:
    plt.figure(figsize=(plot_fig_size_w, plot_fig_size_h))
    x = np.linspace(0.01, sp_1, 1000)
    y = ZBL(x, c1, c2, c3, c4, d1, d2, d3, d4, 0)
    plt.plot(x, y, label='ZBL(r)', color='red')

    x = np.linspace(sp_1, sp_2, 1000)
    y = ZBL(x, c1, c2, c3, c4, d1, d2, d3, d4, 0)
    plt.plot(x, y, label='ZBL(r)', color='red', linestyle='--')

    x = np.linspace(sp_1, sp_2, 1000)
    y = spline(x, f0, f1, f2, f3, f4, f5) - spline_offset
    plt.plot(x, y, label='Spline(r)', color='green')

    x = np.linspace(sp_2, 6, 1000)
    y = Buck(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2, 0)
    plt.plot(x, y, label='Buck(r)', color='blue')

    x = np.linspace(sp_1, sp_2, 1000)
    y = Buck(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2, 0)
    plt.plot(x, y, label='Buck(r)', color='blue', linestyle='--')

    plt.xlabel(r'Pair separation, $\AA$',
               fontweight='bold',
               size=16)
    plt.ylabel("Potential Energy, eV",
               fontweight='bold',
               size=16)

    plt.title("Composite ZBL-Spline-Buck pair potential \nfor the " +
              str(atom1_name) + "-" + str(atom2_name) + " interaction",
              fontweight='bold',
              size=18)

    plt.ylim(min(V1, V2) - 20 - spline_offset, max(V1, V2) + 50 - spline_offset)  # set y range of y axis
    plt.xlim(sp_1 - 0.2, sp_2 + .2)  # set x range of x axis

    plt.legend(loc='upper right',
               fontsize=18,
               )
    plt.grid(True)

    plt.savefig(output_filename_prefac + 'Composite_ZBL-Spline-Buck.png', format="png", dpi=plot_dpi)
    # plt.show()


# Composite plot derivative
if make_plots:
    plt.figure(figsize=(plot_fig_size_w, plot_fig_size_h))
    x = np.linspace(0.01, sp_1, 1000)
    y = ZBL_dr(x, c1, c2, c3, c4, d1, d2, d3, d4)
    plt.plot(x, y, label=r'$\frac{d}{dr} ZBL(r)$', color='red')

    x = np.linspace(sp_1, sp_2, 1000)
    y = ZBL_dr(x, c1, c2, c3, c4, d1, d2, d3, d4)
    plt.plot(x, y, label=r'$\frac{d}{dr} ZBL(r)$', color='red', linestyle='--')

    x = np.linspace(sp_1, sp_2, 1000)
    y = spline_dr(x, f0, f1, f2, f3, f4, f5)
    plt.plot(x, y, label=r'$\frac{d}{dr} Spline(r)$', color='green')

    x = np.linspace(sp_2, 6, 1000)
    y = Buck_dr(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)
    plt.plot(x, y, label=r'$\frac{d}{dr} Buck(r)$', color='blue')

    x = np.linspace(sp_1, sp_2, 1000)
    y = Buck_dr(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)
    plt.plot(x, y, label=r'$\frac{d}{dr} Buck(r)$', color='blue', linestyle='--')

    plt.xlabel(r'Pair separation, $\AA$',
               fontweight='bold',
               size=16)
    plt.ylabel("Potential Energy, eV",
               fontweight='bold',
               size=16)

    plt.title("Composite derivative ZBL-Spline-Buck pair potential \nfor the " +
              str(atom1_name) + "-" + str(atom2_name) + " interaction",
              fontweight='bold',
              size=18)

    plt.ylim(min(F1, F2) - 200, max(F1, F2) + 500)  # set y range of y axis
    plt.xlim(sp_1 - 0.2, sp_2 + .5)  # set x range of x axis

    plt.legend(loc='upper right',
               fontsize=18,
               )
    plt.grid(True)

    plt.savefig(output_filename_prefac + 'Composite_ZBL-Spline-Buck_derivative.png', format="png", dpi=plot_dpi)
    # plt.show()


# Composite plot second derivative
if make_plots:
    plt.figure(figsize=(plot_fig_size_w, plot_fig_size_h))
    x = np.linspace(0.01, sp_1, 1000)
    y = ZBL_dr2(x, c1, c2, c3, c4, d1, d2, d3, d4)
    plt.plot(x, y, label=r'$\frac{d^2}{dr^2} ZBL(r)$', color='red')

    x = np.linspace(sp_1, sp_2, 1000)
    y = ZBL_dr2(x, c1, c2, c3, c4, d1, d2, d3, d4)
    plt.plot(x, y, label=r'$\frac{d^2}{dr^2} ZBL(r)$', color='red', linestyle='--')

    x = np.linspace(sp_1, sp_2, 1000)
    y = spline_dr2(x, f0, f1, f2, f3, f4, f5)
    plt.plot(x, y, label=r'$\frac{d^2}{dr^2} Spline(r)$', color='green')

    x = np.linspace(sp_2, 6, 1000)
    y = Buck_dr2(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)
    plt.plot(x, y, label=r'$\frac{d^2}{dr^2} Buck(r)$', color='blue')

    x = np.linspace(sp_1, sp_2, 1000)
    y = Buck_dr2(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)
    plt.plot(x, y, label=r'$\frac{d^2}{dr^2} Buck(r)$', color='blue', linestyle='--')

    plt.xlabel(r'Pair separation, $\AA$',
               fontweight='bold',
               size=16)
    plt.ylabel("Potential Energy, eV",
               fontweight='bold',
               size=16)

    plt.title(r"Composite 2$^{nd}$ derivative ZBL-Spline-Buck pair potential" + "\nfor the " +
              str(atom1_name) + "-" + str(atom2_name) + " interaction",
              fontweight='bold',
              size=18)

    plt.ylim(min(G1, G2) - 1000, max(G1, G2) + 2000)  # set y range of y axis
    plt.xlim(sp_1 - 0.2, sp_2 + .5)  # set x range of x axis

    plt.legend(loc='upper right',
               fontsize=18,
               )
    plt.grid(True)

    plt.savefig(output_filename_prefac + 'Composite_ZBL-Spline-Buck_second_derivative.png', format="png", dpi=plot_dpi)
    # plt.show()


# Coulomb
def coulomb(r_, atom1_q_, atom2_q_, e2_):
    return (atom1_q_ * atom2_q_ * e2_) / r_


# Coulomb derivative
def coulomb_dr(r_, atom1_q_, atom2_q_, e2_):
    return -(atom1_q_ * atom2_q_ * e2_) / r_**2


# Tabulate
file = open('tabulated_potl.txt', 'w+')

file.write("# DATE: " +
           datetime.datetime.now().strftime("%Y") + "-" +
           datetime.datetime.now().strftime("%m") + "-" +
           datetime.datetime.now().strftime("%d") + "  UNITS: metal  CONTRIBUTOR: Kenny Jolley \n")
file.write("# Tabulated ZBL-Spline-Buck potential written by zbl_buck_spline_fitter.py \n")
file.write("# Coulomb term not included since the table is intended to be used with coul/long  ewald solver \n")
file.write("# " + str(atom1_name) + "-" + str(atom2_name) + " interaction\n")
file.write("# Charges: " + str(atom1_name) + "=" + str(atom1_Q) + " and " + str(atom2_name) + "=" + str(atom2_Q) + "\n")
file.write("# Buck Params: A=" + str(buck_A) + " rho=" + str(buck_rho) + " C=" + str(buck_C) + "\n")
file.write("# Spline function between " + str(sp_1) + " and " + str(sp_2) + " Angstroms, with " + str(spline_offset) +
           " eV offset\n")
file.write("# Spline function parameters: \n" +
           "# f0 =%25.15f" % f0 + "\n" +
           "# f1 =%25.15f" % f1 + "\n" +
           "# f2 =%25.15f" % f2 + "\n" +
           "# f3 =%25.15f" % f3 + "\n" +
           "# f4 =%25.15f" % f4 + "\n" +
           "# f5 =%25.15f" % f5 + "\n")

# potential name
file.write("\n" + str(atom1_name) + "-" + str(atom2_name) + "_interaction\n")

# table setup
tab_step = 0.001
tab_min = 0.2
tab_max = 12.0
tab_points = int(((tab_max - tab_min) / tab_step) + 0.5) + 1

file.write("N " + str(tab_points) + " R " + str(tab_min) + '  ' + str(tab_max) + "\n\n")

for i in range(tab_points):
    r = float(tab_min + i * tab_step)
    if r < sp_1:
        tab_e = ZBL(r, c1, c2, c3, c4, d1, d2, d3, d4, 0) - coulomb(r, atom1_Q, atom2_Q, E2)
        tab_f = -ZBL_dr(r, c1, c2, c3, c4, d1, d2, d3, d4) + coulomb_dr(r, atom1_Q, atom2_Q, E2)
    elif r < sp_2:
        tab_e = spline(r, f0, f1, f2, f3, f4, f5) - spline_offset - coulomb(r, atom1_Q, atom2_Q, E2)
        tab_f = -spline_dr(r, f0, f1, f2, f3, f4, f5) + coulomb_dr(r, atom1_Q, atom2_Q, E2)
    else:
        tab_e = Buck(r, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2, 0) - coulomb(r, atom1_Q, atom2_Q, E2)
        tab_f = -Buck_dr(r, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2) + coulomb_dr(r, atom1_Q, atom2_Q, E2)

    file.write(str('%10d' % (i + 1)) +
               str('%10.4f' % r) +
               str('%30.15f' % tab_e) +
               str('%30.15f' % tab_f) + '\n')
