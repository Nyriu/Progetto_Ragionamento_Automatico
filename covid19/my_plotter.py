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
        o = MySolution.read(
                IOHelper.gen_fpath(
                    num,
                    OUTPUT_MZN_DIR,
                    OUTPUT_MZN_PREFIX,
                    OUTPUT_MZN_EXT))
    except Exception as e:
        i = None
        o = None

    return i,o

def normalize(x, a,b):
    # normalize x into [a,b]
    m = min(x)
    M = max(x)
    res = [(b-a)*(y-m)/(M-m)+a for y in x]
    return res


### ##################################################
### # Main
### ##################################################
def main():
    inputs  = []
    outputs = []
    nums    = []

    num = 0
    i,o = in_out(num)

    while not (o == None):
        inputs.append(i)
        outputs.append(o)
        nums.append(num)

        num+=1
        i,o = in_out(num)

    # print(inputs)
    # print(outputs)

    solveTimes = [y.solveTime for y in outputs]
    input_complexities = [y.calc_complexity(alpha=.2) for y in inputs]
    input_complexities = normalize(input_complexities, min(solveTimes),max(solveTimes))

    #n = len(nums)
    #n = 20
    #n_delta = 4
    #plt.plot(range(n,n+n_delta), solveTimes[n:n+n_delta])
    #plt.plot(range(n,n+n_delta), input_complexities[n:n+n_delta])

    n = len(nums)
    plt.plot(range(n), solveTimes)
    plt.plot(range(n), input_complexities)


    plt.legend(["solveTimes","Complexities"])
    #plt.xticks(ticks=nums[:x], rotation=70)
    plt.show()
    return


if __name__ == "__main__":
    main()
