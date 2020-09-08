import sys
import os
import time
import my_globals
from my_lib import MyInstance, RunnerLp

def get_args():
    args = sys.argv
    if len(args) != 2:
        print("Put one argument!! For example")
        print("python run.py ./input_per_debug.dzn")
        print("python run.py 10")
        exit(1)

    try:
        val = int(args[1])
    except:
        #print("ERROR! Input num is not ad int!")
        #exit(2)
        val = args[1]

    return val




##################################################
# Main
##################################################
def main():
    val = get_args()

    #verbose = True
    verbose = False

    lp_path = "./covid19.lp"
    lp = RunnerLp(lp_path)

    lp_inputs  = os.listdir(my_globals.INPUT_LP_DIR)


    if type(val) == int:
        t0 = time.time()
        ls = lp.run(num, show=True, save=False)
        t1 = time.time()
    else:
        print(val)
        myIns = MyInstance.read(val)
        t0 = time.time()
        ls = lp.runs(myIns, show=True)
        t1 = time.time()

    print("\nDone")
    print("Total Time:", t1-t0)


if __name__ == "__main__":
    main()
