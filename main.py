from ctypes import ArgumentError
import os
from cp.src.solver import SolverCP
from sat.src.solver import SolverSAT
from smt.src.solver import SolverSMT

from lib.utils import load_solution, plot_global_statistics, plot_result, solve_and_write, parse_arguments

if __name__ == "__main__":
    args = parse_arguments(main=True)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if args.bar:
        plot_global_statistics(base_dir)
        exit()

    if os.path.isdir(args.instances):
        inputs = sorted([os.path.join(args.instances, i) for i in os.listdir(args.instances) if os.path.isfile(os.path.join(args.instances, i))])
    elif os.path.isfile(args.instances):
        inputs = [args.instances]
    elif args.instances == "all":
        inputs = ["res/instances/ins-{0}.txt".format(i) for i in range(41)]
    else:
        inputs = [args.instances]

    solver_dir = os.path.join(base_dir, args.solver)

    if args.solver == "cp": 
        solver = SolverCP(int(args.timeout), rotation=args.rotation, solver_dir=solver_dir)
    elif args.solver == "sat": 
        solver = SolverSAT(int(args.timeout), rotation=args.rotation) 
    elif args.solver == "smt": 
        solver = SolverSMT(int(args.timeout), rotation=args.rotation)
    elif args.plot:    
        output_dir = os.path.join(base_dir, args.output)
        for input in inputs:
            filename = os.path.basename(os.path.join(base_dir, input))
            output = os.path.join(output_dir, filename)
            if 'ins' in filename:
                output = output.replace('ins', 'out')
            plate, circuits_pos = load_solution(output)

            if plate is not None and circuits_pos is not None:
                plot_result(plate, circuits_pos, filename)
        exit()
    else:
        raise ArgumentError("Either choose a solver or ask for plots")

    solve_and_write(solver, base_dir, solver_dir, inputs, average=args.average, stats=args.stats, plot=args.plot)    

