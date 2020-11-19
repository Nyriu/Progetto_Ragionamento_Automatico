## Esegue i modelli su tutti gli input

import sys
import os
import time
import my_globals
from my_lib import RunnerMzn, RunnerLp

##################################################
# Main
##################################################
def main():
    #verbose = True
    verbose = False

    run_mzn = True # False # True
    run_lp  = True # True  # False

    if not run_mzn:
        print("\tNOT EXECUTING MZN")
    if not run_lp:
        print("\tNOT EXECUTING ASP")

    print("\n")

    mzn_path="./covid19.mzn"
    mzn = RunnerMzn(mzn_path)

    lp_path = "./covid19.lp"
    lp = RunnerLp(lp_path)

    mzn_inputs = os.listdir(my_globals.INPUT_MZN_DIR)
    lp_inputs  = os.listdir(my_globals.INPUT_LP_DIR)

    if len(mzn_inputs) != len(lp_inputs):
        raise Exception("Le cartelle degli input hanno un \
                numero differente di files...")

    ms = None
    ls = None

    t0 = time.time()
    for num in range(len(mzn_inputs)):
        if run_mzn:
            ms = mzn.run(num, show=False, save=True)
        if run_lp:
            ls = lp.run(num, show=False, save=True)

        if verbose:
            raise Exception("Verbose not implemented!")
        else:
            sys.stdout.write("\r")
            j=(num+1)/len(mzn_inputs)
            sys.stdout.write("[%-20s] %d%%\t%d" % ('='*int(20*j), 100*j, num))

    t1 = time.time()

    print("\nDone")
    print("Total Time:", t1-t0, "s")

if __name__ == "__main__":
    main()
