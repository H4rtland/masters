### Week 1
#### October 23rd-29th 2017

Access HEP cluster

    ssh -Y thartland@lapa.lancs.ac.uk

Have some example data sets and example analysis scripts to test if ROOT is working.
Works well on the cluster, not on my laptop.
Laptop has errors linking the include files / libraries so I'll use the remote machine from now on.

First example reads in pairs of decay product four vectors and calculates Z boson masses.
The data file is z.dat. It is read by z_read.cpp, which is compiled with the command:

    g++ -o z_read z_read.cpp
    
The Z boson masses are written to z.out.

