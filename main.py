from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-S", "--solver", default=None, help="", choices=[None])
    parser.add_argument('-P', '--plot', dest="plot", help="", default=False, action='store_true')
    args = parser.parse_args()

    execution_time = 0
    print("Execution finished in " + str(execution_time) + "s")