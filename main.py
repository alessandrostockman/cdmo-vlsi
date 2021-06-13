from argparse import ArgumentParser
from lib.utils import load_instance, load_solution, plot_result

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-S", "--solver", default=None, help="", choices=[None])
    parser.add_argument('-P', '--plot', dest="plot", help="", default=False, action='store_true')
    args = parser.parse_args()

    width, circuits = load_instance("res/instances/ins-0.txt")
    plate, circuits_pos = load_solution("res/solutions/out-0.txt")

    print("Fill a plate with width: {0}. \nCircuits: {1}".format(width, circuits))
    plot_result(plate, circuits_pos)
    
    execution_time = 0
    print("Execution finished in " + str(execution_time) + "s")