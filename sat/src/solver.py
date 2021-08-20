import os
import time
from z3 import And, Or, Bool, sat, Not, Solver
from itertools import combinations

def solve_sat(data, timeout=60*5, rotation=False):
    plate_width, circuits = data
    circuits_num = len(circuits)

    w, h = ([ i for i, _ in circuits ], [ j for _, j in circuits ])
    lower_bound = sum([h[i]*w[i] for i in range(circuits_num)]) // plate_width
    upper_bound = sum(h)

    def all_true(solver, bool_vars):
        return And(bool_vars)

    def at_least_one(solver, bool_vars):
        return Or(bool_vars)

    def at_most_one(solver, bool_vars):
        return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

    def exactly_one(solver, bool_vars):
        solver.add(at_most_one(solver, bool_vars))
        solver.add(at_least_one(solver, bool_vars))

    start_time = time.time()
    try_timeout = timeout
    for plate_height in range(lower_bound, upper_bound+1):
        sol = Solver()
        sol.set(timeout=try_timeout*1000)
        board = [[[Bool(f"b_{i}_{j}_{k}") for k in range(circuits_num)] for j in range(plate_height)] for i in range(plate_width)]
        rotations = None
        
        if not rotation:
            for k in range(circuits_num):
                configurations = []
                for y in range(plate_height - h[k] + 1):
                    for x in range(plate_width - w[k] + 1):
                        configurations.append(all_true(sol, [board[x+xk][y+yk][k] for yk in range(h[k]) for xk in range(w[k])]))
                sol.add(at_least_one(sol, configurations))
        else:
            rotations = [Bool(f"r_{k}") for k in range(circuits_num)]
            for k in range(circuits_num):
                min_dim = min(h[k], w[k])

                configurations = []
                configurations_r = []
                for y in range(plate_height - min_dim + 1):
                    for x in range(plate_width - min_dim + 1):
                        conf1 = []
                        conf2 = []

                        for yk in range(h[k]):
                            for xk in range(w[k]):
                                if y + h[k] <= plate_height and x + w[k] <= plate_width:
                                    conf1.append(board[x+xk][y+yk][k])
                                if y + w[k] <= plate_height and x + h[k] <= plate_width:
                                    conf2.append(board[x+yk][y+xk][k])
                        
                        if len(conf1) > 0:
                            configurations.append(all_true(sol, conf1))

                        if len(conf2) > 0:
                            configurations_r.append(all_true(sol, conf2))

                if len(configurations) > 0 and len(configurations_r) > 0:
                    exactly_one(sol, [
                        And(at_least_one(sol, configurations), Not(rotations[k])),
                        And(at_least_one(sol, configurations_r), rotations[k])
                    ])
                elif len(configurations) > 0:
                    sol.add(And(at_least_one(sol, configurations), Not(rotations[k])))
                elif len(configurations_r) > 0:
                    sol.add(And(at_least_one(sol, configurations_r), rotations[k]))

        for x in range(plate_width):
            for y in range(plate_height):
                sol.add(at_most_one(sol, [board[x][y][k] for k in range(circuits_num)]))

        if sol.check() == sat:
            m = sol.model()

            circuits_pos = []
            for k in range(circuits_num):
                found = False
                for x in range(plate_width):
                    for y in range(plate_height):
                        if not found and m.evaluate(board[x][y][k]):
                            if not rotation:
                                circuits_pos.append((w[k], h[k], x, y))
                            else:
                                if m.evaluate(rotations[k]):
                                    circuits_pos.append((h[k], w[k], x, y))
                                else:
                                    circuits_pos.append((w[k], h[k], x, y))
                            found = True

            return ((plate_width, plate_height), circuits_pos), (time.time() - start_time)
        else:
            try_timeout = round((timeout - (time.time() - start_time)))
            if try_timeout < 0:
                return None, 0
    return None, 0

if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(base_dir)
    from lib.utils import load_instance, write_solution

    timeout = 5 * 60

    instances_dir = os.path.join(base_dir, "res", "instances")
    output_dir = os.path.join(base_dir, "sat", "out")
    inputs = sorted([os.path.join(instances_dir, i) for i in os.listdir(instances_dir) if os.path.isfile(os.path.join(instances_dir, i))])

    for input in inputs:
        filename = os.path.basename(input)
        output = os.path.join(output_dir, filename)
        if 'ins' in filename:
            output = output.replace('ins', 'out')

        instance = load_instance(input)
        sol, execution_time = solve_sat(instance, timeout)
        write_solution(output, sol)
else:
    from lib.utils import load_instance, write_solution