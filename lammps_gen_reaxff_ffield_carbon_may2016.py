#!/usr/bin/env python

# This function simply generates the ffield file for the May 2016 version
# of the reaxff potential in the current directory.

# verbose = True  , prints some comments to the screen.
# forced  = True  , will overwrite the existing file (if it exists).
# forced  = False , if ffield exists, will ask the user if the existing file should be overwritten.

# Kenny Jolley, Dec 2018

import sys
import os

def lammps_gen_reaxff_ffield_carbon_may2016(**kwargs):
    
    # Read keyword arguments (defaults are False)
    verbose = kwargs.get('verbose', False)
    forced = kwargs.get('forced', False)

    if(verbose):
        print("  +---------------------------------------------------+")
        print("  |  Generate May 2016 version of reaxff ffield file  |")
        print("  +---------------------------------------------------+\n")

    # Set generate file flag to true
    gen_file = True

    # Check for existing file, and ask user if it should be overwritten
    if(not forced):
        # Check if ffield exists
        if(os.path.isfile('ffield')):
            print("> Existing file (ffield) detected.")
            print("> lammps_gen_reaxff_ffield_carbon_may2016 function wants to overwrite this file")
    
            # Ask user if file should be overwritten (python 2/3 handling)
            if sys.version_info[0] < 3:
                user_choice = raw_input('Do you wish to overwrite the existing file? (y/n): ')
            else:
                user_choice = input('Do you wish to overwrite the existing file? (y/n): ')
            
            user_choice = user_choice.lower()
            
            if ((user_choice == 'yes') or (user_choice == 'y') or (user_choice == 'yea') ):
                print(" > Overwriting existing file ... ")
                gen_file = True
            else:
                print( "File not overwritten, exiting function")
                gen_file = False

    # If we are allowed to generate the file, then write the ffield file to current directory
    if(gen_file):
        outputfile = open("ffield", 'w')

        # Write ffield file
        outputfile.write("""Reactive MD-force field: revised C-2013, May 2016
 39       ! Number of general parameters
   50.0000 !Overcoordination parameter
    9.5469 !Overcoordination parameter
   26.5405 !Valency angle conjugation parameter
   -0.8370 !Triple bond stabilisation parameter
    4.3243 !Triple bond stabilisation parameter
   70.0000 !C2-correction
    1.0588 !Undercoordination parameter
    4.6000 !Triple bond stabilisation parameter
   12.1176 !Undercoordination parameter
   13.3056 !Undercoordination parameter
  -69.4358 !Triple bond stabilization energy
    0.0000 !Lower Taper-radius
   10.0000 !Upper Taper-radius
    2.8793 !Not used
   33.8667 !Valency undercoordination
    6.0891 !Valency angle/lone pair parameter
    1.0563 !Valency angle
    2.0384 !Valency angle parameter
    6.1431 !Not used
    6.9290 !Double bond/angle parameter
    0.3989 !Double bond/angle parameter: overcoord
    3.9954 !Double bond/angle parameter: overcoord
   -2.4837 !Not used
    5.7796 !Torsion/BO parameter
   10.0000 !Torsion overcoordination
    1.9487 !Torsion overcoordination
   -1.2327 !Conjugation 0 (not used)
    2.1645 !Conjugation
    1.5591 !vdWaals shielding
    0.1000 !Cutoff for bond order (*100)
    2.1365 !Valency angle conjugation parameter
    0.6991 !Overcoordination parameter
   50.0000 !Overcoordination parameter
    1.8512 !Valency/lone pair parameter
    0.5000 !Not used
   20.0000 !Not used
    5.0000 !Molecular energy (not used)
    0.0000 !Molecular energy (not used)
    2.6962 !Valency angle conjugation parameter
 4    ! Nr of atoms; cov.r; valency;a.m;Rvdw;Evdw;gammaEEM;cov.r2;#
           alfa;gammavdW;valency;Eunder;Eover;chiEEM;etaEEM;n.u.
           cov r3;Elp;Heat inc.;n.u.;n.u.;n.u.;n.u.
           ov/un;val1;n.u.;val3,vval4
C    1.3651   4.0000  12.0000   2.0346   0.1659   0.8485   1.1386   4.0000
     9.1849   1.5000   4.0000  37.4375  79.5548   4.8446   7.0000   0.0000
     1.0860   0.0000 181.0000  16.3532  26.3722   4.9538   0.8563   0.0000
    -5.1769   2.8877   1.0564   4.0000   2.9663   0.0000   0.0000   0.0000
H    0.8930   1.0000   1.0080   1.3550   0.0930   0.8203  -0.1000   1.0000
     8.2230  33.2894   1.0000   0.0000 121.1250   3.7248   9.6093   1.0000
    -0.1000   0.0000  61.6606   3.0408   2.4197   0.0003   1.0698   0.0000
   -19.4571   4.2733   1.0338   1.0000   2.8793   0.0000   0.0000   0.0000
O    1.2450   2.0000  15.9990   2.3890   0.1000   1.0898   1.0548   6.0000
     9.7300  13.8449   4.0000  37.5000 116.0768   8.5000   8.3122   2.0000
     0.9049   0.4056  59.0626   3.5027   0.7640   0.0021   0.9745   0.0000
    -3.5500   2.9000   1.0493   4.0000   2.9225   0.0000   0.0000   0.0000
X   -0.1000   2.0000   1.0080   2.0000   0.0000   0.0100  -0.1000   6.0000
    10.0000   2.5000   4.0000   0.0000   0.0000   5.0000 9999.9999   0.0000
    -0.1000   0.0000  -2.3700   8.7410  13.3640   0.6690   0.9745   0.0000
   -11.0000   2.7466   1.0338   2.0000   2.8793   0.0000   0.0000   0.0000
 6      ! Nr of bonds; Edis1;LPpen;n.u.;pbe1;pbo5;13corr;pbo6
                        pbe2;pbo3;pbo4;n.u.;pbo1;pbo2;ovcorr
 1  1  86.2088 133.9104  27.9063   0.5462  -0.4603   1.0000  34.9951   0.9667
        6.1765  -0.1546   7.9966   1.0000  -0.0613   7.8101   1.0000   0.0000
 1  2 188.8143   0.0000   0.0000  -0.4501   0.0000   1.0000   6.0000   0.5839
       12.0338   1.0000   0.0000   1.0000  -0.0775   6.1485   0.0000   0.0000
 2  2 153.3934   0.0000   0.0000  -0.4600   0.0000   1.0000   6.0000   0.7300
        6.2500   1.0000   0.0000   1.0000  -0.0790   6.0552   0.0000   0.0000
 1  3 163.3110  83.9973  54.4316  -0.5220  -0.3123   1.0000  10.2503   1.0000
        0.3553  -0.3757   7.0000   1.0000  -0.1331   4.6021   0.0000   0.0000
 2  3 160.0000   0.0000   0.0000  -0.5725   0.0000   1.0000   6.0000   0.5626
        1.1150   1.0000   0.0000   0.0000  -0.0920   4.2790   0.0000   0.0000
 3  3 142.2858 145.0000  50.8293   0.2506  -0.1000   1.0000  29.7503   0.6051
        0.3451  -0.1055   9.0000   1.0000  -0.1225   5.5000   1.0000   0.0000
 3    ! Nr of off-diagonal terms; Ediss;Ro;gamma;rsigma;rpi;rpi2
 1  2   0.1200   1.3861   9.8561   1.1254  -1.0000  -1.0000
 1  3   0.1347   1.8343   9.7934   1.3139   1.1498   1.1039
 2  3   0.0283   1.2885  10.9190   0.9215  -1.0000  -1.0000
18    ! Nr of angles;at1;at2;at3;Thetao,o;ka;kb;pv1;pv2
 1  1  1  71.4046  20.3586   2.6552   0.0000   0.0197  10.9275   1.1161
 1  1  2  67.7204  20.0371   3.1168   0.0000   1.2399   0.0000   1.0010
 2  1  2  71.1440  23.5562   4.7193   0.0000   0.0716   0.0000   2.5936
 1  1  3  15.7798   9.0805   4.0304   0.0000   1.8785  70.0000   1.1737
 2  1  3  65.0000  13.4505   1.8249   0.0000   1.5646   0.0000   1.2173
 3  1  3  74.7266  45.0000   1.8020 -16.7178   2.6091   0.1000   2.3556
 1  2  2   0.0000   0.0000   6.0000   0.0000   0.0000   0.0000   1.0400
 1  2  1   0.0000   7.5000   5.0000   0.0000   0.0000   0.0000   1.0400
 1  2  3   0.0000  45.0000   3.0000   0.0000   1.0000   0.0000   1.0400
 2  2  2   0.0000  27.9213   5.8635   0.0000   0.0000   0.0000   1.0400
 2  2  3   0.0000   8.5744   3.0000   0.0000   0.0000   0.0000   1.0421
 3  2  3   0.0000  15.0000   2.8900   0.0000   0.0000   0.0000   2.8774
 1  3  1  76.7840  44.2266   0.9343   0.0000   1.3483   0.0000   1.8301
 1  3  3  63.9120  17.1680   0.8751   0.0000   0.0693  50.9415   3.0000
 1  3  2  79.6413  28.6488   0.3789   0.0000   1.6776   0.0000   1.0010
 2  3  2  85.8000   9.8453   2.2720   0.0000   2.8635   0.0000   1.5800
 2  3  3  79.5453  45.0000   2.1630   0.0000   3.0000   0.0000   1.2391
 3  3  3  80.7324  30.4554   0.9953   0.0000   1.6310  50.0000   1.0783
26    ! Nr of torsions;at1;at2;at3;at4;;V1;V2;V3;V2(BO);vconj;n.u;n
 1  1  1  1   1.7987  80.0000   0.2100  -8.6369  -2.1145   0.0000   0.0000
 1  1  1  2   1.5816  36.2452   0.3067  -5.3163  -1.0125   0.0000   0.0000
 2  1  1  2   1.5695  28.0133   0.5199  -4.0658  -1.1500   0.0000   0.0000
 1  1  1  3   0.9963  17.2365   0.1491  -2.5000  -1.0000   0.0000   0.0000
 2  1  1  3   1.5159  28.6602   0.7169  -7.5489  -3.0000   0.0000   0.0000
 3  1  1  3  -0.2000  23.6540  -1.0000  -5.9155  -1.1552   0.0000   0.0000
 1  1  3  1   1.8231  46.5696  -1.0000  -3.0536  -3.0000   0.0000   0.0000
 1  1  3  2   1.4836  80.0000   0.0363  -4.7349  -1.0000   0.0000   0.0000
 2  1  3  1   0.5983  49.5033   0.7210  -3.4046  -1.6880   0.0000   0.0000
 2  1  3  2  -0.2000  76.3511   1.0000  -4.0709  -1.0000   0.0000   0.0000
 1  1  3  3  -0.2000   5.0000  -1.0000  -3.6523  -2.9000   0.0000   0.0000
 2  1  3  3   2.5000  80.0000   1.0000  -2.6071  -3.0000   0.0000   0.0000
 3  1  3  1  -0.2000  80.0000  -1.0000  -3.6863  -3.0000   0.0000   0.0000
 3  1  3  2   2.5000  38.8954  -0.8368  -4.6681  -2.9000   0.0000   0.0000
 3  1  3  3  -0.2000  78.1766   0.0250  -2.8895  -3.0000   0.0000   0.0000
 1  3  3  1   2.5000   0.1000   1.0000  -2.6905  -2.7573   0.0000   0.0000
 1  3  3  2   0.5241  69.2788  -1.0000  -4.4539  -2.8081   0.0000   0.0000
 2  3  3  2   2.5000   0.1000  -0.4869  -2.8372  -1.0000   0.0000   0.0000
 1  3  3  3   2.5000   0.1000   1.0000  -3.4298  -1.0000   0.0000   0.0000
 2  3  3  3  -0.2000   0.1000  -1.0000  -3.5698  -1.0000   0.0000   0.0000
 3  3  3  3  -0.2000   0.1000   1.0000  -3.8409  -1.0000   0.0000   0.0000
 0  1  2  0   0.0000   0.0000   0.0000   0.0000   0.0000   0.0000   0.0000
 0  2  2  0   0.0000   0.0000   0.0000   0.0000   0.0000   0.0000   0.0000
 0  2  3  0   0.0000   0.1000   0.0200  -2.5415   0.0000   0.0000   0.0000
 0  1  1  0   0.0000  50.0000   0.3000  -4.0000  -2.0000   0.0000   0.0000
 0  3  3  0   0.5511  25.4150   1.1330  -5.1903  -1.0000   0.0000   0.0000
 1    ! Nr of hydrogen bonds;at1;at2;at3;Rhb;Dehb;vhb1
 3  2  3   2.1200  -3.5800   1.4500  19.5000
""")


# If we are running this script interactively, call the function safely
if __name__ == '__main__':
    lammps_gen_reaxff_ffield_carbon_may2016(verbose=True,forced=False)

