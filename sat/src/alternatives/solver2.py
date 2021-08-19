import os
import time
import z3
from z3 import Optimize, And, Or, Implies, Bool, Int
from copy import copy

def solve_sat(data, timeuout=60*5, rotation=False):
    plate_width, circuits = data
    circuits_num = len(circuits)

    w, h = ([ i for i, _ in circuits ], [ j for _, j in circuits ])

    max_y = z3.Int('max_y')

    board = [[[Bool(f"b_{i}_{j}_{k}") for k in range(circuits_num)] for j in range(plate_width)] for i in range(max_y)]

    sol = Optimize()

    def in_boundaries():
        return [And]



    

    for i, (xi, yi, hi, wi) in enumerate(zip(x, y, h, w)):
        constraint1.append(z3.And(xi >= 0, xi + wi <= plate_width)) # xs domain upper bound
        constraint2.append(z3.And(yi >= 0, yi + hi <= max_y)) # ys domain upper bound

    constraint1.append(max_y <= upper_bound)
        
    for i, (xi, yi, hi, wi) in enumerate(zip(x, y, h, w)):
        for j, (xj, yj, hj, wj) in enumerate(zip(x, y, h, w)):
            if j > i:
                constraint3.append(
                    z3.Implies(
                        z3.Or(
                            z3.And(yi <= yj + hj - 1, yi >= yj), 
                            z3.And(yi + hi - 1 <= yj + hj - 1, yi + hi - 1 >= yj)
                        ),
                        z3.Or(xi + wi - 1 < xj, xi > xj + wj - 1)
                    )
                )

                constraint4.append(
                    z3.Implies(
                        z3.Or(
                            z3.And(xi <= xj + wj - 1, xi >= xj), 
                            z3.And(xi + wi - 1 <= xj + wj - 1, xi + wi - 1 >= xj)
                        ),
                        z3.Or(yi + hi - 1 < yj, yi > yj + hj - 1)
                    )
                )

    opt = z3.Optimize()
    opt.set(timeout=timeout*1000)

    opt.add(
        constraint1 + 
        constraint2 + 
        constraint3 +  
        constraint4
    )

    opt.minimize(max_y)

    start_time = time.time()
    if opt.check() == z3.sat:
        m = opt.model()
        circuits_pos = [(wi, hi, m.eval(xi).as_long(), m.eval(yi).as_long()) for wi, hi, xi, yi in zip(w, h, x, y)]
        plate_height = m.eval(max_y).as_long()

        return ((plate_width, plate_height), circuits_pos), (time.time() - start_time)
    else:
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