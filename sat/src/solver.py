import time
import z3
from copy import copy

def solve_sat(data, timeuout=60*5):
    plate_width, circuits = data
    circuits_num = len(circuits)

    w, h = ([ i for i, j in circuits ], [ j for i, j in circuits ])

    x = [ z3.Int('X_%i' % (i + 1)) for i in range(circuits_num) ]
    y = [ z3.Int('Y_%i' % (i + 1)) for i in range(circuits_num) ]
    upper_bound = sum(h)

    constraint1, constraint2, constraint3, constraint4 = [], [], [], []

    max_y = z3.Int('max_y')

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
    opt.set(timeout=timeuout*1000)

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