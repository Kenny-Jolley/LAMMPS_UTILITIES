/*----------------------------------------------------------------------
  PuReMD - Purdue ReaxFF Molecular Dynamics Program

  Copyright (2010) Purdue University
  Hasan Metin Aktulga, hmaktulga@lbl.gov
  Joseph Fogarty, jcfogart@mail.usf.edu
  Sagar Pandit, pandit@usf.edu
  Ananth Y Grama, ayg@cs.purdue.edu

  Please cite the related publication:
  H. M. Aktulga, J. C. Fogarty, S. A. Pandit, A. Y. Grama,
  "Parallel Reactive Molecular Dynamics: Numerical Methods and
  Algorithmic Techniques", Parallel Computing, in press.

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License as
  published by the Free Software Foundation; either version 2 of
  the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  See the GNU General Public License for more details:
  <http://www.gnu.org/licenses/>.
  
  
  Modified to include a hard coded spline to ZBL at short range 
  for pure carbon systems.
  Kenny Jolley  Jan 2017
  kenny.jolley@gmail.com
  
  Work in progress
  
  ----------------------------------------------------------------------*/

#ifndef __NONBONDED_H_
#define __NONBONDED_H_

#include "reaxc_types.h"

// ZBL constants  pre-compute for C-C
//#define ZBL_ACONST  0.88534
//#define ZBL_ABOHR   0.530
//#define ZBL_POW     0.23
//#define ZC_         6.0
//#define ZBL_A  ZBL_ACONST * ABOHR / ( ZC_ ** ZBL_POW + ZC_ ** ZBL_POW )
#define ZBL_A_CC       0.15537501107375

//#define E2B4PE      2.3070796E-28
//#define ZBL_E       1.60217733E-19
//#define ZBL_E2 = E2B4PE / ( 1E-10_PREC * ZBL_E )
#define ZBL_E2     14.3996520035644

//#define CCONST = ZC_ * ZC_ * ZBL_E2
#define ZBL_CCONST_CC    518.387472128319

// Spline parameters for the Carbon-Carbon interaction
// C_ - C_  (0.25 - 0.95) [kcal/mol]

#define FF1CC    13.64101441
#define FF2CC   -33.50452187
#define FF3CC   111.2579538
#define FF4CC  -217.9935929
#define FF5CC   191.6995812
#define FF6CC   -60.77223097
#define AC_C_     0.25
#define BC_C_     1.0


                                      
                                         


void vdW_Coulomb_Energy( reax_system*, control_params*, simulation_data*,
                         storage*, reax_list**, output_controls* );

void Tabulated_vdW_Coulomb_Energy( reax_system*, control_params*,
                                   simulation_data*, storage*,
                                   reax_list**, output_controls* );

void Compute_Polarization_Energy( reax_system*, simulation_data* );

void LR_vdW_Coulomb( reax_system*, storage*, control_params*,
                int, int, double, LR_data* );
#endif
