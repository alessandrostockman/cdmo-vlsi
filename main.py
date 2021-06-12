from argparse import ArgumentParser
from lib.utils import load_solution, plot_result

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-S", "--solver", default=None, help="", choices=[None])
    parser.add_argument('-P', '--plot', dest="plot", help="", default=False, action='store_true')
    args = parser.parse_args()

    plate, circuits = load_solution("res/solutions/out-1.txt")
    plot_result(plate, circuits)
    
    execution_time = 0
    print("Execution finished in " + str(execution_time) + "s")