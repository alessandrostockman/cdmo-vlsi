from minizinc import Instance, Model, Solver

def solve_cp(code_file, instances):
    model = Model(code_file)
    gecode = Solver.lookup("gecode")

    solutions = []
    for data in instances:
        plate_width, circuits = data
        instance = Instance(gecode, model)
        instance["n"] = len(circuits)
        instance["max_w"] = plate_width

        w, h = ([ i for i, j in circuits ],
            [ j for i, j in circuits ])
        instance["w"] = w
        instance["h"] = h

        result = instance.solve()

        circuits_pos = [(w, h, x, y) for (w, h), x, y in zip(circuits, result["x"], result["y"])]
        plate_height = result.objective

        solutions.append(((plate_width, plate_height), circuits_pos))

    return solutions