# Plotta il grafico dei tempi
# Sulle x numero dell'input
# Sulle y tempo in secondi

import my_lib
import os
import sys
import json

import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')



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


###################################################
## TODO
##print(nums[:x])
##print(solveTimes[:x])
## DEBUG
#c = 10
#nums = nums[:c]
#solveTimes = solveTimes[:c]
#inputs = inputs[:c]
#
## END DEBUG
#
#sort_difficulty = True
#if sort_difficulty:
#    print(solveTimes)
#    print(nums)
#    print()
#
#    capienze = [my_lib.capienza_max(i) for i in inputs]
#    print("capienza_max")
#    print(capienze)
#    print()
#    solveTimes = [x for _,x in sorted(zip(capienze,solveTimes))]
#    print(solveTimes)
#    print(capienze)
#    num = [x for _,x in sorted(zip(capienze,nums))]
#    print(nums)
#    print()
###################################################
#N_PEOPLE = "n_peps"
#sort_type= N_PEOPLE
#
#def count_peps(values):
#    peps = 0
#    keys = ['M','P','O','Q']
#    for k in keys:
#        peps+=values[k]
#
#    return peps
#
#
#if sort_type == N_PEOPLE:
#
#    peps = [count_peps(i) for i in inputs]
#    print(peps[:10])
#    print()
#    print(solveTimes[:10])
#    solveTimes = [x for _,x in sorted(zip(peps,solveTimes))]
#    print(solveTimes[:10])
#    print()
#    print(peps[:10])
#    print(nums[:10])
#    nums = [x for _,x in sorted(zip(peps,nums))]
#    print(nums[:10])
#    print()
###################################################


x = len(nums)
plt.plot(range(x), solveTimes[:x])
#plt.xticks(ticks=nums[:x], rotation=70)
plt.show()
#my_dpi=90
#plt.savefig("fig.png", figsize=(10,2))

#def main():
#    args = sys.argv
#    if len(args) < 3:
#        print("Put two arguments!! For example")
#        print("python output_visualizer.py arr_outputs 18")
#        exit(1)
#
#    source_dir = args[1]
#    num = args[2]
#
#    if not os.path.isdir(source_dir):
#        print("ERROR!! %s is not a directory!!" %(source_dir))
#        exit(1)
#    try:
#        num = int(num)
#    except:
#        print("ERROR!! %s must be a number!!" %(num))
#        exit(1)
#
#
#    data = read_output(num, source_dir)
#    print(data)
#    print()
#    show_statistic(data['stats'])
#    show_objective(data['obj'])
#    print()
#    show_solution(data['sol'])
#    print()
#
#
#
#if __name__ == '__main__':
#    main()
