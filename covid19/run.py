## Esegue i modelli su input di num dato
## Usage:
## python run.py #to run on all inputs
## python run.py 0
## python run.py 1
## python run.py 02
## python run.py 23


import sys
import os
import time
import my_globals
from my_lib import RunnerMzn, RunnerLp

##def get_args():
##    args = sys.argv
##    if len(args) > 2:
##        print("Put zero or one arguments!! For example")
##        print("python run.py 10")
##        print("python run.py #to run on all inputs")
##        exit(1)
##
##    try:
##        input_num = int(args[1])
##    except:
##        print("ERROR! Input num is not ad int!")
##        exit(2)
##    return input_num




##################################################
# Main
##################################################
def main():
    ##input_num = get_args()

    #verbose = True
    verbose = False

    run_mzn = True
    run_lp  = False

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
            # print("Obj:", ms.obj)
            # print(ms)
            # print(10*"-")
            # print(ls)
            # print(30*"=")
        else:
            sys.stdout.write("\r")
            j=(num+1)/len(mzn_inputs)
            sys.stdout.write("[%-20s] %d%%\t%d" % ('='*int(20*j), 100*j, num))
            #sys.stdout.flush()


        # if  run_mzn and run_lp and ms.obj != ls.obj:
        #     #raise Exception("Obj differenti!")
        #     s = "Obj differenti per input:  "
        #     s += str(num)
        #     s += "\n"
        #     s += str(mzn_o.obj)
        #     s += "\n"
        #     s += str(lp_o.obj)
        #     s += "\n"
        #     s += "\n"

    t1 = time.time()

    print("\nDone")
    print("Total Time:", t1-t0, "s")


if __name__ == "__main__":
    main()
