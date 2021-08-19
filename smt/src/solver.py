import os
import time
import z3

def solve_smt(data, timeuout=60*5, rotation=False):
    plate_width, circuits = data
    circuits_num = len(circuits)

    w, h = ([ i for i, j in circuits ], [ j for i, j in circuits ])

    return None, 0

if __name__ == "__main__":
    pass #TODO
else:
    from lib.utils import load_instance, write_solution