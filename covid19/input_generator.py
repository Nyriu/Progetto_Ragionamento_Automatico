import sys
from my_lib import  InputGenerator

##################################################
# Main
##################################################
def main():
    print("Genero inputs")

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
