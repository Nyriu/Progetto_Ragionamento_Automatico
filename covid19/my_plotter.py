import sys
import os
from my_globals import *
from my_lib import IOHelper, MyInstance, MySolution

import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

### TODO
### ##################################################
### # Main
### ##################################################
### def main():
###
###
### if __name__ == "__main__":
###     main()

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
    return [(b-a)*(y-m)/(M-m)+a for y in x]


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

print(inputs)
print(outputs)


solveTimes = [y.solveTime for y in outputs]
input_complexities = [y.calc_complexity() for y in inputs]
input_complexities = normalize(input_complexities, min(solveTimes),max(solveTimes))



x = len(nums)
plt.plot(range(x), solveTimes)
plt.plot(range(x), input_complexities)
plt.legend(["solveTimes","Complexities"])
#plt.xticks(ticks=nums[:x], rotation=70)
plt.show()
