import datetime
from minizinc import Instance, Model, Solver, Status
from copy import copy
import os

def solve_cp(data, timeout, rotation=False):
    solver_file = "cp/src/solver.mzn" if not rotation else "cp/src/solver_rotation.mzn"
    model = Model(solver_file)
    gecode = Solver.lookup("gecode")

    plate_width, circuits = data
    instance = Instance(gecode, model)
    instance["num_circuits"] = len(circuits)
    instance["plate_width"] = plate_width

    w, h = ([ i for i, j in circuits ], [ j for i, j in circuits ])
    instance["widths"] = w
    instance["heights"] = h

    result = instance.solve(timeout=datetime.timedelta(seconds=timeout))

    if result.status is Status.OPTIMAL_SOLUTION:
        circuits_pos = [(w, h, x, y) for (w, h), x, y in zip(circuits, result["x"], result["y"])]
        plate_height = result.objective

        return ((plate_width, plate_height), circuits_pos), result.statistics['time'].total_seconds()
    else:
        return None, 0


if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(base_dir)
    from lib.utils import load_instance, write_solution

    solver = os.path.join(base_dir, "cp", "src", "solver.mzn")
    timeout = 5 * 60

    instances_dir = os.path.join(base_dir, "res", "instances")
    output_dir = os.path.join(base_dir, "cp", "out")
    inputs = sorted([os.path.join(instances_dir, i) for i in os.listdir(instances_dir) if os.path.isfile(os.path.join(instances_dir, i))])

    for input in inputs:
        filename = os.path.basename(input)
        output = os.path.join(output_dir, filename)
        if 'ins' in filename:
            output = output.replace('ins', 'out')

        instance = load_instance(input)
        sol, execution_time = solve_cp(solver, instance, timeout)
        write_solution(output, sol)
else:
    from lib.utils import load_instance, write_solution