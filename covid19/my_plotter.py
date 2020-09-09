import sys
import os
from my_globals import *
from my_lib import IOHelper, MyInstance, MySolution

import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

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

def normalize(x, a,b):
    # normalize x into [a,b]
    m = min(x)
    M = max(x)
    res = [(b-a)*(y-m)/(M-m)+a for y in x]
    return res

def plot_solveTimes(inputs, mzn_outputs, lp_outputs):
    mzn_solveTimes     = [y.solveTime for y in mzn_outputs]
    lp_solveTimes      = [y.solveTime for y in lp_outputs]
    input_complexities = [y.calc_complexity(alpha=.2) for y in inputs]
    input_complexities = normalize(input_complexities, min(mzn_solveTimes),max(mzn_solveTimes))

    #n = len(nums)
    #n = 20
    #n_delta = 4
    #plt.plot(range(n,n+n_delta), mzn_solveTimes[n:n+n_delta])
    #plt.plot(range(n,n+n_delta), input_complexities[n:n+n_delta])

    n = len(mzn_solveTimes)
    plt.plot(range(n), mzn_solveTimes)

    n = len(lp_solveTimes)
    plt.plot(range(n), lp_solveTimes)

    n = len(input_complexities)
    plt.plot(range(n), input_complexities)


    plt.legend(["mzn_solveTimes","lp_solveTimes","complexities"])
    #plt.xticks(ticks=nums[:x], rotation=70)
    plt.show()


def plot_times(inputs, mzn_outputs, lp_outputs):
    mzn_times     = [y.time for y in mzn_outputs]
    lp_times      = [y.time for y in lp_outputs]
    input_complexities = [y.calc_complexity(alpha=.2) for y in inputs]
    input_complexities = normalize(input_complexities, min(mzn_times),max(mzn_times))

    n = len(mzn_times)
    plt.plot(range(n), mzn_times)

    n = len(lp_times)
    plt.plot(range(n), lp_times)

    n = len(input_complexities)
    plt.plot(range(n), input_complexities)


    plt.legend(["mzn_times","lp_times","complexities"])
    plt.show()

### ##################################################
### # Main
### ##################################################
def main():
    inputs      = []
    mzn_outputs = []
    lp_outputs  = []
    nums        = []

    num = 0
    i,mzn_o,lp_o = in_out(num)

    while not (mzn_o == None and lp_o == None):
        inputs.append(i)
        if mzn_o == None:
            #empty_sol = MySolution()
            #empty_sol.solveTime = -100
            #mzn_outputs.append(empty_sol)
            pass
        else:
            mzn_outputs.append(mzn_o)

        if lp_o == None:
            #empty_sol = MySolution()
            #empty_sol.solveTime = -100
            #lp_outputs.append(empty_sol)
            pass
        else:
            lp_outputs.append(lp_o)
        nums.append(num)

        num+=1
        i,mzn_o,lp_o = in_out(num)

    # print(inputs)
    # print(outputs)

    plot_solveTimes(inputs, mzn_outputs, lp_outputs)
    plot_times(inputs, mzn_outputs, lp_outputs)

    return


if __name__ == "__main__":
    main()
