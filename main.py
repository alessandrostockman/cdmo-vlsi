from argparse import ArgumentParser
import os
import time

from cp.src.solver import solve_cp
from sat.src.solver import solve_sat
from lib.utils import load_instance, load_solution, plot_result, write_solution

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-S", "--solver", default="null", help="", choices=["null", "cp", "sat"])
    parser.add_argument('-P', '--plot', help="", default=False, action='store_true')
    parser.add_argument('-I', '--instances', help="", default="res/instances")
    parser.add_argument('-O', '--output', help="", default="res/solutions")
    args = parser.parse_args()

    if os.path.isdir(args.instances):
        inputs = sorted([os.path.join(args.instances, i) for i in os.listdir(args.instances) if os.path.isfile(os.path.join(args.instances, i))])
    elif os.path.isfile(args.instances):
        inputs = [args.instances]
    elif args.instances == "all":
        inputs = ["res/instances/ins-{0}.txt".format(i) for i in range(41)]

    solutions = []
    for input in inputs:
        filename = os.path.basename(input)
        output = os.path.join(args.output, filename)
        if 'ins' in filename:
            output = output.replace('ins', 'out')

        instance = load_instance(input)
        if args.solver == "null":
            if not os.path.isfile(output):
                continue
            sol = load_solution(output)
        else:
            timeout = 4
            if args.solver == "cp": 
                sol, execution_time = solve_cp("cp/src/solver.mzn", instance, timeout)
            if args.solver == "sat": 
                sol, execution_time = solve_sat(instance, timeout)
            print("Problem {0} solved in {1}ms".format(input, round(execution_time, 4)))
            
            write_solution(output, sol)
        
        solutions.append((sol, input))
    
    if args.plot:
        for sol, title in solutions:
            plate, circuits_pos = sol
            plot_result(plate, circuits_pos, title)
