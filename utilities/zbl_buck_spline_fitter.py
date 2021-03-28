#!/usr/bin/env python

# This script plots the ZBL and buckingham potential for given parameters and calculates
# a spline function that joins them together.


#    Kenny Jolley, March 2021

# imported modules
import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt

from sympy.core.symbol import symbols
from sympy.solvers.solveset import nonlinsolve
from sympy.polys.polytools import is_zero_dimensional

# --------------------------------------------
# Configurable variables
# --------------------------------------------

# atom 1
atom1_name = "B"
atom1_Z = 5  # number of protons
atom1_Q = 1.4175  # electric charge

# atom 2
atom2_name = "B"
atom2_Z = 5  # number of protons
atom2_Q = 1.4175  # electric charge

# Buckingham Potential Parameters
buck_A = 121.1
buck_rho = 0.49
buck_C = 0.0

# Spline offset (preferred to be zero, but sometimes we need to ensure spline points are not negative)
spline_offset = 0
sp_1 = 0.35
sp_2 = 0.65

# --------------------------------------------


# Constants
q = 1.60217646e-19
epsilon = 8.854187817e-12

E = (q * q / (4 * math.pi * epsilon))
E2 = E / (q * 1e-10)

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
plt.figure(figsize=(9, 6))
x = np.linspace(0.01, 6, 1000)
y = ZBL(x, c1, c2, c3, c4, d1, d2, d3, d4, spline_offset)
plt.plot(x, y, label='ZBL(r)')

y = ZBL_dr(x, c1, c2, c3, c4, d1, d2, d3, d4)
plt.plot(x, y, label=r'$\frac{d}{dr} ZBL(r)$')

y = ZBL_dr2(x, c1, c2, c3, c4, d1, d2, d3, d4)
plt.plot(x, y, label=r'$\frac{d^2}{dr^2} ZBL(r)$')

plt.xlabel(r'Pair separation, $\AA$',
           fontweight='bold',
           size=16)
plt.ylabel("Potential Energy, eV",
           fontweight='bold', )

plt.title("ZBL pair potential for the " + str(atom1_name) + "-" + str(atom1_name) + " interaction",
          fontweight='bold',
          size=18)

plt.ylim(-1000, 1000)  # set y range of y axis
plt.xlim(0, 6)  # set x range of x axis
plt.xticks(np.linspace(0, 6, 13))

plt.legend(loc='upper right',
           fontsize=18,
           )
plt.grid(True)


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
plt.figure(figsize=(9, 6))
x = np.linspace(0.01, 6, 1000)
y = Buck(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2, spline_offset)
plt.plot(x, y, label='Buck(r)')

y = Buck_dr(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)
plt.plot(x, y, label=r'$\frac{d}{dr} Buck(r)$')

y = Buck_dr2(x, buck_A, buck_rho, buck_C, atom1_Q, atom2_Q, E2)
plt.plot(x, y, label=r'$\frac{d^2}{dr^2} Buck(r)$')

plt.xlabel(r'Pair separation, $\AA$',
           fontweight='bold',
           size=16)
plt.ylabel("Potential Energy, eV",
           fontweight='bold', )

plt.title("Buck pair potential for the " + str(atom1_name) + "-" + str(atom1_name) + " interaction",
          fontweight='bold',
          size=18)

plt.ylim(-1000, 1000)  # set y range of y axis
plt.xlim(0, 6)  # set x range of x axis
plt.xticks(np.linspace(0, 6, 13))

plt.legend(loc='upper right',
           fontsize=18,
           )
plt.grid(True)

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
print(is_zero_dimensional(system))

the_solution = nonlinsolve(system, [f0, f1, f2, f3, f4, f5])
print("The full solution: ")
print(the_solution)

f0 = the_solution.args[0][0]
f1 = the_solution.args[0][1]
f2 = the_solution.args[0][2]
f3 = the_solution.args[0][3]
f4 = the_solution.args[0][4]
f5 = the_solution.args[0][5]

print("f0: ", f0)
print("f1: ", f1)
print("f2: ", f2)
print("f3: ", f3)
print("f4: ", f4)
print("f5: ", f5)


# Spline equations
# Spline
def Spline(r, f0, f1, f2, f3, f4, f5):
    return np.exp(f0 + f1 * r + f2 * r ** 2 + f3 * r ** 3 + f4 * r ** 4 + f5 * r ** 5)

# todo complete derivatives
# Spline - first derivative
def Spline_dr(r, f0, f1, f2, f3, f4, f5):
    return 0


# Spline - second derivative
def Spline_dr2(r, f0, f1, f2, f3, f4, f5):
    return 0


# Tabulate
# todo output plots and tables






