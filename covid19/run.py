## Esegue i modelli su tutti gli input

import sys
import os
import time
import my_globals
from my_lib import RunnerMzn, RunnerLp

import psutil ## TODO remove
import objgraph ## TODO remove

##################################################
# Main
##################################################
def main():
    run_mzn = True # False # True
    run_lp  = not True # True  # False

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
    num = 0
    max_num = len(mzn_inputs)
    while num < max_num:
        try:
            if run_mzn:
                ms = mzn.run(num, show=False, save=True)
            if run_lp:
                ls = lp.run(num, show=False, save=True)

        except:
            max_num+=1
            if (max_num > 200):
                break

        sys.stdout.write("\r")
        j=(num+1)/max_num
        sys.stdout.write("[%-20s] %d%%\t%d" % ('='*int(20*j), 100*j, num))

        ## DEBUG
        print(20*'-')
        current_process = psutil.Process()
        os.system('pstree -p ' + str(current_process.pid))
        children = current_process.children(recursive=True)
        for child in children:
            print('Child pid is {}'.format(child.pid))
            child.terminate()
        print()

        #if (num > 14):
        #    breakpoint()

        objgraph.show_most_common_types(limit=5)
        ## DEBUG
        num+=1

    t1 = time.time()

    print("\nDone")
    print("Total Time:", t1-t0, "s")

if __name__ == "__main__":
    main()
