import matplotlib.pyplot as plt
import numpy as np

def load_instance(filename):
    with open(filename, 'r') as sol:
        width = int(sol.readline().strip())
        circuit_num = int(sol.readline().strip())
        circuits = []
        for i in range(circuit_num):
            circuits.append(tuple(int(el) for el in sol.readline().strip().split(" "))[::-1])
        return width, circuits

def load_solution(filename):
    with open(filename, 'r') as sol:
        plate = tuple(int(el) for el in sol.readline().strip().split(" "))[::-1]
        circuit_num = int(sol.readline().strip())
        circuits = []
        for i in range(circuit_num):
            circuits.append(tuple(int(el) for el in sol.readline().strip().split(" "))[::-1])
        return plate, circuits

def plot_result(plate, circuits):
    matrix = np.zeros(plate, dtype=int)

    fig, ax = plt.subplots()
    for idx, (x, y, w, h) in enumerate(circuits):
        for i in range(w):
            for j in range(h):
                matrix[x+i, y+j] = idx+1
                # ax.text(y+j+0.5, x+i+0.5, str(idx+1), va='center', ha='center')

    plt.pcolormesh(matrix)
    ax.set_xticks(np.arange(plate[1]))
    ax.set_yticks(np.arange(plate[0]))
    plt.show()