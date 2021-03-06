import os
import time
from z3 import Optimize, And, Or, Implies, Int, sat, Sum, Product, If, IntVector
import numpy as np

class SolverSMT:
    def __init__(self, timeout=300, rotation=False):
        self.timeout = timeout
        self.rotation = rotation
        
    def solve(self, data):
        plate_width, circuits = data
        circuits_num = len(circuits)

        widths, heights = ([ i for i, _ in circuits ], [ j for _, j in circuits ])

        x = IntVector('x',circuits_num)  
        y = IntVector('y',circuits_num)

        w,h = widths, heights    #actual widths and heights if rotation allowed
        if self.rotation:
            w = IntVector('w',circuits_num) 
            h = IntVector('h',circuits_num)  

        areas_index = np.argsort([heights[i]*widths[i] for i in range(circuits_num)])
        biggests = areas_index[-1], areas_index[-2]

        sol = Optimize()

        plate_height = Int('plate_height')

        #handling rotation 
        if self.rotation:
            for i in range(circuits_num):
                # if rotation allowed and a circuit is square  (width=hight) then force it to be not rotated 
                sol.add(If(w[i]==h[i],And(w[i]==widths[i],h[i]==heights[i]),Or(And(w[i]==widths[i],h[i]==heights[i]),And(w[i]==heights[i],h[i]==widths[i]))))               

        for i in range(circuits_num):
            xi, yi, wi, hi = x[i],y[i], w[i], h[i] 

            sol.add(And(xi >= 0, xi + wi <= plate_width))
            sol.add(And(yi >= 0, yi + hi <= plate_height))
            for j in range(i+1, circuits_num):

                xj, yj, wj, hj = x[j], y[j], w[j], h[j]
                
                #non overlap
                sol.add(Or(xi+wi <= xj, xj+wj <= xi, yi+hi <= yj, yj+hj <= yi))

                #two rectangles with same dimensions
                sol.add(Implies(And(wi == wj,hi == hj),Or(xj>xi,And(xj==xi,yj >= yi))))
                
                #if two rectangles cannot be packed side to side along the x axis 
                sol.add(Implies(wi+wj > plate_width, Or(yi+hi <= yj, yj+hj <= yi)))
                
                #if two rectangles cannot be packed one over the other along the y axis
                sol.add(Implies(hi + hj > plate_height,  Or(xi+wi <= xj, xj+wj <= xi)))

        #bounds on variables range    
        for i in range(circuits_num):
            sol.add(And(x[i]>=0,x[i]<=plate_width-self.min(w)))     
            sol.add(And(y[i]>=0,y[i]<=Sum(h)-self.min(h)))          
               
        #symmetry breaking : fix relative position of the two biggest rectangles 
        sol.add(Or(x[biggests[1]] > x[biggests[0]], And(x[biggests[1]] == x[biggests[0]], y[biggests[1]] >= y[biggests[0]])))

        #area constraint 
        sol.add(plate_height >= (Sum([Product(h[i],w[i]) for i in range(circuits_num)]) / plate_width))
        sol.add(plate_height <= Sum(h))

        sol.set(timeout=self.timeout*1000)

        sol.minimize(plate_height)

        start_time = time.time()
        if sol.check() == sat:
            m = sol.model()
            if self.rotation:
                circuits_pos = [(m.eval(wi), m.eval(hi), m.eval(xi).as_long(), m.eval(yi).as_long()) for wi, hi, xi, yi in zip(w, h, x, y)]
            else : circuits_pos = [(wi, hi, m.eval(xi).as_long(), m.eval(yi).as_long()) for wi, hi, xi, yi in zip(w, h, x, y)]
            height = m.eval(plate_height).as_long()

            return ((plate_width, height), circuits_pos), (time.time() - start_time)
        else:
            return None, 0

    def min(self, vars):
        min = vars[0]
        for v in vars[1:]:
            min = If(v<min,v,min)
        return min

if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    solver_dir = os.path.join(base_dir, "sat")
    sys.path.append(base_dir)
    from lib.utils import solve_and_write, parse_arguments

    args = parse_arguments(main=False)
    solve_and_write(
        SolverSMT(timeout=args.timeout, rotation=args.rotation), 
        base_dir, solver_dir, ["res/instances/ins-{0}.txt".format(i) for i in range(41)], 
        average=args.average, stats=args.stats, plot=args.plot
    )