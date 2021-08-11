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
    parser.add_argument('-X', '--stats', help="", default=False, action='store_true')
    parser.add_argument('-A', '--average', help="", default=False, action='store_true')
    parser.add_argument('-I', '--instances', help="", default="res/instances")
    parser.add_argument('-O', '--output', help="", default="res/solutions")
    parser.add_argument('-T', '--timeout', help="", default=5*60)
    args = parser.parse_args()

    if os.path.isdir(args.instances):
        inputs = sorted([os.path.join(args.instances, i) for i in os.listdir(args.instances) if os.path.isfile(os.path.join(args.instances, i))])
    elif os.path.isfile(args.instances):
        inputs = [args.instances]
    elif args.instances == "all":
        inputs = ["res/instances/ins-{0}.txt".format(i) for i in range(41)]

    solutions = []
    stats_times = []
    
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
            first = True
            times = []
            sol = None
            execution_time = None
            while first or args.average and len(times) < 10:
                first = False
                if args.solver == "cp": 
                    sol, execution_time = solve_cp("cp/src/solver.mzn", instance, int(args.timeout))
                if args.solver == "sat": 
                    sol, execution_time = solve_sat(instance, int(args.timeout))

                if sol is not None:
                    times.append(execution_time)
                    if not args.average:
                        print("Problem {0} solved in {1}s".format(input, round(execution_time, 4)))
                else:
                    print("Problem {0} not solved".format(input))
            
            if sol is not None:
                if args.average:
                    avg_time = sum(times) / len(times)
                    print("Problem {0} solved in an average of {1}s".format(input, round(avg_time, 4)))
                    stats_times.append(avg_time)
                else:
                    stats_times.append(execution_time)
                write_solution(output, sol)
        
        solutions.append((sol, input))

    if args.plot:
        for sol, title in solutions:
            plate, circuits_pos = sol
            plot_result(plate, circuits_pos, title)
