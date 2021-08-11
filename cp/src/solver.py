import datetime
from minizinc import Instance, Model, Solver, Status
from copy import copy
import os
from lib.utils import load_instance, write_solution

def solve_cp(code_file, data, timeout):
    model = Model(code_file)
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

        return ((plate_width, plate_height), circuits_pos), result.statistics['time'].total_seconds() / 1000
    else:
        return None, 0


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    instances_dir = os.path.join(base_dir, "res", "instances")
    output_dir = os.path.join(base_dir, "cp", "out")
    inputs = sorted([os.path.join(instances_dir, i) for i in os.listdir(instances_dir) if os.path.isfile(os.path.join(instances_dir, i))])

    for input in inputs:
        filename = os.path.basename(input)
        output = os.path.join(output_dir, filename)
        if 'ins' in filename:
            output = output.replace('ins', 'out')

        instance = load_instance(input)
        sol = solve_cp("cp/src/solver.mzn", instance)
        write_solution(output, sol)