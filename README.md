# Optimization methods for VLSI
Very large-scale integration (VLSI) is the process of creating an integrated circuit (IC) by integrating circuits into silicon chips.  With the possibility of shrinking more and more the transistor sizes, the need to pack them in smaller areas has grown accordingly. For this reason, developing smart methods for spacial arrangements of the different components on the chips has become crucial for developing modern devices. The aim of this project is to develop optimization strategies (using established technologies), that given a fixed plate-width and a list of rectangular circuits, is able to place them on the plate so that the lengthof the final device is minimized.


![copertina](https://user-images.githubusercontent.com/51266633/131223053-c139dd1d-6ae5-47d4-b78d-9ad40505dcb9.png)



## 1. Requirements

The following libraries are needed:
- minizinc (for executing the CP solver directly from a python API)
- z3-solver (for executing SAT and SMT solvers)
- matplotlib (for the plotting of the solutions and statistics)
- numpy (for handling arrays handly before plotting)

The project has been tested with the following versions:
- python 3.8.5
- minizinc 0.4.2
- z3-solver 4.8.12.0
- matplotlib 3.4.3
- numpy 1.21.2

## 2. Usage

All the solvers are run in the same way by executing `python main.py`, which by default runs the 40 instances present in the folder `res/instances/` one after another using the solver stated by the argument `--solver`.
The instances can be run with the following arguments:

- `-P, --plot`                                          Plots the solution after its computation
- `-X, --stats`                                         Disables automatic plot display of the instances times at the end of execution
- `-A, --average`                                       Solves each instance 5 times and computes an average of the tries
- `-T TIMEOUT, --timeout TIMEOUT`                       Timeout for the execution of the solvers in seconds (default: 300)
- `-R, --rotation`                                      Enables rotation mode (disabled by default)
- `-S {null,cp,sat,smt}, --solver {null,cp,sat,smt}`    Select solver used for execution
- `-I INSTANCES, --instances INSTANCES`                 Instances to be solved. Can be a directory, a file or `all`, which searches by default for the files from ins-0.txt to ins-40.txt in the path `res/instances` (default: `all`)
- `-O OUTPUT, --output OUTPUT`                          Output directory of the files containing the solutions
