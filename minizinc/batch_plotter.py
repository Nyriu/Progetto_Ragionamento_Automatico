# Plotta il grafico dei tempi di inputs e outputs di una cartella data

import my_lib
import os
import sys
import json

import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

batch_dir = "./input_batch_01/"

my_lib.INPUT_DIR  = batch_dir + "/inputs"
my_lib.OUTPUT_DIR = batch_dir + "/outputs"

img_path = batch_dir + "fig.png"


inputs = []
solveTimes = []
nums = []


num = 0
i = my_lib.get_input(num)
d = my_lib.read_output(num, my_lib.OUTPUT_DIR, suppress_error=True)

while not (d == None):
    inputs.append(i)
    solveTimes.append(d['stats']['solveTime'])
    nums.append(num)

    num+=1
    i = my_lib.get_input(num)
    d = my_lib.read_output(num, my_lib.OUTPUT_DIR, suppress_error=True)



x = len(nums)
plt.plot(nums[:x], solveTimes[:x])
#plt.show()
plt.savefig(img_path)




#def main():
#if __name__ == '__main__':
#    main()
