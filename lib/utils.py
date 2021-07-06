import matplotlib.pyplot as plt
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

def plot_result(plate, circuits):
    matrix = np.zeros(plate[::-1], dtype=int)

    fig, ax = plt.subplots()
    for idx, (w, h, x, y) in enumerate(circuits):
        for i in range(w):
            for j in range(h):
                matrix[y+j, x+i] = idx+1
                
                ax.text(x+i+0.5, y+j+0.5, str(idx+1), va='center', ha='center')

    plt.pcolormesh(matrix, edgecolors='black')
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
