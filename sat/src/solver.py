import os
import time
from z3 import And, Or, Bool, sat, Not, Solver, Implies
from itertools import combinations

class SolverSAT:

    def __init__(self, timeout=300, rotation=False):
        self.timeout = timeout
        self.rotation = rotation
        
    def solve(self, data):
        self.plate_width, self.circuits = data
        self.circuits_num = len(self.circuits)

        self.w, self.h = ([ i for i, _ in self.circuits ], [ j for _, j in self.circuits ])

        lower_bound = sum([self.h[i]*self.w[i] for i in range(self.circuits_num)]) // self.plate_width
        upper_bound = sum(self.h)

        start_time = time.time()
        try_timeout = self.timeout
        for plate_height in range(lower_bound, upper_bound+1):
            self.sol = Solver()
            self.sol.set(timeout=self.timeout*1000)
            board, rotations = self.add_constraints(plate_height)

            solve_time = time.time()
            if self.sol.check() == sat:
                circuits_pos = self.evaluate(plate_height, board, rotations)
                return ((self.plate_width, plate_height), circuits_pos), (time.time() - solve_time)
            else:
                try_timeout = round((self.timeout - (time.time() - start_time)))
                if try_timeout < 0:
                    return None, 0
        return None, 0

    def all_true(self, bool_vars):
        return And(bool_vars)

    def at_least_one(self, bool_vars):
        return Or(bool_vars)

    def at_most_one(self, bool_vars):
        return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

    def exactly_one(self, bool_vars):
        self.sol.add(self.at_most_one(bool_vars))
        self.sol.add(self.at_least_one(bool_vars))

    def add_constraints(self, plate_height):
        board = [[[Bool(f"b_{i}_{j}_{k}") for k in range(self.circuits_num)] for j in range(plate_height)] for i in range(self.plate_width)]
        rotations = None

        xs = [[Bool(f"x_{i}_{j}") for j in range(self.circuits_num)] for i in range(self.plate_width)]
        ys = [[Bool(f"y_{i}_{j}") for j in range(self.circuits_num)] for i in range(plate_height)]

        for k in range(self.circuits_num):
            for y in range(plate_height):
                p = self.at_least_one([board[x][y][k] for x in range(self.plate_width)])
                self.sol.add(And(Implies(ys[y][k], p), Implies(p, ys[y][k])))
            for x in range(self.plate_width):
                p = self.at_least_one([board[x][y][k] for y in range(plate_height)])
                self.sol.add(And(Implies(xs[x][k], p), Implies(p, xs[x][k])))

        if not self.rotation:
            for k in range(self.circuits_num):
                configurations = []
                for y in range(plate_height - self.h[k] + 1):
                    for x in range(self.plate_width - self.w[k] + 1):
                        configurations.append(self.all_true([board[x+xk][y+yk][k] for yk in range(self.h[k]) for xk in range(self.w[k])]))
                            
                self.exactly_one(configurations)
        else:
            rotations = [Bool(f"r_{k}") for k in range(self.circuits_num)]
            for k in range(self.circuits_num):
                min_dim = min(self.h[k], self.w[k])

                configurations = []
                configurations_r = []
                for y in range(plate_height - min_dim + 1):
                    for x in range(self.plate_width - min_dim + 1):
                        conf1 = []
                        conf2 = []

                        for yk in range(self.h[k]):
                            for xk in range(self.w[k]):
                                if y + self.h[k] <= plate_height and x + self.w[k] <= self.plate_width:
                                    conf1.append(board[x+xk][y+yk][k])
                                if y + self.w[k] <= plate_height and x + self.h[k] <= self.plate_width:
                                    conf2.append(board[x+yk][y+xk][k])
                        
                        if len(conf1) > 0:
                            configurations.append(self.all_true(conf1))

                        if len(conf2) > 0:
                            configurations_r.append(self.all_true(conf2))

                if len(configurations) > 0 and len(configurations_r) > 0:
                    self.exactly_one([
                        And(self.at_least_one(configurations), Not(rotations[k])),
                        And(self.at_least_one(configurations_r), rotations[k])
                    ])
                elif len(configurations) > 0:
                    self.sol.add(And(self.at_least_one(configurations), Not(rotations[k])))
                elif len(configurations_r) > 0:
                    self.sol.add(And(self.at_least_one(configurations_r), rotations[k]))

        for x in range(self.plate_width):
            for y in range(plate_height):
                self.sol.add(self.at_most_one([board[x][y][k] for k in range(self.circuits_num)]))

        prev = []
        flat_x = [xs[x][k] for x in range(self.plate_width) for k in range(self.circuits_num)]
        flat_x_r = [xs[self.plate_width - x - 1][k] for x in range(self.plate_width) for k in range(self.circuits_num)]
        for x in range(len(flat_x)):
            if len(prev) > 0:
                self.sol.add(Implies(And(prev), Implies(flat_x[x], flat_x_r[x])))
            else:
                self.sol.add(Implies(flat_x[x], flat_x_r[x]))
            prev.append(And(Implies(flat_x[x], flat_x_r[x]), Implies(flat_x_r[x], flat_x[x])))

        prev = []
        flat_y = [ys[y][k] for y in range(plate_height) for k in range(self.circuits_num)]
        flat_y_r = [ys[plate_height - y - 1][k] for y in range(plate_height) for k in range(self.circuits_num)]
        for y in range(len(flat_y)):
            if len(prev) > 0:
                self.sol.add(Implies(And(prev), Implies(flat_y[y], flat_y_r[y])))
            else:
                self.sol.add(Implies(flat_x[y], flat_x_r[y]))

            prev.append(And(Implies(flat_y[y], flat_y_r[y]), Implies(flat_y_r[y], flat_y[y])))
        
        return board, rotations

    def evaluate(self, plate_height, board, rotations):
        m = self.sol.model()

        circuits_pos = []
        for k in range(self.circuits_num):
            found = False
            for x in range(self.plate_width):
                for y in range(plate_height):
                    if not found and m.evaluate(board[x][y][k]):
                        if not self.rotation:
                            circuits_pos.append((self.w[k], self.h[k], x, y))
                        else:
                            if m.evaluate(rotations[k]):
                                circuits_pos.append((self.h[k], self.w[k], x, y))
                            else:
                                circuits_pos.append((self.w[k], self.h[k], x, y))
                        found = True

        return circuits_pos
        
if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    solver_dir = os.path.join(base_dir, "sat")
    sys.path.append(base_dir)
    from lib.utils import solve_and_write, parse_arguments

    args = parse_arguments(main=False)
    solve_and_write(
        SolverSAT(timeout=args.timeout, rotation=args.rotation), 
        base_dir, solver_dir, ["res/instances/ins-{0}.txt".format(i) for i in range(41)], 
        average=args.average, stats=args.stats, plot=args.plot
    )