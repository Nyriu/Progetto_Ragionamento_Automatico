import sys
import os
from my_globals import *
from my_lib import IOHelper, MyInstance, MySolution

def in_out(num):
    try:
        i = MyInstance.read(
                IOHelper.gen_fpath(
                    num,
                    INPUT_MZN_DIR,
                    INPUT_MZN_PREFIX,
                    INPUT_MZN_EXT))
    except Exception as e:
        i = None
        mzn_out = None
        lp_out = None
        return i,mzn_out,lp_out

    try:
        mzn_out = MySolution.read(
                    IOHelper.gen_fpath(
                        num,
                        OUTPUT_MZN_DIR,
                        OUTPUT_MZN_PREFIX,
                        OUTPUT_MZN_EXT))
    except Exception as e:
        mzn_out = None

    try:
        lp_out  = MySolution.read(
                    IOHelper.gen_fpath(
                        num,
                        OUTPUT_LP_DIR,
                        OUTPUT_LP_PREFIX,
                        OUTPUT_LP_EXT))
    except Exception as e:
        lp_out = None

    return i,mzn_out,lp_out

### ##################################################
### # Main
### ##################################################
def main():

    num = 0
    i,mzn_o,lp_o = in_out(num)

    while not (mzn_o == None or lp_o == None):
        if mzn_o.obj != lp_o.obj:
            s = "Obj differenti per input:  "
            s += str(num)
            s += "\n"
            s += str(mzn_o.obj)
            s += "\n"
            s += str(lp_o.obj)
            s += "\n"
            s += "\n"
            if mzn_o.solveTime < 299:
                raise Exception(s)
            else:
                print(s)

        num+=1
        i,mzn_o,lp_o = in_out(num)

    return


if __name__ == "__main__":
    main()
