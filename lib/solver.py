from minizinc import Instance, Model, Solver, Status

def solve_cp(code_file, data):
    model = Model(code_file)
    gecode = Solver.lookup("gecode")

    plate_width, circuits = data
    instance = Instance(gecode, model)
    instance["num_circuits"] = len(circuits)
    instance["plate_width"] = plate_width

    w, h = ([ i for i, j in circuits ],
        [ j for i, j in circuits ])
    instance["widths"] = w
    instance["heights"] = h

    result = instance.solve()

    if result.status is Status.OPTIMAL_SOLUTION:
        circuits_pos = [(w, h, x, y) for (w, h), x, y in zip(circuits, result["x"], result["y"])]
        plate_height = result.objective

        return (plate_width, plate_height), circuits_pos
    else:
        return None