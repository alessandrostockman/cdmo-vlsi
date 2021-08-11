from minizinc import Instance, Model, Solver, Status
import z3
from copy import copy

def solve_cp(code_file, data):
    model = Model(code_file)
    gecode = Solver.lookup("gecode")

    plate_width, circuits = data
    instance = Instance(gecode, model)
    instance["num_circuits"] = len(circuits)
    instance["plate_width"] = plate_width

    w, h = ([ i for i, j in circuits ], [ j for i, j in circuits ])
    instance["widths"] = w
    instance["heights"] = h

    result = instance.solve()

    if result.status is Status.OPTIMAL_SOLUTION:
        circuits_pos = [(w, h, x, y) for (w, h), x, y in zip(circuits, result["x"], result["y"])]
        plate_height = result.objective

    return (plate_width, plate_height), circuits_pos

def solve_sat(data):
    plate_width, circuits = data
    circuits_num = len(circuits)

    w, h = ([ i for i, j in circuits ],
        [ j for i, j in circuits ])

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
    opt.add(
        constraint1 + 
        constraint2 + 
        constraint3 +  
        constraint4
    )

    opt.minimize(max_y)

    if opt.check() == z3.sat:
        m = opt.model()
        circuits_pos = [(wi, hi, m.eval(xi).as_long(), m.eval(yi).as_long()) for wi, hi, xi, yi in zip(w, h, x, y)]
        plate_height = m.eval(max_y).as_long()

        return (plate_width, plate_height), circuits_pos
    else:
        return None