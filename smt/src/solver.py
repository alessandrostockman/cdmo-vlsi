import os
import time
import z3
from z3 import Optimize, And, Or, Implies, Bool, Int, sat
import numpy as np

def solve_smt(data, timeout=60*5, rotation=False):
    plate_width, circuits = data
    circuits_num = len(circuits)

    w, h = ([ i for i, _ in circuits ], [ j for _, j in circuits ])

    x = [Int(f'x_{i}') for i in range(circuits_num) ]
    y = [Int(f'y_{i}') for i in range(circuits_num) ]

    lr = [[Bool(f"l_{i}_{j}") for j in range(circuits_num)] for i in range(circuits_num)]
    ud = [[Bool(f"u_{i}_{j}") for j in range(circuits_num)] for i in range(circuits_num)]

    areas_index = np.argsort([h[i]*w[i] for i in range(circuits_num)])
    biggests = areas_index[-1], areas_index[-2]


    sol = Optimize()

    max_y = Int('max_y')

    for i in range(circuits_num):
        xi, yi, wi, hi = x[i],y[i], w[i], h[i] 

        sol.add(And(xi >= 0, xi + wi <= plate_width))
        sol.add(And(yi >= 0, yi + hi <= max_y))
        for j in range(i+1, circuits_num):

            xj, yj, wj, hj = x[j], y[j], w[j], h[j]
            
            #non overlap 
            sol.add(Or(lr[i][j], lr[j][i], ud[i][j], ud[j][i]))
            sol.add(Implies(lr[i][j], xi+wi <= xj))
            sol.add(Implies(lr[j][i], xj+wj <= xi))
            sol.add(Implies(ud[i][j], yi+hi <= yj))
            sol.add(Implies(ud[j][i], yj+hj <= yi))

            #two rectangles with same dimensions 
            if wi == wj and hi == hj:
                sol.add(lr[j][i] == False)
                sol.add(Implies(ud[i][j], lr[j][i]))
            
            #if two rectangles cannot be packed side to side along the x axis 
            if wi+wj > plate_width:
                sol.add(lr[j][i] == False)
                sol.add(lr[j][i] == False)
            
            #if two rectangles cannot be packed one over the other along the y axis
            sol.add(Implies(hi + hj > max_y, And(ud[j][i] == False, ud[i][j] == False)))
            
    
    #symmetry breaking : fix relative position of the two biggest rectangles 
    sol.add(And(lr[biggests[1]][biggests[0]] == False, ud[biggests[1]][biggests[0]] == False))

    sol.add(max_y <= sum(h))

    sol.set(timeout=timeout*1000)

    sol.minimize(max_y)

    start_time = time.time()
    if sol.check() == z3.sat:
        m = sol.model()
        circuits_pos = [(wi, hi, m.eval(xi).as_long(), m.eval(yi).as_long()) for wi, hi, xi, yi in zip(w, h, x, y)]
        plate_height = m.eval(max_y).as_long()

        return ((plate_width, plate_height), circuits_pos), (time.time() - start_time)
    else:
        return None, 0

if __name__ == "__main__":
    pass #TODO
else:
    from lib.utils import load_instance, write_solution