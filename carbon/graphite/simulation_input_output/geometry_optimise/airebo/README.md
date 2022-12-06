## Geometry optimisation of graphite using the AIREBO potential

To run this simulation you need three files:
- `lammps_airebo_minimize.IN` - The lammps input script [here](lammps_airebo_minimize.IN).
- `lammps.lattice.dat`  - with the C mass defined as generated by the [lammps_gen_graphite_airebo.py](../../../scripts/lammps_gen_graphite_airebo.py) script from the [scripts](../../../scripts) folder.
- `CH.airebo` - from the lammps documentation or [here](../../../../potentials).

Run the simulation by calling lammps and directing the input and output accordingly:  
`lmp < lammps_airebo_minimize.IN > output.txt`

Replace `lmp` with the name of your executable for lammps.  The simulation should also work fine in parallel.  
`mpirun -n 4 lmp < lammps_airebo_minimize.IN > output.txt`

The simulation here is a simple geometry optimisation using the conjugate gradient `'cg'` method.  
Only the conjugate gradient `'cg'` and steepest descent `'sd'` methods will work when the  `fix box/relax` command is used to vary the size of the simulation cell.

The initial structure is a periodic graphite cell consisting of  3x5x2 Unit cells, with ab stacking. The initial lattice `a` parameter is 2.4175 and initial `c` parameter is 3.358.

Table summarises the simulation results of this run (top row) and some other similar runs with different lattice sizes.

| Unit Cells (x,y,z) | Stacking |No. atoms | Initial Box size, Anstroms (x,y,z) | Final Box size, Anstroms (x,y,z) | Optimised `a` lattice param | Optimised `c` lattice param |
|------------|-----------|-----|-----|----------|----------|----------|
|  **3x5x2** |  **AB**  | **240**       | **12.561698481893282 x 12.0875 x 13.432**  | **12.561756  x 12.087555  x 13.431989**  |  **2.417511**   |   **3.35799725**  |
|   5x8x3  |  AB  | 960  | 20.936164136488806 x 19.34 x 20.148 |   20.93626  x  19.340088 x   20.147984 | 2.417511  |  3.357997333 |
