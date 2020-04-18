# Genera dzn realtivi ad istanze casuali
# Usage:
# python input_generator.py

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
    print("Genero inputs")
    my_lib.del_inputs()
    my_lib.del_outputs()

    #K_max, H_max, n = get_args()
    n = 20

    K_max = 3
    H_max = 4

    K_min = 3
    H_min = 2

    my_lib.gen_inputs(K_max, H_max, n, K_min=K_min,H_min=H_min)


if __name__ == "__main__":
    main()
