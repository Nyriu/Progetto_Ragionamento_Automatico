# TODO
# Data una coppia K,H mostra i valori MPOQ delle istanze
# - risolte in minor tempo
# - risolte in maggior tempo
# - con minor numero di persone
# - con maggior numero di persone
# Se un istanza è candidata per più tipologie viene mostrata una sola volta
# Le istanze sono ordinate da sinistra a destra per solveTime crescente

import my_lib
import os
import sys
import json

import numpy as np

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

keys = ['M','P','O','Q']

cut_l = 5
nums = nums[:cut_l]
solveTimes = solveTimes[:cut_l]
inputs = inputs[:cut_l]

for i in inputs:
    print(i)

m = [i['M'] for i in inputs]
p = [i['P'] for i in inputs]
o = [i['O'] for i in inputs]
q = [i['Q'] for i in inputs]

labels = [str(n) for n in nums]

x = np.arange(len(labels))  # the label locations
width = 0.1  # the width of the bars

fig, ax = plt.subplots()
rects_m = ax.bar(x - 3*width/2, m, width, label='M')
rects_p = ax.bar(x - width/2, p, width, label='P')
rects_o = ax.bar(x + width/2, o, width, label='O')
rects_q = ax.bar(x + 3*width/2, q, width, label='Q')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Values')
ax.set_xlabel('Inputs')
#ax.set_title('Scores by group and gender')
ax.set_yticks(range(max(m+p+o+q)+1))
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects_m)
autolabel(rects_p)
autolabel(rects_o)
autolabel(rects_q)

fig.tight_layout()

plt.show()


##def main():
##    args = sys.argv
##    if len(args) < 3:
##        print("Put two arguments!! For example")
##        print("python output_visualizer.py arr_outputs 18")
##        exit(1)
##
##    source_dir = args[1]
##    num = args[2]
##
##    if not os.path.isdir(source_dir):
##        print("ERROR!! %s is not a directory!!" %(source_dir))
##        exit(1)
##    try:
##        num = int(num)
##    except:
##        print("ERROR!! %s must be a number!!" %(num))
##        exit(1)
##
##
##    data = read_output(num, source_dir)
##    print(data)
##    print()
##    show_statistic(data['stats'])
##    show_objective(data['obj'])
##    print()
##    show_solution(data['sol'])
##    print()
##
##
##
##if __name__ == '__main__':
##    main()
