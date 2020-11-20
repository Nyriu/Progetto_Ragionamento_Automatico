import sys
from my_lib import  InputGenerator

##################################################
# Main
##################################################
def main():
    print("Genero inputs")

    n = 2 # Numero di istanze da generare per coppia H,K
    k_min=1
    h_min=2

    k_max=11
    h_max=11

    delete_old=True
    write     =True

    InputGenerator.gen_istanze(n, k_min,h_min, k_max,h_max,
            delete_old=delete_old, write=write)

if __name__ == "__main__":
    main()
