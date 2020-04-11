# Esegue il modello MiniZinc su input di num dato
# Usage:
# python run.py 0
# python run.py 1
# python run.py 02
# python run.py 23


import sys
import my_lib

def get_args():
    args = sys.argv
    if len(args) < 2:
        print("Put pone arguments!! For example")
        print("python run.py 10")
        exit(1)

    try:
        input_num = int(args[1])
    except:
        print("ERROR! Input num is not ad int!")
        exit(2)
    return input_num




##################################################
# Main
##################################################
def main():
    input_num = get_args()
    #my_lib.run_minizinc_model(input_num, show_output=True)
    my_lib.run_minizinc_model(input_num)


if __name__ == "__main__":
    main()
