from argparse import ArgumentParser
from lib.solver import solve_cp
from lib.utils import load_instance, load_solution, plot_result, write_solution
import time

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-S", "--solver", default=None, help="", choices=[None, "cp"])
    parser.add_argument('-P', '--plot', help="", default=False, action='store_true')
    args = parser.parse_args()

    problems = [0, 1, 2, 8]
    inputs = ["res/instances/ins-{0}.txt".format(i) for i in problems]
    outputs = ["res/solutions/out-{0}.txt".format(i) for i in problems]

    solutions = []
    for input, output in zip(inputs, outputs):
        instance = load_instance(input)
        if args.solver is None:
            solutions = load_solution(output)
        else:
            start_time = time.time()
            if args.solver == "cp": 
                sol = solve_cp("solver/naive.mzn", instance)
            if args.solver == "sat": 
                pass
            execution_time = time.time() - start_time
            print("Problem {0} solved in {1}ms".format(input, round(execution_time * 1000, 4)))
            
            write_solution(output, sol)
            solutions.append(sol)
    
    if args.plot:
        for sol, out in zip(solutions, outputs):
            plate, circuits_pos = sol
            plot_result(plate, circuits_pos)
