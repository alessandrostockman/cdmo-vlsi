from argparse import ArgumentParser
import os
from matplotlib import patches
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def load_instance(filename):
    with open(filename, 'r') as sol:
        width = int(sol.readline().strip())
        circuit_num = int(sol.readline().strip())
        circuits = []
        for i in range(circuit_num):
            circuits.append(tuple(int(el) for el in sol.readline().strip().split(" ")))
        return width, circuits

def load_solution(filename):
    with open(filename, 'r') as sol:
        plate = tuple(int(el) for el in sol.readline().strip().split(" "))
        circuit_num = int(sol.readline().strip())
        circuits = []
        for i in range(circuit_num):
            circuits.append(tuple(int(el) for el in sol.readline().strip().split(" ")))
        return plate, circuits


def plot_result(plate, circuits, plot_title):
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(plot_title)
    
    for idx, (w, h, x, y) in enumerate(circuits):
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='black', facecolor=colors.hsv_to_rgb((idx / len(circuits), 1, 1)))
        ax.add_patch(rect)

        for i in range(1, w):
            ax.plot((x+i, x+i), (y, y+h), color="black", linewidth=1)
        for j in range(1, h):
            ax.plot((x, x+w), (y+j, y+j), color="black", linewidth=1)

    ax.set_xticks(np.arange(plate[0]))
    ax.set_yticks(np.arange(plate[1]))
    plt.show()

def plot_statistics(stats_times):
    stats_times = np.array(stats_times)
    stats_times[stats_times == None] = 0
    fig, ax = plt.subplots()
    r = np.arange(0, len(stats_times))
    ax.bar(r, stats_times, 0.4)
    ax.set_yscale('log')

    ax.set(xlabel='Instance', ylabel='Time (s)', title='')
    ax.grid()
    plt.show()

def plot_result_alternative(plate, circuits, plot_title):
    plate_w, plate_h = plate
    matrix = np.zeros(plate[::-1], dtype=int)

    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(plot_title)
    for idx, (w, h, x, y) in enumerate(circuits):
        matrix[y:y+h, x:x+w] = idx+1

        for i in range(w):
            for j in range(h):
                if x+i <= plate_w and y+j <= plate_h:
                    ax.text(x+i+0.5, y+j+0.5, str(idx+1), va='center', ha='center')

    plt.pcolormesh(matrix, edgecolors='black', cmap="prism")
    ax.set_xticks(np.arange(plate[0]))
    ax.set_yticks(np.arange(plate[1]))
    plt.show()

def write_solution(filename, solution):
    with open(filename, 'w') as sol:
        (plate_width, plate_height), circuits_pos = solution
        sol.write("{0} {1}\n".format(plate_width, plate_height))
        sol.write("{0}\n".format(len(circuits_pos)))
        for c in circuits_pos:
            w, h, x, y = c
            sol.write("{0} {1} {2} {3}\n".format(w, h, x, y))

def solve_and_write(solver, base_dir, solver_dir, inputs, average=False, stats=False, plot=False):
    output_dir = os.path.join(solver_dir, "out")

    stats_times = []
    for input in inputs:
        filename = os.path.basename(os.path.join(base_dir, input))
        output = os.path.join(output_dir, filename)
        if 'ins' in filename:
            output = output.replace('ins', 'out')

        instance = load_instance(os.path.join(base_dir, input))

        sol = None
        execution_time = None
        if average:
            times = []
            for _ in range(10):
                sol, execution_time = solver.solve(instance)
                if sol is not None:
                    times.append(execution_time)

            execution_time = sum(times) / len(times)
        else:
            sol, execution_time = solver.solve(instance)

        if sol is not None:
            print("Problem {0} solved in {1}s".format(input, round(execution_time, 4)))
            stats_times.append(execution_time)
            write_solution(output, sol)

            plate, circuits_pos = sol

            if plot:
                plot_result(plate, circuits_pos, input)
        else:
            print("Problem {0} not solved".format(input))
            stats_times.append(None)

    if stats:
        plot_statistics(stats_times)

def parse_arguments(main=True):
    parser = ArgumentParser()

    if main:
        parser.add_argument("-S", "--solver", default="null", help="", choices=["null", "cp", "sat", "smt"])
        parser.add_argument('-I', '--instances', help="", default="res/instances")
        parser.add_argument('-O', '--output', help="", default=None)
        
    parser.add_argument('-P', '--plot', help="", default=False, action='store_true')
    parser.add_argument('-X', '--stats', help="", default=True, action='store_false')
    parser.add_argument('-A', '--average', help="", default=False, action='store_true')
    parser.add_argument('-T', '--timeout', help="", default=300)
    parser.add_argument('-R', '--rotation', help="", default=False, action='store_true')
    return parser.parse_args()