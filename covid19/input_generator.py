import sys
from my_lib import  InputGenerator


"""
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
"""




##################################################
# Main
##################################################
def main():
    print("Genero inputs")

    # TODO gestire come Batch
    n = 3
    k_min=1
    h_min=2

    k_max=7
    h_max=7

    delete_old=True
    write=True

    InputGenerator.gen_istanze(n, k_min,h_min, k_max,h_max,
            delete_old=delete_old, write=write)

if __name__ == "__main__":
    main()
