from argparse import ArgumentParser
from lib.solver import solve_cp
from lib.utils import load_instance, load_solution, plot_result, write_solution
import time

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-S", "--solver", default=None, help="", choices=[None, "cp"])
    parser.add_argument('-P', '--plot', dest="plot", help="", default=False, action='store_true')
    args = parser.parse_args()

    inputs = ["res/instances/ins-{0}.txt".format(i) for i in [0, 1, 2, 8]]
    outputs = ["res/solutions/out-{0}.txt".format(i) for i in [0, 1, 2, 8]]

    instances = [load_instance(i) for i in inputs]
    
    start_time = time.time()
    solutions = solve_cp("solver/naive.mzn", instances)
    execution_time = time.time() - start_time
    
    for sol, out in zip(solutions, outputs):
        write_solution(out, sol)
        plate, circuits_pos = sol

        if args.plot:
            plot_result(plate, circuits_pos)
    print("Execution finished in " + str(execution_time) + "s")
