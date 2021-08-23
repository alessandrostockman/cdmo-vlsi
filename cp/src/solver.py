import datetime
from minizinc import Instance, Model, Solver, Status
import os

class SolverCP:

    def __init__(self, timeout=300, rotation=False, solver_dir=None):
        self.timeout = timeout
        self.rotation = rotation
        self.solver_dir = os.path.join(solver_dir, "src")

    def solve(self, data):
        solver_file = os.path.join(self.solver_dir, "solver.mzn") if not self.rotation else os.path.join(self.solver_dir, "solver_rotation")
        model = Model(solver_file)
        gecode = Solver.lookup("gecode")

        plate_width, circuits = data
        instance = Instance(gecode, model)
        instance["num_circuits"] = len(circuits)
        instance["plate_width"] = plate_width

        w, h = ([ i for i, _ in circuits ], [ j for _, j in circuits ])
        instance["widths"] = w
        instance["heights"] = h

        result = instance.solve(timeout=datetime.timedelta(seconds=self.timeout))

        if result.status is Status.OPTIMAL_SOLUTION:
            if self.rotation:
                circuits_pos = [(w, h, x, y) if not r else (h, w, x, y) for (w, h), x, y, r in zip(circuits, result["x"], result["y"], result["r"])]
            else:
                circuits_pos = [(w, h, x, y) for (w, h), x, y in zip(circuits, result["x"], result["y"])]
            plate_height = result.objective

            return ((plate_width, plate_height), circuits_pos), result.statistics['time'].total_seconds()
        else:
            return None, 0


if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    solver_dir = os.path.join(base_dir, "cp")
    sys.path.append(base_dir)
    from lib.utils import solve_and_write, parse_arguments

    args = parse_arguments(main=False)
    solve_and_write(
        SolverCP(timeout=args.timeout, rotation=args.rotation, solver_dir=solver_dir), 
        base_dir, solver_dir, ["res/instances/ins-{0}.txt".format(i) for i in range(41)], 
        average=args.average, stats=args.stats, plot=args.plot
    )