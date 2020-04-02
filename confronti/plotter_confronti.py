import os
import sys
import json
from output_visualizer import read_output

import matplotlib.pyplot as plt

fname_prefix = "output_"
fname_suffix = ".json"

source1_dir = "./arr_outputs/"
source2_dir = "./mat_outputs/"


#def get_time#s

solveTimes1 = []
solveTimes2 = []
nums = []

num = 0
d1 = read_output(num, source1_dir, suppress_error=True)
d2 = read_output(num, source2_dir, suppress_error=True)


while not (d1 == None or d2 == None):
    solveTimes1.append(d1['stats']['solveTime'])
    solveTimes2.append(d2['stats']['solveTime'])
    nums.append(num)

    num+=1
    d1 = read_output(num, source1_dir, suppress_error=True)
    d2 = read_output(num, source2_dir, suppress_error=True)

print(nums[:5])
print(solveTimes1[:5])
print(solveTimes2[:5])

x = 15
plt.plot(nums[:x], solveTimes1[:x], color='red')
plt.plot(nums[:x], solveTimes2[:x], color='blue')
plt.show()




# per ora sulle x il numero e sulle y il solveTime












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
